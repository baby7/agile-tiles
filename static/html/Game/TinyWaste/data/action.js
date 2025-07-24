var BATTLE_OBJ = new battleObj();
var BATTLE_ATONCE = false;
ITEM_DATA = clone(ITEM_DATA_INIT);
TOOL_DATA = clone(TOOL_DATA_INIT);
CROP_DATA = clone(CROP_DATA_INIT);
MAP_DATA = clone(MAP_DATA_INIT);
PLAYER_STATUS = clone(PLAYER_STATUS_INIT);
//================================================================================================


//====每秒检测====
function tick(){
    updateStatus("hunger", -HUNGER_SPEED);
    updateStatus("thirst", -THIRST_SPEED);
    excreteCheck();
    buffCheck();
    itemCheck();
    disasterChk();
    resRefresh(MAP_DATA);
    var rate = realVal("radiation") - 20;
    var goodlist = ["hulk", "stonelike"];
    var badlist = ["spew", "tumour", "polydactylism", "illness", "anaemia"];
    if(!BEGINNER_FLAG){
        goodlist.push.apply(goodlist, ["longleg", "eagle"]);
        badlist.push.apply(badlist, ["hairlose", "ugly", "slow_1"])
    }

    if((sysTime-LAST_RAD_TIME)/1000/60/60 >= 2){
        if(rate>0 && Math.random()<rate/500/realVal("luck")){
            var goodrate = realVal("luck")>=10 ? 10 : realVal("luck");
            if(Math.random()*13 <= goodrate){
                var buff = goodlist[Math.floor(Math.random()*goodlist.length)];
                getBuff(buff);
            }
            else{
                var buff = badlist[Math.floor(Math.random()*badlist.length)];
                getBuff(buff);
            }
        }
        LAST_RAD_TIME = clone(sysTime);
    }
    if((sysTime-EXPLORE_CHECK)/1000/60/60 >= 6){
        destroyPlace();
        EXPLORE_CHECK = clone(sysTime);
        HAIR_AMOUNT += 0.5;
        HAIR_AMOUNT = HAIR_AMOUNT>100 ? 100 : HAIR_AMOUNT;
    }
    if((sysTime-DAILY_CHECK)/1000/60/60 >= 24){
        DAILY_CHECK = clone(sysTime);
        apCheck(0);
    }
    
    if(TIMER_FLAG){
        setTimeout(tick, 1000);
    }
}

//屎尿功能
function excreteCheck(){
    var excrete = ["shit", "urine"];
    var excreteAmount = [6, 8];
    var sanValue = [-12, -6];
    var statusMinus = ["hunger", "thirst"];
    var statusValue = [-25, -12];
    var flag = 0;
    for(var i in EXCRETE_TIME){
        var timeSpan = Math.floor((sysTime - EXCRETE_TIME[i])/1000/60/60);
        var nowTab = $(".tab-pane.active").attr("id");
        if(!EXCRETE_FLAG[i] && timeSpan>=EXCRETE_INTERVAL[i]){
            EXCRETE_FLAG[i] = true;
            getBuff(excrete[i]+"Ready");
            if($(".tab-pane.active").attr("id")=="map"){
                var newObj = new mapObj($("#map").attr("place"));
                newObj.create();
            }
        }
        if(EXCRETE_FLAG[i] && timeSpan>=EXCRETE_MAX[i] && $.inArray(nowTab, ["battle", "trade", "loading", "temp", "workbench"])==-1){
            clear(TEMP_DATA);
            TEMP_DATA[excrete[i]] = excreteAmount[i];
            updateStatus("san", sanValue[i]);
            updateStatus(statusMinus[i], statusValue[i]);
            EXCRETE_FLAG[i] = false;
            EXCRETE_TIME[i] = clone(sysTime);
            removeBuff(excrete[i]+"Ready");
            flag = 1;
        }
    }
    if(flag){
        toLoading(0.5, "excrete");
    }
}

function buffCheck(){
    for(var i in PLAYER_STATUS.buff){
        var timeSpan = (sysTime - PLAYER_STATUS.buff[i][1])/1000/60;
        var timeLast = (sysTime - PLAYER_STATUS.buff[i][0])/1000/60;
        DEATH_FOR = BUFF_DATA[i].name!=undefined ? "<span class='badBuffName'>"+BUFF_DATA[i].name+"</span>" : DEATH_FOR;

        if(timeSpan>=BUFF_DATA[i].interval){
            if(BUFF_DATA[i].effect!=undefined){
                var buffer = BUFF_DATA[i].temp ? true : null;
                for(var j in BUFF_DATA[i].effect){
                    if(BUFF_DATA[i].effect[j].percent != undefined){
                        var status = BUFF_DATA[i].effect[j].type;
                        var value = Math.round(PLAYER_STATUS[status].value * BUFF_DATA[i].effect[j].percent);
                        updateStatus(j, value, buffer);
                    }
                    else{
                        updateStatus(j, BUFF_DATA[i].effect[j], buffer);
                    }
                }
                PLAYER_STATUS.buff[i][1] = clone(sysTime);
                if(PLAYER_STATUS.buff[i][2] == undefined){
                    PLAYER_STATUS.buff[i].push(1);
                }
                else{
                    PLAYER_STATUS.buff[i][2] += 1;
                }
            }
            if(BUFF_DATA[i].update!=undefined){
                eval(BUFF_DATA[i].update);
                PLAYER_STATUS.buff[i][1] = clone(sysTime);
            }
        }
        if(BUFF_DATA[i].cost!=undefined){
            var cost = "";
            var order = 0;
            for(var j in BUFF_DATA[i].cost){
                for(var k in BAG_DATA){
                    if(k == BUFF_DATA[i].cost[j]){
                        cost = k;
                        order = parseInt(j) + 1;
                        break;
                    }
                }
                if(cost != ""){
                    break;
                }
            }
            if(cost == ""){
                $("#bag .item[id='"+i+"']").trigger("selfUnload");
            }
            if(cost != "" && timeSpan>=BUFF_DATA[i].interval/order){
                caculate(BAG_DATA, cost, -1);
                PLAYER_STATUS.buff[i][1] = clone(sysTime);
                if(BAG_DATA[cost] <= 0){
                    $("#bag .item[id='"+i+"']").trigger("selfUnload");
                }
                updateItem(cost, $("#bag"));
            }
        }
        if(BUFF_DATA[i].last!=undefined && timeLast>=BUFF_DATA[i].last){
            removeBuff(i);
            if(BUFF_DATA[i].after != undefined){
                eval(BUFF_DATA[i].after);
            }
        }
    }
}

function itemCheck(){
    for(var i in BAG_DATA){
        if(ITEM_DATA[i].interval != undefined){
            var timeSpan = (sysTime - PLAYER_STATUS.buff[ITEM_DATA[i].buffPick][1])/1000/60;
            if(timeSpan>=ITEM_DATA[i].interval){
                caculate(BAG_DATA, i, -1);
                updateItem(i, $("#bag"));
                PLAYER_STATUS.buff[ITEM_DATA[i].buffPick][1] = clone(sysTime);
            }
        }
    }
}

function hungerChk(){
    if(realVal("hunger")<=30 && !BEGINNER_FLAG){
        getBuff("starve_1");
    }
    else if(realVal("hunger")>30){
        removeBuff("starve_1");
    }
    
    if(realVal("hunger")<=0){
        getBuff("starve_2");
    }
    else if(realVal("hunger")>0){
        removeBuff("starve_2");
    }
}
function thirstChk(){
    if(realVal("thirst")<=30 && !BEGINNER_FLAG){
        getBuff("hydropenia_1");
    }
    else if(realVal("thirst")>30){
        removeBuff("hydropenia_1");
    }
    
    if(realVal("thirst")<=0 && !BEGINNER_FLAG){
        getBuff("hydropenia_2");
    }
    else if(realVal("thirst")>0){
        removeBuff("hydropenia_2");
    }
    
}
function sanChk(){
    if(realVal("san")<=10){
        getBuff("san_1");
    }
    else if(realVal("san")>10){
        removeBuff("san_1");
    }
    
    if(realVal("san")<=0 && !BEGINNER_FLAG){
        getBuff("san_4");
    }
    else if(realVal("san")>0){
        removeBuff("san_4");
    }
    
    if(realVal("san")<=-10 && !BEGINNER_FLAG){
        getBuff("san_2");
    }
    else if(realVal("san")>-10 && PLAYER_STATUS.buff["san_2"]!=undefined){
        removeBuff("san_2");
    }
    
    if(realVal("san")<=-20 && !BEGINNER_FLAG){
        getBuff("san_3");
    }
    else if(realVal("san")>-20){
        //$("#background").css({"background-color":"#FFFFFF"});
        removeBuff("san_3");
    }
    
    if(realVal("san")<=-50 && !BEGINNER_FLAG){
        getBuff("san_5");
    }
    else if(realVal("san")>-50){
        $("body").css({"font-size":"1.3em"})
        removeBuff("san_5");
    }
}

