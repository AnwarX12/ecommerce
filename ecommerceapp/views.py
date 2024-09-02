from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .models import storetype,items,itemsdetails,card
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login ,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,LoginUserForm

def index(request):
    print(request.user)
    template=loader.get_template('index.html')
    return HttpResponse(template.render({'request':request}))
#display all item in cup
def listitems(request):
    p=items.objects.filter(st_id=2)
    template=loader.get_template('listitems.html')
    return HttpResponse(template.render({'items':p ,'request':request}))

def listitemsC(request):
    p=items.objects.filter(st_id=1)
    template=loader.get_template('listitemsC.html')
    return HttpResponse(template.render({'items':p ,'request':request}))

def listitemsM(request):
    p=items.objects.filter(st_id=3)
    template=loader.get_template('listitemsE.html')
    return HttpResponse(template.render({'items':p,'request':request}))


def detials(request,id):
    template=loader.get_template('details.html')
    data=itemsdetails.objects.select_related('items').filter(id=id).first()
    data.total=data.qty*data.items.price
    #print(data)
    return HttpResponse(template.render({'data':data,'request':request}))

@login_required(login_url='/auth_login/')
def checkout(request):
    # الحصول على جميع عناصر السلة
    cart_items = card.objects.all()
    
    # الحصول على تفاصيل المنتجات من جدول items
    items_list = []
    for cart_item in cart_items:
        item = items.objects.filter(id=cart_item.itmesid).first()
        if item:
            item_details = itemsdetails.objects.filter(items=item).first()
            items_list.append({
                'item': item,
                'item_details': item_details
            })
    
    # حساب الإجمالي
    total = sum(item['item'].price for item in items_list)
    discount = 95  # افترض خصم ثابت
    total_after_discount = total - discount

    # تمرير العناصر إلى القالب
    context = {
        'request': request,
        'items_list': items_list,
        'total': total,
        'discount': discount,
        'total_after_discount': total_after_discount
    }

    template = loader.get_template('checkout.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def add_to_cart(request):
    id=request.POST.get("id")
    p=card(itmesid=id)
    p.save()
    row=card.objects.all()
    count=0
    for item in row:
        count=count+1
    
    request.session["card"]=count
    return JsonResponse({'count':count})

@csrf_exempt
def auth_login(request):
     form=LoginUserForm()
     if request.method=="POST":
          form=LoginUserForm(data=request.POST)
          if form.is_valid():
              username=form.cleaned_data['username']
              password=form.cleaned_data['password']
              print(username)

              user=authenticate(username=username,password=password)
              if user:
                   if user.is_active:
                        login(request,user)
                        return render(request,'checkout.html')
     context={'form':form}
     return render(request,'auth_login.html',context)
            

@csrf_exempt
def auth_register(request):
    template=loader.get_template('auth_register.html')
    form=CreateUserForm()
    if request.method=="POST":
          form=CreateUserForm(request.POST)
          if form.is_valid():
              form.save()
              return redirect('auth_login')
          

    context={'auth_registerform':form}

    return HttpResponse(template.render(context=context))
