//用户状态管理
$(function()
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
                }).done(function(result)
                {
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
                }).done(function(response, textStatus)
                {
                    d.resolve(response);
                }).fail(function(response, textStatus)
                {
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
                }).done(function(response, textStatus)
                {
                    d.resolve(response);
                }).fail(function(response, textStatus)
                {
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

});