function disasterChk(){
    if(DISASTER == ""){
        var a = Object.keys(DISASTER_TYPE);
        if((sysTime-DISASTER_CHECK)/1000/60/60>=5 && (sysTime-DISASTER_LASTTIME)/1000/60/60/24>=15){
            if(Math.random()*100 < 10){
                DISASTER = a[Math.floor(Math.random()*a.length)];
                DISASTER_TIME = Math.floor(Math.random()*DISASTER_TYPE[DISASTER].time + DISASTER_TYPE[DISASTER].time*0.25);
                DISASTER_LAST = Math.floor(Math.random()*DISASTER_TYPE[DISASTER].last + DISASTER_TYPE[DISASTER].last*0.25);
                DISASTER_LASTTIME = clone(sysTime);
                var time = DISASTER_TIME>=60 ? (Math.floor(DISASTER_TIME/60)+"小时"+Math.floor(DISASTER_TIME%60)+"分钟") : (Math.floor(DISASTER_TIME)+"分钟");
                var msg = "<span class='badBuffName'>"+DISASTER_TYPE[DISASTER].name+"</span> "
                        + "即将在 <span class='badBuffName'>"+time+"</span> 后到来。";
                showMsg(msg);

                $("#clock").popover("destroy");
                var clockMsg = "<span id='disasterInfo' class='disasterInfo'>"+DISASTER_TYPE[DISASTER].name+" <span id='countdownType'>倒计时</span>：<span id='countdown'></span></span>";
                $("#clock").popover({html:true, trigger: "click", title:clockMsg});
                $("#clock").popover("show");
            }
            DISASTER_CHECK = clone(sysTime);
        }
    }
    else{
        if((sysTime-DISASTER_LASTTIME)/1000/60>=DISASTER_TIME && !DISASTER_EFFECT){
            DISASTER_EFFECT = true;
            switch(DISASTER){
                case "sandstorm":
                if($(".tab-pane.active").attr("id")=="map" && $.inArray($("#map").attr("place"), ["home", "cave", "vault7"])==-1){
                    getBuff("sandstorm");
                }
                var flag = 0;
                if(!BEGINNER_FLAG){
                    for(var i in MAP_DATA.farm.resource){
                        delete MAP_DATA.farm.resource[i];
                        if($(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")=="farm"){
                            $("#map .btn[id='"+i+"']").remove();
                        }
                        flag = 1;
                    }
                }
                if(flag){
                    getSum(MAP_DATA.farm.resource);
                    showMsg("你的农田由于在地洞之外，受到沙尘暴影响，失去了所有作物。");
                }
                break;
                case "rain":
                if($(".tab-pane.active").attr("id")=="map" && $.inArray($("#map").attr("place"), ["home", "cave", "vault7"])==-1){
                    getBuff("rain");
                }
                var a = Object.keys(MAP_DATA.well.resource.water.get);
                a = MAP_DATA.well.resource.water.get[a[0]];
                MAP_DATA.well.resource.water.get = {dirtyWater:a};
                showMsg("受到辐射雨影响，水井中的水全部受到了污染。");
                break;
            }
        }
        if((sysTime-DISASTER_LASTTIME)/1000/60>=DISASTER_TIME+DISASTER_LAST && DISASTER_EFFECT){
            switch(DISASTER){
                case "sandstorm":
                removeBuff("sandstorm");
                break;
                case "rain":
                var a = Object.keys(MAP_DATA.well.resource.water.get);
                a = MAP_DATA.well.resource.water.get[a[0]];
                MAP_DATA.well.resource.water.get = {water:a};
                if($.inArray("filter_4", TOOL_FINISHED) != -1){
                    MAP_DATA.well.resource.water.get = {cleanWater:a};
                }
                removeBuff("rain");
                break;
            }
            $("#clock").popover("destroy");
            showMsg("<span class='badBuffName'>"+DISASTER_TYPE[DISASTER].name+"</span> 已结束。");
            DISASTER = "";
            DISASTER_EFFECT = false;
            DISASTER_CHECK = clone(sysTime);
        }
    }
}

function spew(){
    var nowTab = $(".tab-pane.active").attr("id");
    if($.inArray(nowTab, ["battle", "trade", "loading", "temp", "workbench"]) == -1){
        updateStatus("san", -10);
        getItem({spew:Math.floor(Math.random()*10)+1}, true);
    }
}

function hairlose(){
    if(HAIR_AMOUNT > 0){
        HAIR_AMOUNT -= 1;
    }
    if(HAIR_AMOUNT <= 0){
        removeBuff("hairlose");
    }
    getItem({hair:1});
}

function crazy(){
    for(var i in BAG_DATA){
        if(ITEM_DATA[i].usable && Math.random()*100<33.33){
            $("#bag .item[id='"+i+"']").trigger("selfUse");
            return;
        }
        if(Math.random()*100<33.33){
            for(var j in PLAYER_STATUS.equip){
                if(PLAYER_STATUS.equip[j] == i){
                    $("#bag .item[id='"+i+"']").trigger("selfUnload");
                    return;
                }
            }
            $("#bag .item[id='"+i+"']").trigger("selfRemove");
            return;
        }
    }
    $(".tab-pane.active button").each(function(){
        if(Math.random()*100 < 33.33){
            $(this).click();
            return false;
        }
    });
}

function rainbow(){
    var color = "#"+("00000"+(Math.random()*0x1000000<<0).toString(16)).substr(-6);
    $("#background").css({"background-color":color});
}

//资源再生
function resInit(data){
    for(var i in data){
        if(typeof data[i] == "object"){
            if(i == "resource"){
                for(var j in data[i]){
                    if(data[i][j].lastGrow == undefined){
                        data[i][j].lastGrow = clone(originTime);
                    }
                }
            }
            else if(i == "enemy"){
                if(data[i].lastGrow == undefined){
                    data[i].lastGrow = clone(originTime);
                }
            }
            else if(i == "trash"){
                if(data.trashLastGrow == undefined){
                    data.trashLastGrow = clone(originTime);
                }
            }
            else {
                resInit(data[i]);
            }
        }
    }
}

function resRefresh(data){
    for(var i in data){
        if(typeof data[i] == "object"){
            if(i == "resource"){
                for(var j in data[i]){
                    var timeSpan = (sysTime - data[i][j].lastGrow)/1000/60;
                    if(data[i][j].refresh!=0 && timeSpan>=data[i][j].refresh && data[i][j].value<data[i][j].max){
                        if(j=="manure_home" || j=="gas_home"){
                            if(TOILET_DATA.shit!=undefined && TOILET_DATA.shit>0){
                                caculate(TOILET_DATA, "shit", -1);
                                if($(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")=="toilet"){
                                    updateItem("shit", $("#toiletData"));
                                }
                                else if(TOILET_DATA.shit <= 0){
                                    delete TOILET_DATA.shit;
                                }
                            }
                            else if(TOILET_DATA.urine!=undefined && TOILET_DATA.urine>=2 && j!="gas_home"){
                                caculate(TOILET_DATA, "urine", -2);
                                if($(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")=="toilet"){
                                    updateItem("urine", $("#toiletData"));
                                }
                                else if(TOILET_DATA.urine <= 0){
                                    delete TOILET_DATA.urine;
                                }
                            }
                            else{
                                continue;
                            }
                        }
                        caculate(data[i][j], "value", 1);
                        data[i][j].lastGrow = clone(sysTime);
                        var flag = 0;
                        if($.inArray($("#map").attr("place"), ["home", "origin", "outside"]) == -1){
                            flag = 1;
                        }
                        if($(".tab-pane.active").attr("id")=="map" && flag){
                            var newObj = new mapObj($("#map").attr("place"));
                            newObj.create();
                        }
                    }
                    else if(data[i][j].refresh!=0 && data[i][j]>=data[i][j].max){
                        data[i][j].lastGrow = clone(sysTime);
                    }
                }
            }
            else if(i=="enemy" && data[i].refresh!=undefined){
                var timeSpan = (sysTime - data[i].lastGrow)/1000/60;
                if(timeSpan >= data[i].refresh){
                    for(var j in data[i].normal){
                        var value = Math.ceil(data[i].normal[j]*0.02);
                        caculate(data[i].normal, j, value==0 ? 1 : value);
                    }
                    data[i].lastGrow = clone(sysTime);
                }
            }
            else if(i=="trash" && data.trashRefresh!=undefined){
                var timeSpan = (sysTime - data.trashLastGrow)/1000/60;
                if(timeSpan >= data.trashRefresh){
                    for(var j in data[i]){
                        var value = Math.ceil(data[i][j].amount*0.1);
                        caculate(data[i][j], "amount", value==0 ? 1 : value);
                    }
                    data.trashLastGrow = clone(sysTime);
                }
            }
            else {
                resRefresh(data[i]);
            }
        }
    }
}
//================================================================================================

//====通用临时界面====
function tempObj(mode){
    function allPickUp(){
        for(var id in TEMP_DATA){
            var volumeFlag = 1;
            if(ITEM_DATA[id].volume != undefined){
                if(KETTLE_VOLUME == 0){
                    volumeFlag = 0;
                    continue;
                }
                coverChk(id, $("#temp"), TEMP_DATA);
                continue;
            }

            var containerFlag = 1;
            if(ITEM_DATA[id].container!=undefined){
                if(BAG_DATA[ITEM_DATA[id].container]==undefined){
                    containerFlag = 0;
                }
                else{
                    containerChk(id, $("#temp"), TEMP_DATA);
                    continue;
                }
            }
            var sum = getSum(BAG_DATA);
            if(BAG_DATA[id] != undefined){
                sum -= 1;
            }

            if(sum<BAG_CAP && containerFlag && volumeFlag){
                pickChk(id, $("#temp"), TEMP_DATA, $("#bag"), BAG_DATA);
            }
        }
        autosort(BAG_DATA);
    }

    this.create = function(){
        $("#temp").empty();
        $("#temp").attr("mode", mode);
        if($.inArray(mode, ["pickUp", "resource", "trash", "output"]) != -1){
            var newBtn = newElement("button", "", "", "btn btn-default", "全部拾取");
            newBtn.onclick = function(){allPickUp();};
            $("#temp").append(newBtn);
        }

        if(EX_RESOURCE!="" && EX_RESOURCE.value>0){
            var flag = 1;
            if(Math.ceil(realVal("energy")) < EX_RESOURCE.energy){
                flag = 0;
            }
            for(var i in EX_RESOURCE.require){
                var own = BAG_DATA[i]==undefined?0:BAG_DATA[i];
                if($.inArray(i, ["axe", "shovel", "pickaxe", "hoe"]) != -1){
                    for(var j in BAG_DATA){
                        if(j.indexOf(i) != -1){
                            own = BAG_DATA[j];
                            break;
                        }
                    }
                }
                if(own < EX_RESOURCE.require[i]){
                    flag = 0;
                    break;
                }
            }
            if(flag){
                var newBtn = newElement("button", "", "", "btn btn-default", "继续采集");
                newBtn.onclick = function(){
                    allPickUp();
                    var requireFlag = EX_RESOURCE.require!=undefined?0:1;
                    for(var i in EX_RESOURCE.require){
                        if(BAG_DATA[i]==undefined && $.inArray(i, ["axe", "shovel", "pickaxe", "hoe"]) != -1){
                            for(var j in BAG_DATA){
                                if(j.indexOf(i) == 0){
                                    caculate(BAG_DATA, j, -EX_RESOURCE.require[i]);
                                    updateItem(j, $("#bag"));
                                    requireFlag = 1;
                                    break;
                                }
                            }
                        }
                        else{
                            caculate(BAG_DATA, i, -EX_RESOURCE.require[i]);
                            updateItem(i, $("#bag"));
                            requireFlag = 1;
                        }
                    }
                    if(requireFlag){
                        caculate(EX_RESOURCE, "value", -1);
                        clear(TEMP_DATA);
                        for(var i in EX_RESOURCE.get){
                            TEMP_DATA[i] = clone(EX_RESOURCE.get[i]);
                        }
                        costTimeFunc(EX_RESOURCE.energy, 1, "resource");
                    }
                };
                $("#temp").append(newBtn);
            }
        }

        getBackBtn($("#temp"));

        $("#temp").append("<p/>");
        for(var i in TEMP_DATA){
            newObj = new itemObj(i, $("#temp"));
            newObj.create();
            if(mode=="output" && ITEM_DATA[i].container!=undefined){
                newObj.deleteItemData("container");
            }
        }
    }
}

//时间加速
function costTimeFunc(cost, costTime, mode, callback){
    if(DEATH_FLAG || !TIMER_FLAG){
        return;
    }
    if(costTime >= 0.5){
        $("#overlay").height(document.body.clientHeight);
        $("#overlay").width(document.body.clientWidth);
        $("#overlay").fadeTo(100, 0);

        $("#tablist a[href='#loading']").tab("show");
        var loadDiv = document.createElement("div");
        loadDiv.className = "loadDiv";
        var bar = document.createElement("div");
        bar.className = "loadingBar";
        loadDiv.appendChild(bar);
        $("#loading").append(loadDiv);
        
        var timecount = 0;
        pauseGame();

        function timeRun(){
            if(cost>1200){
                updateSysClock(Math.floor(cost/1200)*6, cost%1200*3/10, false, 2);
            }
            else if($.inArray(mode, ["resource", "trash"]) != -1){
                updateSysClock(0, cost*12, false, 2);
            }
            else{
                updateSysClock(6, 0, false, 2);
            }

            if($.inArray(mode, ["resource", "trash"]) != -1){
                timecount += cost/10;
            }
            else{
                timecount += cost>1200?cost/200:6;
            }   

            if(timecount < cost){
                $("#loading div div").stop(true);
                $("#loading div div").animate({width:timecount/cost*100+"%"}, 50, "linear");
                setTimeout(timeRun, 50);
            }
            else{
                function remove(){
                    $("#loading").empty();
                    if(mode == "bedUpgrade"){
                        toLoading(0.1, "bed", true, callback);
                    }
                    else if(mode.substr(0, 4) == "dest"){
                        toLoading(0.1, mode.substr(4));
                    }
                    else if($.inArray(mode, ["explore", "makeup"]) != -1){
                        callback();
                    }
                    else{
                        toLoading(0.1, mode, true, callback);
                    }
                    resumeGame();
                }

                $("#loading div div").animate({width:"100%"}, 100);
                if(mode.substr(0, 4) != "dest"){
                    buffCost(mode);
                }
                statusCost(cost, mode);
                itemCost(cost);
                resCost(MAP_DATA);
                if(DEATH_FLAG){
                    return;
                }
                $("#overlay").fadeOut(200, remove);
            }  
        }
        timeRun();
    }
    else{
        updateSysClock(cost, 0, false, 2);
        if(mode.substr(0, 4) != "dest"){
            buffCost(mode);
        }
        statusCost(cost, mode);
        itemCost(cost);
        resCost(MAP_DATA);
        if(DEATH_FLAG){
            return;
        }
        if(mode.substr(0, 4) == "dest"){
            toLoading(0.1, mode.substr(4));
        }
        if(callback != null){
            callback();
        }
    }
}

function statusCost(cost, mode){
    switch(mode){
        case "work": case "handwork": case "tech": case "lab": case "bedUpgrade": case "cook": case "forge": 
        case "filter": case "makeup":
        updateStatus("hunger", -HUNGER_SPEED * WORK_TIME_COST/2.5 * 1.2  * cost);
        updateStatus("thirst", -THIRST_SPEED * WORK_TIME_COST/2.5 * 1.2  * cost);
        updateStatus("energy", -WORK_ENERGY_COST * cost);
        break;
        case "train":
        updateStatus("hunger", -HUNGER_SPEED * WORK_TIME_COST/2.5 * 1.4  * cost);
        updateStatus("thirst", -THIRST_SPEED * WORK_TIME_COST/2.5 * 1.4  * cost);
        updateStatus("energy", -WORK_ENERGY_COST * 1.5 * cost);
        break;
        case "bed":
        updateStatus("hunger", -HUNGER_SPEED * WORK_TIME_COST/2.5 * 0.4  * cost);
        updateStatus("thirst", -THIRST_SPEED * WORK_TIME_COST/2.5 * 0.4  * cost);
        EXCRETE_TIME[0] = new Date(EXCRETE_TIME[0].getTime() + cost*60*1000);
        EXCRETE_TIME[1] = new Date(EXCRETE_TIME[1].getTime() + cost*60*1000);
        break;
        case "resource": case "trash":
        updateStatus("hunger", -HUNGER_SPEED * WORK_TIME_COST/2.5 * cost*2);
        updateStatus("thirst", -THIRST_SPEED * WORK_TIME_COST/2.5 * cost*2);
        updateStatus("energy", -cost);
        break;
        default:
        updateStatus("hunger", -HUNGER_SPEED/2.5 * cost);
        updateStatus("thirst", -THIRST_SPEED/2.5 * cost);
        updateStatus("energy", -1/15 * cost);
    }
}

function buffCost(mode){
    for(var i in PLAYER_STATUS.buff){
        DEATH_FOR = BUFF_DATA[i].name!=undefined ? "<span class='badBuffName'>"+BUFF_DATA[i].name+"</span>" : DEATH_FOR;

        if(BUFF_DATA[i].effect!=undefined && BUFF_DATA[i].interval!=undefined){
            var cost = (sysTime - PLAYER_STATUS.buff[i][1])/1000/60;
            cost = cost>BUFF_DATA[i].last ? BUFF_DATA[i].last : cost;
            if(PLAYER_STATUS.buff[i][2] == undefined){
                PLAYER_STATUS.buff[i].push(Math.floor(cost/BUFF_DATA[i].interval));
            }
            else{
                PLAYER_STATUS.buff[i][2] += Math.floor(cost/BUFF_DATA[i].interval);
            }
            
            var buffer = BUFF_DATA[i].temp ? true : null;
            for(var j in BUFF_DATA[i].effect){
                var times = 1;
                switch(mode){
                    case "bed":times = 0.5;break;
                    case "cook": case "lab": case "tech":times = 0.2;break;
                    case "work": case "handwork": case "forge": case "filter":
                    times = 0.75;break;
                }
                if(BUFF_DATA[i].temp){
                    times = 1;
                }
                if(mode=="bed" && (j=="san" || i=="san_4")){
                    continue;
                }

                if(BUFF_DATA[i].effect[j].percent != undefined){
                    var status = BUFF_DATA[i].effect[j].type;
                    var value = PLAYER_STATUS[status].value * BUFF_DATA[i].effect[j].percent;
                    if(!isNaN(value)){
                        updateStatus(j, value * Math.floor(cost/BUFF_DATA[i].interval) * times, buffer);
                    }
                }
                else{
                    var value = BUFF_DATA[i].effect[j] * Math.floor(cost/BUFF_DATA[i].interval) * times;
                    if(!isNaN(value)){
                        updateStatus(j, value, buffer);
                    }
                }
            }
        }
    }
}

function resCost(data){
    for(var i in data){
        if(typeof data[i] == "object"){
            if(i == "resource"){
                for(var j in data[i]){
                    var cost = (sysTime-data[i][j].lastGrow)/1000/60;
                    var timeSpan = Math.floor(cost/data[i][j].refresh);
                    if(data[i][j].refresh!=0 && cost>=data[i][j].refresh && data[i][j].value<data[i][j].max){
                        if(j=="manure_home" || j=="gas_home"){
                            if(TOILET_DATA.shit!=undefined && TOILET_DATA.shit>0){
                                caculate(TOILET_DATA, "shit", -timeSpan);
                                if(TOILET_DATA.shit <= 0){
                                    delete TOILET_DATA.shit;
                                }
                            }
                            else if(TOILET_DATA.urine!=undefined && TOILET_DATA.urine>=2 && j!="gas_home"){
                                caculate(TOILET_DATA, "urine", -2*timeSpan);
                                if(TOILET_DATA.urine <= 0){
                                    delete TOILET_DATA.urine;
                                }
                            }
                            else{
                                continue;
                            }
                        }
                        caculate(data[i][j], "value", timeSpan);
                        data[i][j].value = data[i][j].value>data[i][j].max ? clone(data[i][j].max) : data[i][j].value;
                        data[i][j].lastGrow = clone(sysTime);
                    }
                    else if(data[i][j].refresh!=0 && data[i][j]>=data[i][j].max){
                        data[i][j].lastGrow = clone(sysTime);
                    }
                }
            }
            else if(i == "enemy" && data[i].refresh!=undefined){
                var cost = (sysTime-data[i].lastGrow)/1000/60;
                var timeSpan = Math.floor(cost/data[i].refresh);
                if(cost >= data[i].refresh){
                    for(var j in data[i].normal){
                        var value = Math.ceil(data[i].normal[j]*0.02 * timeSpan);
                        caculate(data[i].normal, j, value==0 ? 1 : value);
                    }
                    data[i].lastGrow = clone(sysTime);
                }
            }
            else if(i=="trash" && data.trashRefresh!=undefined){
                var cost = (sysTime-data.trashLastGrow)/1000/60;
                var timeSpan = Math.floor(cost/data.trashRefresh);
                if(cost >= data.trashRefresh){
                    for(var j in data[i]){
                        var value = Math.ceil(data[i][j].amount*0.1 * timeSpan);
                        caculate(data[i][j], "amount", value==0 ? 1 : value);
                    }
                    data.trashLastGrow = clone(sysTime);
                }
            }
            else {
                resCost(data[i]);
            }
        }
    }
}

function itemCost(cost){
    for(var i in BAG_DATA){
        if(ITEM_DATA[i].interval != undefined){
            var timeSpan = (sysTime - PLAYER_STATUS.buff[ITEM_DATA[i].buffPick][1])/1000/60;
            if(timeSpan>=ITEM_DATA[i].interval){
                caculate(BAG_DATA, i, -Math.floor(cost/ITEM_DATA[i].interval));
                updateItem(i, $("#bag"));
            }
        }
    }
}
//================================================================================================

//====状态对象====
function statusObj(id){
    //创建状态图标
    this.create = function(){
        var newBtn = newElement("div", id, "", "status", PLAYER_STATUS[id].name + "<br/>" + Math.ceil(realVal(id)));
        newBtn.onmouseover = function(){$("#info").html(PLAYER_STATUS[id].desc);};
        newBtn.ontouchstart = newBtn.onmouseover;
        $("#status").append(newBtn);
    }

    this.update = function(){
        var self = $("div[id='"+id+"']");
        self.html(PLAYER_STATUS[id].name + "<br/>" + Math.ceil(realVal(id)));

        //buff图标
        var buffFlag = 0;
        var buff;
        for(var i in PLAYER_STATUS.buff){
            if(BUFF_DATA[i].name!=undefined && BUFF_DATA[i].on==id){
                buffFlag = 1;
                if(buff!=undefined && BUFF_DATA[i].type!="bad"){
                    continue;
                }
                buff = i;
            }
        }
        if(buffFlag){
            var buffType = BUFF_DATA[buff].type + "Badge";
            self.html(self[0].innerHTML + "<span class='badge "+buffType+"'>!</span>");
        }

        //颜色变化

    };
}
//================================================================================================

//====物品对象====
function itemObj(id, belong){
    var ITEM_DATA_SELF = {};
    this.getItemData = function(){
        return ITEM_DATA_SELF;
    }
    this.setItemData = function(attr, value){
        if(ITEM_DATA_SELF[attr] != undefined){
            ITEM_DATA_SELF[attr] = value;
            belong.find(".item[id='"+id+"']").attr("itemdata", JSON.stringify(ITEM_DATA_SELF));
        }
    }
    this.deleteItemData = function(attr){
        if(ITEM_DATA_SELF[attr] != undefined){
            delete ITEM_DATA_SELF[attr];
        }
    }
    this.cloneItemData = function(itemdata){
        ITEM_DATA_SELF = clone(JSON.parse(itemdata));
        belong.find(".item[id='"+id+"']").attr("itemdata", JSON.stringify(ITEM_DATA_SELF));
    }

    //创建物品图标
    this.create = function(){
        ITEM_DATA_SELF = clone(ITEM_DATA[id]);
        var holder = getHolder(belong[0]);
        var amount = "<br>" + holder[id];
        var name = ITEM_DATA_SELF.name;
        for(var i in PLAYER_STATUS.equip){
            if(PLAYER_STATUS.equip[i]==id && belong.attr("id")=="bag"){
                name = "<span class='noneBuffName'>[" + name + "]</span>";
                break;
            }
        }
        if(ITEM_DATA_SELF.durab != undefined){
            var percent = holder[id] % ITEM_DATA_SELF.durab / ITEM_DATA_SELF.durab * 100;
            percent = percent==0?100:percent;
            var sum = Math.ceil(holder[id] / ITEM_DATA_SELF.durab);
            amount = "<div class='durabDiv'><div class='loadingBar' style='width:"+percent+"%;'></div></div>"
            + "<br>" + sum;
        }
        else{
            var volume = "";
            if(ITEM_DATA[id].volume!=undefined && belong.attr("id")=="bag"){
                volume = "/";
                volume = volume + (Math.ceil(holder[id]/KETTLE_VOLUME) * KETTLE_VOLUME).toString();
            }
            amount = "<br>" + holder[id] + volume;
        }
        var newBtn = newElement("button", id, "", "item", name + amount);
        //newBtn.setAttribute("itemdata", JSON.stringify(ITEM_DATA_SELF));
        function clickChk(item){
            var target = $(".tab-pane.active").attr("id");
            var clickFlag = 0;
            if(target == "map"){
                target = $("#map").attr("place");
            }
            if(target=="toilet" || 
                (target=="workbench" && $("#workbench").attr("mode")=="cook") ||
                target=="trade"){
                clickFlag = 1;
            }
            if(clickFlag){
                $(".item").popover("destroy");
                clickEvent.call(item);
            }
            else{
                item.onclick = function(){clickEvent.call(item);}
                showinfo.call(item);
                item.focus();
            }
        }

        if(navigator.userAgent.match(/mobile/i)){
            newBtn.onclick = function(){
                clickChk(this);
            };
        }
        else{
            newBtn.onmouseover = function(){
            this.onclick = function(){clickEvent.call(this);}
                if(this.parentNode != undefined){
                    var thisparent = this.parentNode.id;
                    var thisid = this.id;
                    $(".item").each(function(){
                        if($(this)[0].parentNode!=undefined && $(this)[0].parentNode.id!=thisparent ||
                            $(this).attr("id")!=thisid){
                            $(this).popover("destroy");
                        }
                    });
                }
                showinfo.call(this);
                this.focus();
            }
        }
        newBtn.onblur = function(){
            if(navigator.userAgent.match(/mobile/i)){
                this.onclick = function(){clickChk(this);}
            }
            else{
                this.onclick = function(){};
            }
            
        }

        belong.append(newBtn);
        belong.find(".item[id='"+id+"']").bind("selfShow", function(){showinfo.call(this);});
        belong.find(".item[id='"+id+"']").bind("selfClick", function(){clickEvent.call(this);});
        belong.find(".item[id='"+id+"']").bind("selfUse", function(){useItem(this);});
        belong.find(".item[id='"+id+"']").bind("selfEquip", function(){equipItem(id, this);});
        belong.find(".item[id='"+id+"']").bind("selfUnload", function(){unloadItem(id, this);});
        belong.find(".item[id='"+id+"']").bind("selfRemove", function(){removeItem(this);});
        getSum(holder);
    }

    //点击事件分发
    function clickEvent(){
        //重新获取父容器
        var layer = $("#"+this.parentNode.id);
        var holder = getHolder(this.parentNode);
        $("#info").empty();
        var target = $(".tab-pane.active").attr("id");
        var toLayer = $("#"+target);
        if(target == "map"){
            target = $("#map").attr("place");
        }
        if(target == "toilet"){
            toLayer = $("#toiletData");
        }
        var toHolder = getHolder(toLayer[0]);
        var cookFlag = 0;
        if(target=="workbench" && $("#workbench").attr("mode")=="cook"){
            cookFlag = 1;
            toLayer = $("#stuff");
        }
        var tradeFlag = 0;
        if(target=="trade"){
            tradeFlag = 1;
            toHolder = TRADE_GIVE;
            toLayer = $("#tradeGive");
        }
        //在背包中，则判断目标是否为箱子和交易框
        if(this.parentNode.id == "bag"){
            if($.inArray(target, ["box", "temp", "toilet"])!=-1 || cookFlag || tradeFlag){
                for(var i in PLAYER_STATUS.equip){
                    if(PLAYER_STATUS.equip[i] == id){
                        return;
                    }
                }
                if(cookFlag && getSum(COOK_DATA)>=3 && COOK_DATA[id]==undefined){
                    return;
                }
                if(target=="toilet" && ((getSum(TOILET_DATA)>=2 && TOILET_DATA[id]==undefined) || $.inArray(id, ["shit", "urine"])==-1)){
                    return;
                }
                
                if(target == "box"){
                    var sum = getSum(BOX_DATA);
                    if(BOX_DATA[id] != undefined){
                        sum -= 1;
                    }
                    if(sum >= BOX_CAP){
                        $(".item").popover("destroy");
                        alert('箱子已满，无法转移。');
                        return;
                    }
                }
                if(tradeFlag){
                    if(holder == BAG_DATA){
                        var amount = $("#x10").is(":checked") ? 10 : 1;
                        amount = $("#x100").is(":checked") ? 100 : amount;
                        if(ITEM_DATA_SELF.durab != undefined){
                            amount *= ITEM_DATA_SELF.durab;
                        }
                        amount = amount>=BAG_DATA[id] ? clone(BAG_DATA[id]) : amount;
                        
                        $(".item").popover("destroy");
                        if(ITEM_DATA_SELF.important){
                            return;
                        }
                        if(toHolder[id] == undefined){
                            toHolder[id] = amount;
                            var newObj = new itemObj(id, toLayer);
                            newObj.create();
                            updateItem(id, toLayer);
                            caculate(BAG_DATA, id, -amount);
                            updateItem(id, $("#bag"));
                        }
                        else{
                            caculate(toHolder, id, amount);
                            updateItem(id, toLayer);
                            caculate(BAG_DATA, id, -amount);
                            updateItem(id, $("#bag"));
                        }
                    }
                    tradeCheck();
                }
                else{
                    $(".item").popover("destroy");
                    pickChk(id, $("#bag"), BAG_DATA, toLayer, toHolder)
                    if(cookFlag){
                        cookCheck();
                    }
                    if(toHolder == BOX_DATA){
                        autosort(toHolder);
                    }
                }
            }
        }
        //默认拾取到背包
        else{
            if(tradeFlag && (holder==TRADE_DATA || holder==TRADE_GET)){
                var amount = $("#x10").is(":checked") ? 10 : 1;
                amount = $("#x100").is(":checked") ? 100 : amount;
                if(ITEM_DATA_SELF.durab != undefined){
                    amount *= ITEM_DATA_SELF.durab;
                }
                amount = amount>=holder[id] ? clone(holder[id]) : amount;
                
                $(".item").popover("destroy");
                if(holder == TRADE_DATA){
                    if(TRADE_GET[id] == undefined){
                        TRADE_GET[id] = amount;
                        var newObj = new itemObj(id, $("#tradeGet"));
                        newObj.create();
                        updateItem(id, $("#tradeGet"));
                        caculate(holder, id, -amount);
                        updateItem(id, layer);
                    }
                    else{
                        caculate(TRADE_GET, id, amount);
                        updateItem(id, $("#tradeGet"));
                        caculate(holder, id, -amount);
                        updateItem(id, layer);
                    }
                }
                else if(holder == TRADE_GET){
                    if(TRADE_DATA[id] == undefined){
                        TRADE_DATA[id] = amount;
                        var newObj = new itemObj(id, $("#goods"));
                        newObj.create();
                        updateItem(id, $("#goods"));
                        caculate(holder, id, -amount);
                        updateItem(id, layer);
                    }
                    else{
                        caculate(TRADE_DATA, id, amount);
                        updateItem(id, $("#goods"));
                        caculate(holder, id, -amount);
                        updateItem(id, layer);
                    }
                }
                tradeCheck();
            }
            else{
                //容器检查
                if(ITEM_DATA_SELF.volume != undefined){
                    if(KETTLE_VOLUME == 0){
                        $(".item").popover("destroy");
                        alert("未制作水壶，无法拾取 "+ITEM_DATA_SELF.name+"。");
                        return;
                    }
                    $(".item").popover("destroy");
                    coverChk(id, layer, holder);
                    autosort(BAG_DATA);
                    if(cookFlag){
                        cookCheck();
                    }
                    if(tradeFlag){
                        tradeCheck();
                    }
                    return;
                }
                if(ITEM_DATA_SELF.container!=undefined && holder!=BOX_DATA && !tradeFlag){
                    if(BAG_DATA[ITEM_DATA_SELF.container] == undefined){
                        $(".item").popover("destroy");
                        alert("背包中没有 "+ITEM_DATA[ITEM_DATA_SELF.container].name+"，无法拾取 "+ITEM_DATA_SELF.name+"。");
                        return;
                    }
                    else{
                        $(".item").popover("destroy");
                        containerChk(id, layer, holder);
                        if(cookFlag){
                            cookCheck();
                        }
                        if(tradeFlag){
                            tradeCheck();
                        }
                        autosort(BAG_DATA);
                        return;
                    }
                }
                
                var sum = getSum(BAG_DATA);
                if(BAG_DATA[id] != undefined){
                    sum -= 1;
                }
                if(sum >= BAG_CAP){
                    $(".item").popover("destroy");
                    alert("背包已满，请先清理。");
                    return;
                }
                
                $(".item").popover("destroy");
                pickChk(id, layer, holder, $("#bag"), BAG_DATA);
                if(cookFlag){
                    cookCheck();
                }
                if(tradeFlag){
                    tradeCheck();
                }
                autosort(BAG_DATA);
            }
        }
    };

    //使用物品
    function useItem(item){
        //重新获取父容器
        var holder = getHolder(item.parentNode);
        var layer = $("#"+item.parentNode.id);
        DEATH_FOR = "<span class='badBuffName'>"+ITEM_DATA_SELF.name+"</span>";

        //物品生效
        if(ITEM_DATA_SELF.effect != undefined){
            for(var i in ITEM_DATA_SELF.effect){
                updateStatus(i, ITEM_DATA_SELF.effect[i]);
            }
        }
        //物品buff
        if(ITEM_DATA_SELF.buffUse != undefined){
            if(Math.random()*100 < ITEM_DATA_SELF.buffRate){
                getBuff(ITEM_DATA_SELF.buffUse);
            }
        }
        if(ITEM_DATA_SELF.clearBuffUse != undefined){
            for(var i in PLAYER_STATUS.buff){
                if(i.indexOf(ITEM_DATA_SELF.clearBuffUse) != -1){
                    removeBuff(i);
                }
            }
        }
        if(ITEM_DATA_SELF.useUpdate != undefined){
            eval(ITEM_DATA_SELF.useUpdate);
        }
        //减少数量
        if(ITEM_DATA_SELF.eternal == undefined){
            caculate(holder, id, -1);
        }
        updateItem(id, layer); 
        battleEquip();
    };

    //丢弃物品
    function removeItem(item){
        $(".item").popover("destroy");
        var holder = getHolder(item.parentNode);
        var amount = ITEM_DATA_SELF.durab!=undefined ? Math.ceil(holder[id]/ITEM_DATA_SELF.durab) : clone(holder[id]);
        if(confirm(ITEM_DATA_SELF.name+"("+amount+")"+" 丢弃后不可找回，确认丢弃吗？")){
            holder[id] = 0;
            var layer = $("#"+item.parentNode.id);
            updateItem(id, layer);
        }
    }

    //装备物品
    function equipItem(itemId, item){
        var itemType = ITEM_DATA[itemId].attack!=undefined?"weapon":ITEM_DATA[itemId].type;
        if(PLAYER_STATUS.equip[itemType] != ""){
            unloadItem(PLAYER_STATUS.equip[itemType], item);
        }
        PLAYER_STATUS.equip[itemType] = itemId;
        if(ITEM_DATA[itemId].attack != undefined){
            updateStatus("attack", ITEM_DATA[itemId].attack, true);
            if(ITEM_DATA[itemId].ammo!=undefined&&ITEM_DATA[itemId].ammo[0]==itemId){
                PLAYER_STATUS.equip.ammo = itemId;
            }
        }
        if($.inArray(ITEM_DATA[itemId].type, ["head", "body", "foot"]) != -1){
            if(ITEM_DATA[itemId].buffUse != undefined){
                getBuff(ITEM_DATA[itemId].buffUse);
            }
            if(itemId == "shoe_2"){
                MOVE_SPEED -= 0.15;
            }
        }
        if(ITEM_DATA[itemId].effect != undefined){
            for(var i in ITEM_DATA[itemId].effect){
                updateStatus(i, ITEM_DATA[itemId].effect[i], true);
            }
        }
        gameSet();
        autosort(BAG_DATA);
        battleEquip();
        updateItem(itemId, $("#bag"));
    }
    function unloadItem(itemId, item){
        var itemType = ITEM_DATA[itemId].attack!=undefined?"weapon":ITEM_DATA[itemId].type;
        PLAYER_STATUS.equip[itemType] = "";
        if(ITEM_DATA[itemId].attack != undefined){
            updateStatus("attack", -ITEM_DATA[itemId].attack, true);
            if(ITEM_DATA[itemId].ammo != undefined){
                for(var i in ITEM_DATA[itemId].ammo){
                    if(PLAYER_STATUS.equip.ammo == ITEM_DATA[itemId].ammo[i]){
                        unloadItem(PLAYER_STATUS.equip.ammo, null);
                    }
                }
            }
        }
        if($.inArray(ITEM_DATA[itemId].type, ["head", "body", "foot"]) != -1){
            if(ITEM_DATA[itemId].buffUse != undefined){
                removeBuff(ITEM_DATA[itemId].buffUse);
            }
            if(itemId == "shoe_2"){
                MOVE_SPEED += 0.15;
            }
        }
        if(ITEM_DATA[itemId].effect != undefined){
            for(var i in ITEM_DATA[itemId].effect){
                updateStatus(i, -ITEM_DATA[itemId].effect[i], true);
            }
        }
        gameSet();
        autosort(BAG_DATA);
        battleEquip();
        updateItem(itemId, $("#bag"));
    }

    //战斗中更换装备
    function battleEquip(){
        if($(".tab-pane.active").attr("id") != "battle"){
            return;
        }
        BATTLE_OBJ.resetPlayer();
        BATTLE_OBJ.setValue();
        if(!BATTLE_OBJ.getLoading()){
            BATTLE_OBJ.enemyResume();
        }
        BATTLE_OBJ.playerAp();
        $("#info").empty();
    }

    //修理物品
    function fixItem(item) {
        var desc = "修理["+ITEM_DATA_SELF.name+"]需要材料：";
        if(TOOL_DATA[id].tech!=undefined && PLAYER_STATUS.tech.value<TOOL_DATA[id].tech){
            desc = "该物品需求技术<span class='badBuffName'>"+TOOL_DATA[id].tech+"</span>，技术不足，无法修理。";
            $("#info").html(desc);
            return;
        }
        if(TOOL_DATA[id].level!=undefined && TOOL_LEVEL[TOOL_DATA[id].type[0]]<TOOL_DATA[id].level){
            desc = "该物品需求 "+WORK_TAB_NAME[TOOL_DATA[id].type[0]]+" 等级<span class='badBuffName'>"
                 + TOOL_DATA[id].level+"</span>， "+WORK_TAB_NAME[TOOL_DATA[id].type[0]]+" 等级不足，无法修理。";
            $("#info").html(desc);
            return;
        }

        var holder = getHolder(item.parentNode);
        var percent = 1.08 - holder[id]%ITEM_DATA_SELF.durab/ITEM_DATA_SELF.durab;
        var material = {};
        var flag = 1;
        for(var i in TOOL_DATA[id].require){
            if(ITEM_DATA[i].durab != undefined){
                continue;
            }
            var value = Math.ceil(TOOL_DATA[id].require[i]*percent);
            value = value>TOOL_DATA[id].require[i]?TOOL_DATA[id].require[i]:value;
            material[i] = value;
            var own = (BAG_DATA[i]==undefined ? 0 : BAG_DATA[i]) + (BOX_DATA[i]==undefined ? 0 : BOX_DATA[i]);
            var color = "goodBuffName";
            if(own < value){
                color = "badBuffName";
                flag = 0;
            }
            desc += "<span class='" + color + "'>" + ITEM_DATA[i].name + "</span>" + value;
        }
        $("#info").html(desc);
        var buttonGroup = newElement("div", "", "", "popoverButton", "");
        buttonGroup.appendChild(newElement("button", "fixBtn", "", "btn btn-default", "确认修理(F)"));
        $(".popover-title").empty();
        $(".popover-title").append(buttonGroup);
        if(flag){
            $("#fixBtn").click(function(){
                $(".item").popover("destroy");
                for(var i in material){
                    var need = clone(material[i]);
                    if(isNaN(need)){
                        return;
                    }
                    if(BAG_DATA[i] < need){
                        need -= BAG_DATA[i];
                        BAG_DATA[i] = 0;
                        updateItem(i, $("#bag"));
                        caculate(BOX_DATA, i, -need);
                        updateItem(i, $("#box"));
                    }
                    else if(BAG_DATA[i] == undefined){
                        caculate(BOX_DATA, i, -need);
                        updateItem(i, $("#box"));
                    }
                    else{
                        caculate(BAG_DATA, i, -need);
                        updateItem(i, $("#bag"));
                    }
                }
                caculate(BAG_DATA, id, ITEM_DATA_SELF.durab-BAG_DATA[id]%ITEM_DATA_SELF.durab);
                updateItem(id, $("#bag"));
                $("#info").empty();
            });
        }
        else{
            $("#fixBtn").attr("disabled", "disabled");
        }
    }

    //拆解物品
    function unpackItem(item) {
        var desc = "拆解["+ITEM_DATA_SELF.name+"]可获取：";
        if(TOOL_DATA[id].tech!=undefined && PLAYER_STATUS.tech.value<TOOL_DATA[id].tech){
            desc = "该物品需求技术<span class='badBuffName'>"+TOOL_DATA[id].tech+"</span>，技术不足，无法拆解。";
            $("#info").html(desc);
            return;
        }
        if(TOOL_DATA[id].level!=undefined && TOOL_LEVEL[TOOL_DATA[id].type[0]]<TOOL_DATA[id].level){
            desc = "该物品需求"+WORK_TAB_NAME[TOOL_DATA[id].type[0]]+"等级<span class='badBuffName'>"
                 + TOOL_DATA[id].level+"</span>，"
                 + WORK_TAB_NAME[TOOL_DATA[id].type[0]]+"等级不足，无法拆解。";
            $("#info").html(desc);
            return;
        }

        var holder = getHolder(item.parentNode);
        var percent = holder[id] % ITEM_DATA_SELF.durab;
        percent = percent==0 ? 0.88 : percent/ITEM_DATA_SELF.durab-0.12;
        percent = percent<=0 ? 0.01 : percent;
        percent = ITEM_DATA_SELF.durab==undefined?0.65:percent;
        var material = {};
        for(var i in TOOL_DATA[id].require){
            if(ITEM_DATA[i].durab != undefined){
                continue;
            }
            var value = Math.floor(TOOL_DATA[id].require[i]*percent);
            if(value > 0){
                material[i] = value;
                desc += "<span class='goodBuffName'>" + ITEM_DATA[i].name + "</span>" + value;
            }
        }
        $("#info").html(desc);
        var buttonGroup = newElement("div", "", "", "popoverButton", "");
        buttonGroup.appendChild(newElement("button", "unpackBtn", "", "btn btn-default", "确认拆解(C)"))
        if(getSum(material) > 0){
            $(".popover-title").empty();
            $(".popover-title").append(buttonGroup);
        }
        $("#unpackBtn").click(function(){
            $(".item").popover("destroy");
            var amount = ITEM_DATA_SELF.durab!=undefined ? BAG_DATA[id]%ITEM_DATA_SELF.durab : 1;
            amount = amount==0 ? clone(ITEM_DATA_SELF.durab) : amount;
            caculate(BAG_DATA, id, -amount);
            updateItem(id, $("#bag"));
            getItem(material);
            $("#info").empty();
        });
    }

    //信息显示
    function showinfo(){
        var holder = getHolder(this.parentNode);
        var desc = "[" + ITEM_DATA_SELF.name + "]" + (ITEM_DATA_SELF.desc!=undefined ? ITEM_DATA_SELF.desc: "");
        if(ITEM_DATA_SELF.require != undefined){
            desc += "装备需求：";
            for(var i in ITEM_DATA_SELF.require){
                var color = "goodBuffName";
                if(realVal(i) < ITEM_DATA_SELF.require[i]){
                    color = "badBuffName";
                }
                desc += "<span class='" + color + "'>" + PLAYER_STATUS[i].name + "</span>" + ITEM_DATA_SELF.require[i];
            }
        }
        desc += "<br>";
        
        //物品效果
        var effectGroup = newElement("div", "", "", "effectGroup", "");
        equipEffect(effectGroup, this);
        itemEffect(effectGroup);

        //视情况添加按钮
        var buttonGroup = newElement("div", "", "", "popoverButton", "");
        var item = this;
        if(ITEM_DATA_SELF.usable && holder!=TRADE_GET && holder!=TRADE_DATA && !(holder==TEMP_DATA && $(".tab-pane.active").attr("id")=="trade") && holder!=COOK_DATA){
            var newBtn = newElement("button", "", "", "btn btn-default", "使用(E)");
            newBtn.onclick = function(){useItem(item);};
            buttonGroup.appendChild(newBtn);
        }
        if(this.parentNode.id == "bag"){
            if($.inArray(ITEM_DATA_SELF.type, ["ammo", "head", "body", "foot"])!=-1 || ITEM_DATA_SELF.attack!=undefined){
                var flag = 1;
                for(var i in PLAYER_STATUS.equip){
                    if(PLAYER_STATUS.equip[i] == id){
                        var newBtn = newElement("button", "", "", "btn btn-default", "卸下(W)");
                        newBtn.onclick = function(){unloadItem(id, item);$(".item").popover("destroy");};
                        buttonGroup.appendChild(newBtn);
                        flag = 0;
                        break;
                    }
                }
                var requireFlag = 0;
                if(ITEM_DATA_SELF.require != undefined){
                    for(var i in ITEM_DATA_SELF.require){
                        if(realVal(i) < ITEM_DATA_SELF.require[i]){
                            requireFlag = 1;
                            break;
                        }
                    }
                }
                if(flag){
                    var newBtn = newElement("button", "", "", "btn btn-default", "装备(W)");
                    newBtn.onclick = function(){equipItem(id, item);$(".item").popover("destroy");};
                    if(requireFlag){
                        newBtn.setAttribute("disabled", "disabled");
                    }
                    buttonGroup.appendChild(newBtn);
                }
            }
            //种植
            if(ITEM_DATA_SELF.plant != undefined && $(".tab-pane.active").attr("id")=="map" && MAP_DATA[$("#map").attr("place")].resource!=undefined){
                var plantFlag = 0;
                for(var i in MAP_DATA[$("#map").attr("place")].resource){
                    if(i.indexOf("farmland") == 0){
                        plantFlag = 1;
                        break;
                    }
                }
                if(plantFlag){
                    var n = 1;
                    for(var i in ITEM_DATA_SELF.plant){
                        var name = CROP_DATA[ITEM_DATA_SELF.plant[i]].name;
                        var newBtn = newElement("button", ITEM_DATA_SELF.plant[i], "", "btn btn-default", "种" + name + "("+n+")");
                        plantInfo(newBtn, item);
                        newBtn.onmouseover = function(){
                            $("#info").html(this.getAttribute("plantInfo"));
                        };
                        taphold(newBtn, newBtn.onmouseover);
                        buttonGroup.appendChild(newBtn);
                        n += 1;
                    }
                }
            }
            if(ITEM_DATA_SELF.useIn && $(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")==ITEM_DATA_SELF.useIn){
                var newBtn = newElement("button", "", "", "btn btn-default", "使用(E)");
                newBtn.onclick = function(){useItem(item);};
                buttonGroup.appendChild(newBtn);
            }

            //组装
            if(ITEM_DATA_SELF.makeup != undefined){
                var newBtn = newElement("button", "", "", "btn btn-default", "组装");
                newBtn.onclick = function(){
                    $(".item").popover("destroy");
                    for(var i in TOOL_DATA[ITEM_DATA_SELF.makeup].require){
                        caculate(BAG_DATA, i, -TOOL_DATA[ITEM_DATA_SELF.makeup].require[i]);
                        updateItem(i, $("#bag"));
                    }
                    caculate(BAG_DATA, id, -1);
                    updateItem(id, $("#bag"));
                    var amount = ITEM_DATA[ITEM_DATA_SELF.makeup].durab!=undefined ? ITEM_DATA[ITEM_DATA_SELF.makeup].durab : 1;
                    var callback = function(){
                        eval("getItem({"+ITEM_DATA_SELF.makeup+":"+amount+"}, true);");
                    }
                    var cost = TOOL_DATA[ITEM_DATA_SELF.makeup].cost;
                    getNowTab();
                    costTimeFunc(cost, cost/120, "makeup", callback);
                }
                for(var i in TOOL_DATA[ITEM_DATA_SELF.makeup].require){
                    if(BAG_DATA[i]==undefined || BAG_DATA[i]<TOOL_DATA[ITEM_DATA_SELF.makeup].require[i]){
                        newBtn.setAttribute("disabled", "disabled");
                        break;
                    }
                }
                if(realVal("energy")<=0 || PLAYER_STATUS.buff.overwork!=undefined){
                    newBtn.setAttribute("disabled", "disabled");
                }
                buttonGroup.appendChild(newBtn);
            }

            var flag = 1;
            for(var i in PLAYER_STATUS.equip){
                if(PLAYER_STATUS.equip[i] == id){
                    flag = 0;
                    break;
                }
            }
            if(flag){
                if(ITEM_DATA_SELF.important == undefined){
                    var newBtn = newElement("button", "", "", "btn btn-default", "丢弃(D)");
                    newBtn.onclick = function(){removeItem(item);};
                    buttonGroup.appendChild(newBtn);
                }
                if($(".tab-pane.active").attr("id")=="workbench" && $("#workbench").attr("mode")=="work" && TOOL_DATA[id]!=undefined){
                    if(ITEM_DATA_SELF.durab!=undefined && holder[id]%ITEM_DATA_SELF.durab!=0){
                        var fixBtn = newElement("button", "", "", "btn btn-default", "修理(F)");
                        fixBtn.onclick = function(){fixItem(item);};
                        buttonGroup.appendChild(fixBtn);
                    }
                    if($.inArray(ITEM_DATA_SELF.type, ["weapon", "head", "body", "foot", "tool"]) != -1){
                        var unpackBtn = newElement("button", "", "", "btn btn-default", "拆解(C)");
                        unpackBtn.onclick = function(){unpackItem(item);};
                        buttonGroup.appendChild(unpackBtn);
                    }
                }
                //buff对应的特殊物品行为
                for(var i in PLAYER_STATUS.buff){
                    if(BUFF_DATA[i].operation != undefined){
                        var name = BUFF_DATA[i].operation;
                        var require = "";
                        var need = "";
                        var disabled = 0;
                        var n = 1;
                        if(BUFF_DATA[i].operationRequire!=undefined){
                            var keys = Object.keys(BUFF_DATA[i].operationRequire);
                            if(keys[0] == id){
                                if(BAG_DATA[id] < BUFF_DATA[i].operationRequire[id]){
                                    require = ITEM_DATA[keys[0]].name + "耐久" + BUFF_DATA[i].operationRequire[id];
                                    disabled = 1;
                                }
                                if(BUFF_DATA[i].operationNeed!=undefined){
                                    for(var j in BUFF_DATA[i].operationNeed){
                                        if(realVal(j) < BUFF_DATA[i].operationNeed[j]){
                                            need += PLAYER_STATUS[j].name + BUFF_DATA[i].operationNeed[j];
                                            disabled = 1;
                                        }
                                    }
                                }
                                name = require!=""||need!=""?name+"("+require+need+")":name;
                                var operationBtn = newElement("button", "buffid"+i, "", "btn btn-default", name + "("+n+")");
                                
                                if(disabled){
                                    operationBtn.setAttribute("disabled", "disabled");
                                }
                                else{
                                    operationBtn.onclick = function(){
                                        $(".item").popover("destroy");
                                        caculate(BAG_DATA, id, -BUFF_DATA[this.id.replace("buffid","")].operationRequire[id]);
                                        updateItem(id, $("#bag"));
                                        eval(BUFF_DATA[this.id.replace("buffid","")].operationUpdate);
                                    };
                                }
                                buttonGroup.appendChild(operationBtn);
                                n += 1;
                            }
                        }
                    }
                }
            }
        }
        
        $("#info").empty();
        $("#info").append(desc);
        $("#info").append(effectGroup);
        this.setAttribute("data-toggle", "popover");
        this.setAttribute("data-placement", "auto right");
        this.setAttribute("data-container", "body");
        if(buttonGroup.innerHTML.length != 0){
            $("#"+this.parentNode.id+" .item[id='"+this.id+"']").popover({html:true, trigger: "manual", title:buttonGroup});
            $("#"+this.parentNode.id+" .item[id='"+this.id+"']").popover("show");
        }
    }

    function equipEffect(effectGroup, item){
        var itemType = ITEM_DATA_SELF.attack!=undefined?"weapon":ITEM_DATA_SELF.type;
        switch(itemType){
            case "weapon":
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "武器"));
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "攻击+"+ITEM_DATA_SELF.attack));
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "射程"+ITEM_DATA_SELF.range));
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "速度"+ITEM_DATA_SELF.speed/10));
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "命中修正"+Math.floor(ITEM_DATA_SELF.hitrate*100)+"%"));
            if(ITEM_DATA_SELF.continuous){
                effectGroup.appendChild(newElement("span", "", "", "label label-default", "连射时间"+Math.floor(ITEM_DATA_SELF.contiTime/10)));
            }
            break;
            case "ammo":
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "弹药"));
            break;
            case "head": case "body": case "foot": 
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "装备"));
            switch(itemType){
                case "head":
                effectGroup.appendChild(newElement("span", "", "", "label label-default", "头部"));
                break;
                case "body":
                effectGroup.appendChild(newElement("span", "", "", "label label-default", "身体"));
                break;
                case "foot":
                effectGroup.appendChild(newElement("span", "", "", "label label-default", "脚部"));
                break;
            }
            break;
        }
        if(ITEM_DATA_SELF.durab != undefined){
            var holder = getHolder(item.parentNode);
            var durab = holder[id]%ITEM_DATA_SELF.durab;
            durab = durab==0?ITEM_DATA_SELF.durab:durab;
            effectGroup.appendChild(newElement("span", "", "", "label label-default", "耐久"+durab+"/"+ITEM_DATA_SELF.durab));
        }
    }

    function itemEffect(effectGroup){
        for(var i in ITEM_DATA_SELF.effect){
            var value;
            if(ITEM_DATA_SELF.effect[i].percent != undefined){
                value = Math.floor(ITEM_DATA_SELF.effect[i].percent*100);
            }
            else{
                value = ITEM_DATA_SELF.effect[i];
            }
            var effect = document.createElement("span");
            if(value != 0){
                if((value > 0 && i != "radiation") || (value < 0 && i == "radiation")){
                    effect.className = "label label-success" 
                    effect.innerHTML = PLAYER_STATUS[i].name + (i=="radiation"?"":"+") + value;
                }
                else{
                    effect.className = "label label-danger" 
                    effect.innerHTML = PLAYER_STATUS[i].name + (i=="radiation"?"+":"") + value;
                }
                if(PLAYER_STATUS[i].percent!=undefined || ITEM_DATA_SELF.effect[i].percent!=undefined){
                    effect.innerHTML += "%";
                }
                effectGroup.appendChild(effect);
            }
        }
        if(ITEM_DATA_SELF.attack!=undefined && ITEM_DATA_SELF.ammo!=undefined){
            var desc = "需求弹药：";
            for(var i in ITEM_DATA_SELF.ammo){
                if(i > 0){
                    desc += "/";
                }
                desc += ITEM_DATA[ITEM_DATA_SELF.ammo[i]].name;
            }
            effectGroup.appendChild(newElement("span", "", "", "label label-default", desc));
        }
        if(ITEM_DATA_SELF.buffUse!=undefined && BUFF_DATA[ITEM_DATA_SELF.buffUse].name!=undefined){
            var desc = BUFF_DATA[ITEM_DATA_SELF.buffUse].name;
            if(ITEM_DATA_SELF.buffRate != undefined){
                desc += ITEM_DATA_SELF.buffRate + "%";
            }
            effectGroup.appendChild(newElement("span", "", "", "label label-primary", desc));
        }
        if(ITEM_DATA_SELF.skillName != undefined){
            var desc = "[主动]" + ITEM_DATA_SELF.skillName;
            effectGroup.appendChild(newElement("span", "", "", "label label-warning", desc));
        }
    }
}

