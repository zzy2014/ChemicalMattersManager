//审批流程设置
$(function()
{
    var userTypes = [];  //数组用于存储从数据库中获取的信息
    userTypes.push({"id":0, "EF_TypeName":""});

    //从数据库获取所有药品
    $.ajax({
        type: "GET",
        url: "/AppUserManager/userTypes/",
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
            userTypes.push(newFields);
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
                    url: "/AppMatterManager/censorePatterns/",
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
                    url: "/AppMatterManager/censorePatterns/",
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
                    url: "/AppMatterManager/censorePatterns/",
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
                    url: "/AppMatterManager/censorePatterns/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "审核流程ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_StepsCount", title: "审核步数", type: "number", width:70, alin:"left"},
            { name: "EF_UserTypeId1", title: "用户类型1", type: "select", items: userTypes, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserTypeId2", title: "用户类型2", type: "select", items: userTypes, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_UserTypeId3", title: "用户类型3", type: "select", items: userTypes, valueField:"id", textField:"EF_TypeName"},
            { type: "control" }
        ]
    });

});

