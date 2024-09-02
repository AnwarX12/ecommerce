
function addtoacrt(id)
{
        var card=document.getElementById('card')
    var ajaxurl="/add_to_cart/";
    $.ajax({

        headers: { "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content") },
        url:ajaxurl,
        data:{id:id},
        method:"post",

        success:function(response){
            card.innerHTML=response.count
            Swal.fire({
                position: "center",
                icon: "success",
                title: "تم الإضافة الى السلة بنجاح",
                showConfirmButton: false,
                timer: 1500
              });
          
        }

    });
}