function coverChk(id, layer, holder){
    var list = ["tea", "hotWater", "cleanWater", "water", "dirtyWater", "urine"];
    
    function liquidMix(a, b, amount){
        if($.inArray(a, list) > $.inArray(b, list)){
            var pickAmount = clone(holder[b]);
            if(amount >= KETTLE_VOLUME){
                alert("水壶已满，无法拾取 "+ITEM_DATA[b].name+"。");
                return;
            }
            BAG_DATA[a] = amount + pickAmount;
            BAG_DATA[a] = BAG_DATA[a]>KETTLE_VOLUME ? KETTLE_VOLUME : clone(BAG_DATA[a]);
            updateItem(a, $("#bag"));
            caculate(holder, b, -(KETTLE_VOLUME-amount));
            updateItem(b, layer);
            
        }
        else if($.inArray(a, list) <= $.inArray(b, list)){
            var pickAmount = clone(holder[b]);
            if(amount >= KETTLE_VOLUME){
                alert("水壶已满，无法拾取 "+ITEM_DATA[b].name+"。");
                return;
            }
            if(BAG_DATA[a]/KETTLE_VOLUME > 1){
                caculate(BAG_DATA, a, -amount);
            }
            else{
                BAG_DATA[a] = 0;
            }
            updateItem(a, $("#bag"));
            BAG_DATA[b] = amount + pickAmount;
            BAG_DATA[b] = BAG_DATA[b]>KETTLE_VOLUME ? KETTLE_VOLUME : clone(BAG_DATA[b]);
            var newObj = new itemObj(b, $("#bag"));
            newObj.create();
            holder[b] = pickAmount - (KETTLE_VOLUME-amount);
            updateItem(b, layer);
        }
    }

    var liquidAmount = 0;
    var liquidKinds = 0;
    for(var i in BAG_DATA){
        if(ITEM_DATA[i].volume){
            liquidAmount += Math.floor(BAG_DATA[i]/KETTLE_VOLUME);
            liquidKinds += 1;
        }
    }
    var volume = KETTLE_VOLUME*KETTLE_AMOUNT;
    volume = liquidKinds>0 ? volume-KETTLE_VOLUME*(liquidKinds-1) : volume;
    if(liquidKinds>0 && (BAG_DATA[id]==undefined || (BAG_DATA[id]+holder[id])/KETTLE_VOLUME > KETTLE_AMOUNT-liquidKinds+1)){
        volume -= KETTLE_VOLUME;
    }
    //若该液体未装满，则锁定
    var bagItem;
    for(var i in BAG_DATA){
        if($.inArray(i, list)!=-1 && BAG_DATA[i]<volume){
            bagItem = i;
        }
    }
    if($.inArray(id, list) > $.inArray(bagItem, list)){
        bagItem = id;
    }
    if(BAG_DATA[id] == undefined){
        bagItem = undefined;
    }
    else if(BAG_DATA[id]!=undefined && BAG_DATA[id]<volume){
        bagItem = id;
    }

    //自动分装到相应类型的水壶中
    if(liquidAmount>=KETTLE_AMOUNT && bagItem==undefined){
        alert("水壶已满，无法拾取 "+ITEM_DATA[id].name+"。");
        return;
    }
    else if(liquidAmount<KETTLE_AMOUNT && (bagItem==id || bagItem==undefined)){
        var first = -1;
        for(var i in BAG_DATA){
            var pos = $.inArray(i, list);
            if(pos!=-1 && pos>first && BAG_DATA[i]>volume && bagItem!=id){
                first = pos;
            }
        }
        var last = 99;
        for(var i in BAG_DATA){
            var pos = $.inArray(i, list);
            var thisVolume = BAG_DATA[i]!=undefined ? volume+KETTLE_VOLUME : volume;
            if(pos!=-1 && pos<last && BAG_DATA[i]<thisVolume){
                last = pos;
            }
        }
        //壶中存在优先级更高的液体，且未装满
        if((last<$.inArray(id, list) && bagItem==id) || (first!=-1 && bagItem==undefined)){
            //壶中液体优先级更高
            volume += KETTLE_VOLUME;
            if(bagItem==undefined && $.inArray(id, list)<first){
                var amount = clone(holder[id]);
                var have = BAG_DATA[list[first]]==undefined ? 0 : clone(BAG_DATA[list[first]]);
                amount = amount>volume-have?volume-have:amount;
                if(amount == 0){
                    var lastAmount = BAG_DATA[list[last]] % KETTLE_VOLUME;
                    liquidMix(list[last], id, lastAmount);
                    return;
                }
                else{
                    //同时存在高优先级和低优先级，用现有液体覆盖低优先级
                    if(BAG_DATA[list[last]] != undefined){
                        var lastAmount = BAG_DATA[list[last]] % KETTLE_VOLUME;
                        liquidMix(list[last], id, lastAmount);
                        return;
                    }
                    caculate(BAG_DATA, list[first], amount);
                    updateItem(list[first], $("#bag"));
                    caculate(holder, id, -amount);
                    updateItem(id, layer);
                    return;
                }
            }
            //壶中未装满的液体优先级低，高优先级物品可继续盛装
            else{
                if($.inArray(id, list)>=first && BAG_DATA[id]==undefined){
                    var amount = BAG_DATA[list[first]] % KETTLE_VOLUME;
                    liquidMix(list[first], id, amount);
                    return;
                }
                first = -1;
                if(BAG_DATA[id] >= volume){
                    caculate(BAG_DATA, id, BAG_DATA[list[last]]);
                    updateItem(id, $("#bag"));
                    BAG_DATA[list[last]] = 0;
                    updateItem(list[last], $("#bag"));
                    volume += KETTLE_VOLUME;
                }
            }
        }

        //若有空间则将水壶分开再装入新液体，触发混合
        if(first != -1){
            var amount = BAG_DATA[list[first]] % KETTLE_VOLUME;
            liquidMix(list[first], id, amount);
            return;  
        }
        //否则装入同一水壶
        else{
            if(volume==0 && BAG_DATA[id]!=undefined){
                volume += KETTLE_VOLUME;
            }
            var amount = clone(holder[id]);
            var have = BAG_DATA[id]==undefined ? 0 : clone(BAG_DATA[id]);
            amount = amount>volume-have ? volume-have : amount;
            caculate(holder, id, -amount);
            updateItem(id, layer);
            pickChk(id, layer, holder, $("#bag"), BAG_DATA, amount);
            return;
        }
    }
    //相应类型已满则装入其他水壶，触发混合
    liquidMix(bagItem, id, clone(BAG_DATA[bagItem]));
}

