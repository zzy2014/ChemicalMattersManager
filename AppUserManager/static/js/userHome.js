//点击主菜单时显示子菜单
function showSubNavi(subUlId)
{
    $("#"+subUlId).toggle();
}

//用户状态管理
function showUserStates()
{
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


