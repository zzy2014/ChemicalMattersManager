//药品最小库存量
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

    var purities = [];  //数组用于存储从数据库中获取的信息
    purities.push({"id":0, "EF_LevelName":""});

    //从数据库获取所有纯度规格
    $.ajax({
        type: "GET",
        url: "/AppMatterSetting/purityLevels/",
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
            purities.push(newFields);
        });
    });

    //纯度规格字典
    var purityDict = {};
    for (var nIndex = 0; nIndex < purities.length; nIndex++)
    {
        purityDict[ purities[nIndex].id ] = purities[nIndex].EF_LevelName;
    }

    //生成材料ID对应的纯度规格名
    var mattersPurityDict = {};
    for (var nIndex = 0; nIndex < matters.length; nIndex++)
    {
        mattersPurityDict[ matters[nIndex].id ] = purityDict[ matters[nIndex].EF_PurityId ];
    }

 
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
                    url: "/AppMatterSetting/matterMinRemains/",
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
                    url: "/AppMatterSetting/matterMinRemains/",
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
                    url: "/AppMatterSetting/matterMinRemains/",
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
                    url: "/AppMatterSetting/matterMinRemains/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "最小剩余量ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_MatterId", title: "药品名", type: "select", width:70, items: matters, valueField:"id", textField:"EF_Name"},
            {
                headerTemplate: function() 
                {
                       return "药品规格";
                },
                itemTemplate: function(value, item)
                {
                    return mattersPurityDict[item.EF_MatterId]
                }
            },
            { name: "EF_MinRemain", title:"最小剩余量", type: "number", width: 100, align:"left"},
            { type: "control" }
        ]
    });

});