function containerChk(id, layer, holder){
    var amount = ITEM_DATA[id].containerCost!=undefined ? Math.ceil(holder[id]/ITEM_DATA[id].containerCost) : clone(holder[id]);
    amount = amount>BAG_DATA[ITEM_DATA[id].container] ? clone(BAG_DATA[ITEM_DATA[id].container]) : amount;
    var pickAmount = ITEM_DATA[id].containerCost!=undefined ? amount*ITEM_DATA[id].containerCost : amount;
    pickAmount = pickAmount>holder[id] ? clone(holder[id]) : pickAmount;
    caculate(holder, id, -pickAmount);
    updateItem(id, layer);
    caculate(BAG_DATA, ITEM_DATA[id].container, -amount);
    updateItem(ITEM_DATA[id].container, $("#bag"));
    pickChk(id, layer, holder, $("#bag"), BAG_DATA, pickAmount);
}

function pickChk(id, layer, holder, toLayer, toHolder, amount){
    //不存在相同物品则转移
    var maxFlag = 0;
    if(toHolder[id] == undefined){
        if(holder[id] > MAX_AMOUNT){
            maxFlag = 1;
            if(ITEM_DATA[id].durab != undefined){
                caculate(holder, id, -(amount!=null ? amount : MAX_AMOUNT*ITEM_DATA[id].durab));
            }
            else{
                caculate(holder, id, -(amount!=null ? amount : MAX_AMOUNT));
            }
            updateItem(id, layer);
            toHolder[id] = amount!=null ? amount : MAX_AMOUNT;
            var newObj = new itemObj(id, toLayer);
            newObj.create();
            updateItem(id, toLayer);
        }
        else{
            toHolder[id] = amount!=null ? amount : clone(holder[id]);
            var newObj = new itemObj(id, toLayer);
            newObj.create();
            updateItem(id, toLayer);
        }
        
        //获取buff
        if(ITEM_DATA[id].buffPick!=undefined && toHolder==BAG_DATA){
            getBuff(ITEM_DATA[id].buffPick);
        }
    }
    //存在相同物品则叠加
    else{
        var have = clone(toHolder[id]);
        have = ITEM_DATA[id].durab!=undefined?Math.ceil(have/ITEM_DATA[id].durab):have;
        var take = clone(holder[id]);
        take = ITEM_DATA[id].durab!=undefined?Math.ceil(take/ITEM_DATA[id].durab):take;
        if(have+take > MAX_AMOUNT){
            maxFlag = 1;
            if(ITEM_DATA[id].durab != undefined){
                var overAmount = have*ITEM_DATA[id].durab;
                caculate(holder, id, -(amount!=null ? amount : MAX_AMOUNT-overAmount));
                caculate(toHolder, id, amount!=null ? amount : MAX_AMOUNT-overAmount);
            }
            else{
                caculate(holder, id, -(amount!=null ? amount : MAX_AMOUNT-have));
                caculate(toHolder, id, amount!=null ? amount : MAX_AMOUNT-have);
            }
            updateItem(id, layer);
            updateItem(id, toLayer);
        }
        else{
            caculate(toHolder, id, amount!=null ? amount : clone(holder[id]));
            updateItem(id, toLayer);
        }
    }
    if(amount==null && !maxFlag){
        holder[id] = 0;
        updateItem(id, layer);
    }
}

function getItem(items, show, output){
    if(LOAD_FLAG){
        return;
    }

    for(var id in items){
        TEMP_DATA[id] = TEMP_DATA[id]==undefined ? clone(items[id]) : TEMP_DATA[id]+items[id];
    }
    
    if(show){
        if(output){
            toLoading(0.5, "output");
        }
        else{
            toLoading(0.5, "pickUp");
        }
    }
    else{
        for(var id in items){
            if($("#temp .item[id='"+id+"']").attr("id") == undefined){
                var newObj = new itemObj(id, $("#temp"));
                newObj.create();
                if(output){
                    newObj.deleteItemData("container");
                }
            }
            if(getSum(BAG_DATA)<BAG_CAP || BAG_DATA[id]!=undefined){
                $("#temp .item[id='"+id+"']").trigger("selfClick");
            }
        }
        if(getSum(TEMP_DATA) > 0){
            if(output){
                toLoading(0.5, "output");
            }
            else{
                toLoading(0.5, "pickUp");
            }
        }
    }
}
//================================================================================================

