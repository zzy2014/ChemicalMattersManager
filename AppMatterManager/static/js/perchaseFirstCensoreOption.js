function confirmCensore()
{
    //设置当前预采购表的第一个审核人;
    var censoreUserId1 = $("#select_censoreOption").find("option:selected").val();
    var postData = {censoreUserId:censoreUserId1, formTableName:"PerchaseForms", detailTableName:"PerchaseMatterDetails"};

    //新建预采购表并设置审核人
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/createNewForm/",
        dataType: "text",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(response, textStatus){
        alert(response["responseText"]);
        return false;
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
