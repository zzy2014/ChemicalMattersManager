//点击确认修改按钮后
function modifyPassword(oldPasswordId, newPasswordId, reNewPasswordId)
{
    strOldPassword = $("#" + oldPasswordId).val()
    if (strOldPassword == "")
    {
        alert("请输入原密码！");
        return false;
    }

    strNewPassword = $("#" + newPasswordId).val()
    if (strNewPassword == "")
    {
        alert("请输入新密码！");
        return false;
    }
    
    strReNewPassword = $("#" + reNewPasswordId).val()
    if (strReNewPassword == "")
    {
        alert("请再次输入新密码！");
        return false;
    }

    if (strNewPassword != strReNewPassword)
    {
        alert("两次输入的密码不相同！");
        return false;
    }

    var postData = {oldPassword:strOldPassword, newPassword:strNewPassword};

    $.ajax({
        type: "POST",
        url: "/AppUserManager/modifyCurPassword/",
        dataType: "json",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        intRetCode = result["intRetCode"]
        if (intRetCode > 0)
        {
            alert("修改成功！");
            return true;
        }
        else
        {
            alert("修改失败!");
            return false;
        }
    }).fail(function(result)
    {
        alert("修改失败!");
        return false;
    });

    return false;
}