//====工作台对象====
function workbenchObj(mode){
    var showType = [];
    //创建制作项列表
    this.create = function(){
        var self = this;
        $("#workbench").attr("mode", mode);
        $("#workbench").empty();
        if(mode == "cook"){
            getBackBtn($("#workbench"));
            $("#workbench").append(newElement("button", "cookBegin", "", "btn btn-default", "制作"));
            $("#workbench").append(newElement("div", "stuff", "stuff", "", ""));
            $("#workbench").append("<br>");
            $("#workbench").append(newElement("div", "cookResult", "cookResult", "", ""));
            $("#workbench").append("<br>");
            $("#workbench").append(newElement("div", "diet", "", "", ""));
            var amount = "<input type='text' id='workAmount'><input type='range' id='workSlider' style='margin-bottom:10px;' value=1><br>用时：<span id='workTime'></span>";
            $("#workbench").append(newElement("div", "cookAmount", "", "", amount));
            $("#cookAmount").bind("slider", function(){createSlider($("#cookAmount").attr("cook"));});
            $("#cookAmount").hide();
            $("#cookBegin").bind("begin", function(){makeItem($("#cookAmount").attr("cook"));});
            $("#cookBegin").click(function(){$("#cookBegin").trigger("begin");});
            $("#cookBegin").attr("disabled", "disabled");
            if(getSum(COOK_DATA) > 0){
                for(var i in COOK_DATA){
                    var newObj = new itemObj(i, $("#stuff"));
                    newObj.create();
                }
            }
            if(getSum(COOK_RESULT) > 0){
                for(var i in COOK_RESULT){
                    var newObj = new itemObj(i, $("#cookResult"));
                    newObj.create();
                }
            }
            cookCheck();
            return;
        }

        //创建表格
        var divTb = newElement("div", "", "", "divTb", "");
        var tb = newElement("table", "workbenchTb", "", "table table-hover infoTb", "");

        var tbTitle;
        switch(mode){
            case "work":case "handwork": case "lab": case "forge":case "filter":
            tbTitle = "物品";
            break;
            case "tech": tbTitle = "科技";break;
            case "bed": tbTitle = "动作";break;
            case "train": tbTitle = "项目";break;
        }

        var thead = newElement("thead", "", "", "", "<tr><th>" + tbTitle + "</th><th>材料</th><th>信息</th></tr>");
        tb.appendChild(thead);
        var tbody = document.createElement("tbody");
        for(var i in TOOL_DATA){
            var modeFlag = 0;
            for(var j in TOOL_DATA[i].type){
                if(TOOL_DATA[i].type[j] == mode){
                    if(showType.length > 0){
                        //显示类型检查
                        var typeFlag = TOOL_DATA[i].only==undefined && $.inArray((TOOL_DATA[i].turn!=undefined?ITEM_DATA[TOOL_DATA[i].turn].type:ITEM_DATA[i].type), showType)==-1
                        if(showType[0]!="only" && (TOOL_DATA[i].only!=undefined || typeFlag)){
                            break;
                        }
                        else if(showType[0]=="only" && TOOL_DATA[i].only==undefined){
                            break;
                        }
                    }
                    modeFlag = 1;
                    break;
                }
            }
            //个别升级项极值检测
            if(TOOL_DATA[i].max!=undefined && eval(TOOL_DATA[i].maxAttr + ">=" + TOOL_DATA[i].max)){
                continue;
            }

            if(modeFlag && TOOL_DATA[i].show && TOOL_LEVEL[mode]>=(TOOL_DATA[i].level==undefined?0:TOOL_DATA[i].level)){
                var tr = document.createElement("tr");
                tr.id = i;
                //点击选定待制作物品
                tr.onclick = function(){clickEvent.call(this);};
                tr.innerHTML = "";
                tr.innerHTML += "<td>" + TOOL_DATA[i].name + (TOOL_DATA[i].newflag?"<span class='goodBuffName'>new</span>":"") + "</td>";
                tr.innerHTML += "<td>" + getRequire(i) + "</td>";
                var desc = TOOL_DATA[i].desc;
                if($.inArray(i, ["train_endurance", "train_perception", "train_agility"]) != -1){
                    var special = i.replace("train_", "");
                    if(PLAYER_STATUS[special].value >= 10){
                        desc = "已达到训练上限，无法继续通过训练提升。";
                    }
                    desc += "当前进度" + (PLAYER_STATUS[special].progerss / nextProgress(special) * 100).toFixed(1) + "%";
                }
                if(ITEM_DATA[i]!=undefined && ITEM_DATA[i].require!=undefined){
                    desc += "装备需求：";
                    for(var j in ITEM_DATA[i].require){
                        var color = "badBuffName";
                        if(realVal(j) >= ITEM_DATA[i].require[j]){
                            color = "goodBuffName";
                        }
                        desc += "<span class='" + color + "'>" + PLAYER_STATUS[j].name + "</span>" + ITEM_DATA[i].require[j];
                    }
                }
                tr.innerHTML += "<td>" + desc + "</td>";
                tbody.appendChild(tr);
            }
        }
        tb.appendChild(tbody);
        divTb.appendChild(tb);

        getBackBtn($("#workbench"));
        if(mode == "work"){
            $("#workbench").append("<br>");
            $("#workbench").append(newElement("button", "showall", "", "btn btn-default showItem", "全部"));
            $("#workbench").append(newElement("button", "showonly", "", "btn btn-default showItem", "升级"));
            $("#workbench").append(newElement("button", "showweapon", "", "btn btn-default showItem", "武器"));
            $("#workbench").append(newElement("button", "showequip", "", "btn btn-default showItem", "装备"));
            $("#workbench").append(newElement("button", "showtool", "", "btn btn-default showItem", "工具"));
            $("#workbench .showItem").click(function(){
                switch($(this).attr("id").replace("show","")){
                    case "all":showType = [];break;
                    case "only":showType = ["only"];break;
                    case "weapon":showType = ["weapon", "ammo"];break;
                    case "equip":showType = ["head", "body", "foot"];break;
                    case "tool":showType = ["tool", "material"];break;
                }
                self.create();
            });
        }
        $("#workbench").append(divTb);
    }

    //点击激活执行框
    function clickEvent(){
        $("#info").empty();

        var i = this.id;
        if(TOOL_DATA[i].newflag){
            delete TOOL_DATA[i].newflag;
        }
        var tb = newElement("table", "workbenchMenu", "", "table table-hover infoTb", "");

        var thead;
        switch(mode){
            case "work": case "handwork": case "lab": case "forge":case "filter":
            thead = newElement("thead", "", "", "", "<tr><th>物品</th><th>数量</th><th>消耗</th><th>用时</th></tr>");
            break;
            case "tech": 
            thead = newElement("thead", "", "", "", "<tr><th>科技</th><th>消耗</th><th>用时</th></tr>");
            break;
            case "bed": 
            thead = newElement("thead", "", "", "", "<tr><th>升级</th><th>消耗</th><th>效果</th></tr>");
            break;
        }
        if($.inArray(i, ["sleep", "research_1", "research_2", "train_endurance", "train_perception", "train_agility"]) != -1){
            thead = newElement("thead", "", "", "", "<tr><th>动作</th><th>用时</th><th>效果</th></tr>");
        }
        tb.appendChild(thead);

        var tbody = document.createElement("tbody");
        var tr = document.createElement("tr");
        tr.innerHTML = "<td>" + TOOL_DATA[i].name + (TOOL_DATA[i].amount!=undefined?"*"+TOOL_DATA[i].amount:"") + "</td>";
        switch(mode){
            case "work": case "handwork": case "lab": case "forge":case "filter":
            tr.innerHTML += "<td><input type='text' id='workAmount' for='workSlider'/>"
            + "<input type='range' id='workSlider' value=1></td>"
            + "<td id='workCost'>" + getRequire(i, 1) + "</td>"
            + "<td><span id='workTime'></span></td>";
            break;
            case "tech":
            tr.innerHTML += "<td id='workCost'>" + getRequire(i, 1) + "</td>"
            +"<td><span id='workTime'></span></td>";
            break;
            case "bed":
            tr.innerHTML += "<td id='workCost'>" + getRequire(i, 1) + "</td>"
            +"<td><span id='workTime'></span></td>";
            break;
        }
        if($.inArray(i, ["sleep", "research_1", "research_2", "train_endurance", "train_perception", "train_agility"]) != -1){
            tr.innerHTML = "<td>" + TOOL_DATA[i].name + (TOOL_DATA[i].amount!=undefined?"*"+TOOL_DATA[i].amount:"") + "</td>"
            + "<td><input type='text' id='workAmount' for='workSlider'/>"
            + "<input type='range' id='workSlider' value=1></td>"
            + "<td id='workCost'>" + getRecover(i, 1) + "</td>";
        }
        tbody.appendChild(tr);
        tb.appendChild(tbody);

        var btn = newElement("button", "workBegin", "", "btn btn-default", "");
        switch(mode){
            case "work": case "handwork": case "lab": case "forge":case "filter":
            btn.innerHTML = "制造";        
            break;
            case "tech":
            btn.innerHTML = "研究";
            break;
            case "bed": case "train":
            btn.innerHTML = "执行";
            break;
        }
        if($.inArray(i, ["research_1", "research_2"]) != -1){
            btn.innerHTML = "执行";
        }
        btn.onclick = function(){makeItem(i);};
        btn.setAttribute("disabled", "disabled");
        
        $("#info").append(tb);
        $("#info").append(btn);

        createSlider(i);
    };

    function createSlider(i){
        var maxMake = getMaxMake(i);
        if(maxMake>0 && realVal("energy")>0 && PLAYER_STATUS.buff.overwork==undefined || i=="sleep"){
            $("#workBegin").removeAttr("disabled");
        }
        //滑块设置
        if($.inArray(mode, ["work", "handwork", "lab", "cook", "forge", "filter", "train"])!=-1 || $.inArray(i, ["sleep", "research_1", "research_2"]) != -1){
            $("#workSlider").attr("min", 1);
            $("#workSlider").attr("max", maxMake<=0 ? 1 : maxMake);
            $("#workAmount").val(1);
            $("#workSlider").on("input", function(){
                $("#workAmount").val(this.value);
                if($.inArray(i, ["sleep", "research_1", "research_2", "train_endurance", "train_perception", "train_agility"]) != -1){
                    $("#workCost").html(getRecover(i, this.value));
                }
                else{
                    $("#workTime").html(getCost(i, this.value));
                    $("#workCost").html(getRequire(i, this.value));
                }
            });
            $("#workAmount").change(function(){
                if(this.value <= parseInt($("#workSlider").attr("max"))){
                    $("#workSlider").val(this.value);
                    if($.inArray(i, ["sleep", "research_1", "research_2", "train_endurance", "train_perception", "train_agility"]) != -1){
                        $("#workCost").html(getRecover(i, this.value));
                    }
                    else{
                        $("#workTime").html(getCost(i, this.value));
                        $("#workCost").html(getRequire(i, this.value));
                    }
                }
                else{
                    this.value = maxMake;
                    $("#workSlider").attr("value", maxMake);
                }
            });
            $("#workAmount").val($("#workSlider").attr("value"));
            $("#workTime").html(getCost(i, $("#workAmount").val()));
        }
        else{
            $("#workTime").html(getCost(i, 1));
        }
    }

    //制作物品
    function makeItem(item){
        //检查背包
        var bagAmount = getSum(BAG_DATA);
        var amount = parseInt($("#workAmount").val()>1?$("#workAmount").val():1);
        var cost = amount * TOOL_DATA[item].cost;
        
        if(mode == "cook"){
            cost *= COOK_SPEED;
        }
        else if($.inArray(mode, ["work", "handwork", "lab", "forge", "filter"]) != -1){
            cost *= WORK_SPEED;
        }
        if($.inArray(item, ["train_endurance", "train_perception", "train_agility"]) != -1){
            for(var i in TOOL_DATA[item].recover){
                updateProgress(i, TOOL_DATA[item].recover[i] * amount);
            }
        }

        var callback = function(){costMaterialFunc(cost, item, amount);};
        if(mode=="bed" && item!="sleep"){
            costTimeFunc(cost, cost/120, "bedUpgrade", callback);
        }
        else{
            costTimeFunc(cost, cost/120, mode, callback);
        }
        
    };

    //减少材料数量
    function costMaterialFunc(cost, item, amount){
        $("#info").empty();
        if($.inArray(item, ["sleep", "research_1", "research_2"]) != -1){
            for(var i in TOOL_DATA[item].recover){
                updateStatus(i, TOOL_DATA[item].recover[i] * amount);
            }
        }
        else if(mode == "cook"){
            for(var i in TOOL_DATA[item].require){
                caculate(COOK_DATA, i, -TOOL_DATA[item].require[i] * amount);
                updateItem(i, $("#stuff"));
                
            }
            cookCheck();
        }
        else{
            for(var i in TOOL_DATA[item].require){
                var need = TOOL_DATA[item].require[i] * amount;
                if(isNaN(need)){
                    return;
                }
                if(BAG_DATA[i] < need){
                    need -= BAG_DATA[i];
                    BAG_DATA[i] = 0;
                    updateItem(i, $("#bag"));
                    caculate(BOX_DATA, i, -need);
                    updateItem(i, $("#box"));
                }
                else if(BAG_DATA[i] == undefined){
                    caculate(BOX_DATA, i, -need);
                    updateItem(i, $("#box"));
                }
                else{
                    caculate(BAG_DATA, i, -need);
                    updateItem(i, $("#bag"));
                }
            }
        }

        if(TOOL_DATA[item].only){
            if(TOOL_DATA[item].upgrade != undefined){
                eval(TOOL_DATA[item].upgrade);
            }
            if(TOOL_DATA[item].eternal == undefined){
                delete TOOL_DATA[item].show;
                TOOL_FINISHED.push(item);
            }
            var newObj = new workbenchObj(mode);
            newObj.create();
        }
        else if($.inArray(item, ["sleep", "train_endurance", "train_perception", "train_agility"]) != -1){

        }
        else if($.inArray(item, ["research_1", "research_2"]) != -1){
            var timeSpan = (sysTime - RESEARCH_TIME)/1000/60;
            if(timeSpan <= 600){
                RESEARCH_LIMIT += cost;
            }
            else{
                RESEARCH_LIMIT = 0;
            }
            if(RESEARCH_LIMIT > 600){
                if(PLAYER_STATUS.buff.overResearch != undefined){
                    removeBuff("overResearch");
                }
                getBuff("overResearch");
            }
            RESEARCH_TIME = clone(sysTime);
        }
        else if(mode == "cook"){
            var itemName = item;
            if(TOOL_DATA[item].turn != undefined){
                itemName = TOOL_DATA[item].turn;
            }
            if(COOK_RESULT[itemName] == undefined){
                COOK_RESULT[itemName] = amount;
                var newItem = new itemObj(itemName, $("#cookResult"));
                newItem.create();
            }
            else{
                caculate(COOK_RESULT, itemName, amount);
                updateItem(itemName, $("#cookResult"));
            }
            cookCheck();
        }
        else{
            var itemName = item;
            if(TOOL_DATA[item].turn != undefined){
                itemName = TOOL_DATA[item].turn;
            }
            if(ITEM_DATA[itemName].durab != undefined){
                amount *= ITEM_DATA[itemName].durab;
            }
            if(TOOL_DATA[item].amount != undefined){
                amount *= TOOL_DATA[item].amount;
            }
            if(ITEM_DATA[itemName].volume || ITEM_DATA[itemName].container!=undefined || ITEM_DATA[itemName].interval!=undefined){
                eval("getItem({"+itemName+":"+amount+"}, true, true);");
            }
            else{
                eval("getItem({"+itemName+":"+amount+"}, null, true);");
            }
            var progress = ITEM_DATA[itemName].price==undefined ? 1 : clone(ITEM_DATA[itemName].price);
            progress = progress/100 * amount;
            progress = ITEM_DATA[itemName].durab==undefined ? progress : progress/ITEM_DATA[itemName].durab;
            updateProgress("agility", progress);
            var newObj = new workbenchObj(mode);
            newObj.create();
        }
    }

    function getCost(i, cost){
        var result = cost * TOOL_DATA[i].cost;
        if(mode == "cook"){
            result *= COOK_SPEED;
        }
        else if($.inArray(mode, ["work", "handwork", "lab", "forge", "filter"]) != -1){
            result *= WORK_SPEED;
        }
        result = result>=60?(Math.floor(result/60)+"小时"+Math.floor(result%60)+"分钟"):(Math.floor(result)+"分钟");
        return result;
    }

    function getMaxMake(i){
        if($.inArray(i, ["sleep", "research_1", "research_2"]) != -1){
            return 16;
        }
        else if($.inArray(i, ["train_endurance", "train_perception", "train_agility"]) != -1){
            if(PLAYER_STATUS[i.replace("train_","")].value >= 10){
                return 0;
            }
            else{
                return 16;
            }
        }
        var a = min(TOOL_DATA[i].require, mode);
        var b = (BAG_DATA[a[1]]==undefined ? 0 : BAG_DATA[a[1]]) + (BOX_DATA[a[1]]==undefined ? 0 : BOX_DATA[a[1]]);
        if(mode == "cook"){
            b = clone(COOK_DATA[a[1]]);
        }
        var maxMake = Math.floor(b/TOOL_DATA[i].require[a[1]]);
        if(maxMake > 0 && ($.inArray(mode, ["work", "handwork", "lab", "cook", "forge", "filter"]) == -1 || TOOL_DATA[i].only)){
            maxMake = 1;
        }
        return maxMake;
    }

    function getRequire(i, amount){
        var require = "";
        if(TOOL_DATA[i].require == undefined){
            return require;
        }
        for(var j in TOOL_DATA[i].require){
            var sum = TOOL_DATA[i].require[j];
            sum = sum * (amount==null?1:amount);
            var own = (BAG_DATA[j]==undefined ? 0 : BAG_DATA[j]) + (BOX_DATA[j]==undefined ? 0 : BOX_DATA[j]);
            var color = "badBuffName";
            if(own >= sum){
                color = "goodBuffName";
            }
            if(ITEM_DATA[j].durab!=undefined){
                sum = sum/ITEM_DATA[j].durab;
                own = own/ITEM_DATA[j].durab;
            }
            var name = "<span class='" + color + "'>" + ITEM_DATA[j].name + "</span>" + sum;
            if(amount != null){
                name += "/" + own + "<br>";
            }
            require += name;
        }
        return require;
    }
    function getRecover(i, amount){
        var recover = "";
        if(TOOL_DATA[i].recover == undefined){
            return recover;
        }
        for(var j in TOOL_DATA[i].recover){
            var sum = (TOOL_DATA[i].recover[j] * (amount==null?1:amount)).toFixed(1);
            var name = PLAYER_STATUS[j].name;
            if($.inArray(i, ["train_endurance", "train_perception", "train_agility"]) != -1){
                name += "训练进度";
                sum = ((parseFloat(sum)+PLAYER_STATUS[j].progerss) / nextProgress(j) * 100).toFixed(1) + "%";
            }
            var desc = "<span class='goodBuffName'>" + name + "</span>" + sum;
            recover += desc;
        }
        return recover;
    }
}
//================================================================================================

