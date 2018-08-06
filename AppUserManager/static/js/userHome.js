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
            { name: "EF_UserStateId", title: "状态ID", type: "number", width: 50, editing: false, align:"left"},
            { name: "EF_UserName", title:"名称", type: "text", width: 100, align:"left"},
            { name: "EF_PassWord", title:"密码", type: "text", width: 100, align:"left"},
            { name: "EF_OfficeAddress", title:"办公室", type: "text", width: 100, align:"left"},
            { name: "EF_PhoneNum", title:"电话号码", type: "text", width: 100, align:"left"},
            { type: "control" }
        ]
    });

}

