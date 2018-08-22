//点击主菜单时显示子菜单
function showSubNavi(subUlId)
{
    $("#"+subUlId).toggle();
}

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

//个人主页
function showUserInfo()
{
    $("#jsGrid").hide();
    $("#div_RightPage").show();

    //从数据库获取用户信息
    $.ajax({
        type: "GET",
        url: "/AppUserManager/getCurUserInfo/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        var jsonObj = JSON.parse(result);
        $("#userType").html(jsonObj.userType);
        $("#userState").html(jsonObj.userState);
        if (jsonObj.userOffice.length > 0)
            $("#userOffice").html(jsonObj.userOffice);
        if (jsonObj.userPhone.length > 0)
            $("#userPhone").html(jsonObj.userPhone);
        $("#infoImage").attr("src", jsonObj.userImageUrl);
    }).fail(function(result)
    {
        alert("获取个人信息出错!");
    });

}


//点击修改信息
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

//修改密码
function modifyPassword()
{
}

//退出登录
function logout()
{
}

//用户状态管理
function showUserStates()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    $("#jsGrid").jsGrid({
        height: "600px",
        width: "88%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/userStates/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/userStates/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/userStates/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/userStates/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "用户状态ID", type: "number", width: 200, editing: false, align:"left"},
            { name: "EF_TypeName", title:"用户状态名称", type: "text", width: 200, align:"left"},
            { type: "control" }
        ]
    });

}

//用户类型管理
function showUserTypes()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    $("#jsGrid").jsGrid({
        height: "600px",
        width: "88%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/userTypes/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/userTypes/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/userTypes/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/userTypes/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "用户类型ID", type: "number", width: 200, editing: false, align:"left"},
            { name: "EF_TypeName", title:"用户类型名称", type: "text", width: 200, align:"left"},
            { type: "control" }
        ]
    });

}


//学生类型管理
function showStudentTypes()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    $("#jsGrid").jsGrid({
        height: "600px",
        width: "88%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/studentTypes/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/studentTypes/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/studentTypes/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/studentTypes/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "学生类型ID", type: "number", width: 200, editing: false, align:"left"},
            { name: "EF_TypeName", title:"学生类型名称", type: "text", width: 200, align:"left"},
            { type: "control" }
        ]
    });

}


//管理员管理
function showAdministrators()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    var userStates = [];  //数组用于存储从数据库中获取的信息
    userStates.push({"id":0, "EF_TypeName":""});

    //从数据库获取用户状态
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userStates/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            userStates.push(newFields);
        });
    });


    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/administrators/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/administrators/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/administrators/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/administrators/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "管理员ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_UserStateId", title:"状态", type: "select", items: userStates, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { name: "EF_OfficeAddress", title:"办公室", type: "text", width: 100, align:"left"},
            { name: "EF_PhoneNum", title:"电话号码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });

}