//====战斗模块====
function battleObj(){
    var dis = 5;
    var log = "";
    var pause = 0;
    var enemyName = "roach_1";
    var enemyIn = "";
    var callback = null;

    this.setEnemy = function(i){
        enemyName = i;
    }
    this.setEnemyIn = function(i){
        enemyIn = i;
    }
    this.setCallback = function(i){
        callback = i;
    }
    
    //玩家变量
    var weapon = "fist";
    var player = {};
    var playerLoading = 0;
    

    //敌人变量
    var enemy = {};
    var enemyLoading = 1;

    //绘制界面
    this.create = function(){
        $("#battle").empty();
        var self = this;
        //玩家状态
        var outterDiv = newElement("div", "battlePlayer", "", "battleStatus", "");
        var newDiv = newElement("div", "", "", "battleTitle", "");
        outterDiv.appendChild(newDiv);
        newDiv = newElement("div", "hpPlayer", "", "hpDiv", "<div class='loadingBar'></div>");
        outterDiv.appendChild(newDiv);
        outterDiv.appendChild(document.createElement("span"));
        newDiv = newElement("div", "apPlayer", "", "apDiv", "<div class='loadingBar'></div>");
        outterDiv.appendChild(newDiv);
        $("#battle").append(outterDiv);

        //敌人状态
        outterDiv = newElement("div", "battleEnemy", "", "battleStatus", "");
        newDiv = newElement("div", "", "", "battleTitle", "");
        outterDiv.appendChild(newDiv);
        newDiv = newElement("div", "hpEnemy", "", "hpDiv", "<div class='loadingBar'></div>");
        outterDiv.appendChild(newDiv);
        outterDiv.appendChild(document.createElement("span"));
        newDiv = newElement("div", "apEnemy", "", "apDiv", "<div class='loadingBar'></div>");
        outterDiv.appendChild(newDiv);
        $("#battle").append(outterDiv);

        //武器信息
        $("#battle").append(newElement("div", "", "", "battleDis", ""));
        $("#battle").append(newElement("div", "", "", "battleInfo", ""));
        $("#battle").append(newElement("div", "", "", "battleWeapon", ""));
        $("#battle").append(newElement("div", "", "", "battleOptions", ""));
        $("#battle").append(newElement("div", "", "", "battleSkills", ""));
        var tb = newElement("table", "", "", "table infoTb", "");
        var thead = newElement("thead", "", "", "", "<tr><th>武器</th><th>攻击力</th><th>射程</th><th>命中</th><th>消耗</th></tr>");
        tb.appendChild(thead);
        var tbody = newElement("tbody", "", "", "", "<tr><td></td><td></td><td></td><td></td><td></td>");
        tb.appendChild(tbody);
        $("#battle div[class='battleWeapon']").append(tb);
        $("#battle div[class='battleWeapon']").hide();

        //基本操作
        $("#battle div[class='battleOptions']").append(newElement("button", "escape", "", "btn btn-default", "逃跑"));
        $("#battle div[class='battleOptions']").append(newElement("button", "defence", "", "btn btn-default", "防御(D)"));
        $("#battle div[class='battleOptions']").append(newElement("button", "attack", "", "btn btn-default", "进攻(A)"));
        $("#battle div[class='battleOptions']").append(newElement("button", "forward", "", "btn btn-default", "前进(W)"));
        $("#battle div[class='battleOptions']").append(newElement("button", "backward", "", "btn btn-default", "后退(S)"));
        $("#escape").click(function(){
            exitBattle.call(self);
        });
        $("#defence").click(function(){
            defence.call(self);
        });
        $("#defence").bind("nextTurn", function(){nextTurn.call(self);});
        $("#attack").click(function(){
            attack.call(self);
        });
        $("#forward").click(function(){
            aStep.call(self, -player.step);
        });
        $("#backward").click(function(){
            aStep.call(self, player.step);
        });

        $("#battle div[class='battleOptions'] button").each(function(){
            $(this).attr("disabled", "disabled");
        });
    }

    this.play = function(){
        log = "";
        dis = disCheck();
        this.resetPlayer();
        this.resetEnemy();
        //界面赋值
        $("#hpPlayer div").width(realVal("life")/PLAYER_STATUS.life.max * 100 + "%");
        $("#battlePlayer span").html(Math.ceil(realVal("life")) + "/" + Math.ceil(PLAYER_STATUS.life.max));  
        $("#battlePlayer div[class='battleTitle']").html(player.name);
        $("#hpEnemy div").width(enemy.life/CREEP_DATA[enemyName].life * 100 + "%");
        $("#battleEnemy span").html(Math.ceil(enemy.life) + "/" + Math.ceil(CREEP_DATA[enemyName].life));
        $("#battleEnemy div[class='battleTitle']").html(enemy.name);
        appendLog(player.name + " 遇到了 " + enemy.name);
        this.setValue();
        
        //进入战斗循环
        pauseGame();
        BATTLE_FLAG = true;
        playerLoading = 0;
        $("#apPlayer div").css({width: "100%"});
        playerMove();
        enemyLoading = 1;
        //enemyAp();
    }

    this.setValue = function(){
        var weaponInfo = "<label class='noneBuffName'"
        + " onmouseover='$(\"#info\").html($(\"#battle div[class=\\\"battleWeapon\\\"]\").html());'"
        + " ontouchstart='$(\"#info\").html($(\"#battle div[class=\\\"battleWeapon\\\"]\").html());'>"
        + ITEM_DATA[player.weapon].name + "</label>";
        $("#battle div[class='battleDis']").html("距离:<span id='dis'>" + dis + "</span>&nbsp;&nbsp;武器:");
        $("#battle div[class='battleDis']").append(weaponInfo);
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(0)").html(ITEM_DATA[player.weapon].name);
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(1)").html(player.attack);
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(2)").html(player.range);
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(3)").html(hitRateChk() + "%");
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(4)").html(ITEM_DATA[player.weapon].cost);
    }
    this.resetPlayer = function(){
        weapon = PLAYER_STATUS.equip.weapon==""?"fist":PLAYER_STATUS.equip.weapon;
        player = {
            name: "你",
            weapon: weapon,
            speed: clone(ITEM_DATA[weapon].speed),
            attack: realVal("attack"),
            defence: realVal("defence"),
            range: clone(ITEM_DATA[weapon].range),
            cri: realVal("critical"),
            criTimes: realVal("critimes"),
            dodge: realVal("dodge"),
            hitrate: realVal("hitrate"),
            escape: realVal("escape"),
            cost: clone(ITEM_DATA[weapon].cost),
            step: 1
        };
        if(PLAYER_STATUS.buff.longleg != undefined){
            player.step += 1;
        }
        if(PLAYER_STATUS.equip.foot == "shoe_3"){
            player.step += 1;
        }
        if(PLAYER_STATUS.buff.slow_1 != undefined){
            player.speed = Math.floor(player.speed * 1.5);
        }
        
        extraSkill.call(this, true);
    }
    this.resetEnemy = function(){
        enemy = {
            name: clone(CREEP_DATA[enemyName].name.replace("<br>","")),
            life: clone(CREEP_DATA[enemyName].life),
            speed: clone(CREEP_DATA[enemyName].speed),
            attack: clone(CREEP_DATA[enemyName].attack),
            defence: clone(CREEP_DATA[enemyName].defence),
            range: clone(CREEP_DATA[enemyName].range),
            cri: clone(CREEP_DATA[enemyName].critical),
            criTimes: clone(CREEP_DATA[enemyName].criTimes),
            dodge: clone(CREEP_DATA[enemyName].dodge),
            hitrate: clone(CREEP_DATA[enemyName].hitrate),
            buff: {}
        };
    }

    //玩家行动
    this.playerAp = function(){
        if(playerLoading){
            $("#apPlayer div").stop();
        }
        playerLoading = 1;
        $("#apPlayer div").width("0%");
        $("#battle div[class='battleOptions'] .btn").each(function(){
            $(this).attr("disabled", "disabled");
        });
        $("#battle div[class='battleSkills'] .btn").each(function(){
            $(this).attr("disabled", "disabled");
        });
        $("#apPlayer div").animate({width: "100%"}, player.speed*100, "linear", playerMove);
    }

    function playerMove(){
        playerLoading = 0;
        player.defence = realVal("defence");
        
        if(PLAYER_STATUS.buff.stun_enemy != undefined){
            appendLog(player.name + " <span class='badBuffName'>眩晕中</span>");
            $("#defence").trigger("nextTurn");
            sysTime = new Date(sysTime.getTime() + player.speed/10*1000*60);
            updateSysClock(0, 0, false, 2);
            tick();
            return;
        }

        if(enemyLoading){
            $("#apEnemy div").stop();
            pause = $("#apEnemy div").width()/$("#apEnemy").width();
        }

        extraSkill();
        $("#battle div[class='battleOptions'] button").each(function(){
            $(this).removeAttr("disabled");
        });
        if(dis>player.range || Math.ceil(realVal("energy"))<player.cost || PLAYER_STATUS.buff.overwork!=undefined || !ammoCheck()){
            $("#attack").attr("disabled", "disabled");
        }
        if(dis == 0){
            $("#forward").attr("disabled", "disabled");
        }
        if(PLAYER_STATUS.buff.freeze_enemy_1 != undefined){
            appendLog(player.name + " <span class='badBuffName'>无法移动</span>");
            $("#forward").attr("disabled", "disabled");
            $("#backward").attr("disabled", "disabled");
        }
        if(PLAYER_STATUS.buff.disarm_enemy != undefined){
            appendLog(player.name + " <span class='badBuffName'>无法攻击</span>");
            $("#attack").attr("disabled", "disabled");
        }

        sysTime = new Date(sysTime.getTime() + player.speed/10*1000*60);
        updateSysClock(0, 0, false, 2);
        tick();
    }

    //敌人行动
    function enemyAp(){
        $("#apEnemy div").width("0%");
        $("#apEnemy div").animate({width: "100%"}, enemy.speed*100, "linear", enemyMove);
        enemyLoading = 1;
    }

    function enemyMove(){
        enemyLoading = 0;
        var invisibleFlag = 0;
        for(var i in PLAYER_STATUS.buff){
            if(i.indexOf("invisible") != -1){
                invisibleFlag = 1;
                break;
            }
        }
        
        var buff = enemyBuffChk();
        if(buff == "stop"){
            appendLog(enemy.name + " <span class='badBuffName'>无法移动</span>");
        }
        if(buff == "freeze"){
            appendLog(enemy.name + " <span class='badBuffName'>冰冻中</span>");
            enemyAp();
            return;
        }
        if(buff == "stun"){
            appendLog(enemy.name + " <span class='badBuffName'>眩晕中</span>");
            enemyAp();
            return;
        }
        if(buff == "win"){
            winBattle();
            return;
        }
        if(dis>enemy.range && !invisibleFlag && buff!="stop"){
            if(CREEP_DATA[enemyName].preBuff != undefined){
                for(var i in CREEP_DATA[enemyName].preBuff){
                    if(Math.random()*100 < CREEP_DATA[enemyName].preBuff[i]){
                        enemy.buff[i] = {
                            effect:clone(BUFF_DATA[i].effect),
                            last:clone(BUFF_DATA[i].last)
                        };
                        appendLog(enemy.name + " 发动了特效 <span class='noneBuffName'>"+BUFF_DATA[i].name+"</span>");
                        enemyBuffChk();
                        enemyAp();
                        return;
                    }
                }
                
            }
            beClose(enemy.name, player.name, -1);
        }
        else if(dis<=enemy.range && !invisibleFlag){
            if(Math.random()*100 < enemy.hitrate * (100-player.dodge)/100){
                var percent = (100-player.defence)/100<0.1 ? 0.1 : (100-player.defence)/100;
                var damage = enemy.attack * percent * 1;
                damage = Math.ceil(damage<enemy.attack*0.1?enemy.attack*0.1:damage);
                if(Math.random()*100 < enemy.cri){
                    damage = Math.round(enemy.attack * enemy.criTimes) * percent * 1;
                    damage = Math.ceil(damage<enemy.attack*0.1?enemy.attack*0.1:damage);
                    appendLog(enemy.name + " 对 " + player.name + " 造成 <span class='badBuffName'>" + damage + "</span> 点暴击伤害");
                }
                else{
                    appendLog(enemy.name + " 对 " + player.name + " 造成 " + damage + " 点伤害");
                }
                DEATH_FOR = "被 <span class='badBuffName'>" + enemy.name + "</span> 杀死";
                updateStatus("life", -damage);
                if(CREEP_DATA[enemyName].buff != undefined){
                    for(var i in CREEP_DATA[enemyName].buff){
                        if(Math.random()*100<CREEP_DATA[enemyName].buff[i] && enemy.buff[i]==undefined){
                            appendLog(enemy.name + " 发动了特效 <span class='noneBuffName'>" + BUFF_DATA[i].name + "</span>");
                            if(BUFF_DATA[i].enemy){
                                enemy.buff[i] = {
                                    effect:clone(BUFF_DATA[i].effect),
                                    after:clone(BUFF_DATA[i].after),
                                    last:clone(BUFF_DATA[i].last)
                                };
                                for(var j in enemy.buff[i].effect){
                                    if(enemy.buff[i].effect[j].percent != undefined){
                                        if(enemy.buff[i].effect[j].toEnemy){
                                            enemy.buff[i].effect[j] = enemy[enemy.buff[i].effect[j].type] * enemy.buff[i].effect[j].percent;
                                        }
                                        else{
                                            enemy.buff[i].effect[j] = player[enemy.buff[i].effect[j].type] * enemy.buff[i].effect[j].percent;
                                        }
                                    }
                                }
                                if(enemy.buff[i].after != undefined){
                                    enemy.speed = 10;
                                }
                                if(BUFF_DATA[i].atonce){
                                    enemyBuffChk();
                                }
                            }
                            else{
                                getBuff(i);
                            }
                        }
                    }
                }
                for(var i in PLAYER_STATUS.buff){
                    if(BUFF_DATA[i].passive){
                        if(BUFF_DATA[i].passiveRate!=undefined && Math.random()*100>=BUFF_DATA[i].passiveRate){
                            continue;
                        }
                        eval(BUFF_DATA[i].passiveUpdate);
                    }
                }
                update();
            }
            else{
                appendLog(enemy.name + " 发动攻击，但被 " + player.name + " 躲开了");
            }
        }
        enemyAp();
    }

    //战斗操作
    function attack(){
        if(ITEM_DATA[player.weapon].ammoEnd == undefined){
            ammoCost();
        }
        if(Math.random()*100 < hitRateChk()){
            var percent = (100-enemy.defence)/100<0.1 ? 0.1 : (100-enemy.defence)/100;
            var damage = player.attack * percent * 1;
            damage = Math.ceil(damage<player.attack*0.1?player.attack*0.1:damage);
            if(Math.random()*100 < player.cri){
                damage = Math.round(player.attack * player.criTimes) * percent * 1;
                damage = Math.ceil(damage<player.attack*0.1?player.attack*0.1:damage);
                appendLog(player.name + " 对 " + enemy.name + " 造成 <span class='badBuffName'>" + damage + "</span> 点暴击伤害");
            }
            else{
                appendLog(player.name + " 击中了 " + enemy.name + " ，对其造成 " + damage + " 点伤害");
            }
            caculate(enemy, "life", -damage);
            buffAttack(player.weapon);
            if(CREEP_DATA[enemyName].passiveBuff != undefined){
                for(var i in CREEP_DATA[enemyName].passiveBuff){
                    if(Math.random()*100 < CREEP_DATA[enemyName].passiveBuff[i]){
                        appendLog(enemy.name + " 发动了特效 <span class='noneBuffName'>" + BUFF_DATA[i].name + "</span>");
                        for(var j in BUFF_DATA[i].effect){
                            var value = 0;
                            if(BUFF_DATA[i].effect[j].percent != undefined){
                                if(BUFF_DATA[i].effect[j].toEnemy){
                                    value = enemy[BUFF_DATA[i].effect[j].type] * BUFF_DATA[i].effect[j].percent;
                                }
                                else{
                                    value = player[BUFF_DATA[i].effect[j].type] * BUFF_DATA[i].effect[j].percent;
                                }
                            }
                            else{
                                value = BUFF_DATA[i].effect[j];
                            }
                            DEATH_FOR = "因 <span class='badBuffName'>" + BUFF_DATA[i].name + "</span> 致死";
                            updateStatus(j, value);
                            value = Math.round(value);
                            var msg = player.name + " 因 <span class='noneBuffName'>" + BUFF_DATA[i].name + "</span> "
                            + "造成 <span class='badBuffName'>" + PLAYER_STATUS[j].name + "</span>"
                            + (value>0?"+":"")
                            + value;
                            appendLog(msg);
                        }
                    }
                }
            }
            update();
        }
        else{
            appendLog(player.name + " 对 " + enemy.name + " 的攻击没有打中");
        }
        updateStatus("energy", -player.cost);
        if(player.weapon != "fist"){
            caculate(BAG_DATA, player.weapon, -1);
            updateItem(player.weapon, $("#bag"));
        }

        if(enemy.life <= 0){
            winBattle();
            return;
        }
        
        if(ITEM_DATA[player.weapon].continuous){
            if($("#apPlayer div").width()/$("#apPlayer").width()*100 >= 99.99){
                $("#apPlayer div").stop();
                $("#apPlayer div").animate({width: "0%"}, ITEM_DATA[player.weapon].contiTime*100, "linear");
            }
            var timer = setTimeout(function(){$("#attack").removeAttr("disabled");}, 50);
            $("#attack").attr("disabled", "disabled");
            if($("#apPlayer div").width() == 0){
                if(ITEM_DATA[player.weapon].ammoEnd){
                    ammoCost();
                }
                clearTimeout(timer);
                this.enemyResume();
                this.playerAp();
            }
        }
        else{
            this.enemyResume();
            this.playerAp();
        }
    }

    function aStep(value){
        beClose(player.name, enemy.name, value);
        this.enemyResume();
        this.playerAp();
    }

    function defence(){
        player.defence = player.defence * 1.1;
        this.enemyResume();
        this.playerAp();
    }

    function nextTurn(){
        this.playerAp();
    }

    function exitBattle(){
        if(Math.random()*100 < player.escape){
            var percent = $("#apPlayer div").width()/$("#apPlayer").width()*100;
            if(ITEM_DATA[player.weapon].ammoEnd && percent>0 && percent<100){
                ammoCost();
            }
            $("#battle").empty();
            var escapeTo = EX_TAB[EX_TAB.length-1];
            if(CREEP_DATA[enemyName].danger){
                escapeTo = "outside";
                showMsg("已脱离与危险敌人的交战，确认自己能战胜对方前，请勿再次进入该地点。");
            }
            if(enemyIn != ""){
                enemyIn = "";
            }
            if(callback != null){
                callback = null;
            }
            toLoading(0.1, escapeTo, "back");
            BATTLE_FLAG = false;
            resumeGame();
        }
        else{
            appendLog("===逃跑失败===");
            this.enemyResume();
            this.playerAp();
        }
    }

    //物品附加技能
    function extraSkill(flag){
        var self = this;
        var layer = $("#battle div[class='battleSkills']");
        if(flag){
            layer.empty();
            for(var i in PLAYER_STATUS.equip){
                if(PLAYER_STATUS.equip[i]!="" && ITEM_DATA[PLAYER_STATUS.equip[i]].skillName!=undefined){
                    var newBtn = newElement("button", PLAYER_STATUS.equip[i], "", "btn btn-default", ITEM_DATA[PLAYER_STATUS.equip[i]].skillName);
                    newBtn.onclick = function(){
                        var itemdata = ITEM_DATA[this.id];
                        appendLog(player.name + " 发动了技能 <span class='rare'>" + itemdata.skillName + "</span>");
                        for(var j in itemdata.skillCost){
                            updateStatus(j, -itemdata.skillCost[j]);
                        }
                        eval(itemdata.skill);
                        self.enemyResume();
                        self.playerAp();
                    };
                    newBtn.onmouseover = function(){$("#info").html(ITEM_DATA[this.id].skillDesc);};
                    taphold(newBtn, newBtn.onmouseover);
                    newBtn.setAttribute("disabled", "disabled");
                    layer.append(newBtn);
                }
            }
        }
        layer.find(".btn").each(function(){
            var itemdata = ITEM_DATA[$(this).attr("id")];
            var costFlag = 1;
            for(var j in itemdata.skillCost){
                if(realVal(j) < itemdata.skillCost[j]){
                    costFlag = 0;
                    break;
                }
            }
            if(itemdata.skillRange!=undefined && dis>itemdata.skillRange){
                costFlag = 0;
            }
            if(costFlag){
                $(this).removeAttr("disabled");
            }
        });
        
    }

    function hitRateChk(){
        var hitrate = player.hitrate;
        if(player.range < dis){
            hitrate = 0;
        }
        else if(player.range > dis){
            hitrate = hitrate * (1+(player.range-dis)/player.range/10);
        }
        hitrate *= (100-enemy.dodge)/100;
        hitrate = Math.floor(hitrate>100?100:hitrate);
        return hitrate;
    }

    function disCheck(){
        var result = 5 * (1+(realVal("perception") - 5)/2.5);
        result = result>10 ? 10 : result;
        var nightFlag = 0;
        if((sysTime.getHours()>=20 && sysTime.getHours()<=23)||(sysTime.getHours()>=0 && sysTime.getHours()<=4)){
            nightFlag = 1;
            result *= 0.5;
        }
        for(var i in PLAYER_STATUS.buff){
            if(i.indexOf("radar") != -1 || (i=="nightVision" && nightFlag)){
                result *= BUFF_DATA[i].dis;
            }
        }
        result = Math.floor(result);
        return result<=0?1:result;
    }

    function ammoCheck(){
        if(ITEM_DATA[player.weapon].ammo != undefined){
            if(PLAYER_STATUS.equip.ammo != ""){
                for(var i in ITEM_DATA[player.weapon].ammo){
                    var cost = ITEM_DATA[player.weapon].ammoCost==undefined?1:ITEM_DATA[player.weapon].ammoCost;
                    if(PLAYER_STATUS.equip.ammo==ITEM_DATA[player.weapon].ammo[i] && BAG_DATA[PLAYER_STATUS.equip.ammo]>=cost){
                        return 1;
                    }
                }
                return 0;
            }
            else{
                return 0;
            }
        }
        else{
            return 1;
        }
    }

    function ammoCost(){
        if(ITEM_DATA[player.weapon].ammo != undefined){
            var cost = ITEM_DATA[player.weapon].ammoCost==undefined?1:ITEM_DATA[player.weapon].ammoCost;
            caculate(BAG_DATA, PLAYER_STATUS.equip.ammo, -cost);
            buffAttack(PLAYER_STATUS.equip.ammo);
            updateItem(PLAYER_STATUS.equip.ammo, $("#bag"));
        }
    }

    function buffAttack(item){
        if(ITEM_DATA[item].buffUse != undefined){
            var buff = ITEM_DATA[item].buffUse;
            if(Math.random()*100<ITEM_DATA[item].buffRate && enemy.buff[buff]==undefined){
                if(BUFF_DATA[buff].effect == "dis"){
                    appendLog(enemy.name + " 被<span class='noneBuffName'>击飞</span>");
                    beClose(enemy.name, player.name, BUFF_DATA[buff].dis, true);
                }
                else{
                    if(BUFF_DATA[buff].self){
                        getBuff(buff);
                        return;
                    }
                    enemy.buff[buff] = {
                        effect:clone(BUFF_DATA[buff].effect),
                        last:clone(BUFF_DATA[buff].last)
                    };
                    for(var i in enemy.buff[buff].effect){
                        if(enemy.buff[buff].effect[i].percent != undefined){
                            if(enemy.buff[buff].effect[i].toEnemy){
                                enemy.buff[buff].effect[i] = enemy[enemy.buff[buff].effect[i].type] * enemy.buff[buff].effect[i].percent;
                            }
                            else{
                                enemy.buff[buff].effect[i] = player[enemy.buff[buff].effect[i].type] * enemy.buff[buff].effect[i].percent;
                            }
                        }
                    }
                    appendLog(player.name + " 发动了特效 <span class='noneBuffName'>" + BUFF_DATA[buff].name + "</span>");
                    if(BUFF_DATA[buff].atonce){
                        enemyBuffChk();
                    }
                }
            }
        }
    }

    function enemyBuffChk(){
        for(var i in enemy.buff){
            if(enemy.buff[i].effect != undefined){
                if(BUFF_DATA[i].effect=="dis"){
                    beClose(enemy.name, player.name, BUFF_DATA[i].dis, true);
                }
                else{
                    for(var j in enemy.buff[i].effect){
                        var effectValue = Math.round(enemy.buff[i].effect[j]);
                        enemy[j] += effectValue;
                        if(j=="life" && enemy[j]>CREEP_DATA[enemyName].life){
                            enemy[j] = CREEP_DATA[enemyName].life;
                        }

                        var statusName = "";
                        if(j == "speed"){
                            statusName = "速度";
                            effectValue *= -1;
                        }
                        else{
                            statusName = PLAYER_STATUS[j].name;
                        }
                        var msg = enemy.name + " 因 <span class='noneBuffName'>" + BUFF_DATA[i].name + "</span> "
                        + "造成 <span class='badBuffName'>" + statusName + "</span>"
                        + (effectValue>0?"+":"")
                        + effectValue;
                        appendLog(msg);
                        update();
                    }
                }
            }
            caculate(enemy.buff[i], "last", -1);
            if(enemy.buff[i].after != undefined){
                appendLog("<span class='badBuffName'>" + BUFF_DATA[i].name + "</span> 生效倒计时：" + enemy.buff[i].last);
            }
            if(enemy.buff[i].last <= 0){
                if(enemy.buff[i].after != undefined){
                    eval(enemy.buff[i].after);
                    enemy.speed = clone(CREEP_DATA[enemyName].speed);
                }
                delete enemy.buff[i];
            }
            if(BUFF_DATA[i].freeze){
                return "freeze";
            }
            if(BUFF_DATA[i].stop){
                return "stop";
            }
            if(BUFF_DATA[i].stun){
                return "stun";
            }
        }
        if(enemy.life <= 0){
            return "win";
        }
    }

    this.enemyResume = function(){
        var left = enemy.speed * (1 - pause);
        $("#apEnemy div").animate({width: "100%"}, left*100, "linear", enemyMove);
        pause = 0;
    }

    this.getLoading = function(){
        update();
        return playerLoading;
    }

    function beClose(a, b, value, flag){
        dis += value;
        dis = dis<0?0:dis;
        $("#battle div[class='battleDis'] span[id='dis']").html(dis);
        $("#battle div[class='battleDis'] span[id='dis']").hide();
        $("#battle div[class='battleDis'] span[id='dis']").fadeIn(200);
        if(flag){
            appendLog("距离" + (value>0 ? "增加"+value : "减少"+value*-1));
        }
        else{
            appendLog(value<0?(a + " 向 " + b + " 接近了一步"):(a + "后退了一步"));
        }
        $("#battle div[class='battleWeapon'] table tbody tr td:eq(3)").html(hitRateChk() + "%");
    }

    function update(){
        if(enemy.life > CREEP_DATA[enemyName].life){
            enemy.life = clone(CREEP_DATA[enemyName].life);
        }
        $("#hpPlayer div").animate({width: realVal("life")/PLAYER_STATUS.life.max * 100 + "%"}, 100);
        $("#battlePlayer span").html(Math.ceil(realVal("life")) + "/" + Math.ceil(PLAYER_STATUS.life.max));

        $("#hpEnemy div").animate({width: enemy.life/CREEP_DATA[enemyName].life * 100 + "%"}, 100);
        $("#battleEnemy span").html(Math.ceil(enemy.life) + "/" + Math.ceil(CREEP_DATA[enemyName].life));
    }

    function appendLog(newLog){
        log += newLog + "<br>";
        $("#battle div[class='battleInfo']").html(log);
        $("#battle div[class='battleInfo']").scrollTop($("#battle div[class='battleInfo']")[0].scrollHeight);
    }

    function winBattle(){
        var percent = $("#apPlayer div").width()/$("#apPlayer").width()*100;
        if(ITEM_DATA[player.weapon].ammoEnd && percent>0 && percent<100){
            ammoCost();
        }
        clear(TEMP_DATA);
        for(var i in CREEP_DATA[enemyName].drop){
            TEMP_DATA[i] = Math.floor(Math.random()*(CREEP_DATA[enemyName].drop[i][1]-CREEP_DATA[enemyName].drop[i][0])+CREEP_DATA[enemyName].drop[i][0]);
        }
        if(CREEP_DATA[enemyName].rare != undefined){
            for(var i in CREEP_DATA[enemyName].rare){
                var luck = 1 + Math.log((realVal("luck")+1)/5);
                if(Math.random()*100 < CREEP_DATA[enemyName].rare[i][1]*luck){
                    TEMP_DATA[i] = Math.floor(Math.random()*CREEP_DATA[enemyName].rare[i][0]+1);
                }
            }
        }
        if(CREEP_DATA[enemyName].chest != undefined){
            var unlocker = ["crowbar", "unlocker", "eUnlocker"];
            unlocker = unlocker[Math.floor(Math.random()*unlocker.length)];
            var cost = Math.floor(Math.random() * 2 * ITEM_DATA[unlocker].durab + 1);
            var require = {};
            require[unlocker] = cost;
            var get = {};
            var chest = Object.keys(CREEP_DATA[enemyName].chest);
            for(var i=0;i<Math.floor(Math.random()*4 + 1);i++){
                var drop = chest[Math.floor(Math.random()*chest.length)];
                if(get[drop] == undefined){
                    get[drop] = ITEM_DATA[drop].durab!=undefined ? ITEM_DATA[drop].durab : Math.floor(Math.random()*CREEP_DATA[enemyName].chest[drop]+1);
                }
            }
            if(MAP_DATA[enemyIn].resource == undefined){
                MAP_DATA[enemyIn].resource = {};
            }
            var n = 0;
            var chestName = "chest" + n.toString();;
            while(MAP_DATA[enemyIn].resource[chestName] != undefined){
                n += 1;
                chestName = "chest" + n.toString();
            }
            MAP_DATA[enemyIn].resource[chestName] = {
                name:"箱子",
                get:clone(get),
                refresh:0,
                max:1,
                value:1,
                energy:20,
                require:clone(require)
            }
            showMsg("击败敌人后，你在附近某个角落找到了对方看守的箱子，不知里面装着什么。");
        }

        var place = enemyIn==""?EX_TAB[EX_TAB.length-1]:enemyIn;
        if(callback==null && CREEP_DATA[enemyName].only==undefined){
            for(var i in MAP_DATA[place].enemy.exist){
                if(MAP_DATA[place].enemy.exist[i] == enemyName){
                    MAP_DATA[place].enemy.exist.splice(i, 1);
                    break;
                }
            }
            caculate(MAP_DATA[place].enemy, "amount", -1);
        }
        if(callback != null){
            callback();
            callback = null;
        }
        if(enemyIn != ""){
            EX_TAB.push(enemyIn);
            enemyIn = "";
        }
        toLoading(0.5, "pickUp", true);
        BATTLE_FLAG = false;
        resumeGame();
        updateProgress("endurance", Math.ceil(CREEP_DATA[enemyName].attack/40));
        $("#battle").empty();
    }
}
//================================================================================================


