

function getArray(value)
{   var replace=null
    var list=document.getElementsByName(value)
    var array=new Array("")
       for(var i= 0,j=0;i<list.length;i++)
          {
              if(list[i].value!=""&&list[i].value!=null)
                 {
                       array[j]=list[i].value.replace(/\\/,"/");
                       j=j+1
                 }
          }

    for(var i=1;i<array.length;i++)
    {
        for(var j=0;j<array.length-i;j++)
        {
            var a=splitIP(array[j])
            var b=splitIP(array[j+1])
            for(var k=0;k<4;k++)
            {
               if(parseInt(a[k])<parseInt(b[k]))
                    break
                else if(parseInt(a[k])>parseInt(b[k]))
               {
                replace=array[j+1]
                array[j+1]=array[j]
                array[j]=replace
                   break
               }
             }
        }
    }

    return array
}



function addtext(getValue,getSize){
    $('.'+getValue).append("<br/><input type='text' name='"+getValue+"' size='"+getSize+"'/>")
}





function splitIP(ip)
{
 var str=ip.replace(/\\/,"/")
 str=str.split("/")[0].split(".")
 return str

}

function setkey(id){
   var ip=document.getElementsByName("Diagram")[0].value
    if(ip=="")
    {
        alert("请输入IP地址")
        return
    }
    var ID=document.getElementById("ID").value
    if(ID=="")
    {
        alert("请输入机构代码")
        return
    }
    ip=splitIP(ip)[0]+splitIP(ip)[1]+splitIP(ip)[2]
    $("#"+id).val(ip+ID)
}
function makegrekey(){
    var ip=document.getElementsByName("Diagram")[0].value
    if(ip=="")
    {
        alert("请输入IP地址")
        return
    }
    ip=splitIP(ip)[0]+splitIP(ip)[1]+splitIP(ip)[2]
    $("#grekey").val(ip)
}

function ChangeSelect(me,id){
    var text=$(me).find("option:selected").text();
    var reChat=new RegExp("光纤专线");
    var reAD=new RegExp("ADSL")
    $("#"+id).val(text)
    if(id=='circuit'){
        if(reChat.test(text)!=true){
            $("input[name='PublicIP']").attr("disabled","true");
            $("input[name='PublicGATEWAY']").attr("disabled","true");

        }
        else{
            $("input[name='PublicIP']").removeAttr("disabled");
            $("input[name='PublicGATEWAY']").removeAttr("disabled");
        }
    }
    if(reAD.test(text)){
        $("#uplinkBandwidth").val("512K")
    }

}
function IP2V(ip){
    var re = /^([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$/;   //匹配IP地址的正则表达式
    var re2=/^([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\\|\/(\d{1,2})$/;
    if(!re2.test(ip)&&!re.test(ip)){
        alert("IP段格式错误，请按照'X.X.X.X'或'X.X.X.X/XX'格式输入");
    }
}
