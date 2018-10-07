function confirmCensore()
{
    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");

    //删除所有ImportFormId=0的数据
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/delTempMatterDetails/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(response){
        alert("数据初始化失败");
        return;
    });
    
    $("#jsGrid").jsGrid("loadData");
}

function cancelCensore()
{
    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");
}