//地图对象
function mapObj(dest){
    this.name = MAP_DATA[dest].name;

    this.create = function(){
        $("#map").empty();
        $("#map").attr("place", dest);

        if(MAP_DATA[dest].buff!=undefined){
            getBuff(MAP_DATA[dest].buff);
        }

        if($.inArray(dest, ["outside", "origin", "toilet", "farm", "well"]) == -1){
            var newBtn = newElement("button", "make", "make", "btn btn-default", "制作");
            newBtn.onmouseover = function(){$("#info").html("制作简单工具或搭建设施。");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){toLoading(0.1, "handwork");};
            $("#map").append(newBtn);
        }
        if(dest == "home"){
            var newBtn = newElement("button", "toTrain", "toTrain", "btn btn-default", "训练");
            newBtn.onmouseover = function(){$("#info").html("变得更强。");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){toLoading(0.1, "train");};
            $("#map").append(newBtn);
        }
        if(dest=="outside" && EXPLORE_FLAG){
            var newBtn = newElement("button", "toExplore", "toExplore", "btn btn-default", "探索");
            var desc = "探索未知地域，发现更多的新地点<br>"
                     + "用时：2~" + Math.ceil(EXPLORE_TIME/60) + "小时<br>"
            newBtn.onmouseover = function(){$("#info").html(desc);};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){explore();};
            $("#map").append(newBtn);
        }
        if(EXCRETE_FLAG[0]){
            var newBtn = newElement("button", "toPoo", "", "btn btn-default", "排便");
            newBtn.onmouseover = function(){$("#info").html("这还有什么好解释的。");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){toLoading(1.5, "poo");};
            $("#map").append(newBtn);
        }
        if(EXCRETE_FLAG[1]){
            var newBtn = newElement("button", "toPee", "", "btn btn-default", "排尿");
            newBtn.onmouseover = function(){$("#info").html("这还有什么好解释的。");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){toLoading(0.5, "pee");};
            $("#map").append(newBtn);
        }
        if(MAP_DATA[dest].outside != undefined){
            var newBtn = newElement("button", "toOutside", "", "btn btn-default", "外出");
            newBtn.onmouseover = function(){$("#info").html("");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){EX_TAB.pop();toLoading(0.1, "outside");};
            $("#map").append(newBtn);
        }
        if(MAP_DATA[dest].goHome == undefined){
            var newBtn = newElement("button", "goBackHome", "", "btn btn-default", "回家");
            var cost = 0.1;
            newBtn.onmouseover = function(){$("#info").html("");};
            taphold(newBtn, newBtn.onmouseover);
            if($("#map").attr("place") == "outside"){
                newBtn.onclick = function(){EX_TAB.pop();toLoading(cost, "home");};
            }
            else{
                cost = MAP_DATA.outside.place[$("#map").attr("place")].cost;
                newBtn.onclick = function(){EX_TAB.pop();costTimeFunc(cost*60, cost/2, "desthome");};
            }
            $("#map").append(newBtn);
        }
        if(MAP_DATA[dest].back == undefined){
            getBackBtn($("#map"));
            $("#map br").remove();
        }
        $("#map").append("<br>");

        if(dest == "toilet"){
            $("#map").append(newElement("div", "toiletData", "toiletData", "", ""));
            for(var i in TOILET_DATA){
                var newObj = new itemObj(i, $("#toiletData"));
                newObj.create();
            }
            $("#map").append("<br>");
        }

        if(MAP_DATA[dest].resource != undefined){
            for(var i in MAP_DATA[dest].resource){
                //纠错功能--资源变更
                if(MAP_DATA[dest].resource[i].name == undefined){
                    delete MAP_DATA[dest].resource[i];
                    continue;
                }
                createResource(MAP_DATA[dest].resource[i], i);
            }
        }

        if(MAP_DATA[dest].trash != undefined){
            createTrash(MAP_DATA[dest].trash);
        }

        if(MAP_DATA[dest].enemy != undefined){
            createEnemy();
        }

        $("#map").append("<br>");
        if(MAP_DATA[dest].place != undefined){
            for(var i in MAP_DATA[dest].place){
                if(MAP_DATA[dest].place[i].show != undefined){
                    createPlace(MAP_DATA[dest].place[i], i);
                }
            }
        }
        

        if(MAP_DATA[dest].quest!=undefined && MAP_DATA[dest].quest.length>0 && QUEST_DATA[MAP_DATA[dest].quest[0]].done){
            if(QUEST_DATA[MAP_DATA[dest].quest[0]].after != undefined){
                showMsg(QUEST_DATA[MAP_DATA[dest].quest[0]].after, QUEST_DATA[MAP_DATA[dest].quest[0]].afterTime);
            }
            if(QUEST_DATA[MAP_DATA[dest].quest[0]].update != undefined){
                eval(QUEST_DATA[MAP_DATA[dest].quest[0]].update);
            }
            QUEST_FINISHED.push([MAP_DATA[dest].quest[0], dest]);
            //delete QUEST_DATA[MAP_DATA[dest].quest[0]];
            MAP_DATA[dest].quest.shift();
        }
    }

    function createPlace(place, name){
        if(place.need != undefined){
            for(var i in place.need){
                if(realVal(i) < place.need[i]){
                    return;
                }
            }
            $(".place[id='"+place.replace+"']").remove();
        }
        var newBtn = newElement("button", name, name, "btn btn-default moveBtn place", place.name);
        var todest = place.dest;
        var cost = place.cost==undefined ? 0.1 : place.cost;
        cost = cost==0.1 ? 0.1 : (cost*MOVE_SPEED).toFixed(1);
        var desc = place.desc;
        if(cost >= 0.5){
            desc += "<br>路程：" + cost + " 小时";
        }
        if(MAP_DATA[name]!=undefined && place.name!="未知" && place.name!="未开放"){
            desc += "<br>" + placeDesc(MAP_DATA[name]);
        }
        newBtn.onmouseover = function(){$("#info").html(desc);};
        taphold(newBtn, newBtn.onmouseover);
        if(place.quest != undefined && place.quest.length > 0){
            newBtn.onclick = function(){toQuest(place.quest[0], place);};
        }
        else{
            newBtn.onclick = function(){costTimeFunc(cost*60, cost/2, "dest"+todest);};
        }
        if(place.enemy){
            newBtn = newElement("button", name, name, "btn btn-default moveBtn enemy", place.name);
            desc = "";
            if(CREEP_DATA[name].drop != undefined){
                desc += "战利品：";
                for(var drop in CREEP_DATA[name].drop){
                    desc += "[" + ITEM_DATA[drop].name + "] ";
                }
            }
            if(CREEP_DATA[name].rare != undefined){
                desc += "<br>稀有物品：";
                for(var drop in CREEP_DATA[name].rare){
                    desc += "[" + ITEM_DATA[drop].name + "] ";
                }
                if(CREEP_DATA[name].chest != undefined){
                    for(var drop in CREEP_DATA[name].chest){
                        desc += "[" + ITEM_DATA[drop].name + "] ";
                    }
                }
            }
            newBtn.onmouseover = function(){$("#info").html(desc);};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){
                BATTLE_OBJ.setEnemy(name);
                BATTLE_OBJ.setEnemyIn(dest);
                BATTLE_OBJ.setCallback(function(){
                    delete place.show;
                });
                toLoading(0.5, "battle");
            };
        }
        $("#map").append(newBtn);
        function toQuest(quest, place){
            if(QUEST_DATA[quest].done){
                finishQuest(quest, place);
                return;
            }
            $("#quest").empty();
            getBackBtn($("#quest"));
            $("#quest").append(newElement("div", "", "", "info", QUEST_DATA[quest].desc));
            if(QUEST_DATA[quest].next != undefined){
                var flag = 1;
                if(QUEST_DATA[quest].require != undefined){
                    for(var i in QUEST_DATA[quest].require){
                        if(i != "buff"){
                            var itemName = i;
                            if(ITEM_DATA[i].type == "food2"){
                                for(var item in BAG_DATA){
                                    if(item!=itemName && item.indexOf(itemName)==0){
                                        itemName = item;
                                        break;
                                    }
                                }
                            }
                            if(i=="water" && BAG_DATA.cleanWater!=undefined){
                                itemName = "cleanWater";
                            }
                            if(BAG_DATA[itemName]==undefined || BAG_DATA[itemName]<QUEST_DATA[quest].require[i]){
                                flag = 0;
                                break;
                            }
                        }
                        if(i=="buff" && PLAYER_STATUS.buff[QUEST_DATA[quest].require[i]]==undefined){
                            flag = 0;
                            break;
                        }
                    }
                }
                if(QUEST_DATA[quest].need != undefined){
                    for(var i in QUEST_DATA[quest].need){
                        if(realVal(i) < QUEST_DATA[quest].need[i]){
                            flag = 0;
                            break;
                        }
                    }
                }
                if(flag){
                    toQuest(QUEST_DATA[quest].next, place);
                }
            }
            else if(QUEST_DATA[quest].option != undefined){
                for(var i in QUEST_DATA[quest].option){
                    var needFlag = 1;
                    var needDesc = "";
                    if(QUEST_DATA[quest].option[i].need != undefined){
                        for(var j in QUEST_DATA[quest].option[i].need){
                            if(realVal(j) < QUEST_DATA[quest].option[i].need[j]){
                                needFlag = 0;
                                needDesc += PLAYER_STATUS[j].name + QUEST_DATA[quest].option[i].need[j];
                            }
                        }
                    }
                    var requireFlag = 1;
                    if(QUEST_DATA[quest].option[i].require != undefined){
                        for(var j in QUEST_DATA[quest].option[i].require){
                            if(BAG_DATA[j]==undefined || BAG_DATA[j]<QUEST_DATA[quest].option[i].require[j]){
                                requireFlag = 0;
                            }
                        }
                    }
                    if(QUEST_DATA[quest].option[i].hide==undefined && requireFlag){
                        var newBtn = newElement("button", i, "", "btn btn-default", QUEST_DATA[quest].option[i].action + (needDesc!=""?"("+needDesc+")":""));
                        newBtn.onclick = function(){toQuest(this.id);};
                        if(!needFlag){
                            newBtn.setAttribute("disabled", "disabled");
                        }
                        if(QUEST_DATA[quest].option[i].random){
                            newBtn.onclick = function(){
                                var ranType = QUEST_DATA[quest].option[i].ranType;
                                var chance = realVal(ranType);
                                chance = QUEST_DATA[quest].option[i].chance + Math.log((chance+1)/6);
                                if(Math.random() < chance){
                                    toQuest(this.id);
                                }
                                else{
                                    if(QUEST_DATA[quest].option[i].after != undefined){
                                        showMsg(QUEST_DATA[quest].option[i].after, QUEST_DATA[quest].option[i].afterTime);
                                    }
                                    if(QUEST_DATA[quest].option[i].fail != undefined){
                                        toQuest(QUEST_DATA[quest].option[i].fail);
                                    }
                                    else{
                                        toLoading(0.1, dest);
                                    }
                                    caculate(QUEST_DATA[quest].option[i], "tryed", 1);
                                    if(QUEST_DATA[quest].option[i].tryed >= QUEST_DATA[quest].option[i].maxtry){
                                        delete QUEST_DATA[quest].option[i];
                                    }
                                }
                            }
                        }
                        $("#quest").append(newBtn);
                    }
                }
            }
            else{
                var newBtn = newElement("button", "questAction", "", "btn btn-default", QUEST_DATA[quest].action);
                newBtn.onclick = function(){finishQuest(quest, place);};
                $("#quest").append(newBtn);
                if(QUEST_DATA[quest].require != undefined){
                    var flag = 0;
                    for(var i in QUEST_DATA[quest].require){
                        var itemName = i;
                        if(ITEM_DATA[i].type == "food2"){
                            for(var item in BAG_DATA){
                                if(item!=itemName && item.indexOf(itemName)==0){
                                    itemName = item;
                                    break;
                                }
                            }
                        }
                        if(i=="water" && BAG_DATA.cleanWater!=undefined){
                            itemName = "cleanWater";
                        }
                        if(BAG_DATA[itemName]==undefined || BAG_DATA[itemName]<QUEST_DATA[quest].require[i]){
                            flag = 1;
                            break;
                        }
                        if(i=="buff" && PLAYER_STATUS.buff[QUEST_DATA[quest].require[i]]==undefined){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag){
                        $("#questAction").attr("disabled", "disabled");
                    }
                }
            }

            toLoading(0.1, "quest");
        }

        function finishQuest(quest, place){
            if(QUEST_DATA[quest].require != undefined){
                for(var i in QUEST_DATA[quest].require){
                    if(i != "buff"){
                        var itemName = i;
                        if(ITEM_DATA[i].type == "food2"){
                            for(var item in BAG_DATA){
                                if(item!=itemName && item.indexOf(itemName)==0){
                                    itemName = item;
                                    break;
                                }
                            }
                        }
                        if(i=="water" && BAG_DATA.cleanWater!=undefined){
                            itemName = "cleanWater";
                        }
                        caculate(BAG_DATA, itemName, -QUEST_DATA[quest].require[i]);
                        if(QUEST_DATA[quest].clearItem){
                            BAG_DATA[itemName] = 0;
                        }
                        updateItem(itemName, $("#bag"));
                    }
                }
            }
            if(QUEST_DATA[quest].after != undefined){
                showMsg(QUEST_DATA[quest].after, QUEST_DATA[quest].afterTime);
            }
            if(QUEST_DATA[quest].repeat == undefined){
                if(place != null){
                    QUEST_FINISHED.push([quest, dest+".place."+name]);
                    place.quest.shift();
                }
                else{
                    QUEST_FINISHED.push([quest, "null"])
                }
            }

            if(QUEST_DATA[quest].update != undefined){
                var update = clone(QUEST_DATA[quest].update);
                eval(update);
                
                if($(".tab-pane.active").attr("id")=="quest" && update.indexOf("BATTLE_OBJ")==-1 && update.indexOf("toLoading")==-1){
                    toLoading(0.1, dest);
                }
                else if($(".tab-pane.active").attr("id")!="quest" && update.indexOf("toLoading") == -1){
                    var newObj = new mapObj(dest);
                    newObj.create();
                    $(".main").hide();
                    $(".main").fadeIn(500);
                }
            }
            else{
                toLoading(0.1, dest);
            }
        }
    }

    function createResource(res, name){
        if(res.hide){
            return;
        }
        var newBtn = newElement("button", name, name, "btn btn-default moveBtn res", "");
        var desc = "";
        var flag = 1;
        if(res.value <= 0 || PLAYER_STATUS.buff.overwork!=undefined){
            flag = 0;
        }
        
        if(name.indexOf("farmland") == 0){
            flag = 0;
            desc = "可播种";
        }
        else{
            if(name.indexOf("chest") == -1){
                for(var i in res.get){
                    desc += "获取：" + ITEM_DATA[i].name + res.get[i];
                }
            }
            desc += "<br>消耗：";
            if(Math.ceil(realVal("energy"))>=res.energy){
                desc += "<span class='goodBuffName'>精力</span>" + res.energy + "<br>";
            }
            else{
                flag = 0;
                desc += "<span class='badBuffName'>精力</span>" + res.energy + "<br>";
            }
            if(res.require != undefined){
                desc += "需求：";
                for(var i in res.require){
                    var own = BAG_DATA[i]==undefined?0:BAG_DATA[i];
                    if(own==0 && $.inArray(i, ["axe", "shovel", "pickaxe", "hoe"])!=-1){
                        for(var j in BAG_DATA){
                            if(j.indexOf(i) == 0){
                                own = BAG_DATA[j];
                                break;
                            }
                        }
                    }
                    var color = "goodBuffName";
                    if(own < res.require[i]){
                        flag = 0;
                        color = "badBuffName";
                    }
                    desc += "<span class='" + color + "'>" + ITEM_DATA[i].name + "</span>" + res.require[i];
                }
            }
        }
        newBtn.innerHTML = res.name + "<br>" + (name.indexOf("chest")==0||res.value==0||res.crop||res.value==undefined?"":res.value);
        newBtn.onmouseover = function(){$("#info").html(desc);};
        taphold(newBtn, newBtn.onmouseover);
        if(flag){
            newBtn.onclick = function(){getResource();};
        }
        $("#map").append(newBtn);
        if(res.refresh!=0 && res.value<res.max){
            var percent = (sysTime-res.lastGrow)/1000/60 / res.refresh * 100;
            var restTime = (res.refresh-(sysTime-res.lastGrow)/1000/60) / 2.5 * 1000;
            var bar = "<div class='apDiv'><div class='loadingBar' style='width:"+percent+"%;'></div></div>";
            $("#map button[id='"+name+"']").html(res.name + bar + (res.value==0||res.crop||res.value==undefined?"":res.value));
            $("#map button[id='"+name+"'] div div").animate({width:"100%"}, restTime, "linear");
        } 

        function getResource(){
            if(res.crop){
                updateStatus("energy", -res.energy);
                $("#map button[id='"+name+"']").remove();
                getItem(res.get);
                delete MAP_DATA.farm.resource[name];
                getSum(MAP_DATA.farm.resource);
            }
            else if(name.indexOf("chest") == 0){
                updateStatus("energy", -res.energy);
                $("#map button[id='"+name+"']").remove();
                getItem(res.get, true);
                delete MAP_DATA[dest].resource[name];
            }
            else if(res.getall){
                clear(TEMP_DATA);
                for(var i in res.get){
                    var value = res.get[i] * res.value;
                    if(!isNaN(value)){
                        TEMP_DATA[i] = value;
                    }
                }
                for(var i in res.require){
                    caculate(BAG_DATA, i, -res.require[i]);
                    updateItem(i, $("#bag"));
                }
                res.value = 0;
                costTimeFunc(res.energy, 1, "resource", function(){EX_TAB.push($("#map").attr("place"));});
            }
            else{
                var requireFlag = res.require!=undefined?0:1;
                for(var i in res.require){
                    if(BAG_DATA[i]==undefined && $.inArray(i, ["axe", "shovel", "pickaxe", "hoe"])!=-1){
                        for(var j in BAG_DATA){
                            if(j.indexOf(i) == 0){
                                caculate(BAG_DATA, j, -res.require[i]);
                                updateItem(j, $("#bag"));
                                requireFlag = 1;
                                break;
                            }
                        }
                    }
                    else{
                        caculate(BAG_DATA, i, -res.require[i]);
                        updateItem(i, $("#bag"));
                        requireFlag = 1;
                    }
                }
                if(requireFlag){
                    caculate(res, "value", -1);
                    clear(TEMP_DATA);
                    for(var i in res.get){
                        TEMP_DATA[i] = clone(res.get[i]);
                    }
                    EX_RESOURCE = res;
                    costTimeFunc(res.energy, 1, "resource", function(){EX_TAB.push($("#map").attr("place"));});
                }
            }
        }
    }

    function createTrash(trash){
        var newBtn = newElement("button", "trash", "trash", "btn btn-default moveBtn", "捡垃圾");
        var desc = "";
        var flag = 1;
        for(var i in trash){
            if(trash[i].amount > 0){
                flag = 0;
            }
        }
        for(var i in trash){
            if(trash[i].amount > 0){
                desc += ITEM_DATA[i].name + "：&#9;" + amountDesc(trash[i].amount)
                      + "&#9;获取概率：" + chanceDesc(trash[i].get[2]) + "<br>";
            }
        }
        newBtn.onmouseover = function(){$("#info").html("<pre>" + desc + "</pre>");};
        taphold(newBtn, newBtn.onmouseover);
        if(flag || PLAYER_STATUS.buff.overwork!=undefined || Math.ceil(realVal("energy")) <= 0){
            newBtn.setAttribute("disabled", "disabled");
        }
        else{
            newBtn.onclick = function(){
                clear(TEMP_DATA);
                for(var i in trash){
                    var get = Math.floor(Math.random()*(trash[i].get[1]-trash[i].get[0])+trash[i].get[0]);
                    if(trash[i].amount>0 && Math.random()*100< trash[i].get[2]){
                        TEMP_DATA[i] = get;
                        caculate(trash[i], "amount", -get);
                        trash[i].amount = trash[i].amount<get ? 0 : clone(trash[i].amount);
                    }
                }
                costTimeFunc(5, 1, "trash", function(){EX_TAB.push($("#map").attr("place"));});
            };
        }
        $("#map").append("<br>");
        $("#map").append(newBtn);
    }

    function createEnemy(){
        if(MAP_DATA[dest].enemy.exist.length == 0){
            var bossSum = MAP_DATA[dest].enemy.boss==undefined ? 0 : getSum(MAP_DATA[dest].enemy.boss);
            if(MAP_DATA[dest].enemy.normal==undefined || (getSum(MAP_DATA[dest].enemy.normal)+bossSum==0)){
                return;
            }
            $("#map").append("<br>");
            var newBtn = newElement("button", "search", "search", "btn btn-default moveBtn", "搜寻");
            var desc = "敌人密度：" + densityDesc(dest);
            for(var i in MAP_DATA[dest].enemy.normal){
                if(MAP_DATA[dest].enemy.normal[i] > 0){
                    if(CREEP_DATA[i].danger){
                        desc += "<br><span class='badBuffName'>[危险]</span>"
                        + CREEP_DATA[i].name.replace("<br>","") + "&#9;数量："
                        + amountDesc(MAP_DATA[dest].enemy.normal[i]);
                    }
                    else{
                        desc += "<br>[中立]" + CREEP_DATA[i].name.replace("<br>","") + "&#9;数量："
                        + amountDesc(MAP_DATA[dest].enemy.normal[i]);
                    }
                }
            }
            if(MAP_DATA[dest].enemy.boss != undefined){
                //纠错功能--boss版本变更
                if(MAP_DATA[dest].enemy.boss.name != undefined){
                    delete MAP_DATA[dest].enemy.boss.name;
                    delete MAP_DATA[dest].enemy.boss.rate;
                }
                for(var i in MAP_DATA[dest].enemy.boss){
                    if(MAP_DATA[dest].enemy.boss[i].hide == undefined){
                        desc += "<br><span class='rare'>[精英]</span>"
                        + CREEP_DATA[i].name.replace("<br>","")
                        + "&#9;相遇概率：" + chanceDesc(MAP_DATA[dest].enemy.boss[i].rate);
                    }
                }
            }
            desc += "<br><span class='badBuffName'>【注意】</span>一旦与危险生物相遇，将立刻进入战斗。可能遭遇连续战斗。";
            newBtn.onmouseover = function(){$("#info").html("<pre>" + desc + "</pre>");};
            taphold(newBtn, newBtn.onmouseover);
            newBtn.onclick = function(){search();};
            $("#map").append(newBtn);
        }
        else{
            $("#map").append("<br>");
            for(var i in MAP_DATA[dest].enemy.exist){
                if(CREEP_DATA[MAP_DATA[dest].enemy.exist[i]].danger){
                    BATTLE_OBJ.setEnemy(MAP_DATA[dest].enemy.exist[i]);
                    BATTLE_OBJ.setEnemyIn(dest);
                    BATTLE_ATONCE = true;
                    break;
                }
                create(MAP_DATA[dest].enemy.exist[i]);
            }
        }

        function search(){
            var get = Math.floor(Math.random()*(MAP_DATA[dest].enemy.get[1]-MAP_DATA[dest].enemy.get[0])+MAP_DATA[dest].enemy.get[0]);
            for(var i=0;i<get;i++){
                var a = Math.floor(Math.random()*getSum(MAP_DATA[dest].enemy.normal));
                var b = Object.keys(MAP_DATA[dest].enemy.normal);
                if(MAP_DATA[dest].enemy.normal[b[a]] > 0){
                    MAP_DATA[dest].enemy.exist.push(b[a]);
                }
            }
            if(MAP_DATA[dest].enemy.boss != undefined){
                for(var i in MAP_DATA[dest].enemy.boss){
                    if(MAP_DATA[dest].enemy.boss[i].hide == undefined){
                        if(Math.random()*100 < MAP_DATA[dest].enemy.boss[i].rate){
                            MAP_DATA[dest].enemy.exist.push(i);
                        }
                    }
                }
            }
            toLoading(1, $("#map").attr("place"));
        }

        function create(creep){
            var newBtn = newElement("button", creep, creep, "btn btn-default moveBtn enemy", CREEP_DATA[creep].name);
            newBtn.onmouseover = function(){$("#info").empty();}
            newBtn.onclick = function(){
                BATTLE_OBJ.setEnemy(creep);
                toLoading(0.1, "battle");
            };
            $("#map").append(newBtn);
        }
    }
}
//================================================================================================

