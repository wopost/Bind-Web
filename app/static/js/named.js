
// 添加解析记录模态框
$("#AddZone").on('click',function(){
    $('#AddZoneModal').modal('show')  
})

// 添加解析记录
$("#addzonebtn").click(function(){
    var check = $("#addzoneForm").Validform().check()
     if (check) {
        $.post("/namedadd/",$("#addzoneForm").serialize(),function(data) {
        data=JSON.parse(data)
        if(data["code"]==0){
                   swal({
                     title:"success",
                     text:"解析记录添加成功",
                     type:"success",
                     confirmButtonText:'确定'
                    },function(){
                        location.reload()
                    })

        }else{
            alert("add  error")
      }
        })
         return false;
   }     
})


// 点击更新按钮，获取id，从逻辑端查出对应的数据，弹出模态窗渲染数据
$(".update").click(function(){   
    //$('#updateModal').modal('hide')
    var id=$(this).attr("data-id")
    $.getJSON("/namedupdate",{'id':id},function(data){
            console.log(data);
            $("#upid").val(data["id"]);
            $("#zones").val(data["zone"]);
            $("#host").val(data["host"]);
            $("#type").val(data["type"]);
            $("#data").val(data["data"]);
            $("#ttl").val(data["ttl"]);
            $('#updateModal').modal('show')
                

        })
})

// 更新数据
$("#updatebtn").click(function(){
$.post("/namedupdate/",$("#updateForm").serialize(),function(data) {
    data=JSON.parse(data)
    if(data["code"]==0){
        swal({
                title:"success",
                text:"更新成功",
                type:"success",
                confirmButtonText:'确定'
                },function(){
                    location.reload()
                })

    }else{
        alert("update error")
    }
    })
    return false;
})

/*用户详情*/
$('.detail').click(function(){
    var id=$(this).attr('list_id')
    var url = "/namedupdate/?id="+id
    $.getJSON(url,function(data){
	    result = data
        console.log(result)
		 $('#detail_zone').html('<pre>'+result['zone']+'</pre>')
         $('#detail_host').html('<pre>'+result['host']+'</pre>')		 
         $('#detail_type').html('<pre>'+result['type']+'</pre>')
         $('#detail_data').html('<pre>'+result['data']+'</pre>')
    })
    $('#infoModel').modal('show')
})



/*删除解析记录*/
$(".del").click(function(){
	if(confirm("是否确认删除？")){		var id = $(this).attr('data-id')
		var id = $(this).attr('data-id')
        var url = "/nameddelete/?id="+id
		$.getJSON(url,function(data){
			if (data['code']== 0 ){
                   swal({
                     title:"success",
                     text:"解析删除成功",
                     type:"success",
                     confirmButtonText:'确定'
                    },function(){
                        location.reload()
                    })  
			}else{
                alert(data["msg"])
			}
    	})
    }  // end confirm
})   


$(function(){
   $(".adduser").Validform({                 
           tiptype:3
     });
})
