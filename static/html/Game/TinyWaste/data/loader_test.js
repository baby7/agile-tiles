loader();
$(function() {
    FastClick.attach(document.body);
    $("body").on("click touchend", function(e) {
        var target = $(e.target);
        if(target.hasClass("item")){
            target.siblings().popover("destroy");
        }
        else if(!target.hasClass("popover") && target.parent(".popoverButton").length === 0){
            $(".item").popover("destroy");
        }
    });
});
    
function loader(){
    if(self.location.host != "tw.wislay.com"){
        $("#overlay").show();
        $("#overlay").html("<span style='font-size:1.5em;color:#FFFFFF;'>域名已转移，跳转中...</span>");
        setTimeout(function(){
            top.location.href = "http://tw.wislay.com" + self.location.pathname;
        }, 1000);
        return;
    }
    var LOAD_LIST = ["item", "status", "work", "map", "creep", "lib", "action"];
    var LOAD_INFO = ["孵化蟑螂", "散布辐射尘", "增殖肿瘤细胞", "编写命运", "什么也没在做", "种植杂草", "放置石块", "制造人类躯壳", "轮回网运转中", "调整反应堆参数", "检查避难所管理系统", "生成工具蓝图", "重置下界数据库"];

    $("#overlay").show();
    $("#overlay").append('<div id="loadGame"><div class="loadingBar"></div></div>');
    $("#overlay").append('<br><div id="loadInfo"></div>');
    $("#loadGame div").animate({width:"28%"}, 1000);
    var i = 0;
    loop();

    function loop(){
        $.ajax({
            type:'GET',
            url:"./data/" + LOAD_LIST.shift() + ".js",
            success:function(data){
                var width = i*9+28;
                var nextWidth = (i+1)*9+28;
                $("#loadGame div").stop(true);
                $("#loadGame div").animate({width:width+"%"}, 500).animate({width:nextWidth>100?100:nextWidth+"%"}, 1000);
                var info = LOAD_INFO[Math.floor(Math.random()*LOAD_INFO.length)];
                $("#loadInfo").html(info);
                for(var j in LOAD_INFO){
                    if(LOAD_INFO[j] == info){
                        LOAD_INFO.splice(j, 1);
                        break;
                    }
                }

                if(LOAD_LIST.length > 0){
		            i += 1;
		            setTimeout(loop, 100);
		        }
		        else{
		            $("#loadGame div").stop(true);
		            $("#loadGame div").animate({width:"100%"}, 1000, function(){
			            $("#overlay").empty();
		                BEFORE_GAME.create();
		                $("#beforeGame").hide();
		                $("#beforeGame").fadeIn(1000);
		                $("#overlay").fadeOut(1000);
		            });
		        }
            }
        });
    }
}