//种植功能
function reclaim(id){
    if(DISASTER_EFFECT && !BEGINNER_FLAG){
        alert("当前情况无法耕作。");
        return;
    }
    if(getSum(MAP_DATA[$("#map").attr("place")].resource)<FARM_CAP){
        var n = 0;
        var landName = "farmland" + n.toString();;
        while(MAP_DATA[$("#map").attr("place")].resource[landName] != undefined){
            n += 1;
            landName = "farmland" + n.toString();
        }
        caculate(BAG_DATA, id, -3);
        updateItem(id, $("#bag"));
        MAP_DATA[$("#map").attr("place")].resource[landName] = {name:"耕地"};
        var newObj = new mapObj($("#map").attr("place"));
        newObj.create();
        getSum(MAP_DATA[$("#map").attr("place")].resource);
    }
    else{
        caculate(BAG_DATA, id, 1);
        updateItem(id, $("#bag"));
    }
}

function plantInfo(btn, refItem){
    var seed = btn.id;
    var desc = "种植需求：";
    var flag = 1;
    for(var i in CROP_DATA[seed].require){
        var item = i;
        if(i == "water"){
            for(var j in BAG_DATA){
                if(j.toUpperCase().indexOf(i.toUpperCase())!=-1){
                    item = j;
                    break;
                }
            }
        }
        var own = BAG_DATA[item]==undefined?0:BAG_DATA[item];
        var color = "goodBuffName";
        if(own < CROP_DATA[seed].require[i]){
            color = "badBuffName";
            flag = 0;
        }
        desc += "<span class='" + color + "'>" + ITEM_DATA[i].name + "</span>" + CROP_DATA[seed].require[i];
    }
    btn.setAttribute("plantInfo", desc);

    if(flag && Math.ceil(realVal("energy"))>0 && PLAYER_STATUS.buff.overwork==undefined){
        btn.onclick = function(){
            $(".item").popover("destroy");
            plant(seed);
        };
    }
    else{
        btn.style = "cursor: not-allowed;";
        btn.innerHTML = "<s>" + btn.innerHTML + "</s>";
    }
}

function plant(seed){
    var farmlandName;
    for(var i in MAP_DATA[$("#map").attr("place")].resource){
        if(i.indexOf("farmland") == 0){
            farmlandName = i;
            break;
        }
    }
    if(farmlandName == undefined){
        return;
    }
    for(var i in CROP_DATA[seed].require){
        if(i == "water"){
            var waterFlag = 0;
            var waterSelect = "water";
            for(var j in BAG_DATA){
                if(j.toUpperCase().indexOf(i.toUpperCase())!=-1){
                    waterFlag = 1;
                    waterSelect = j;
                    break;
                }
            }
            if(waterFlag && BAG_DATA[waterSelect]>=CROP_DATA[seed].require[i]){
                caculate(BAG_DATA, waterSelect, -CROP_DATA[seed].require[i]);
                updateItem(waterSelect, $("#bag"));
            }
            else{
                return;
            }
        }
        else{
            if(BAG_DATA[i]!=undefined && BAG_DATA[i]>=CROP_DATA[seed].require[i]){
                caculate(BAG_DATA, i, -CROP_DATA[seed].require[i]);
                updateItem(i, $("#bag"));
            }
            else{
                return;
            }
        }
    }
    delete MAP_DATA[$("#map").attr("place")].resource[farmlandName];
    var n = 0;
    var seedName = seed + n.toString();;
    while(MAP_DATA[$("#map").attr("place")].resource[seedName] != undefined){
        n += 1;
        seedName = seed + n.toString();
    }
    MAP_DATA[$("#map").attr("place")].resource[seedName] = {
        name:clone(CROP_DATA[seed].name),
        get:clone(CROP_DATA[seed].get),
        refresh:clone(CROP_DATA[seed].refresh),
        max:1,
        value:0,
        energy:clone(CROP_DATA[seed].energy),
        crop:true,
        lastGrow:clone(sysTime)
    }
    toLoading(1, "farm", true);
}
//================================================================================================

//烹饪功能
function cookCheck(){
    $("#diet").empty();
    $("#cookAmount").hide();
    $("#cookBegin").attr("disabled", "disabled");
    for(var i in TOOL_DATA){
        if(TOOL_DATA[i].type[0]=="cook" && TOOL_DATA[i].show){
            var itemName = i;
            if(TOOL_DATA[i].turn != undefined){
                itemName = TOOL_DATA[i].turn;
            }
            var flag = 1;
            for(var j in TOOL_DATA[i].require){
                if(COOK_DATA[j]==undefined || COOK_DATA[j] < TOOL_DATA[i].require[j]){
                    flag = 0;
                    break;
                }
            }
            if(getSum(COOK_RESULT)>0 && COOK_RESULT[itemName]==undefined){
                flag = 0;
            }
            if(flag){
                var desc = "";
                var n = 0;
                for(var j in TOOL_DATA[i].require){
                    if(n > 0){
                        desc += " + ";
                    }
                    desc += "<span style='font-weight:bold;'>" + ITEM_DATA[j].name + TOOL_DATA[i].require[j] + "</span>";
                    n++;
                }
                desc += " = <span class='badBuffName'>" + ITEM_DATA[itemName].name + "</span>";
                $("#diet").html(desc);
                $("#cookAmount").attr("cook", i);
                $("#cookAmount").trigger("slider");
                $("#cookAmount").show();
                if(realVal("energy") > 0){
                    $("#cookBegin").removeAttr("disabled");
                }
                break;
            }
        }
    }
}
//================================================================================================

//交易功能
function tradeCreate(){
    $("#trade").empty();
    getBackBtn($("#trade"));
    $("#trade").append("<br><input type='checkbox' id='x10'/>X10&nbsp;&nbsp;<input type='checkbox' id='x100'/>X100");
    $("#trade").append("<div id='tradeGive' name='tradeGive'></div><br>");
    $("#trade").append("<div id='price'></div><br>");   
    $("#trade").append(newElement("button", "tradeBegin", "", "btn btn-default", "成交"));
    $("#trade").append("<div id='tradeGet' name='tradeGet'></div><br>");
    $("#trade").append("<div id='goods' name='goods'></div>");
    
    $("#tradeBegin").click(function(){
        clear(TRADE_GIVE);
        if(getSum(TRADE_GET) > 0){
            getItem(TRADE_GET);
        }
        clear(TRADE_GET);
        $("#tradeGive").empty();
        $("#tradeGet").empty();
        $("#price").empty();
        $("#tradeBegin").attr("disabled", "disabled");
        tradeCheck();
    });
    $("#tradeBegin").attr("disabled", "disabled");
    $("#x10").change(function(){
        if($("#x100").is(":checked")){
            $("#x100").removeAttr("checked");
        }
    });
    $("#x100").change(function(){
        if($("#x10").is(":checked")){
            $("#x10").removeAttr("checked");
        }
    });
    
    clear(TRADE_GIVE);

    if(getSum(TRADE_DATA) == 0){
        for(var i=1;i<=TRADE_LEVEL;i++){
            var sells = clone(TRADE_ITEM);
            for(var lv in sells){
                if(sells[lv] != i){
                    delete sells[lv];
                }
            }
            var kinds = TRADE_KINDS+1-i;
            kinds = kinds<=0?1:kinds;
            for(var j=0;j<kinds;j++){
                var a = Math.floor(Math.random()*getSum(sells));
                var b = Object.keys(sells);
                TRADE_DATA[b[a]] = Math.floor(Math.random()*90+10);
                if($.inArray(ITEM_DATA[b[a]].type, ["weapon", "head", "body", "foot", "quest"]) != -1){
                    TRADE_DATA[b[a]] = 1;
                }
                delete sells[b[a]];
            }
        }
    }
    for(var i in TRADE_DATA){
        var newObj = new itemObj(i, $("#goods"));
        newObj.create();
    }
    if(TRADE_GET.cap != undefined){
        delete TRADE_GET.cap;
    }
    for(var i in TRADE_GET){
        var newObj = new itemObj(i, $("#tradeGet"));
        newObj.create();
    }
}

function tradeCheck(){
    if(TRADE_GET.cap != undefined){
        delete TRADE_GET.cap;
    }
    $("#tradeBegin").attr("disabled", "disabled");
    var price = 0;
    for(var i in TRADE_GET){
        var sum = (ITEM_DATA[i].price==undefined?1:ITEM_DATA[i].price) * TRADE_GET[i];
        if(ITEM_DATA[i].durab != undefined){
            sum = Math.floor(sum/ITEM_DATA[i].durab);
        }
        price += sum;
    }
    var give = 0;
    for(var i in TRADE_GIVE){
        var sum = (ITEM_DATA[i].price==undefined?1:ITEM_DATA[i].price) * TRADE_GIVE[i];
        if(ITEM_DATA[i].durab != undefined){
            sum = Math.floor(sum/ITEM_DATA[i].durab);
        }
        give += sum;
    }
    var free = 1 - Math.log((realVal("charm")+1)/7.5);
    free = free<0.7 ? 0.7 : free;
    price = price*free - give;
    if(price > 0){
        $("#price").html("仍相差价值相当于 <span class='badBuffName'>" + Math.ceil(price/10) + "</span> 个瓶盖的物品");
    }
    else{
        give = TRADE_GIVE.cap!=undefined ? give-TRADE_GIVE.cap*10 : give;
        if(getSum(TRADE_GET)==0 && getSum(TRADE_GIVE)!=0 && give>0){
            free = free<0.85 ? 0.85 : free;
            var sellPrice = Math.floor(give/free/10);
            if(sellPrice == 0){
                $("#price").html("物品总价不足1瓶盖，商队不会收购");
                return;
            }
            $("#price").html("商队愿意用 <span class='badBuffName'>" + sellPrice + "</span> 个瓶盖收购你的货物");
            TRADE_GET.cap = sellPrice;
            $("#tradeBegin").removeAttr("disabled");
        }
        else{
            $("#price").html("任何物品均可用来交易，商人会折算成相应的瓶盖价值");
            if(getSum(TRADE_GET) > 0){
                $("#price").empty();
                $("#tradeBegin").removeAttr("disabled");
            }
        }
    }
}

function tradeGenerate(){
    if(MAP_DATA.outside.place.toTrade.show==undefined && (sysTime - MAP_DATA.outside.place.toTrade.lastShow)/1000/60/60>=36 && Math.random()*100<TRADE_RATE && DISASTER==""){
        MAP_DATA.outside.place.toTrade.show = true;
        MAP_DATA.outside.place.toTrade.lastShow = clone(sysTime);
    }

    if(MAP_DATA.outside.place.toTrade.show && (sysTime - MAP_DATA.outside.place.toTrade.lastShow)/1000/60/60>=10){
        delete MAP_DATA.outside.place.toTrade.show;
        clear(TRADE_DATA);
    }
}