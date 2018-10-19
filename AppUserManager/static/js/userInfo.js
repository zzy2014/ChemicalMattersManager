//点击图像时
function clickUserImage(imgInputId)
{
    $("#"+imgInputId).click();
}


//修改用户头像
function changeUserImage(file)
{
    //限制大小
    var fileSize = 0;
    var fileMaxSize = 1024;//1M
    var filePath = file.value;
    if(filePath)
    {
        fileSize =file.files[0].size;
        var size = fileSize / 1024;
        if (size > fileMaxSize)
        {
            alert("文件大小不能大于1M！");
            file.value = "";
            return false;
        }
        else if (size <= 0)
        {
            alert("文件大小不能为0M！");
            file.value = "";
            return false;
        }
    }
    else
    {
        return false;
    }

    var formData = new FormData(); 
    formData.append('uploadImage', file.files[0]);  //添加图片信息的参数

    $.ajax({
        type: 'POST',
        cache: false, //上传文件不需要缓存
        url: "/AppUserManager/uploadCurUserImage/",
        data: formData,
        dataType: "json",
        processData: false, // 告诉jQuery不要去处理发送的数据
        contentType: false, // 告诉jQuery不要去设置Content-Type请求头
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //var jsonObj = JSON.parse(result); 返回的己经为object了不需要再转换
        $("#infoImage").attr("src", result.newUrl);
    }).fail(function(result)
    {
        alert("修改头像出错!");
    });

    return true;
}

//点击文本修改信息
function changeInformation(ItemId)
{
    curItem = $('#'+ItemId);

    //防止多次点击
    if ($(curItem).hasClass('clicked'))
    {
        return false;
    }

    if ($(curItem).hasClass('dealed'))
    {
        $(curItem).removeClass('dealed');
        return false;
    }

    $(curItem).addClass('clicked');

    var oldString = $(curItem).html();

    var strContent = '<form id = "formInform">';
    strContent = '<textarea id = "textInform" rows="1">' + oldString + '</textarea>';
    strContent += '<input id = "saveBtn" type="button" value="Save" />';
    strContent += '<input id = "cancelBtn" type="button" value="Cancel" />';
    strContent += '</form>';
    $(curItem).html(strContent);
    var textarea = $('textarea');

    $('#saveBtn').click(function()
    {
        var curString = textarea.val();
        if (curString.length == 0)
        {
            alert("请输入信息！");
        }
        else
        {
            $(curItem).html(curString);
            $(curItem).removeClass('clicked');
            //用removeClass后，事件处理程序仍会走一遍点击事件，导致html未恢复到原来
            $(curItem).addClass('dealed');

            //ajsx保存
            var postData = {
                type:ItemId,
                value:curString,
            };

            $.ajax({
                type: "POST",
                url: "/AppUserManager/saveCurUserInfo/",
                dataType: "json",
                data: postData,
                async :false,  //改为同步执行，否则不能对外部变量附值
            }).done(function(result)
            {
            }).fail(function(result)
            {
                alert("保存信息失败!");
            });

        }
    });

    $('#cancelBtn').click(function()
    {
        $(curItem).html(oldString);
        $(curItem).removeClass('clicked');
        $(curItem).addClass('dealed');
    });
}

