function showDivBlock(idShow, idBlock)
{
    document.getElementById(idShow).style.display='block'; 
    document.getElementById(idBlock).style.display='block';
}

function hideDivBlock(idHide, idBlock)
{
    document.getElementById(idHide).style.display='none';
    document.getElementById(idBlock).style.display='none';
}

//注册
function register(idType, idName, idPassword, idRePassword)
{
    strType = $("#" + idType + " option:selected").val()
    if (strType == "")
    {
        alert("用户类型为空！");
        return false;
    }

    strName = $("#" + idName).val()
    if (strName == "")
    {
        alert("用户名为空！");
        return false; 
    }

    strPassword = $("#" + idPassword).val()
    if (strPassword == "")
    {
        alert("密码为空！");
        return false;
    }

    strRePassword = $("#" + idRePassword).val()
    if (strRePassword == "")
    {
        alert("请再次输入密码！");
        return false;
    }
    else if (strRePassword != strPassword)
    {
        alert("两次输入的密码不相同！");
        return false;
    }
    
    //向后台发送注册请求
    var ajax =$.ajax({
        'type':"POST",
        'url':'/AppUserManager/register/',
        'data': {'type':strType, 'name': strName, 'password':strPassword}, //要发送的数据（参数）格式为{'val1':"1","val2":"2"}
        'dataType':'json'
    });

    ajax.done(
            function(data)
            {
                var intRetCode = data["retCode"];

                //回调函数获取的data就是view返回的json数据
                if(intRetCode < 0)
                {
                    alert('注册失败！');
                    return false;
                }
                else if(intRetCode == 0)
                {
                    alert('当前用户名己存在');
                    return false;
                }
                else
                {
                    hideDivBlock('div_register','div_block');
                    alert('注册成功！');
                    return true;
                }

            }
    );

    ajax.fail(
        function()
        {
            alert('服务器请求失败')
        }
    );

    return false;
}


function loginVertify(idLoginType, idLoginName, idLoginPs)
{
    strUserType = $("#" + idLoginType + " option:selected").val()
    if (strUserType == "")
    {
        alert("用户类型为空！");
        return false;
    }

    strUserName = $("#"+idLoginName).val()
    if (strUserName == "")
    {
        alert("用户名为空！");
        return false; 
    }


    strPassWord = $("#"+idLoginPs).val()
    if (strPassWord == "")
    {
        alert("密码为空！");
        return false;
    }

    var ajax =$.ajax({
        'type':"POST",
        'url':'/AppUserManager/loginVerify/',
        'data': {'type':strUserType, 'name': strUserName, 'password':strPassWord}, //要发送的数据（参数）格式为{'val1':"1","val2":"2"}
        'dataType':'json'
    });

    ajax.done(
            function(data)
            {
                var intUserId = data["userId"];

                //回调函数获取的data就是view返回的json数据
                if(intUserId <= 0)
                {
                    alert('用户名或密码不正确！');
                    return false;
                }
                else
                {
                    //验证成功后将当前用户信息传入，登录首页
                    location.href = '/AppUserManager/userHome/';
                    return true;
                }

            }
    );

    ajax.fail(
        function()
        {
            alert('服务器请求失败')
        }
    );

    return false;
}


