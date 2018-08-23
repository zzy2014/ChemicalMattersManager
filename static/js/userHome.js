//点击主菜单时显示子菜单
function showSubNavi(subUlId)
{
    $("#"+subUlId).toggle();
}

//显示右侧界面, 传入类型参数
function showRightPage(strPageType)
{
    $.ajax({
        type: "POST",
        url: "/AppUserManager/showRightPage/",
        data: {"pageType":strPageType},
        dataType: "text",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        $("#div_RightPage").html(result);
    }).fail(function(result)
    {
        $("#div_RightPage").html(result);
    });
}

//退出登录
function logout()
{
    var retCode = confirm("确定要退出吗？");
	if(!retCode)
	    return false;

    $.ajax({
        type: "POST",
        url: "/AppUserManager/logout/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        intRetCode = result["intRetCode"]
        if (intRetCode > 0)
        {
            location.href = '/index/';
            return true;
        }
        else
        {
            alert("退出失败!");
            return false;
        }
    }).fail(function(result)
    {
        alert("退出失败!");
        return false;
    });

    return false;
}
