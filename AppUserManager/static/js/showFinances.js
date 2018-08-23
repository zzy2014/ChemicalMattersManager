//经费管理
$(function()
{
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

});

