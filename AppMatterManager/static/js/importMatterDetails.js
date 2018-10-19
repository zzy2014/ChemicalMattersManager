//入库
$(function()
{
    //删除所有临时的数据
    var postData = {tableName:"ImportMatterDetails", fieldMethod:"EF_FormId", methodValue:0};
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/deleteFromOneTable/",
        dataType: "text",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(result, textStatus){
        alert(result["responseText"]);
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
                filter["EF_FormId"] = 0;

                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/AppMatterManager/importMatterDetails/",
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
                newItem["EF_FormId"] = 0;
                var d = $.Deferred();
                $.ajax({
                    type: "POST",
                    url: "/AppMatterManager/importMatterDetails/",
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
                curItem["EF_FormId"] = 0;
                var d = $.Deferred();
                $.ajax({
                    type: "PUT",
                    url: "/AppMatterManager/importMatterDetails/",
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
                    url: "/AppMatterManager/importMatterDetails/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "入库药品信息ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_FormId", title: "入库单ID", type: "number", width: 80, editing: false, visible:false, align:"left"},
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
            { name: "EF_MatterCount", title: "药品数量", type: "number", width:80, editing:true, align:"left"},
            { type: "control" }
        ]
    });

});


function importForm()
{
    alert("import");
}

function upLoadForm()
{
    //获取审核模式，并返回弹出的html
    var tmpHtml = "";
    var postData = {tableName:"ImportMatterDetails"};

    $.ajax({
        type: "POST",
        url: "/AppMatterManager/calculateCensorePattern/",
        dataType: "text",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        tmpHtml = result;
    }).fail(function(result, textStatus)
    {
        alert(result["responseText"]);
        return false;
    });

    if (tmpHtml == "")
        return false;

    $("#div_popWindow").html(tmpHtml);
    $("#div_popWindow").css('display','block');
    $("#div_block").css('display','block');
}
