function confirmCensore()
{
    //设置当前入库单的第一个审核人;
    var censoreUserId1 = $("#select_censoreOption").find("option:selected").val();
    var postData = {censoreUserId:censoreUserId1};

    //新建入库表并设置入库表的审核人
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/createNewImportForm/",
        dataType: "json",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(response){
        alert("创建入库单失败！");
        return;
    });

    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");

    $("#jsGrid").jsGrid("loadData");
}

function cancelCensore()
{
    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");
}