//院长管理
function showChiefCollegeLeaders()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();


    var userStates = [];  //数组用于存储从数据库中获取的信息
    userStates.push({"id":0, "EF_TypeName":""});

    //从数据库获取用户状态
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userStates/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            userStates.push(newFields);
        });
    });

    var teachers = []; //获取所有的教师
    teachers.push({"id":0, "EF_UserStateId":0, "EF_FinancialId":0, "EF_UserName":"",
                "EF_PassWord":"", "EF_OfficeAddress":"", "EF_PhoneNum":""});
    $.ajax({
        type: "GET",
        url: "/AppUserManager/teachers/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            teachers.push(newFields);
        });
    });

    
    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/chiefCollegeLeaders/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/chiefCollegeLeaders/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/chiefCollegeLeaders/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/chiefCollegeLeaders/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "院长ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_TeacherId", title: "教师", type: "select", items: teachers, valueField:"id", textField:"EF_UserName"},
            { name: "EF_UserStateId", title:"状态", type: "select", items: userStates, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { name: "EF_OfficeAddress", title:"办公室", type: "text", width: 100, align:"left"},
            { name: "EF_PhoneNum", title:"电话号码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });

}

//副院长管理
function showCollegeLeaders()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    var userStates = [];  //数组用于存储从数据库中获取的信息
    userStates.push({"id":0, "EF_TypeName":""});

    //从数据库获取用户状态
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userStates/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            userStates.push(newFields);
        });
    });


    var teachers = []; //获取所有的教师
    teachers.push({"id":0, "EF_UserStateId":0, "EF_FinancialId":0, "EF_UserName":"",
                "EF_PassWord":"", "EF_OfficeAddress":"", "EF_PhoneNum":""});
    $.ajax({
        type: "GET",
        url: "/AppUserManager/teachers/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            teachers.push(newFields);
        });
    });



    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/collegeLeaders/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/collegeLeaders/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/collegeLeaders/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/collegeLeaders/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "副院长ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_TeacherId", title: "教师", type: "select", items: teachers, valueField:"id", textField:"EF_UserName"},
            { name: "EF_UserStateId", title:"状态", type: "select", items: userStates, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { name: "EF_OfficeAddress", title:"办公室", type: "text", width: 100, align:"left"},
            { name: "EF_PhoneNum", title:"电话号码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });

}

//教师管理
function showTeachers()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    var userStates = [];  //数组用于存储从数据库中获取的信息
    userStates.push({"id":0, "EF_TypeName":""});

    //从数据库获取用户状态
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userStates/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            userStates.push(newFields);
        });
    });


    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/teachers/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/teachers/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/teachers/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/teachers/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "教师ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_UserStateId", title:"状态", type: "select", items: userStates, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { name: "EF_OfficeAddress", title:"办公室", type: "text", width: 100, align:"left"},
            { name: "EF_PhoneNum", title:"电话号码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });
}


//学生管理
function showStudents()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    var userStates = [];  //数组用于存储从数据库中获取的信息
    userStates.push({"id":0, "EF_TypeName":""});

    //从数据库获取用户状态
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userStates/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            userStates.push(newFields);
        });
    });

    //从数据库获取用户状态
    var stuTypes = [];
    stuTypes.push({"id":0, "EF_TypeName":""});

    $.ajax({
        type: "GET",
        url: "/AppUserManager/studentTypes/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            stuTypes.push(newFields);
        });
    });


    //从数据库获取所有教师信息
    var teachers = [];
    teachers.push({"id":0, "EF_UserStateId":0, "EF_FinancialId":0, "EF_UserName":"",
                "EF_PassWord":"", "EF_OfficeAddress":"", "EF_PhoneNum":""});
    $.ajax({
        type: "GET",
        url: "/AppUserManager/teachers/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            teachers.push(newFields);
        });
    });



    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/students/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/students/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/students/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/students/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "学生ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_TypeId", title: "类型", type: "select", items:stuTypes, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_TeacherId", title: "教师", type: "select", items: teachers, valueField:"id", textField:"EF_UserName"},
            { name: "EF_UserStateId", title:"状态", type: "select", items: userStates, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });
}


//经费管理
function showFinances()
{
    $("#div_RightPage").hide();
    $("#jsGrid").show();

    var teachers = []; //获取所有的教师
    teachers.push({"id":0, "EF_UserStateId":0, "EF_FinancialId":0, "EF_UserName":"",
                "EF_PassWord":"", "EF_OfficeAddress":"", "EF_PhoneNum":""});
    $.ajax({
        type: "GET",
        url: "/AppUserManager/teachers/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            teachers.push(newFields);
        });
    });


    //表格本身
    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppUserManager/finances/",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem) {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppUserManager/finances/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    alert(newItem.EF_TotalAmount);
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                    alert(newItem.EF_TotalAmount);
                });

                return d.promise();
            },

            updateItem: function(curItem){
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppUserManager/finances/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppUserManager/finances/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "经费ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_TeacherId", title: "教师", type: "select", items: teachers, valueField:"id", textField:"EF_UserName"},
            { name: "EF_Name", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_TotalAmount", title:"金额", type: "floatNumber", width: 100, align:"left"},
            { type: "control" }
        ]
    });

}



