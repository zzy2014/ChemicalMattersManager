function confirmCensore()
{
    //获取当前选中的审核状态、下一个审核人与评论
    var censoreStateId = $("#select_StateOption").find("option:selected").val();

    var nextCensoreUserId = 0;
    var count = $("#select_censoreOption").val();
    if (count > 0)
        nextCensoreUserId = $("#select_censoreOption").find("option:selected").val();

    var strComment = $("#textarea_censoreComment").val();

    //设置当前入库单的第一个审核人;
    var postData = {censoreStateId:censoreStateId, nextCensoreUserId:nextCensoreUserId, strComment:strComment };

    //审核操作
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/censoreImportForm/",
        dataType: "html",
        data: postData,
        async: false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result, textStatus){
        //alert("yes!");
    }).fail(function(result, textStatus){
        alert(result["responseText"]);
    });

    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");
    $("#jsUpGrid").jsGrid("loadData");
}

function cancelCensore()
{
    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");
}
