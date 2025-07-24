var originTime = new Date("2241/2/1 07:07:00");
var sysTime = new Date("2241/2/1 07:05:00");
var baseTime = new Date("2241/2/1 00:00:00");
var EXCRETE_TIME = [clone(originTime), clone(originTime)];
var EXCRETE_INTERVAL = [20, 12];
var EXCRETE_FLAG = [false, false];
var EXCRETE_MAX = [36, 16];

var HUNGER_SPEED = 1/18;
var THIRST_SPEED = 1/12;
var WORK_TIME_COST = 2.5;
var WORK_SPEED = 1;
var COOK_SPEED = 1;
var MOVE_SPEED = 1;
var WORK_ENERGY_COST = 1/10;

var FPS = 20;
var STATUS_LIST = ["life", "hunger", "thirst", "energy", "san", "radiation"];
var SPECIAL_LIST = ["endurance", "perception", "charm", "luck", "agility"];
var EX_TAB = [];
var EX_RESOURCE = "";
var TRASH_FLAG = false;
var BATTLE_FLAG = false;
var RESEARCH_LIMIT = 0;
var RESEARCH_TIME = clone(originTime);
var LAST_RAD_TIME = clone(originTime);
var EXPLORE_FLAG = false;
var EXPLORE_TIME = 720;
var EXPLORE_RATE = 35;
var EXPLORE_LASTTIME = clone(originTime);
var EXPLORE_CHECK = clone(originTime);
var HAIR_AMOUNT = 100;
var DISASTER = "";
var DISASTER_EFFECT = false;
var DISASTER_CHECK = clone(originTime);
var DISASTER_TYPE = {
	sandstorm:{name:'沙尘暴', time:2880, last:1440},
	rain:{name:'辐射雨', time:4320, last:4320}
};
var DISASTER_TIME = 0;
var DISASTER_LAST = 0;
var DISASTER_LASTTIME = clone(originTime);
var DAILY_CHECK = clone(originTime);

var SAVE_KEY = "";
var SAVE_FAST = false;
var SAVE_LIST = ["PLAYER_STATUS", "BAG_CAP", "BOX_CAP", "BAG_DATA", "BOX_DATA", "sysTime", "EXCRETE_TIME", "EXCRETE_FLAG", "COOK_DATA", "COOK_RESULT", "TOILET_DATA", "MAP_DATA", "TOOL_FINISHED", "QUEST_FINISHED", "EXPLORE_DATA", "DISASTER", "DISASTER_TIME", "DISASTER_LAST", "DISASTER_LASTTIME", "BEGINNER_FLAG"];
var LOAD_FLAG = false;
var USERNAME = "";
var DEATH_FLAG = false;
var DEATH_FOR = "";
var TIMER_FLAG = false;
var BEGINNER_FLAG = false;
var TAPHOLD_FLAG = false;
var DAYNIGHT_TIMES = 0;

//================================================================================================

//获取物品所在容器
function getHolder(belong){
	switch(belong.getAttribute("name")){
		case "bag": return BAG_DATA;break;
		case "box": return BOX_DATA;break;
		case "workbench": if($("#workbench").attr("mode")=="cook"){
			return COOK_DATA;
		}
		else{
			return TEMP_DATA;
		}
		break;
		case "stuff": return COOK_DATA;break;
		case "cookResult": return COOK_RESULT;break;
		case "toiletData": return TOILET_DATA;break;
		case "goods": return TRADE_DATA;break;
		case "tradeGet": return TRADE_GET;break;
		case "tradeGive": return TRADE_GIVE;break;
		default : return TEMP_DATA;break;
	}
}

function getBackBtn(layer){
	var newBtn = newElement("button", "", "", "btn btn-default backBtn", "返回");
	newBtn.onclick = function(){
		$(".item").popover("destroy");
		if(TRASH_FLAG){
			if(getSum(TEMP_DATA)>0 && MAP_DATA[EX_TAB[EX_TAB.length-1]]!=undefined && MAP_DATA[EX_TAB[EX_TAB.length-1]].trash!=undefined){
				for(var i in TEMP_DATA){
					if(MAP_DATA[EX_TAB[EX_TAB.length-1]].trash[i] != undefined){
						caculate(MAP_DATA[EX_TAB[EX_TAB.length-1]].trash[i], "amount", TEMP_DATA[i]);
					}
				}
			}
			TRASH_FLAG = false;
		}
		else{
			if(getSum(TEMP_DATA)>0 && $(".tab-pane.active").attr("id")=="temp" && $.inArray($("#temp").attr("mode"), ["excrete", "pee", "poo", "spew"])==-1){
				if(!confirm("仍有物品未拾取，确定返回？")){
					return;
				}
			}
			if(getSum(TRADE_GIVE)>0 && $(".tab-pane.active").attr("id")=="trade"){
				if(!confirm("请取回你展示在商队面前的物品，难道你想免费送给他们吗？")){
					return;
				}
			}
		}
		for(var i in TEMP_DATA){
			if(ITEM_DATA[i].important){
				alert("存在重要物品，不可丢弃，请取回。");
				return;
			}
		}
		clear(TEMP_DATA);
		EX_RESOURCE = "";
		toLoading(0.1, EX_TAB[EX_TAB.length-1], "back");
	}
	layer.append(newBtn);
	layer.append("<br>");
}

