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

function loginVertify(idSubmitBtn, idLoginName, idLoginPs)
{
    strUserName = $('#input_loginname').val()
    if (strUserName == "")
    {
        alert("用户名为空！")
        return false; 
    }

    strPassWord = $('#input_loginpassword').val()
    if (strPassWord == "")
    {
        alert("密码为空！");
        return false;
    }

    var ajax =$.ajax({
        'type':"POST",
        'url':'/AppUserManager/loginVerify/',
        'data': {'name': strUserName, 'password':strPassWord}, //要发送的数据（参数）格式为{'val1':"1","val2":"2"}
        'dataType':'json'
    });

    ajax.done(
            function(data)
            {
                var intUserId = data["userId"];
                var strUserType = data["userType"]; 
                var strUserSubType = data["userSubType"]; 
                //回调函数获取的data就是view返回的json数据
                if (intUserId < 0)
                {
                    alert('传入数据有误！'); //jQuery动态添加网页内容
                    return false;
                }
                else if(intUserId == 0)
                {
                    alert('用户名或密码不正确！');
                    return false;
                }
                else
                {
                    //验证成功后将当前用户信息传入，登录首页
                    location.href = '/AppUserManager/userHome/?userId='+intUserId+'&userType='+strUserType+'&userSubType='+strUserSubType;
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


