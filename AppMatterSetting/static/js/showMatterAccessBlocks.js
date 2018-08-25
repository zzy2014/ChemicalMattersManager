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
    
    var students = [];  //数组用于存储从数据库中获取的信息
    students.push({"id":0, "EF_UserName":""});

    //从数据库获取所有学生类型
    $.ajax({
        type: "GET",
        url: "/AppUserManager/students/",
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
            students.push(newFields);
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
                    url: "/AppMatterSetting/matterAccessBlocks/",
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
                    url: "/AppMatterSetting/matterAccessBlocks/",
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
                    url: "/AppMatterSetting/matterAccessBlocks/",
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
                    url: "/AppMatterSetting/matterAccessBlocks/" + curItem.id,
                });
            }
        },

        onOptionChanged: function (curItem)
        {
            //alert("ddd");
		},

        fields: [
            { name: "id", title: "最小剩余量ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_MatterId", title: "药品名", type: "select", width:70, items: matters, valueField:"id", textField:"EF_Name"},
            { name: "EF_StudentTypeId", title: "学生类型", type: "select", width:70, items: studentTypes, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_StudentId", title: "学生", type: "select", width:70, items: students, valueField:"id", textField:"EF_UserName"},
            { type: "control" }
        ]
    });

});