//loading过渡画面
function toLoading(time, dest, stay, callback){
	if(LOAD_FLAG || DEATH_FLAG){
		return;
	}
	//进出家时自动保存
	var autoflag = false;
	if(dest=="outside" && $(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")=="home"){
		autoflag = true;
		if(DISASTER_EFFECT && (sysTime-DISASTER_LASTTIME)/1000/60>=DISASTER_TIME){
			getBuff(DISASTER);
		}
	}
	if(dest=="home" && $(".tab-pane.active").attr("id")=="map"){
		autoflag = true;
		removeBuff("sandstorm");
		removeBuff("rain");
	}
	if(autoflag){
		autosave();
	}
	//若已手动保存，回家时生成快速保存按钮
	if(SAVE_FAST && SAVE_KEY!="" && dest=="home" && $("#fastsave").attr("id")==undefined){
		$("#pauseBtn").before(newElement("button", "fastsave", "", "btn btn-default", "快速保存(F6)"));
		$("#fastsave").click(function(){$("#fastsave").html("保存中...");$("#fastsave").attr("disabled", "disabled");save(true,SAVE_KEY);});
	}
	else{
		if($("#fastsave").attr("id") != undefined){
			$("#fastsave").remove();
		}
	}
	
	$("#info").empty();
	$(".item").popover("destroy");
	if(stay == null){
		getNowTab();
	}
	else if(stay == "back"){
		EX_TAB.pop();
	}
	if(EX_TAB[EX_TAB.length-1]==EX_TAB[EX_TAB.length-2]){
		EX_TAB.pop();
	}
	//显示遮罩层
	$("#overlay").height(document.body.clientHeight);
	$("#overlay").width(document.body.clientWidth);
	$("#overlay").fadeTo(100, 0);

	if(time >= 0.5){
		//转到loading画面，播放完毕后转到指定标签页
		$("#tablist a[href='#loading']").tab("show");
		var loadDiv = document.createElement("div");
		loadDiv.className = "loadDiv";
		var bar = document.createElement("div");
		bar.className = "loadingBar";
		loadDiv.appendChild(bar);
		$("#loading").append(loadDiv);
		$("#loading div div").animate({width: "100%"}, time * 1000, toNext);

		setTimeout(generate, 300);
	}
	else{
		generate();
		toNext();
	}

    //目标标签页生成
    function generate(){
    	var newObj;
    	switch(dest){
    		case "excrete":case "spew": case "pickUp": case "resource": case "trash": case "output":
    		newObj = new tempObj(dest);
    		newObj.create();
    		break;
    		case "poo":
    		updateStatus("hunger", -8);
    		EXCRETE_FLAG[0] = false;
    		EXCRETE_TIME[0] = clone(sysTime);
    		removeBuff("shitReady");
    		if(EX_TAB[EX_TAB.length-1] == "toilet"){
    			TOILET_DATA.shit = TOILET_DATA.shit==undefined?0:TOILET_DATA.shit;
    			caculate(TOILET_DATA, "shit", 4);
    			newObj = new mapObj("toilet");
    			newObj.create();
    		}
    		else{
    			clear(TEMP_DATA);
    			TEMP_DATA.shit = 4;
    			newObj = new tempObj(dest);
    			newObj.create();
    		}
    		break;
    		case "pee":
    		updateStatus("thirst", -5);
    		EXCRETE_FLAG[1] = false;
    		EXCRETE_TIME[1] = clone(sysTime);
    		removeBuff("urineReady");
    		if(EX_TAB[EX_TAB.length-1] == "toilet"){
    			TOILET_DATA.urine = TOILET_DATA.urine==undefined?0:TOILET_DATA.urine;
    			caculate(TOILET_DATA, "urine", 5);
    			newObj = new mapObj("toilet");
    			newObj.create();
    		}
    		else{
    			clear(TEMP_DATA);
    			TEMP_DATA.urine = 5;
    			newObj = new tempObj(dest);
    			newObj.create();
    		}
    		break;
    		case "work": case "tech": case "lab": case "handwork": case "bed": case "cook": case "forge":case "filter": 
    		case "train": 
    		newObj = new workbenchObj(dest);
    		newObj.create();
    		break;
    		case "battle":
    		BATTLE_OBJ.create();
    		BATTLE_OBJ.play();
    		break;
    		case "quest":
    		break;
    		case "trade":
    		tradeCreate();
    		tradeCheck();
    		break;
    		case "box":
    		if($("#box .item").length != getSum(BOX_DATA)){
    			for(var i in BOX_DATA){
    				if($("#box .item[id='"+i+"']").attr("id") != undefined){
    					$("#box .item[id='"+i+"']").remove();
    				}
    				var newItem = new itemObj(i, $("#box"));
    				newItem.create();
    			}
    		}
    		break;
    		default:
    		if($("#map").attr("place") != dest){
    			var buff = MAP_DATA[$("#map").attr("place")].buff;
    			if(MAP_DATA[dest].buff==undefined || MAP_DATA[dest].buff != buff){
    				removeBuff(buff);
    				if(PLAYER_STATUS.buffPause[buff] != undefined){
    					delete PLAYER_STATUS.buffPause[buff];
    				}
    			}
    		}
    		if(dest == "outside"){
    			tradeGenerate();
    		}
    		newObj = new mapObj(dest);
    		newObj.create();
    		break;
    	}
    }

    function toNext(){
    	var nextTab = $(".tab-pane.active").attr("id");
    	var nextName = "";
    	switch(dest){
    		case "work": case "tech": case "lab": case "handwork": case "bed": case "cook": case "forge":case "filter": 
    		case "train": 
    		nextTab = "workbench";
    		nextName = WORK_TAB_NAME[dest];
    		break;
    		case "battle":
    		nextTab = "battle";
    		nextName = "战斗";
    		break;
    		case "pickUp": case "output":
    		nextTab = "temp";
    		nextName = "拾取";
    		break;
    		case "excrete":
    		nextTab = "temp";
    		nextName = "强制排泄(噫~)";
    		break;
    		case "spew":
    		nextTab = "temp";
    		nextName = "呕吐";
    		break;
    		case "poo": case "pee":
    		if(EX_TAB[EX_TAB.length-1] == "toilet"){
    			EX_TAB.pop();
    			nextTab = "map";
    			var newObj = new mapObj("toilet");
    			nextName = newObj.name;
    		}
    		else{
    			nextTab = "temp";
    			nextName = "排泄物";
    		}
    		break;
    		case "resource":
    		nextTab = "temp";
    		nextName = "获取资源";
    		break;
    		case "trash":
    		nextTab = "temp";
    		nextName = "垃圾";
    		TRASH_FLAG = true;
    		break;
    		case "quest":
    		nextTab = "quest";
    		break;
    		case "trade":
    		nextTab = "trade";
    		nextName = "旅行商队";
    		break;
    		case "box":
    		nextTab = "box";
    		nextName = "箱子<span id='boxCap'></span>";
    		break;
    		default:
    		nextTab = "map";
    		var newObj = new mapObj(dest);
    		nextName = newObj.name;
    		if(BATTLE_ATONCE){
    			BATTLE_ATONCE = false;
    			nextTab = "battle";
    			nextName = "战斗";
    			BATTLE_OBJ.create();
    			BATTLE_OBJ.play();
    		}
    		break;
    	}

    	if(nextTab != $(".tab-pane.active").attr("id")){
    		$("#tablist a[href='#"+nextTab+"']").tab("show");
    	}
    	if(nextName != ""){
    		$("#mainTitle").html(nextName);
    		if(dest == "farm"){
    			getSum(MAP_DATA.farm.resource);
    		}
    		if(dest == "box"){
    			getSum(BOX_DATA);
    		}
    	}
    	$("#overlay").fadeOut(300, remove);
    }

    function remove(){
    	$("#loading").empty();
    	if(callback != null){
    		callback();
    	}
    }
}

function getNowTab(){
	var activeTab = $(".tab-pane.active").attr("id");
	if($.inArray(activeTab, ["map", "workbench", "box"]) != -1){
		if(activeTab == "map"){
			EX_TAB.push($("#map").attr("place"));
		}
		else if(activeTab == "workbench"){
			EX_TAB.push($("#workbench").attr("mode"));
		}
		else{
			EX_TAB.push($(".tab-pane.active").attr("id"));
		}
	}
}


//物品计数
function getSum(belong){
	var sum = Object.getOwnPropertyNames(belong).length;
	switch(belong){
		case BAG_DATA:
		for(var i in BAG_DATA){
			if(ITEM_DATA[i].volume){
				sum -= 1;
			}
		}
		$("#bagCap").text(sum+"/"+BAG_CAP);
		break;
		case BOX_DATA:$("#boxCap").text(sum+"/"+BOX_CAP);break;
		case MAP_DATA.farm.resource:$("#farmCap").text(sum+"/"+FARM_CAP);break;
	}
	return sum;
}

function autosort(holder){
	$(".item").popover("destroy");
	var temp = [];
	var order = ["food", "material", "tool", "quest", "foot", "body", "head", "ammo", "weapon"];
	var layer = holder==BAG_DATA?$("#bag"):$("#box");
	for(var i in holder){
		var index = $.inArray(ITEM_DATA[i].type, order);
		for(var j in PLAYER_STATUS.equip){
			if(PLAYER_STATUS.equip[j]==i && holder==BAG_DATA){
				index = 99;
				break;
			}
		}
		temp.push({id:i, order:index});
	}
	function compare(name,minor){
	    return function(o,p){
	        var a,b;
	        if(o && p && typeof o === 'object' && typeof p ==='object'){
	            a = o[name];
	            b = p[name];
	            if(a === b){
	                return typeof minor === 'function' ? minor(o,p):0;
	            }
	            if(typeof a === typeof b){
	                return a > b ? -1:1;
	            }
	            return typeof a > typeof b ? -1 : 1;
	        }
	    }
	}
	temp.sort(compare("order", compare("id")));
	layer.find(".item").remove();
	for(var i in temp){
		var newObj = new itemObj(temp[i].id, layer);
		newObj.create();
	}
}

function min(array, mode){
	var a = 9999999;
	var b = "";
	for(var i in array){
		var own = (BAG_DATA[i]==undefined?0:BAG_DATA[i]) + (BOX_DATA[i]==undefined?0:BOX_DATA[i]);
		if(mode == "cook"){
			own = COOK_DATA[i];
		}
		if(own/array[i] < a){
			a = own/array[i];
			b = i;
		}
	}
	return [a, b];
}

//时钟更新
function updateSysClock(min, sec, flag, stepval){
	var step = stepval;
	sysTime = new Date(sysTime.getTime() + min*60*1000 + sec*1000);
	var hh = (sysTime.getHours()<10?"0":"") + sysTime.getHours();
	var mm = (sysTime.getMinutes()<10?"0":"") + sysTime.getMinutes();
	var day = (sysTime - baseTime)/1000/60/60/24 + 1;
	var countdown;
	if(DISASTER!="" && !DISASTER_EFFECT){
		countdown = DISASTER_TIME - (sysTime-DISASTER_LASTTIME)/1000/60;
	}
	if(DISASTER_EFFECT){
		$("#countdownType").html("持续时间");
		countdown = DISASTER_LAST + DISASTER_TIME - (sysTime-DISASTER_LASTTIME)/1000/60;
	}
	if(step == 2){
		$("#clock").html("第 "+Math.floor(day)+" 日  "+hh+":"+mm);
		if($("#countdown").attr("id") != undefined){
	    	countdown = countdown>=60 ? (Math.floor(countdown/60)+"小时"+Math.floor(countdown%60)+"分钟") : (Math.floor(countdown)+"分钟");
	    	$("#countdown").html(countdown);
	    } 
		step = 0;
	}
	
    //颜色变化
    /*
    var hhNum = parseInt(hh);
    var mmNum = parseInt(mm);
    if(hhNum>=18 && hhNum<=23 || hhNum<3){
    	if(hhNum<3){
    		hhNum = 23 + hhNum + 1;
    	}
    	var background = 255 - ((hhNum-18)*60 + mmNum);
    	background = background>=40 && background<=60 ? 60 : background;
    	background = background<0 ? 0 : background;
    	var color = 255 - background;
    	colorChange($("#background"), [background,background,background+20>255 ? 255 : background], "background-color");
    	colorChange($("#footer"), [background,background,background+20>255 ? 255 : background], "background-color");
    }
    else if(hhNum>=3 && hhNum<=8){
    	var background = (hhNum-3)*60 + mmNum;
    	background = background>=40 && background<=60 ? 60 : background;
    	background = background>255 ? 255 : background;
    	var color = 255 - background;
    	colorChange($("#background"), [background,background,background+20>255 ? 255 : background], "background-color");
    	colorChange($("#footer"), [background,background,background+20>255 ? 255 : background], "background-color");
    }*/

    if(TIMER_FLAG && flag){
    	setTimeout(function(){updateSysClock(1, 15, true, step+1);}, 500);
    }
};

//状态值改变
function updateStatus(status, value, buffer){
	if(LOAD_FLAG){
		return;
	}
	if(value != null){
		if(buffer){
			if(PLAYER_STATUS[status].buffer == undefined){
				PLAYER_STATUS[status].buffer = 0;
			}
			caculate(PLAYER_STATUS[status], "buffer", parseFloat(value));
		}
		else{
			caculate(PLAYER_STATUS[status], "value", parseFloat(value));
		}
		//实时属性影响
		switch(status){
			case "life":
			if(realVal(status)<=0 && !DEATH_FLAG){
				death();
			}
			break;
			case "hunger":
			hungerChk();
			break;
			case "thirst":
			thirstChk();
			break;
			case "energy":
			if(PLAYER_STATUS.energy.value<-10){
				getBuff("overwork");
			}
			break;
			case "san":
			sanChk();
			break;
			case "radiation":
			if(value < 0){
				if(PLAYER_STATUS.radiation.value <= 75){
					removeBuff("longleg");
					removeBuff("eagle");
				}
				if(PLAYER_STATUS.radiation.value <= 40){
					removeBuff("hulk");
					removeBuff("stonelike");
				}
				if(PLAYER_STATUS.radiation.value <= 0){
					removeBuff("ugly");
					removeBuff("slow_1");
					removeBuff("hairlose");
				}
			}
			break;
			case "tech":
			var n = 0;
			var newDesc = "<span style='color:#000;'>";
			for(var i in TOOL_DATA){
				if(TOOL_DATA[i].tech!=undefined && PLAYER_STATUS.tech.value>=TOOL_DATA[i].tech && TOOL_DATA[i].show==undefined && $.inArray(i, TOOL_FINISHED)==-1){
					if(TOOL_DATA[i].level!=undefined && TOOL_DATA[i].level>TOOL_LEVEL[TOOL_DATA[i].type[0]]){
						continue;
					}
					if(n <= 4){
						if(n > 0){
							newDesc += "、";
						}
						newDesc += "[" + TOOL_DATA[i].name + "]";
					}
					TOOL_DATA[i].show = true;
					TOOL_DATA[i].newflag = true;
					n += 1;
				}
			}
			newDesc += "</span>";
			if(n > 0){
				showMsg("技术提升，解锁了 "+newDesc+" 等新的制造物和科技，请留意查看。")
			}
			break;
		}

		if(PLAYER_STATUS[status].max!=undefined && PLAYER_STATUS[status].value>PLAYER_STATUS[status].max){
			PLAYER_STATUS[status].value = clone(PLAYER_STATUS[status].max);
		}
		if(PLAYER_STATUS[status].min!=undefined && PLAYER_STATUS[status].value<PLAYER_STATUS[status].min){
			PLAYER_STATUS[status].value = clone(PLAYER_STATUS[status].min);
		}
	}
	if($.inArray(status, STATUS_LIST)==-1 || status=="radiation"){
		gameSet();
	}
	var newObj = new statusObj(status);
	newObj.update();
}

function nextProgress(status){
	return (PLAYER_STATUS[status].value+1)*PLAYER_STATUS[status].value*5+50;
}
function updateProgress(status, value){
	if(LOAD_FLAG){
		return;
	}
	if(value!=null && PLAYER_STATUS[status].progerss!=undefined){
		caculate(PLAYER_STATUS[status], "progerss", value);
		if(PLAYER_STATUS[status].progerss >= nextProgress(status)){
			caculate(PLAYER_STATUS[status], "progerss", -nextProgress(status));
			updateStatus(status, 1);
		}
	}
}

//物品数量改变
function updateItem(id, belong){
	var layer = belong[0].getAttribute("name");
	var holder = getHolder(belong[0]);
	var name = ITEM_DATA[id].name;
	for(var i in PLAYER_STATUS.equip){
		if(PLAYER_STATUS.equip[i]==id && layer=="bag"){
			name = "<span class='noneBuffName'>[" + name + "]</span>";
			break;
		}
	}
	if(ITEM_DATA[id].durab != undefined){
		var percent = holder[id] % ITEM_DATA[id].durab / ITEM_DATA[id].durab * 100;
		percent = percent==0?100:percent;
		var sum = Math.ceil(holder[id] / ITEM_DATA[id].durab);
		var amount = "<div class='durabDiv'><div class='loadingBar' style='width:"+percent+"%;'></div></div>"
		+ "<br>" + sum;
		belong.find(".item[id = "+id+"]").html(name + amount);
	}
	else{
		var volume = "";
		if(ITEM_DATA[id].volume!=undefined && layer=="bag"){
			volume = "/";
			volume = volume + (Math.ceil(holder[id]/KETTLE_VOLUME) * KETTLE_VOLUME).toString();
		}
		belong.find(".item[id = "+id+"]").html(name + "<br>" + holder[id] + volume);
	}
	if(holder[id] <= 0){
		for(var i in PLAYER_STATUS.equip){
			if(PLAYER_STATUS.equip[i]==id && layer=="bag"){
				var itemType = ITEM_DATA[id].attack!=undefined?"weapon":ITEM_DATA[id].type;
				PLAYER_STATUS.equip[itemType] = "";
				if(ITEM_DATA[id].attack != undefined){
					updateStatus("attack", -ITEM_DATA[id].attack, true);
				}
				if($.inArray(ITEM_DATA[id].type, ["head", "body", "foot"]) != -1){
					if(ITEM_DATA[id].buffUse != undefined){
						removeBuff(ITEM_DATA[id].buffUse);
					}
				}
				if(ITEM_DATA[id].effect != undefined){
					for(var i in ITEM_DATA[id].effect){
						updateStatus(i, -ITEM_DATA[id].effect[i], true);
					}
				}
				if($(".tab-pane.active").attr("id") == "battle"){
					BATTLE_OBJ.resetPlayer();
					BATTLE_OBJ.setValue();
				}
			}
			break;
		}
		$(".item").popover("destroy");
		$("#info").empty();
		belong.find(".item[id = "+id+"]").remove();
		if(ITEM_DATA[id].buffPick!=undefined && layer=="bag"){
			removeBuff(ITEM_DATA[id].buffPick);
			if(PLAYER_STATUS.buffPause[ITEM_DATA[id].buffPick]){
				delete PLAYER_STATUS.buffPause[ITEM_DATA[id].buffPick];
			}
		}
		delete holder[id];
	}
	NaNcheck(holder);
	getSum(holder);
}

//简化生成新控件
function newElement(type, id, name, className, innerHTML){
	var newElement = document.createElement(type);
	newElement.id = id;
	newElement.setAttribute("name", name);
	newElement.className = className;
	newElement.innerHTML = innerHTML;
	return newElement;
}

//全局计时器暂停
function pauseGame(){
	TIMER_FLAG = false;
}

//全局计时器重启
function resumeGame(){
	if(DEATH_FLAG || TIMER_FLAG){
		return;
	}
	TIMER_FLAG = true;
	updateSysClock(1, 15, true, 1);
	tick();
}

//buff功能
function getBuff(buff){
	var flag = 1;
	if(PLAYER_STATUS.buff[buff] == undefined){
		for(var i in PLAYER_STATUS.buff){
			if(BUFF_DATA[i].clearBuff!=undefined && buff.indexOf(BUFF_DATA[i].clearBuff)!=-1){
				flag = 0;
				PLAYER_STATUS.buffPause[buff] = true;
			}
		}
		if(flag){
			PLAYER_STATUS.buff[buff] = [clone(sysTime), clone(sysTime)];
			if(BUFF_DATA[buff].cost){
				PLAYER_STATUS.buff[buff][1] = new Date(sysTime.getTime() - BUFF_DATA[buff].interval*1000*60);
			}
			if(BUFF_DATA[buff].name != undefined){
				var info = "<br><span class='"+BUFF_DATA[buff].type+"BuffName'>"+BUFF_DATA[buff].name+"</span>："+BUFF_DATA[buff].desc;
				if(PLAYER_STATUS[BUFF_DATA[buff].on].desc.indexOf(info) < 0){
					PLAYER_STATUS[BUFF_DATA[buff].on].desc += info;
				}
			}
			//临时效果首次生效
			if(BUFF_DATA[buff].effect!=undefined && (BUFF_DATA[buff].temp || BUFF_DATA[buff].atonce)){
				var buffer = BUFF_DATA[buff].temp ? true : null;
				for(var i in BUFF_DATA[buff].effect){
					if(BUFF_DATA[buff].effect[i].percent != undefined){
						var status = BUFF_DATA[buff].effect[i].type;
						var value = realVal(i);
						if(status != i){
							value = realVal(status);
						}
						value *= BUFF_DATA[buff].effect[i].percent;
						updateStatus(i, value, buffer);
					}
					else{
						updateStatus(i, BUFF_DATA[buff].effect[i], buffer);
					}
				}
			}
			if(BUFF_DATA[buff].clearBuff != undefined){
				for(var i in PLAYER_STATUS.buff){
					if(i.indexOf(BUFF_DATA[buff].clearBuff) != -1){
						removeBuff(i);
					}
				}
			}
			if(BUFF_DATA[buff].on != undefined){
				updateStatus(BUFF_DATA[buff].on);
			}
		}
	}
}
function removeBuff(buff){
	if(PLAYER_STATUS.buff[buff] != undefined){
		if(BUFF_DATA[buff].name != undefined){
			var info = "<br><span class='"+BUFF_DATA[buff].type+"BuffName'>"+BUFF_DATA[buff].name+"</span>："+BUFF_DATA[buff].desc;
			var str = PLAYER_STATUS[BUFF_DATA[buff].on].desc;
			PLAYER_STATUS[BUFF_DATA[buff].on].desc = str.replace(info, "");
		}
		if(BUFF_DATA[buff].effect!=undefined && BUFF_DATA[buff].temp){
			var a = Object.keys(BUFF_DATA[buff].effect);
			var times = BUFF_DATA[buff].interval!=undefined ? PLAYER_STATUS.buff[buff][2]+1 : 1;
			for(var j=0;j<times;j++){
				for(var i=a.length-1;i>-1;i--){
					if(BUFF_DATA[buff].effect[a[i]].percent != undefined){
						var status = BUFF_DATA[buff].effect[a[i]].type;
						var value = realVal(a[i]) * (BUFF_DATA[buff].effect[a[i]].percent/(1+BUFF_DATA[buff].effect[a[i]].percent));
						if(status != a[i]){
							value = realVal(status) * BUFF_DATA[buff].effect[a[i]].percent;
						}
						updateStatus(a[i], -value, true);
					}
					else{
						updateStatus(a[i], -BUFF_DATA[buff].effect[a[i]], true);
					}
				}
			}
			//脱下装备
			for(var i in PLAYER_STATUS.equip){
				if(PLAYER_STATUS.equip[i]!="" && ITEM_DATA[PLAYER_STATUS.equip[i]].require != undefined){
					for(var j in ITEM_DATA[PLAYER_STATUS.equip[i]].require){
						if(realVal(j) < ITEM_DATA[PLAYER_STATUS.equip[i]].require[j]){
							$("#bag .item[id='"+PLAYER_STATUS.equip[i]+"']").trigger("selfUnload");
							break;
						}
					}
				}
			}
		}
		delete PLAYER_STATUS.buff[buff];
		if(BUFF_DATA[buff].clearBuff != undefined){
			for(var i in PLAYER_STATUS.buffPause){
				if(PLAYER_STATUS.buffPause[i] && i.indexOf(BUFF_DATA[buff].clearBuff)!=-1){
					delete PLAYER_STATUS.buffPause[i];
					getBuff(i);
				}
			}
		}
	if(BUFF_DATA[buff].on != undefined){
			updateStatus(BUFF_DATA[buff].on);
		}
	}
}

function showMsg(msg, time){
	if($("#message") != undefined){
		$("#message").remove();
	}
	var newDiv = newElement("div", "message", "", "alert alert-info alert-dismissible message", "");
	newDiv.setAttribute("role", "alert");
	var newBtn = newElement("button", "", "", "close", "<span aria-hidden='true'>&times;</span>");
	newBtn.setAttribute("data-dismiss", "alert");
	newBtn.setAttribute("aria-label", "Close");
	newDiv.appendChild(newBtn);
	newDiv.innerHTML += msg;
	$("#background").append(newDiv);
	$("#message").hide();
	var delay = time==undefined ? 5000 : time;
	$("#message").fadeIn(500, function(){$("#message").addClass("fade in");}).delay(delay).fadeOut(500, closeMsg);
	$("#message").offset({left:$("#info").offset().left, top:$("#info").offset().top});

	function closeMsg(){
		if($("#message") != undefined){
			$("#message").alert("close");
		}
	}
}

function showAD(pos){
	var className = "alert alert-info alert-dismissible";
	if(pos != null){
		className += " " + pos;
	}
	var newDiv = newElement("div", "adsense", "", className, "");
	newDiv.setAttribute("role", "alert");
	var newBtn = newElement("button", "", "", "close", "<span aria-hidden='true'>&times;</span>");
	newBtn.setAttribute("data-dismiss", "alert");
	newBtn.setAttribute("aria-label", "Close");
	newDiv.appendChild(newBtn);
	newDiv.innerHTML += GGAD;
	return newDiv;
}

//快捷键
//E:69, W:87, D:68, F:70, S:83, A:65, Ctrl:17, Shift:16, F6:117
$(document).keyup(function(e){
	var id = document.activeElement.id;
	var layer = document.activeElement.parentNode.id;
	if(DEATH_FLAG || $(".tab-pane.active").attr("id")=="loading"){
		return;
	}
	//物品快捷键
	var keycode = {
		"49":"(1)",
		"50":"(2)",
		"51":"(3)",
		"52":"(4)",
		"53":"(5)",
		"54":"(6)",
		"65":"(A)",
		"67":"(C)",
		"69":"(E)",
		"68":"(D)",
		"70":"(F)",
		"83":"(S)",
		"87":"(W)",
	}
	if(keycode[e.which] != undefined){
		$(".popover-title .btn").each(function(){
			if($(this).html().indexOf(keycode[e.which])!=-1 && $(this).attr("disabled")==undefined){
				$(this).click();
				return;
			}
		});
		//战斗快捷键
		if(BATTLE_FLAG){
			if(e.which==65 && $("#attack").attr("disabled")==undefined){
				$("#attack").click();
			}
			if(e.which==68 && $("#defence").attr("disabled")==undefined){
				$("#defence").click();
			}
			if(e.which==87 && $("#forward").attr("disabled")==undefined){
				$("#forward").click();
			}
			if(e.which==83 && $("#backward").attr("disabled")==undefined){
				$("#backward").click();
			}
		}
	}

	//快速保存
	if(e.which==117 && $("#fastsave").attr("id")!=undefined){
		SAVE_FAST = false;
		$("#fastsave").html("保存中...");$("#fastsave").attr("disabled", "disabled");
		save(true, SAVE_KEY);
	}
});

function placeDesc(data){
	var result = "";
	if(data.resource!=undefined && getSum(data.resource)>0){
		result += "资源：";
		for(var i in data.resource){
			if(data.resource[i].hide){
				continue;
			}
			result += "[" + data.resource[i].name + "] ";
		}
		result += "<br>";
	}
	if(data.trash!=undefined && getSum(data.trash)>0){
		result += "垃圾：";
		for(var i in data.trash){
			result += "[" + ITEM_DATA[i].name + "] ";
		}
		result += "<br>";
	}
	if(data.enemy!=undefined && (data.enemy.normal!=undefined || data.enemy.boss!=undefined)){
		result += "生物：";
		for(var i in data.enemy.normal){
			result += "[" + CREEP_DATA[i].name.replace("<br>", "") + "] ";
		}
		if(data.enemy.boss != undefined){
			for(var j in data.enemy.boss){
				//纠错功能--boss版本变更
				if(j=="name" || j=="rate"){
					continue;
				}
				result += "[" + CREEP_DATA[j].name.replace("<br>", "") + "] ";
			}
		}
	}
	if(data.place!=undefined && getSum(data.place)>0){
		for(var i in data.place){
			if(data.place[i].enemy){
				result += "[" + CREEP_DATA[i].name.replace("<br>", "") + "] ";
			}
		}
	}
	return result;
}

function amountDesc(a){
	var b = ["几个", "少量", "一般", "很多", "大量", "丰富"];
	for(var i in b){
		if(a <= i*15+5){
			return b[i];
		}
	}
	return b[5];
}

function densityDesc(a){
	var density = (MAP_DATA[a].enemy.get[1]+MAP_DATA[a].enemy.get[0])/2;
	var b = ["几个", "稀疏", "中等", "较多", "密集", "海量！"];
	for(var i in b){
		if(density <= i+1){
			return b[i];
		}
	}
	return b[5];
}

function chanceDesc(a){
	var b = ["极低", "很低", "较低", "一般", "较高", "很高", "极高", "必然"];
	for(var i in b){
		if(a < i*15+10){
			return b[i];
		}
	}
	return b[7];
}

//值传递
function clone(a){
	var b;
	switch(typeof a){
		case "object":
		if(a instanceof Array){
			b = [];
			for(var i in a){
				b.push(clone(a[i]));
			}
		}
		else if(a instanceof Date){
			b = new Date(a);
		}
		else{
			b = {};
			for(var i in a){
				b[i] = clone(a[i]);
			}
		}
		break;
		case "number":
		b = a + 0;
		break;
		case "string":
		b = a + "";
		break;
		case "undefined":
		break;
		default:
		b = a;
	}
	return b;
}

function clear(a){
	for(var i in a){
		delete a[i];
	}
}

function caculate(data, name, value){
	if(data[name]!=undefined && !isNaN(data[name]) && value!=undefined && !isNaN(value)){
		data[name] += value;
	}
}

function realVal(status){
	var val = clone(PLAYER_STATUS[status].value);
	if(PLAYER_STATUS[status].buffer != undefined){
		val += PLAYER_STATUS[status].buffer;
	}
	if(PLAYER_STATUS[status].max!=undefined && val>PLAYER_STATUS[status].max){
		val = clone(PLAYER_STATUS[status].max);
	}
	if(PLAYER_STATUS[status].min!=undefined && val<PLAYER_STATUS[status].min){
		val = clone(PLAYER_STATUS[status].min);
	}
	return val;
}

//变色
function colorChange(obj, toColor, type, step, aniFlag){
    var nowColor = obj.css(type);
    if(nowColor == undefined){
        return;
    }
    nowColor = nowColor.replace("rgb(","").replace(")","").split(",");
    var flag = 0;
    for(var i in nowColor){
        nowColor[i] = parseInt(nowColor[i]);
        if(nowColor[i] != toColor[i]){
            flag = 1;
            if(step == null){
            	nowColor[i] = toColor[i];
            }
            else{
            	nowColor[i] += toColor[i]>nowColor[i] ? (toColor[i]-nowColor[i]<step ? toColor[i]-nowColor[i] : step) : (toColor[i]-nowColor[i]>-step ? toColor[i]-nowColor[i] : -step);
        	}
        }
    }
    obj.css(type, "rgb("+nowColor.toString().replace("[","").replace("]","")+")");
    if(aniFlag && flag){
        setTimeout(function(){colorChange(obj, toColor, type, step, aniFlag);}, 30);
    }
}

//手机端长按事件
function taphold(obj, func){
	var taptime;
	obj.ontouchstart = function(){
		taptime = setTimeout(function(){
			TAPHOLD_FLAG = true;
			func.call(obj);
		}, 500);
	}

	obj.ontouchend = function(){
		TAPHOLD_FLAG = false;
		clearTimeout(taptime);
	}

	obj.ontouchmove = function(){
		TAPHOLD_FLAG = false;
		clearTimeout(taptime);
	}

	obj.ontouchcancel = function(){
		TAPHOLD_FLAG = false;
		clearTimeout(taptime);
	}
}

function randomUnicode(){
	var result;
	eval("result = '\\u" + Math.floor(Math.random() * 9664 + 26159).toString(16) + "';")
	return result;
}
//================================================================================================

//S/L


function saveData(){
	try{
		var data = {};	
		for(var i in SAVE_LIST){
			data[SAVE_LIST[i]] = eval("clone(" + SAVE_LIST[i] + ");");
		}
		for(var i in data.PLAYER_STATUS){
			for(var j in data.PLAYER_STATUS[i]){
				if(j=="value" && Math.ceil(data.PLAYER_STATUS[i][j])!==data.PLAYER_STATUS[i][j] && $.inArray(i, ["critical", "critimes", "dodge", "hitrate", "escape", "tech"])==-1){
					data.PLAYER_STATUS[i][j] = Math.ceil(data.PLAYER_STATUS[i][j]);
				}
				if($.inArray(j, ["name", "desc", "percent", "overflow"]) != -1){
					delete data.PLAYER_STATUS[i][j];
				}
			}
		}
		for(var i in data.MAP_DATA){
			if(EXPLORE_DATA[i] != undefined){
				continue;
			}
			for(var j in data.MAP_DATA[i]){
				if(j!="resource" && j!="trash" && j!="enemy"){
					if(j!="place" || i!="outside"){
						delete data.MAP_DATA[i][j];
					}
				}
				for(var k in data.MAP_DATA[i][j]){
					if(j=="place" && i=="outside" && EXPLORE_DATA[k]==undefined){
						delete data.MAP_DATA[i][j][k];
					}
					if(j=="enemy"&&k!="normal"){
						delete data.MAP_DATA[i][j][k];
					}
					if(j=="trash"){
						delete data.MAP_DATA[i][j][k].get;
					}
					for(var l in data.MAP_DATA[i][j][k]){
						if(i=="farm"){
							continue;
						}
						if(j=="resource"&&l!="value"){
							delete data.MAP_DATA[i][j][k][l];
						}
					}
				}
			}
		}
		data = timeTrans(data);
		return JSON.stringify(data);	
	}
	catch(e){
		return false;
	}
}

function autosave(){
	var data = saveData();
	if(!data){
		alert("存档文件生成失败。");
	}
	else{
		if(window.localStorage != undefined){
			localStorage.setItem("autosave", escape(data));
		}
		
		/*
		var savecookie = $.cookie();
		for(var i in savecookie){
			$.removeCookie(i, {path:"/"});
		}
		//cookie长度限制，分段存放
		var n = 0;
		n = 0;
		while(data.length >= 1000){
			//防止分段开头出现"
			var end = 1000;
			while($.inArray(data.substr(end, 1), ["\"", "[", "]", ","]) != -1){
				end += 1;
			}
			var str = data.substr(0, end);
			$.cookie("autosave"+n, encodeURI(str), {expires:7, path:"/"});
			data = data.substr(end);
			n += 1;
		}
		$.cookie("autosave"+n, encodeURI(data), {expires:7, path:"/"});
		*/
	}
}

function loadData(data){
	try{
		var json = JSON.parse(data);
		json = timeTrans(json);
	}
	catch(e){
		return false;
	}
	
	LOAD_FLAG = true;
	for(var i in json){
		switch(typeof json[i]){
			case "object":
			if(json[i] instanceof Array){
				eval(i + " = clone(json[i]);");
			}
			else if(json[i] instanceof Date){
				eval(i + " = clone(json[i]);");
			}
			else{
				eval(i + " = $.extend(true, {}, " + i + ", clone(json[i]));");
			}
			break;
			default:
			eval(i + " = clone(json[i]);");
		}
	}

	//纠错功能--属性
	PLAYER_STATUS.critimes.value = 1.5;
	PLAYER_STATUS.hitrate.value = 100;

	for(var i in TOOL_DATA){
		if(TOOL_DATA[i].tech!=undefined && PLAYER_STATUS.tech.value>=TOOL_DATA[i].tech && TOOL_DATA[i].show==undefined){
			TOOL_DATA[i].show = true;
		}
	}
	//纠错功能--旧的箱子容量升级项不再重复计算，显示下一升级项
	var nextBoxUp = 0;
	var boxUpFlag = false;
	for(var i in TOOL_FINISHED){
		if(TOOL_FINISHED[i] == "box_1"){
			MAP_DATA.home.place.toBox.show = true;
			delete TOOL_DATA.box_1.show;
		}
		if(TOOL_FINISHED[i]=="box_9" && BOX_CAP>60){
			boxUpFlag = true;
		}
		if(TOOL_FINISHED[i].indexOf("box")==0 && TOOL_FINISHED[i]!="box_10"){
			if(nextBoxUp < parseInt(TOOL_FINISHED[i].replace("box_", ""))){
				nextBoxUp = parseInt(TOOL_FINISHED[i].replace("box_", ""));
			}
		}
	}
	TOOL_DATA["box_" + (nextBoxUp+1).toString()].show = true;

	for(var i in TOOL_FINISHED){
		if(TOOL_DATA[TOOL_FINISHED[i]] == undefined){
			continue;
		}
		if(TOOL_FINISHED[i].indexOf("box")==0 && boxUpFlag){
			continue;
		}

		if(TOOL_DATA[TOOL_FINISHED[i]].upgrade != undefined){
			eval(TOOL_DATA[TOOL_FINISHED[i]].upgrade);
		}
		if(TOOL_DATA[TOOL_FINISHED[i]].newflag){
			delete TOOL_DATA[TOOL_FINISHED[i]].newflag;
		}
		delete TOOL_DATA[TOOL_FINISHED[i]].show;
	}
	for(var i in QUEST_FINISHED){
		if(QUEST_DATA[QUEST_FINISHED[i][0]] == undefined){
			continue;
		}
		if(QUEST_DATA[QUEST_FINISHED[i][0]].update!=undefined && QUEST_DATA[QUEST_FINISHED[i][0]].dontload==undefined){
			eval(QUEST_DATA[QUEST_FINISHED[i][0]].update);
		}
		if(QUEST_FINISHED[i][1] != "null"){
			eval("MAP_DATA."+QUEST_FINISHED[i][1]+".quest.shift();");
		}
	}
	for(var i in PLAYER_STATUS.buff){
		if(BUFF_DATA[i].name != undefined){
			var info = "<br><span class='"+BUFF_DATA[i].type+"BuffName'>"+BUFF_DATA[i].name+"</span>："+BUFF_DATA[i].desc;
			if(PLAYER_STATUS[BUFF_DATA[i].on].desc.indexOf(info) < 0){
				PLAYER_STATUS[BUFF_DATA[i].on].desc += info;
			}
		}
	}
	//纠错功能--探索地图、垃圾变更
	for(var i in MAP_DATA){
		if(i.indexOf("explore_")==0 && EXPLORE_DATA[i]!=undefined && MAP_DATA.outside.place[i]==undefined){
			delete MAP_DATA[i];
			delete EXPLORE_DATA[i];
		}
		if(MAP_DATA[i].trash != undefined){
			for(var j in MAP_DATA[i].trash){
				if(MAP_DATA[i].trash[j].get == undefined){
					delete MAP_DATA[i].trash[j];
				}
			}
		}
	}
	delete MAP_DATA.vault7.enemy.normal.ghoul_1;
	delete MAP_DATA.vault7.enemy.normal.ghoul_2;
	EXPLORE_CHECK = clone(sysTime);
	DISASTER_CHECK = clone(sysTime);
	disasterChk();
	if(DISASTER!="" && $("#disasterInfo").attr("id")==undefined){
        var clockMsg = "<span id='disasterInfo' class='disasterInfo'>"+DISASTER_TYPE[DISASTER].name+" <span id='countdownType'>倒计时</span>：<span id='countdown'></span></span>";
        $("#clock").popover({html:true, trigger: "click", title:clockMsg});
        $("#clock").popover("show");
    }
    

	/*/测试期间不允许探索地图
	for(var i in MAP_DATA){
		if(i.indexOf("explore_") == 0){
			delete MAP_DATA[i];
			delete MAP_DATA.outside.place[i];
		}
	}*/
	resInit(MAP_DATA);
	cookCheck();
	gameSet();

	$("#bag").empty();
	for(var i in BAG_DATA){
		var newObj = new itemObj(i, $("#bag"));
		newObj.create();
	}
	autosort(BAG_DATA);
	getSum(BAG_DATA);
	if(BEGINNER_FLAG){
		ITEM_DATA.meat.effect = {hunger:10, radiation:1};
		ITEM_DATA.roachMeat.effect = {hunger:8, radiation:1};
		ITEM_DATA.wormMeat.effect = {hunger:8, radiation:1};
		BUFF_DATA.sandstorm.interval = 15;
		BUFF_DATA.rain.interval = 15;
		$("#clock").after(newElement("div", "beginnerFlag", "", "", "新手模式"));
	}

	LOAD_FLAG = false;
	USERNAME = "";
	toLoading(0.1, "home");
	return true;
}

function fixsave(){
	for(var i in PLAYER_STATUS){
		if($.inArray(i, ["tech", "buff", "buffPause", "equip"]) == -1){
			var bufferSum = 0;
			for(var j in PLAYER_STATUS.equip){
				if(PLAYER_STATUS.equip[j]!="" && ITEM_DATA[PLAYER_STATUS.equip[j]].effect!=undefined){
					var effect = ITEM_DATA[PLAYER_STATUS.equip[j]].effect;
					for(var k in effect){
						if(k == i){
							bufferSum += effect[k];
						}
					}
				}
				if(PLAYER_STATUS.equip[j]!="" && j=="weapon" && i=="attack"){
					bufferSum += ITEM_DATA[PLAYER_STATUS.equip[j]].attack;
				}
			}
			for(var j in PLAYER_STATUS.buff){
				if(BUFF_DATA[j].effect!=undefined && BUFF_DATA[j].temp){
					for(var k in BUFF_DATA[j].effect){
						if(k == i){
							var times = 1;
							if(PLAYER_STATUS.buff[j][2] != undefined){
								times = PLAYER_STATUS.buff[j][2];
							}
							if(BUFF_DATA[j].effect[k].percent != undefined){
								var status = BUFF_DATA[j].effect[k].type;
								var value = realVal(k);
								if(status != k){
									value = realVal(status);
								}
								value *= BUFF_DATA[j].effect[k].percent;
								bufferSum += value;
							}
							else{
								bufferSum += BUFF_DATA[j].effect[k];
							}
						}
					}
				}
			}
			if(PLAYER_STATUS[i].buffer!=undefined && PLAYER_STATUS[i].buffer!=bufferSum){
				PLAYER_STATUS[i].buffer = bufferSum;
				if(bufferSum!=0 && PLAYER_STATUS[i].value!=PLAYER_STATUS_INIT[i].value){
					PLAYER_STATUS[i].value = PLAYER_STATUS_INIT[i].value - bufferSum;
				}
			}
			else if(PLAYER_STATUS[i].buffer==undefined && bufferSum!=0){
				PLAYER_STATUS[i].buffer = bufferSum;
				if(PLAYER_STATUS[i].value != PLAYER_STATUS_INIT[i].value){
					PLAYER_STATUS[i].value = PLAYER_STATUS_INIT[i].value - bufferSum;
				}
			}
		}
	}
}

function NaNcheck(data){
	for(var i in data){
		if(isNaN(data[i])){
			delete data[i];
		}
	}
}

function timeTrans(a){
	var b;
	switch(typeof a){
		case "object":
		if(a instanceof Array){
			b = [];
			for(var i in a){
				b.push(timeTrans(a[i]));
			}
		}
		else if(a instanceof Date){
			b = a.getTime();
		}
		else{
			b = {};
			for(var i in a){
				b[i] = timeTrans(a[i]);
			}
		}
		break;
		case "number":
		if(a.toString().length == 13){
			b = new Date(a);
		}
		else{
			b = a + 0;
		}
		break;
		case "string":
		b = a + "";
		break;
		case "undefined":
		break;
		default:
		b = a;
	}
	return b;
}
//================================================================================================

//====游戏前选项====
var BEFORE_GAME = new beforeGameObj();
function beforeGameObj(){
	var freePoint = 2;
	var points = [];
	var ranSum = 0;

	this.create = function(){
		$("div[class='container-fluid']").append(newElement("div","beforeGame","","",""));

		$("#beforeGame").append("<p></p>");
		$("#beforeGame p").append(newElement("button", "newPlay", "", "btn btn-default", "新建"));
		$("#beforeGame p").append(newElement("button", "load", "", "btn btn-default", "读取"));
		var savecookie;
		if(window.localStorage != undefined){
			savecookie = localStorage.getItem("autosave");
		}
		if(savecookie != undefined){
			$("#beforeGame p").append("<br>");
			$("#beforeGame p").append(newElement("button", "continue", "", "btn btn-default", "继续游戏"));
			$("#continue").click(function(){
				$(this).html("读取中...");
				$(this).attr("disabled", "disabled");
				//var autosave = $.cookie();
				
				/*
				for(var i in autosave){
					if(i.indexOf("autosave") != -1){
						data += decodeURI(autosave[i]);
					}
				}
				*/
				startGame();
				if(loadData(unescape(savecookie))){
					$("#beforeGame").fadeOut(1000, function(){
						$("#beforeGame").remove();
						resumeGame();
					});
				}
				else{
					$("#background").empty();
					resetGame();
					alert("存档文件出现问题，读取失败。");
				}
				$(this).removeAttr("disabled");
				$(this).html("继续游戏");
			});
			
		}

		$("#newPlay").click(function(){
			$("#beforeGame").fadeOut(500, roleBuild);
		});
		$("#load").click(function(){
			slView("load", "beforeGame");
		});
	}

	function roleBuild(){
		freePoint = 2;
		points = [];
		ranSum = 0;
		for(var i in SPECIAL_LIST){
			points[i] = Math.random();
			ranSum += points[i];
		}
		for(var i in SPECIAL_LIST){
			points[i] = 2 + Math.round(12*points[i]/ranSum);
		}
		$("#beforeGame").empty();
		$("#beforeGame").append("<div id='buildDiv'></div>");

		var tip = "自由属性点:<span>" + freePoint + "</span><br>点击分配";
		$("#buildDiv").append(newElement("div", "pointInfo", "", "", tip));

		var names = newElement("tr", "", "", "", "");
		var values = newElement("tr", "values", "", "", "");
		for(var i in SPECIAL_LIST){
			var tdName = newElement("td", SPECIAL_LIST[i], "", "", PLAYER_STATUS[SPECIAL_LIST[i]].name);
			tdName.onmouseover = function(){showinfo.call(this);};
			tdName.ontouchstart = tdName.onmouseover;
			names.appendChild(tdName);
			var tdValue = newElement("td", SPECIAL_LIST[i], "", "", "");
			tdValue.onmouseover = function(){showinfo.call(this);};
			tdValue.ontouchstart = tdValue.onmouseover;
			var minusBtn = newElement("button", SPECIAL_LIST[i], "", "btn btn-default", "-");
			minusBtn.onclick = function(){minusPoint.call(this);};
			var plusBtn = newElement("button", SPECIAL_LIST[i], "", "btn btn-default", "+");
			plusBtn.onclick = function(){addPoint.call(this);};
			tdValue.appendChild(minusBtn);
			tdValue.appendChild(newElement("span", "", "", "", points[i]));
			tdValue.appendChild(plusBtn);
			values.appendChild(tdValue);
		}
		var tb = newElement("table", "", "", "table", "");
		var thead = document.createElement("thead");
		var tbody = document.createElement("tbody");
		thead.appendChild(names);
		tbody.appendChild(values);
		tb.appendChild(thead);
		tb.appendChild(tbody);
		$("#buildDiv").append(tb);
		applyPoint();

		var beginner = newElement("input", "", "", "beginner", "");
		beginner.type = "checkbox";
		beginner.onmouseover = function(){
			$("#buildDiv div[class='info']").html("饥饿、干渴速度减慢，不会获取大部分负面效果，降低部分惩罚。");
		};
		$("#buildDiv").append(beginner);$("#buildDiv").append("新手模式");
		$("#buildDiv").append("<div class='info'>鼠标置于属性名上查看说明</div>");
		$("#buildDiv").append(newElement("button", "", "confirm", "btn btn-default", "确认"));
		$("#buildDiv").append(newElement("button", "", "reroll", "btn btn-default", "重置"));

		$("#buildDiv button[name='confirm']").click(function(){
			if(confirm("确认使用此套属性点进行游戏吗？")){
				if(freePoint > 0){
					alert("仍有属性点未分配。");
				}
				else{
					applyPoint();
					if($("#buildDiv .beginner").is(":checked")){
						BEGINNER_FLAG = true;
						delete TOOL_DATA.compass.show;
						eval(TOOL_DATA.cook_rad.upgrade);
						eval(TOOL_DATA.lantern.upgrade);
						delete TOOL_DATA.cook_rad.tech;
						delete TOOL_DATA.lantern.show;
						TOOL_FINISHED.push("cook_rad");
						TOOL_FINISHED.push("lantern");
						ITEM_DATA.meat.effect = {hunger:10, radiation:1};
						ITEM_DATA.roachMeat.effect = {hunger:8, radiation:1};
						ITEM_DATA.wormMeat.effect = {hunger:8, radiation:1};
						BUFF_DATA.sandstorm.interval = 15;
						BUFF_DATA.rain.interval = 15;
					}
					$("#beforeGame").fadeOut(1000, function(){
						$("#beforeGame").remove();
						startGame();
						updateSysClock(2, 0, false, 2);
						resumeGame();
					});
				}
			}
		});
		$("#buildDiv button[name='reroll']").click(function(){reroll();});

		$("#beforeGame").fadeIn(500);
	}

	function showinfo(){
		$("#buildDiv div[class='info']").html(PLAYER_STATUS[this.id].desc);
	}

	function reroll(){
		freePoint = 2;
		points = [];
		ranSum = 0;
		for(var i in SPECIAL_LIST){
			points[i] = Math.random();
			ranSum += points[i];
		}
		for(var i in SPECIAL_LIST){
			points[i] = 2 + Math.round(12*points[i]/ranSum);
			$("#buildDiv #values td:eq("+i+") span").html(points[i]);
		}
		applyPoint();
		$("#pointInfo span").html(freePoint);
	}

	function minusPoint(){
		var value = parseInt($("#buildDiv #values #"+this.id+" span").html());
		if(freePoint < 2 && value>PLAYER_STATUS[this.id].value){
			$("#buildDiv #values #"+this.id+" span").html(value - 1);
			freePoint += 1;
			$("#pointInfo span").html(freePoint);
		}
	}

	function addPoint(){
		if(freePoint > 0){
			var value = parseInt($("#buildDiv #values #"+this.id+" span").html());
			$("#buildDiv #values #"+this.id+" span").html(value + 1);
			freePoint -= 1;
			$("#pointInfo span").html(freePoint);
		}
	}

	function applyPoint(){
		for(var i in SPECIAL_LIST){
			PLAYER_STATUS[SPECIAL_LIST[i]].value = parseInt($("#buildDiv #values #"+SPECIAL_LIST[i]+" span").html());
		}
	}
}

function startGame(){
	createUI();
	gameSet();
	PLAYER_STATUS.life.value = PLAYER_STATUS.life.max;
	resInit(MAP_DATA);

	for(var i in STATUS_LIST){         
		var newObj = new statusObj(STATUS_LIST[i]);
		newObj.create();
	}

	for(var i in BAG_DATA){
		var newObj = new itemObj(i, $("#bag"));
		newObj.create();
	}
	getSum(BAG_DATA);

	var map = new mapObj("origin");
	map.create();
}

function createUI(){
	$("#background").empty();
    //主界面绘制
    var TAB_LIST = ['map', 'box', 'workbench', 'battle', 'trade', 'quest', 'temp', 'loading'];
    $("#background").append('<ul id="tablist" role="tablist" style="display:none;">');
    for(var i in TAB_LIST){
    	$("#tablist").append('<a href="#'+TAB_LIST[i]+'" role="tab"></a>');
    }
    if(document.body.clientWidth>=1024){
    	$("#background").append('<div id="status"></div>');
	    $("#background").append(newElement("label", "bagTitle", "", "frameTitle bagTitlePc", '背包<span id="bagCap"></span>'));
	    $("#background").append(newElement("div", "bag", "bag", "frame", ""));
	    $("#background").append(newElement("label", "infoTitle", "", "frameTitle infoTitlePc", "信息"));
    	$("#background").append(newElement("div", "info", "", "frame", ""));
    	$("#background").append('<hr style="clear:both;">');
	    $("#background").append(newElement("label", "mainTitle", "", "frameTitle mainTitlePc", "地图"));
    }
    else{
    	$("#background").append('<div id="status"></div>');
	    $("#background").append('<hr style="clear:both;">');
	    $("#background").append(newElement("label", "bagTitle", "", "frameTitle", '<span id="bagOpen">打开</span>背包<span id="bagCap"></span>'));
	    $("#background").append(newElement("div", "bag", "bag", "frame", ""));
	    function bagOpen(){
	    	var height = parseFloat($("#bag").css("height").replace("px",""));
	        var newHeight = $("#bag")[0].scrollHeight + 4;
	    	$("#bag").css({height:newHeight + "px"});
	    	var mainTop = parseFloat($(".main").css("top").replace("px",""));
	    	$(".main").css({top:mainTop + newHeight - height + "px"});
	    	if($("#message") != undefined){
	    		$("#message").offset({left:$("#info").offset().left, top:$("#info").offset().top});
	    	}
	    	$("#bagOpen").html("收起");
	    	$("#bagTitle").unbind("click");
	    	$("#bagTitle").click(function(){bagClose(height);});
	    }
	    function bagClose(oldHeight){
	    	var height = parseFloat($("#bag").css("height").replace("px",""));
	    	$("#bag").css({height:oldHeight + "px"});
	    	var newHeight = parseFloat($("#bag").css("height").replace("px",""));
	    	var mainTop = parseFloat($(".main").css("top").replace("px",""));
	    	$(".main").css({top:mainTop + newHeight - height + "px"});
	    	if($("#message") != undefined){
	    		$("#message").offset({left:$("#info").offset().left, top:$("#info").offset().top});
	    	}
	    	$("#bagOpen").html("打开");
	    	$("#bagTitle").unbind("click");
	    	$("#bagTitle").click(bagOpen);
	    }
	    $("#bagTitle").click(bagOpen);
	    $("#background").append(newElement("label", "infoTitle", "", "frameTitle", "信息"));
    	$("#background").append(newElement("div", "info", "", "frame", ""));
    	$("#background").append(newElement("label", "mainTitle", "", "frameTitle", "地图"));
    }  
    
    var content = newElement("div", "", "", "tab-content main", "");
    for(var i in TAB_LIST){
    	var newTab = newElement("div", TAB_LIST[i], TAB_LIST[i], "tab-pane fade", "");
    	if(i == 0){
    		newTab.className = "tab-pane fade in active";
    	}
    	newTab.setAttribute("role", "tabpanel");
    	content.appendChild(newTab);
    }
    $("#background").append(content);
    var footer = newElement("div", "footer", "", "", "");
    footer.appendChild(document.createElement("hr"));
    var clock = newElement("div", "clock", "", "", "");
    clock.setAttribute("data-toggle", "popover");
    clock.setAttribute("data-placement", "auto top");
    clock.setAttribute("data-container", "body");
    footer.appendChild(clock);
    
    if(BEGINNER_FLAG){
    	footer.appendChild(newElement("div", "beginnerFlag", "", "", "新手模式"));
    }
    footer.appendChild(newElement("button", "pauseBtn", "", "btn btn-default", "暂停"));
    $("#background").append(footer);
    $("#pauseBtn").click(function(){pauseView();});

    getBackBtn($("#box"));
    //$(".container-fluid").after(showAD("bottomAD"));
}

function gameSet(){
	PLAYER_STATUS.life.max = Math.ceil(100 * (1+(realVal("endurance")-4)/20));
	PLAYER_STATUS.life.toplimit = PLAYER_STATUS.life.max;
	var limit = 5;
	if(PLAYER_STATUS.buff.slow_1 != undefined){
		limit = 10;
	}
	PLAYER_STATUS.life.max = PLAYER_STATUS.life.toplimit - Math.floor(realVal("radiation")/limit);
	PLAYER_STATUS.life.value = PLAYER_STATUS.life.value<PLAYER_STATUS.life.max?PLAYER_STATUS.life.value:PLAYER_STATUS.life.max;
	if(PLAYER_STATUS.life.value<=0 && !DEATH_FLAG){
		DEATH_FOR = "辐射";
		death();
	}
	HUNGER_SPEED = (BEGINNER_FLAG?1/45:1/18) * (1-(realVal("endurance")-4)/20);
	HUNGER_SPEED = HUNGER_SPEED<=0?1/440:HUNGER_SPEED;
	THIRST_SPEED = (BEGINNER_FLAG?1/30:1/12) * (1-(realVal("endurance")-4)/20);
	THIRST_SPEED = THIRST_SPEED<=0?1/300:THIRST_SPEED;
	WORK_TIME_COST = BEGINNER_FLAG?1.5:2.5;
	WORK_ENERGY_COST = BEGINNER_FLAG?1/15:1/10;

	PLAYER_STATUS.critical.value = (realVal("luck") - 4) * 2.5;
	PLAYER_STATUS.critical.value = PLAYER_STATUS.critical.value<0 ? 0 : PLAYER_STATUS.critical.value;

	PLAYER_STATUS.dodge.value = (realVal("agility") - 4) * 2;
	PLAYER_STATUS.dodge.value = PLAYER_STATUS.dodge.value>99 ? 99 : PLAYER_STATUS.dodge.value;
	PLAYER_STATUS.dodge.value = PLAYER_STATUS.dodge.value<0 ? 0 : PLAYER_STATUS.dodge.value;

	PLAYER_STATUS.escape.value = 40 * (1+(realVal("agility") - 4) * 0.2);
	PLAYER_STATUS.escape.value = PLAYER_STATUS.escape.value>90 ? 90 : PLAYER_STATUS.escape.value;
	PLAYER_STATUS.escape.value = PLAYER_STATUS.escape.value<0 ? 0 : PLAYER_STATUS.escape.value;

	BATTLE_OBJ.resetPlayer();

	for(var i in STATUS_LIST){         
		var newObj = new statusObj(STATUS_LIST[i]);
		newObj.update();
	}
}

function pauseView(){
	pauseGame();
	$("#overlay").fadeTo(10, 0.5);
	$("#pauseDiv").fadeIn(500);

	//基本属性
	var names = newElement("tr", "", "", "", "");
	var values = newElement("tr", "values", "", "", "");
	for(var i in SPECIAL_LIST){
		var tdName = newElement("td", SPECIAL_LIST[i], "", "", PLAYER_STATUS[SPECIAL_LIST[i]].name);
		tdName.onmouseover = function(){showinfo.call(this);};
		tdName.ontouchstart = tdName.onmouseover;
		names.appendChild(tdName);
		var tdValue = newElement("td", SPECIAL_LIST[i], "", "", Math.floor(realVal(SPECIAL_LIST[i])));
		tdValue.onmouseover = function(){showinfo.call(this);};
		tdValue.ontouchstart = tdValue.onmouseover;
		values.appendChild(tdValue);
	}
	var tb = newElement("table", "", "", "table specialTb", "");
	var tbody = document.createElement("tbody");
	tbody.appendChild(names);
	tbody.appendChild(values);
	tb.appendChild(tbody);
	$("#pauseDiv").append(tb);
	//外在属性
	names = newElement("tr", "", "", "", "");
	values = newElement("tr", "values", "", "", "");
	for(var i in PLAYER_STATUS){
		if($.inArray(i, ["equip", "buff", "buffPause", "achivement"]) == -1 && $.inArray(i, STATUS_LIST) == -1 && $.inArray(i, SPECIAL_LIST) == -1){
			var tdName = newElement("td", i, "", "", PLAYER_STATUS[i].name);
			tdName.onmouseover = function(){showinfo.call(this);};
			tdName.ontouchstart = tdName.onmouseover;
			names.appendChild(tdName);
			var value = realVal(i);
			if(i=="tech" || i=="critimes"){
				value = value.toFixed(1);
			}
			else{
				value = Math.round(value);
			}
			if(PLAYER_STATUS[i].percent){
				value += "%";
			}
			var tdValue = newElement("td", i, "", "", value);
			tdValue.onmouseover = function(){showinfo.call(this);};
			tdValue.ontouchstart = tdValue.onmouseover;
			values.appendChild(tdValue);
		}
	}
	tb = newElement("table", "", "", "table attrTb", "");
	tbody = document.createElement("tbody");
	tbody.appendChild(names);
	tbody.appendChild(values);
	tb.appendChild(tbody);
	$("#pauseDiv").append(tb);
	
	$("#pauseDiv").append("附加状态：");
	for(var i in PLAYER_STATUS.buff){
		if(BUFF_DATA[i].name == undefined){
			continue;
		}
		var span = newElement("span", i, "", BUFF_DATA[i].type+"BuffName margin5", BUFF_DATA[i].name);
		span.onmouseover = function(){$("#pauseDiv div[class='info']").html(BUFF_DATA[this.id].desc);}
		span.ontouchstart = span.onmouseover;
		$("#pauseDiv").append(span);
	}

	$("#pauseDiv").append("<div class='info' style='text-align:left;'>鼠标置于属性名上查看说明</div>");
	
	$("#pauseDiv").append(newElement("button", "achivement", "", "btn btn-default", "成就"));
	$("#pauseDiv").append(newElement("button", "close", "", "btn btn-default", "返回"));
	$("#pauseDiv").append("<br>");
	if($(".tab-pane.active").attr("id")=="map" && $("#map").attr("place")=="home"){
		$("#pauseDiv").append(newElement("button", "save", "", "btn btn-default", "保存"));
	}
	$("#pauseDiv").append(newElement("button", "load", "", "btn btn-default", "读取"));
	$("#pauseDiv").append("<a href='http://tinywaste.lofter.com/post/1dd2c191_9e5eeff' target='_blank' class='btn btn-default'>说明</a>");
	
	$("#close").click(function(){
		$("#pauseDiv").fadeOut(500, function(){
			$("#pauseDiv").empty();
			$("#overlay").hide();
			if(!BATTLE_FLAG){
				resumeGame();
			}
		});
	});

	$("#achivement").click(function(){
		$("#pauseDiv").fadeOut(500, function(){
			$("#pauseDiv").empty();
			$("#pauseDiv").fadeIn(500);
			apView();
		});
	});

	$("#save").click(function(){slView("save");});

	$("#load").click(function(){slView("load");});

	function showinfo(){
		$("#pauseDiv div[class='info']").html(PLAYER_STATUS[this.id].desc);
	}

	function apView(){
        var divTb = newElement("div", "", "", "divTb", "");
        var tb = newElement("table", "achiveTb", "", "table table-hover infoTb", "");

        var thead = newElement("thead", "", "", "", "<tr><th>成就</th><th>说明</th><th>奖励</th></tr>");
        tb.appendChild(thead);
        var tbody = document.createElement("tbody");
        for(var i in PLAYER_STATUS.achivement){
	        var tr = document.createElement("tr");
	        tr.id = i;
	        apItem = ACHIVEMENT_DATA["type_" + PLAYER_STATUS.achivement[i]][i];
	        tr.innerHTML = "<td>" + apItem.name + "</td>" //成就颜色待补
	        			 + "<td>" + apItem.info + "</td>";

	        var getDesc = "";
	        	if(apItem.get != undefined){
	        	for(var j in apItem.get){
	        		getDesc += ITEM_DATA[j].name + apItem.get[j];
	        	}
	        }
	        tr.innerHTML += "<td>" + getDesc + "</td>";

	        tbody.appendChild(tr);
	    }
        tb.appendChild(tbody);
        divTb.appendChild(tb);

        $("#pauseDiv").append(divTb);
        $("#pauseDiv").append(newElement("button", "close", "", "btn btn-default", "返回"));
        $("#close").click(function(){
			$("#pauseDiv").fadeOut(500, function(){
				$("#pauseDiv").empty();
				pauseView();
			});
		});
	}
}

function slView(mode, flag){
	var layer = $("#pauseDiv");
	if(flag != null){
		$("#beforeGame").html("<div id='buildDiv'></div>");
		layer = $("#buildDiv");
		layer.hide();
		$("#beforeGame").fadeOut(500, function(){
			$("#beforeGame").fadeIn(500);
			layer.show();
		});
		
	}
	layer.empty();
	layer.append("<div class='info' style='text-align:left;'>请使用自定义的用户名和密码进行保存和读取，无须注册。</div>");
	layer.append(newElement("div", "username", "", "slView", "用户名:<input type='text' class='form-control'/>"));
	layer.append("<br>");
	layer.append(newElement("div", "pwd", "", "slView", "密码:<input type='password' class='form-control'/>"));
	layer.append(newElement("button", "sl", "", "btn btn-default", ""));
	if(flag==null){
		layer.append(newElement("button", "back", "", "btn btn-default", "返回"));
		$("#back").click(function(){
			layer.empty();
			pauseView();
		});
	}

	if(mode == "save"){
		$("#sl").html("保存");
		$("#sl").click(function(){
			var name = saveEncode();
			if(name != -1){
				USERNAME = $("#username input").val().replace(/(^s*)|(s*$)/g, "");
				save(false, name);
			}
		});
	}
	else{
		$("#sl").html("读取");

		//纠错功能--修复属性数值
		var fixCheck = newElement("input", "fixCheck", "", "", "");
		fixCheck.type = "checkbox";
		$("#sl").before(fixCheck);
		var fixInfo = newElement("div", "fixInfo", "", "noneBuffName", "修复式读取");
		$("#sl").before(fixInfo);
        var fixDesc = "若你的存档因版本冲突或bug造成数值不正确，可勾选此项。<br>此为自动修复，不保证能识别某些偶然错误，请在修复后仔细检查，确认无误后再保存。";
        $("#fixInfo").css({"cursor":"pointer"});
        $("#fixInfo").attr("data-toggle", "popover");
        $("#fixInfo").attr("data-placement", "auto top");
        $("#fixInfo").attr("data-container", "body");
        $("#fixInfo").popover({html:true, trigger: "click", title:fixDesc});
		
		$("#sl").click(function(){
			$("#fixInfo").popover("destroy");
			var name = -1;
			if($("#username input").val().replace(/(^s*)|(s*$)/g, "").indexOf("loadkey=") == 0){
				name = $("#username input").val().replace(/(^s*)|(s*$)/g, "").replace("loadkey=", "");
			}
			else{
				name = saveEncode();
			}

			if(name == -1){
				return;
			}

			$("#sl").html("读取中...");
			$("#sl").attr("disabled", "disabled");
			$.ajax({
				type:'POST',
				url:"load.php",
				data:{key:name},
				contentType:"application/x-www-form-urlencoded",
				success:function(msg){
					var result = JSON.parse(msg.substr(0, msg.indexOf('<script type')));
					switch(result.msg){
						case "success":
						if(flag != null){
							startGame();
							if(loadData(result.data)){
								if($("#fixCheck").is(":checked")){
									fixsave();
								}
								$("#beforeGame").fadeOut(1000, function(){
									$("#beforeGame").remove();
									resumeGame();
								});
							}
							else{
								alert("存档文件出现问题，读取失败。");
							}
						}
						else{
							if(loadData(result.data)){
								resetGame();
								loadData(result.data);
								if($("#fixCheck").is(":checked")){
									fixsave();
								}
								if(!BEGINNER_FLAG && $("#beginnerFlag").attr("id")!=undefined){
									$("#beginnerFlag").remove();
								}
								$("#pauseDiv").fadeOut(500, function(){
									$("#pauseDiv").empty();
									$("#overlay").hide();
									resumeGame();
								});
							}
							else{
								alert("存档文件出现问题，读取失败。");
							}
						}
						SAVE_KEY = name;
						break;
						default:
						SAVE_KEY = "";
						alert(result.data);
					}
					SAVE_FAST = false;
					$("#sl").removeAttr("disabled");
					$("#sl").html("读取");
				},
				error:function(XMLHttpRequest, textStatus, errorThrown) {
					alert("status:" + XMLHttpRequest.status + "<br>readyState:" + XMLHttpRequest.readyState);
					SAVE_KEY = "";
					SAVE_FAST = false;
					$("#sl").removeAttr("disabled");
					$("#sl").html("读取");
				}
			});
});
}
}
function saveCheck(){
	var username = $("#username input").val().replace(/(^s*)|(s*$)/g, "");
	var pwd = $("#pwd input").val().replace(/(^s*)|(s*$)/g, "");
	var illegal = "'\"><*";
	var usnflag = 0;
	var pwdflag = 0;
	for(var i=0;i<illegal.length;i++){
		var a = illegal.substr(i, i+1);
		if(username.indexOf(a)>-1){
			usnflag = 1;
		}
		if(pwd.indexOf(a)>-1){
			pwdflag = 1;
		}
	}
	if(username.length < 4 || username.length > 20){
		alert("用户名长度应为4~20。");
		return 0;
	}
	else if(username.indexOf("　")>-1 || username.indexOf(" ")>-1){
		alert("用户名不可带空格。");
		return 0;
	}
	else if(usnflag){
		alert("用户名含非法字符。");
		return 0;
	}
	if(pwd.length < 4 || pwd.length > 20){
		alert("密码长度应为4~20。");
		return 0;
	}
	else if(pwd.indexOf("　")>-1 || pwd.indexOf(" ")>-1){
		alert("密码不可带空格。");
		return 0;
	}
	else if(usnflag){
		alert("密码含非法字符。");
		return 0;
	}
	return 1;
}

function saveEncode(){
	var username = $("#username input").val().replace(/(^s*)|(s*$)/g, "");
	var pwd = $("#pwd input").val().replace(/(^s*)|(s*$)/g, "");
	if(saveCheck()){
		return $.md5(username+"k"+pwd, username);
	}
	else{
		return -1;
	}
}

function save(overwrite, name){
	$("#sl").html("保存中...");
	$("#sl").attr("disabled", "disabled");
	var savefile = saveData();
	if(!savefile){
		alert("存档生成失败。");
		$("#sl").removeAttr("disabled");
		$("#sl").html("保存");
		$("#fastsave").removeAttr("disabled");
		$("#fastsave").html("快速保存(F6)");
		return;
	}
	var savecookie = $.cookie();
	for(var i in savecookie){
		$.removeCookie(i, {path:"/"});
	}
	
	$.ajax({
		type:'POST',
		url:"save_test.php",
		data:{key:name,username:USERNAME,data:savefile,overwrite:overwrite},
		contentType:"application/x-www-form-urlencoded",
		success:function(msg){
			var result = JSON.parse(msg.substr(0, msg.indexOf('<script type')));
			switch(result.msg){
				case "repeated":
				alert("该用户名已存在，请修改用户名再试。")
				break;
				case "success":
				autosave();
				alert("保存成功。");
				if(!SAVE_FAST){
					SAVE_FAST = true;
					SAVE_KEY = name;
					if($("#fastsave").attr("id") == undefined){
						$("#pauseBtn").before(newElement("button", "fastsave", "", "btn btn-default", "快速保存(F6)"));
						$("#fastsave").click(function(){$("#fastsave").html("保存中...");$("#fastsave").attr("disabled", "disabled");save(true,SAVE_KEY);});
					}
				}
				break;
				default:
				//alert(result.msg);
				SAVE_KEY = "";
				alert("存档写入出错，请暂时不要关闭游戏，稍后再试。");
			}
			$("#sl").removeAttr("disabled");
			$("#sl").html("保存");
			$("#fastsave").removeAttr("disabled");
			$("#fastsave").html("快速保存(F6)");
		},
		error:function(XMLHttpRequest, textStatus, errorThrown) {
			alert("status:" + XMLHttpRequest.status + "<br>readyState:" + XMLHttpRequest.readyState);
			SAVE_KEY = "";
			$("#sl").removeAttr("disabled");
			$("#sl").html("保存");
			$("#fastsave").removeAttr("disabled");
			$("#fastsave").html("快速保存(F6)");
		}
	});
}

function death(){
	DEATH_FLAG = true;
	pauseGame();
	apCheck(0);
	/*
	//死亡惩罚
	var items = Object.keys(BAG_DATA);
	var dropItem = {};
	if($("#map").attr("place")!="home" && DEATH_FOR!="意外"){
		for(var i=0;i<Math.floor(Math.random()*2+1);i++){
			var item = items[Math.floor(Math.random()*items.length)];
			dropItem[item] = Math.floor(Math.random()*BAG_DATA[item]*0.45 + BAG_DATA[item]*0.3);
			dropItem[item] = dropItem[item]==0 ? 1 : dropItem[item];
		}
	}
	var dropDesc = getSum(dropItem)>0 ? "失去物品：" : "";
	for(var i in dropItem){
		var amount = ITEM_DATA[i].durab!=undefined ? Math.ceil(dropItem[i]/ITEM_DATA[i].durab) : clone(dropItem[i]);
		dropDesc += ITEM_DATA[i].name + "(" + amount + ") ";
		caculate(BAG_DATA, i, -dropItem[i]);
		updateItem(i, $("#bag"));
	}
	
	if(SAVE_KEY != ""){
		save(true, SAVE_KEY);
	}
	else{
		autosave();
	}*/
	
	var deathInfo = "你死了<br>"
				  + "死因是：" + DEATH_FOR + "<br>"
				  //+ (dropDesc!="" ? dropDesc+"<br>" : "")
				  + "总计存活 " + Math.floor((sysTime - originTime)/1000/60/60/24) + " 天<br>";
    var apInfo = "获得成就：";
    for(var i in PLAYER_STATUS.achivement){
    	apInfo += ACHIVEMENT_DATA["type_" + PLAYER_STATUS.achivement[i]][i].name + "<br>";
    }
    deathInfo += apInfo;

	$("#overlay").fadeTo(10, 0.01);
	$("#overlay").fadeTo(1000, 0.7);
	$("#pauseDiv").empty();
	$("#pauseDiv").show();
	$("#pauseDiv").append("<span style='font-size:1.2em;'>"+deathInfo+"</span><br>");
	$("#pauseDiv").append(newElement("button", "again", "", "btn btn-default", "重玩"));
	$("#pauseDiv").append(showAD("messageAD"));
	//$("#pauseDiv").append(newElement("button", "load", "", "btn btn-default", "读取"));
	
	$("#load").click(function(){slView("load");});

	$("#again").click(function(){
		DEATH_FLAG = false;
		resetGame();
		$("#pauseDiv").fadeOut(1000);
		$("#background").empty();
		$("#overlay").fadeOut(1500, function(){
			$("#pauseDiv").empty();
			BEFORE_GAME.create();
		});
	});

}

function resetGame(){
	$("body").css({"font-size":"1.3em"});
	$("#background").css({"background-color":"#FFFFFF"});
	sysTime = new Date("2241/2/1 07:05:00");
	EXCRETE_INTERVAL = [20, 12];
	EXCRETE_FLAG = [false, false];
	EXCRETE_MAX = [36, 16];
	WORK_SPEED = 1;
	COOK_SPEED = 1;
	EX_TAB = ["origin"];
	EX_RESOURCE = "";
	TIMER_FLAG = false;
	BATTLE_OBJ = new battleObj();
	BATTLE_ATONCE = false;
	BATTLE_FLAG = false;
	SAVE_FAST = false;
	SAVE_KEY = "";
	BEGINNER_FLAG = false;
	BAG_CAP = 12;
	BOX_CAP = 10;
	KETTLE_VOLUME = 0;
	KETTLE_AMOUNT = 1;
	FARM_CAP = 1;
	BAG_DATA = {};
	BOX_DATA = {};
	TEMP_DATA = {};
	TOILET_DATA = {};
	COOK_DATA = {};
	COOK_RESULT = {};
	TOOL_FINISHED = [];
	TOOL_LEVEL = {
		work:0,
		tech:0,
		lab:0,
		handwork:0,
		bed:0,
		cook:0,
		forge:0,
		filter:0,
		train:0
	};
	QUEST_FINISHED = [];
	TRADE_LEVEL = 1;
	TRADE_KINDS = 2;
	TRADE_RATE = 15;
	ITEM_DATA = clone(ITEM_DATA_INIT);
	TOOL_DATA = clone(TOOL_DATA_INIT);
	CROP_DATA = clone(CROP_DATA_INIT);
	MAP_DATA = clone(MAP_DATA_INIT);
	PLAYER_STATUS = clone(PLAYER_STATUS_INIT);
	RESEARCH_LIMIT = 0;
	RESEARCH_TIME = clone(originTime);
	LAST_RAD_TIME = clone(originTime);
	EXPLORE_FLAG = false;
	EXPLORE_TIME = 720;
	EXPLORE_RATE = 23;
	EXPLORE_DATA = {};
	EXPLORE_LASTTIME = clone(originTime);
	EXPLORE_CHECK = clone(originTime);
	DISASTER = "";
	DISASTER_EFFECT = false;
    DISASTER_CHECK = clone(originTime);
    DISASTER_TIME = 0;
    DISASTER_LAST = 0;
    DISASTER_LASTTIME = clone(originTime);
    DAILY_CHECK = clone(originTime);
    USERNAME = "";
    TAPHOLD_FLAG = false;
    DAYNIGHT_TIMES = 0;
}

function blink(obj, i){
	if(LOAD_FLAG){
		return;
	}
	if(i<12 && obj!=undefined){
		obj.css({"background-color":i%2==0?"#333333":"transparent", "color":i%2==0?"#FFFFFF":"#333333"});
		setTimeout(function(){blink(obj, i+1);}, 200);
	}
}

var GGAD = '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'
		 + '<!-- tinywaste -->'
		 + '<ins class="adsbygoogle"'
		 + '     style="display:block"'
		 + '     data-ad-client="ca-pub-9759799214726921"'
		 + '     data-ad-slot="2055370295"'
		 + '     data-ad-format="auto"></ins>'
		 + '<script>'
		 + '(adsbygoogle = window.adsbygoogle || []).push({});'
		 + '</script>';

//=============================================================================
//成就系统

function apCheck(type){
	var apType = ACHIVEMENT_DATA["type_" + type];
	var liveDays = Math.floor((sysTime - baseTime)/1000/60/60/24);
	for(var i in apType){
		if(eval(apType[i].check) && PLAYER_STATUS.achivement[i]==undefined){
			PLAYER_STATUS.achivement[i] = type;
			showMsg("获得成就：[" + apType[i].name + "]");
		}
	}
}