//入库清单
$(function()
{
    //从数据库获取所有用户类型
    var userTypes = [];
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

    //获取所有的单据状态
    var formStates = [];
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/formStates/",
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
            formStates.push(newFields);
        });
    });

    //获取所有的审核状态
    var censoreStates = [];
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/censoreStates/",
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
            censoreStates.push(newFields);
        });
    });

    //获取所有的审核模型
    var censorePatterns = [];
    $.ajax({
        type: "GET",
        url: "/AppMatterManager/censorePatterns/",
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
            censorePatterns.push(newFields);
        });
    });



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
            {
                headerTemplate: function() 
                {
                       return "入库用户类型";
                },
                itemTemplate: function(value, item)
                {
                    var curUserType =$.grep(userTypes,function(tmp){ return tmp.id == item.EF_UserTypeId });
                    if (curUserType.length > 0)
                        return curUserType[0].EF_TypeName;
                }
            },

            {
                headerTemplate: function() 
                {
                       return "入库用户";
                },
                itemTemplate: function(value, item)
                {
                    var users = GetUsersFromTypeId(userTypes, item.EF_UserTypeId);
                    var curUser =$.grep(users,function(tmp){ return tmp.id == item.EF_UserId });
                    if (curUser.length > 0)
                        return curUser[0].EF_UserName;
                }
            },

            {
                headerTemplate: function() 
                {
                       return "单据状态";
                },
                itemTemplate: function(value, item)
                {
                    var curformState =$.grep(formStates,function(tmp){ return tmp.id == item.EF_FormStateId });
                    if (curformState.length > 0)
                        return curformState[0].EF_StateName;
                }
            },

            { name: "EF_Time", title: "创建时间", type: "text", width: 80, editing: false, align:"left"},

            {
                headerTemplate: function() 
                {
                       return "审核人1";
                },
                itemTemplate: function(value, item)
                {
                    //获取此审核模型相应的审核人员类型 
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
                        return "";

                    var users = GetUsersFromTypeId(userTypes, curPattern[0].EF_UserTypeId1);

                    var curUser =$.grep(users,function(tmp){ return tmp.id == item.EF_UserId1 });
                    if (curUser.length > 0)
                        return curUser[0].EF_UserName;
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核结果1";
                },
                itemTemplate: function(value, item)
                {
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
                        return "";

                    var paraments = {};
                    paraments["curCensoreUserId"] = item.EF_UserId1;
                    paraments["curCensoreStateId"] = item.EF_CensoreStateId1;
                    paraments["censoreStates"] = censoreStates;
                    paraments["nextUserTypeId"] = curPattern[0].EF_UserTypeId2;

                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId1 });

                    return $("<button>").attr("type", "button").text(curcensoreState[0].EF_StateName)
                                    .on("click", paraments, ShowCensoreDialog);
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核明细1";
                },
                itemTemplate: function(value, item)
                {
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
                        return "";
                    else
                        return item.EF_CensoreComment1;
                }
            },

            {
                headerTemplate: function() 
                {
                       return "审核人2";
                },
                itemTemplate: function(value, item)
                {
                    //获取此审核模型相应的审核人员类型 
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 1)
                        return "";

                    var users = GetUsersFromTypeId(userTypes, curPattern[0].EF_UserTypeId2);

                    var curUser =$.grep(users,function(tmp){ return tmp.id == item.EF_UserId2 });
                    if (curUser.length > 0)
                        return curUser[0].EF_UserName;
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核结果2";
                },
                itemTemplate: function(value, item)
                {
                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId1 });
                    if (curcensoreState.length < 1)
                        return "";

                    return $("<button>").attr("type", "button").text(curcensoreState[0].EF_StateName)
                                    .on("click", ShowCensoreDialog);
                }
            },
            { name: "EF_CensoreComment2", title: "审核明细2", type: "number", width: 80, editing: false, align:"left"},

            {
                headerTemplate: function() 
                {
                       return "审核人3";
                },
                itemTemplate: function(value, item)
                {
                    //获取此审核模型相应的审核人员类型 
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 1)
                        return "";

                    var users = GetUsersFromTypeId(userTypes, curPattern[0].EF_UserTypeId3);

                    var curUser =$.grep(users,function(tmp){ return tmp.id == item.EF_UserId3 });
                    if (curUser.length > 0)
                        return curUser[0].EF_UserName;
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核结果3";
                },
                itemTemplate: function(value, item)
                {
                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId1 });
                    if (curcensoreState.length < 1)
                        return "";

                    return $("<button>").attr("type", "button").text(curcensoreState[0].EF_StateName)
                                    .on("click", ShowCensoreDialog);
                }
            },
            { name: "EF_CensoreComment3", title: "审核明细3", type: "number", width: 80, editing: false, align:"left"},

            { type: "control" }
        ]
    });

});


//获取用户类型id相关的所有用户
function GetUsersFromTypeId(userTypes, userTypeId)
{
    //获取用户类型
    var curUserType =$.grep(userTypes,function(tmp){ return tmp.id == userTypeId });
    if (curUserType.length < 1)
        return "";

    var strUrl = "/AppUserManager/"
    if (curUserType[0].EF_TypeName == "超级管理员")
        strUrl += "superAdministrators/";
    else if (curUserType[0].EF_TypeName == "管理员")
        strUrl += "administrators/";
    else if (curUserType[0].EF_TypeName == "教师")
        strUrl += "teachers/";
    else if (curUserType[0].EF_TypeName == "院长")
        strUrl += "chiefCollegeLeaders/";
    else if (curUserType[0].EF_TypeName == "副院长")
        strUrl += "collegeLeaders/";
    else if (curUserType[0].EF_TypeName == "学生")
        strUrl += "students/";


    //从数据库获取相应用户
    var users = [];
    $.ajax({
        type: "GET",
        url: strUrl,
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
            users.push(newFields);
        });
    });

    return users;
}

//用户进行审核
function ShowCensoreDialog(event)
{
    var tmpHtml = "<p>访问服务器出错！</p>";
    //获取审核界面，并返回弹出的html
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/doCensore/",
        dataType: "text",
        data:event.data,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).done(function(result)
    {
        tmpHtml = result;
    }).fail(function(result)
    {
        alert("error");
    });

    $("#div_popWindow").html(tmpHtml);
    $("#div_popWindow").css('display','block');
    $("#div_block").css('display','block');

    return false;
}

//展示子表格
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

