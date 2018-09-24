//入库
$(function()
{
    //删除所有ImportFormId=0的数据
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/delTempMatterDetails/",
        dataType: "json",
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(response){
        alert("数据初始化失败");
        return;
    });

    var matters = [];  //数组用于存储从数据库中获取的信息
    matters.push({"id":0});

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
                    url: "/AppMatterManager/addMatterDetails/",
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
                    url: "/AppMatterManager/addMatterDetails/",
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
                    url: "/AppMatterManager/addMatterDetails/",
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
                    url: "/AppMatterManager/addMatterDetails/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "入库药品信息ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_ImportFormId", title: "入库单ID", type: "number", width: 80, editing: false, visible:false, align:"left"},
            { name: "EF_MatterId", title: "药品名", type: "select", width:70, items: matters, valueField:"id", textField:"EF_Name"},
            { name: "EF_MatterCount", title: "药品数量", type: "number", width:80, editing:true, align:"left"},
            { type: "control" }
        ]
    });

});

