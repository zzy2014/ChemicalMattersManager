//入库清单
$(function()
{
     var lastClickRow = "";

    $("#jsUpGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: false,
        editing: false,
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

            var intImportFormId = args.item.id;
            ShowDownGrid(intImportFormId);
        },


        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppMatterManager/importForms/",
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
                //不可新增
                return;
            },

            updateItem: function(curItem){
                //不可修改
                return;
            },

            deleteItem: function(curItem){
                return $.ajax({
                    type: "DELETE",
                    url: "/AppMatterManager/importForms/" + curItem.id,
                });
            }
        },

        fields: [
            { name: "id", title: "清单ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_UserId", title: "入库用户", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_FormStateId", title: "单据状态", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_Time", title: "创建时间", type: "text", width: 80, editing: false, align:"left"},
            { name: "EF_UserId1", title: "审核人1", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreStateId1", title: "审核状态1", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreComment1", title: "审核明细1", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_UserId2", title: "审核人2", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreStateId2", title: "审核状态2", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreComment2", title: "审核明细2", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_UserId3", title: "审核人3", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreStateId3", title: "审核状态3", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_CensoreComment3", title: "审核明细3", type: "number", width: 80, editing: false, align:"left"},

            { type: "control" }
        ]
    });

});


function ShowDownGrid(intImportFormId)
{
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


    $("#jsDownGrid").jsGrid({
        height: "100%",
        width: "100%",

        filtering: true,
        inserting: false,
        editing: false,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();
                filter["EF_ImportFormId"] = intImportFormId;

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
                return ;
            },

            updateItem: function(curItem){
                return ;
            },

            deleteItem: function(curItem){
                return ;
            }
        },

        fields: [
            { name: "id", title: "入库药品信息ID", type: "number", width: 80, editing: false, align:"left"},
            { name: "EF_ImportFormId", title: "入库单ID", type: "number", width: 80, editing: false, visible:false, align:"left"},
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
}

