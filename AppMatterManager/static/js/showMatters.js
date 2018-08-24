//所有药品
$(function()
{
    var matterUnits = [];  //数组用于存储从数据库中获取的信息
    matterUnits.push({"id":0, "EF_UnitName":""});

    //从数据库获取单位
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/matterUnits/",
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
            matterUnits.push(newFields);
        });
    });


    var matterStates = [];  //数组用于存储从数据库中获取的信息
    matterStates.push({"id":0, "EF_StateName":""});

    //从数据库获取理化状态
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/matterStates/",
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
            matterStates.push(newFields);
        });
    });


    var matterPurities = [];  //数组用于存储从数据库中获取的信息
    matterPurities.push({"id":0, "EF_LevelName":""});

    //从数据库获取纯度规格
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/purityLevels/",
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
            matterPurities.push(newFields);
        });
    });


    var matterTypes = [];  //数组用于存储从数据库中获取的信息
    matterTypes.push({"id":0, "EF_TypeName":""});

    //从数据库获取单位
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/matterTypes/",
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
            matterTypes.push(newFields);
        });
    });


    var matterStores = [];  //数组用于存储从数据库中获取的信息
    matterStores.push({"id":0, "EF_RoomName":""});

    //从数据库获取单位
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/storeRooms/",
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
            matterStores.push(newFields);
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
                    url: "/AppMatterManager/matters/",
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
                    url: "/AppMatterManager/matters/",
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
                    url: "/AppMatterManager/matters/",
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
                    url: "/AppMatterManager/matters/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "药品ID", type: "number", width: 70, editing: false, align:"left"},
            { name: "EF_TypeId", title: "类别", type: "select", width:70, items: matterTypes, valueField:"id", textField:"EF_TypeName"},
            { name: "EF_StateId", title: "理化状态", type: "select", width:70, items: matterStates, valueField:"id", textField:"EF_StateName"},
            { name: "EF_PurityId", title: "纯度规格", type: "select", width:70, items: matterPurities, valueField:"id", textField:"EF_LevelName"},
            { name: "EF_UnitId", title: "单位", type: "select", width:70, items: matterUnits, valueField:"id", textField:"EF_UnitName"},
            { name: "EF_StoreId", title: "仓库", type: "select", width:70, items: matterStores, valueField:"id", textField:"EF_RoomName"},
            { name: "EF_Name", title:"名称", type: "text", width: 70, align:"left"},
            { name: "EF_CAS", title:"CAS号", type: "text", width: 70, align:"left"},
            { name: "EF_Format", title:"化学式", type: "text", width: 70, align:"left"},
            { name: "EF_Amount", title:"数量", type: "number", width: 70, align:"left"},
            { name: "EF_Price", title:"单价", type: "floatNumber", width: 70, align:"left"},
            { name: "EF_Location", title:"位置", type: "text", width: 70, align:"left"},
            { name: "EF_Saler", title:"供应商", type: "text", width: 70, align:"left"},
            { name: "EF_Note", title:"备注", type: "text", width:70, align:"left"},
            { type: "control" }
        ]
    });

});

