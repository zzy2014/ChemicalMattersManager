//药品权限禁止
$(function()
{
    var matters = [];  //数组用于存储从数据库中获取的信息
    matters.push({"id":0, "EF_UnitName":""});

    //从数据库获取所有药品
    $.ajax({
        type: "GET",
        url: "/AppMatterSetting/matters/",
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
            matters.push(newFields);
        });
    });


    var studentTypes = [];  //数组用于存储从数据库中获取的信息
    studentTypes.push({"id":0, "EF_TypeName":""});

    //从数据库获取所有学生类型
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
            studentTypes.push(newFields);
        });
    });


    var lastClickRow = "";

    $("#jsUpGrid").jsGrid({
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

        //点击时显示下面表格
        rowClick: function (args)
        {
            if (lastClickRow != "")
                lastClickRow.removeClass("highLightRow");

            lastClickRow = $("#jsUpGrid").jsGrid("rowByItem", args.item);
            lastClickRow.addClass("highLightRow");

            var intBlockId = args.item.id;
            var intStudentTypeId = args.item.EF_StudentTypeId;
            ShowDownGrid(intBlockId, intStudentTypeId);
        },

        controller: {
            loadData: function(filter)
            {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/AppMatterSetting/matterAccessBlocks/",
                    dataType: "json",
                    data: filter
                }).done(function(result)
                {
                    d.resolve($.map(result, function(item)
                    {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });

                return d.promise();
            },

            insertItem: function(newItem)
            {
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppMatterSetting/matterAccessBlocks/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsUpGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem)
            {
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppMatterSetting/matterAccessBlocks/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus)
                {
                    d.resolve(response);
                    $("#jsUpGrid").jsGrid("loadData");
                    $("#jsDownGrid").jsGrid("loadData");
                }).fail(function(response, textStatus)
                {
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem)
            {
                return $.ajax({
                    type: "DELETE",
                    url: "/AppMatterSetting/matterAccessBlocks/" + curItem.id,
                });
            },
        },

        fields: [
            { name: "id", title: "权限禁止ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_MatterId", title: "药品名", type: "select", width:70, items: matters, valueField:"id", textField:"EF_Name"},
            { name: "EF_StudentTypeId", title: "学生类型", type: "select", width:70, items: studentTypes, valueField:"id", textField:"EF_TypeName"},
            { type: "control" }
        ]
    });

});



function ShowDownGrid(intBlockId, intStudentTypeId)
{
    var students = [];  //数组用于存储从数据库中获取的信息
    students.push({"id":0, "EF_UserName":""});

    //从数据库获取所有药品
    $.ajax({
        type: "GET",
        url: "/AppUserManager/students/",
        dataType: "json",
        data: {"EF_TypeId":intStudentTypeId},
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        //对result数组中每个元素执行function
        $.map(result, function(item)
        {
            //将后面的元素合并到前面的参数中
            var newFields = {id : item.pk};
            $.extend(newFields, item.fields);
            students.push(newFields);
        });
    });


    $("#jsDownGrid").jsGrid({
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
                filter.EF_BlockId = intBlockId;
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/AppMatterSetting/subMatterAccessBlocks/",
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
                newItem.EF_BlockId = intBlockId;
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppMatterSetting/subMatterAccessBlocks/",
                    dataType: "json",
                    data: newItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsDownGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("插入数据失败！");
                });

                return d.promise();
            },

            updateItem: function(curItem){
                curItem.EF_BlockId = intBlockId;
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppMatterSetting/subMatterAccessBlocks/",
                    dataType: "json",
                    data: curItem,
                }).done(function(response, textStatus){
                    d.resolve(response);
                    $("#jsDownGrid").jsGrid("loadData");
                }).fail(function(response, textStatus){
                    alert("更新数据失败！");
                });

                return d.promise();
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppMatterSetting/subMatterAccessBlocks/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "学生权限禁止ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_BlockId", title: "权限禁止ID", type: "text", width:100, editing:false, align:"left"},
            { name: "EF_StudentId", title: "学生", type: "select", width:100, items: students, valueField:"id", textField:"EF_UserName"},
            { type: "control" }
        ]
    });
}

