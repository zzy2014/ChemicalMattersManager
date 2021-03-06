//点击主菜单时显示子菜单
function showSubNavi(subUlId)
{
    $("#"+subUlId).toggle();
}

//显示右侧界面, 传入类型参数
function showOneTable(curLink, strAppName, strPageType)
{
    //高亮此节点
    $("a.a_leftsubnavi").css("background-color", "");
    $("a.a_leftsubnavi").css("color", "black");
    $(curLink).css("background-color","blue");
    $(curLink).css("color","white");

    $.ajax({
        type: "POST",
        url: "/" + strAppName + "/showOneTable/",
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

//显示上下两级界面，
function showTwoTables(curLink, strAppName, strPageType)
{
    //高亮此节点
    $("a.a_leftsubnavi").css("background-color", "");
    $("a.a_leftsubnavi").css("color", "black");
    $(curLink).css("background-color","blue");
    $(curLink).css("color","white");


    $.ajax({
        type: "POST",
        url: "/" + strAppName + "/showTwoTables/",
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
function logout(curLink)
{
    //高亮此节点
    $("a.a_leftsubnavi").css("background-color", "");
    $("a.a_leftsubnavi").css("color", "black");
    $(curLink).css("background-color","blue");
    $(curLink).css("color","white");

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
