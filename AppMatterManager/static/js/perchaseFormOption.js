var nLastSelFormId = 0;

//预采购清单
$(function()
{
    //调整弹出窗口的大小
    $("#div_popWindow").css('top','10%');
    $("#div_popWindow").css('left','5%');
    $("#div_popWindow").css('width','90%');
    $("#div_popWindow").css('height','50%');

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

    $("#formGrid").jsGrid({
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

        //点击时显示下面表格
        rowClick: function (args)
        {
            if (lastClickRow != "")
                lastClickRow.removeClass("highLightRow");

            lastClickRow = this.rowByItem(args.item); 
            lastClickRow.addClass("highLightRow");
            nLastSelFormId = args.item.id;
        },


        //自主处理每行的显示
        rowRenderer: function(item, itemIndex)
        {
            var row = $("<tr>");

            //调用父函数处理各单元格
            this._renderCells(row, item);

            //循环处理每一列,添加tooltip
            var cells = row.children("td");
            for(var nIndex = 0; nIndex < cells.length; nIndex++ )
            {
                cells.eq(nIndex).attr("title", cells.eq(nIndex).text());
            }

            return row;
        },

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();

                $.ajax({
                    type: "GET",
                    url: "/AppMatterManager/perchaseForms/",
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
                    url: "/AppMatterManager/perchaseForms/" + curItem.id,
                });
            }
        },

        fields: [
            {
                headerTemplate: function() 
                {
                       return "预采购用户类型";
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
                       return "预采购用户";
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
                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId1 });
                    if (curcensoreState.length < 1)
                        return "";
                    else
                        return curcensoreState[0].EF_StateName;
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
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
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
                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId2 });
                    if (curcensoreState.length < 1)
                        return "";
                    else
                        return curcensoreState[0].EF_StateName;
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核明细2";
                },
                itemTemplate: function(value, item)
                {
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
                        return "";
                    else
                        return item.EF_CensoreComment2;
                }
            },

            {
                headerTemplate: function() 
                {
                       return "审核人3";
                },
                itemTemplate: function(value, item)
                {
                    //获取此审核模型相应的审核人员类型 
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
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
                    var curcensoreState =$.grep(censoreStates,function(tmp){ return tmp.id == item.EF_CensoreStateId3 });
                    if (curcensoreState.length < 1)
                        return "";
                    else
                        return curcensoreState[0].EF_StateName;
                }
            },
            {
                headerTemplate: function() 
                {
                       return "审核明细3";
                },
                itemTemplate: function(value, item)
                {
                    var curPattern = $.grep(censorePatterns,function(tmp){ return tmp.id == item.EF_CensorePatternId });
                    if (curPattern.length < 0 || curPattern[0].EF_StepsCount < 1)
                        return "";
                    else
                        return item.EF_CensoreComment3;
                }
            },

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


function confirmForm()
{
    //设置当前入库单的第一个审核人;
    var postData = {fromTableName:"PerchaseMatterDetails", fromTableFormId:nLastSelFormId,
                    toTableName:"ImportMatterDetails", toTableFormId:0};

    //新建入库表并设置入库表的审核人
    $.ajax({
        type: "POST",
        url: "/AppMatterManager/copyMatterDetails/",
        dataType: "text",
        data: postData,
        async :false,  //改为同步执行，否则不能对外部变量附值
    }).fail(function(response, textStatus){
        alert(response["responseText"]);
        return;
    });

    //调整弹出窗口的大小
    $("#div_popWindow").css('top','20%');
    $("#div_popWindow").css('left','35%');
    $("#div_popWindow").css('width','30%');
    $("#div_popWindow").css('height','20%');

    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");

    $("#jsGrid").jsGrid("loadData");
}

function cancelForm()
{
    //调整弹出窗口的大小
    $("#div_popWindow").css('top','20%');
    $("#div_popWindow").css('left','35%');
    $("#div_popWindow").css('width','30%');
    $("#div_popWindow").css('height','20%');

    $("#div_block").css('display','none');
    $("#div_popWindow").css('display','none');
    $("#div_popWindow").html("");
}
