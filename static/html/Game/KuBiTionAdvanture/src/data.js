// 调试模式
var MODE = 'DEBUG';
var MODE = 'RELEASE';

var STOLE = 0.3;
var STOLE_CHANCE = 0.05;
var ROBBER_DAY = 10;
var MAX_STATE = 100;//所有状态的基础
//宏变量

var COOK_TIME_NEED = 0.5;
var SAVE_URL = '//kubitionadvanture.sinaapp.com/save.php';
var DELAY_MUL = (MODE == 'DEBUG')?0:400;
// var DELAY_MUL = 400;
var MIX_DELAY = 100;

var DUNGEON_DEC = 1;

var MAKE_SPEED_MUL = 0.8;
var COOK_SPEED_MUL = 0.8;
// var DELAY_MUL = 0;
// var MIX_DELAY = 0;
var MAX_DISCOVER = 45;//最大探索度 

var BIG_BOX_BASE_SIZE = 16;
var BAG_BASE_SIZE = 12;
var FULL_DESC_PER_HOUR = 1;
var MOIST_DESC_PER_HOUR = 1;
var SAN_DESC_PER_HOUR = 3;
var PICK_TIME = 3;
var NIGHT_BEGIN = 22;
var NIGHT_END = 2;
var SEASON_CIRCLE = 15;
var TRADE_MUL = 0.75;
var COLOR = {
    BLACK:'#222',
    GREEN:'#74AB6A',
    BLUE:'#62BBBE',
    RED:'#B25242',
    WHITE:'#eee',
    YELLOW:'#CBCB7D',
}
var MSG_TIME = 2000;
//游戏数据层////////////////////////////////////////////////////////////////////////

var TYPE_DATA = {
    'quest':{
        name:"特殊",
        color:'#ADAD73'
    },
    'special':{
        name:"技能提升",
        color:'#ADAD73'
    },
    'equip':{
        name:"装备",
        color:'#7E3558'
    },
    'food':{
        name:"食材",
        color:'#9694D8'
    },
    'weapon':{
        name:"武器",
        color:'#DD6820'
    },
    'cooked':{
        name:"食品",
        color:'#A67575'
    },
    'bullet':{
        name:"弹药",
        color:COLOR.YELLOW,
    },
    'met':{
        name:"材料",
        color:COLOR.GREEN,
    },
    'poizon':{
        name:"药剂",
        color:'#AB6DAB'
    },
    'tool':{
        name:"工具",
        color:'#222222'
    },
    'art':{
        name:'工艺品',
        color:'#116666'
    },
    '?':{
        name:"未知",
        color:'#000000'
    },
};
var BUILDING_DATA = {
    build:{
        name:'建造',
        desc:'建造建筑物。',
        require:{},
    },
    makeTable:{
        name:'制造台',
        desc:'可以制作各种工具。',
        require:{wood:8},
        timeNeed:4,
    },
    trap:{
        name:'陷阱',
        desc:'陷阱可以诱捕小动物。',
        require:{wood:10,part:4},
        timeNeed:4,
        building:'makeTable',
    },

    alchemyTable:{
        name:'炼金台',
        desc:'可以提炼各种药剂。',
        require:{wood:10,part:5},
        timeNeed:4,
        building:'makeTable',
    },
    magicTable:{
        name:'秘术台',
        desc:'可以研制魔法武器与卷轴。',
        require:{wood:10,gem:2},
        timeNeed:4,
        building:'makeTable',
    },
    scienceTable:{
        name:'科研台',
        desc:'可以研发各种科技。',
        require:{wood:10,part:5},
        timeNeed:4,
    },
    alco:{
        name:'酿酒桶',
        desc:'可以酿造酒。',
        require:{wood:10,iron:5},
        timeNeed:4,
        building:'cooker'
    },
    cooker:{
        name:'炊具',
        desc:'允许你烹饪食物。',
        require:{wood:10,iron:5},
        timeNeed:4,
    },
    well:{
        name:'井',
        desc:'源源不断的水将从这里溢出。',
        require:{pickaxe:3,wood:10},
        timeNeed:4,
        building:'makeTable',
    },
    farm:{
        name:'农田',
        desc:'可以种植农作物。',
        require:{wood:10,fertilizer:10},
        timeNeed:4,
        building:'makeTable',
    },
    toilet:{
        name:'卫生间',
        desc:'可以收集粪便，升级后可以洗澡。',
        require:{wood:10,part:5},
        timeNeed:4,
        building:'makeTable',
    },
    sleepPlace:{
        name:'床铺',
        desc:'你可以在这里回复体力与精力。',
        require:{bark:2},
        timeNeed:4,
    },
    bigBox:{
        name:'大箱子',
        desc:'存放许多东西。',
        require:{wood:12},
        timeNeed:4,
    },
};
var BUILDING_UPDATE_DATA = {
    cookerUpdate:{
        cooker_1:{
            timeNeed:4,
            require:{"iron":4,'wood':4},
        },
        cooker_2:{
            timeNeed:4,
            require:{"iron":20,'wood':20},
            science:'cooker_1',
        },
        cooker_3:{
            timeNeed:4,
            require:{"iron":80,'wood':80},
            science:'cooker_2',
        },
        cooker_4:{
            timeNeed:4,
            require:{"gold":80,'wood':160},
            science:'cooker_3',
        },
        cooker_5:{
            timeNeed:4,
            require:{"gold":200,'wood':200},
            science:'cooker_4',
        },
    },
    wellUpdate:{
        wellDig_1:{
            timeNeed:4,
            require:{"pickaxe":1,'wood':4},
        },
        wellDig_2:{
            timeNeed:4,
            require:{"pickaxe":2,'wood':5},
            science:'wellDig_1'
        },
        wellDig_3:{
            timeNeed:4,
            require:{"pickaxe":3,'wood':6},
            science:'wellDig_2'
        },
        wellDig_4:{
            timeNeed:4,
            require:{"pickaxe":5,'wood':7},
            science:'wellDig_3'
        },
        wellDig_5:{
            timeNeed:4,
            require:{"pickaxe":7,'wood':8},
            science:'wellDig_4'
        },
        wellDig_6:{
            timeNeed:4,
            require:{"pickaxe":10,'wood':10},
            science:'wellDig_5'
        },
    },
    bigBoxUpdate:{
        bigBoxSize_1:{
            timeNeed:4,
            require:{"part":4,'wood':4}
        },
        bigBoxSize_2:{
            timeNeed:4,
            require:{"part":8,'wood':8},
            science:'bigBoxSize_1'
        },
        bigBoxSize_3:{
            timeNeed:4,
            require:{"part":12,'wood':12},
            science:'bigBoxSize_2'
        },
        bigBoxSize_4:{
            timeNeed:4,
            require:{"part":20,'wood':20},
            science:'bigBoxSize_3'
        },
        bigBoxSize_5:{
            timeNeed:4,
            require:{"part":32,'wood':32},
            science:'bigBoxSize_4'
        },
        bigBoxSize_6:{
            timeNeed:4,
            require:{"part":48,'wood':48},
            science:'bigBoxSize_5'
        },
        bigBoxSize_7:{
            timeNeed:4,
            require:{"part":64,'wood':64},
            science:'bigBoxSize_6'
        },
        bigBoxSize_8:{
            timeNeed:4,
            require:{"part":96,'wood':96},
            science:'bigBoxSize_7'
        },
        bigBoxSize_9:{
            timeNeed:4,
            require:{"part":128,'wood':128},
            science:'bigBoxSize_8'
        },
        bigBoxSize_10:{
            timeNeed:4,
            require:{"part":160,'wood':160},
            science:'bigBoxSize_9'
        },
        bigBoxSize_11:{
            timeNeed:4,
            require:{"part":192,'wood':192},
            science:'bigBoxSize_10'
        },
        bigBoxSize_12:{
            timeNeed:4,
            require:{"part":256,'wood':256},
            science:'bigBoxSize_11'
        },
        bigBoxSize_13:{
            timeNeed:4,
            require:{"part":288,'wood':288},
            science:'bigBoxSize_12'
        },
        bigBoxSize_14:{
            timeNeed:4,
            require:{"part":320,'wood':320},
            science:'bigBoxSize_13'
        },
        bigBoxSize_15:{
            timeNeed:4,
            require:{"part":352,'wood':352},
            science:'bigBoxSize_14'
        },
        bigBoxSize_16:{
            timeNeed:4,
            require:{"part":384,'wood':384},
            science:'bigBoxSize_15'
        },
        bigBoxSize_17:{
            timeNeed:4,
            require:{"part":416,'wood':416},
            science:'bigBoxSize_16'
        },
        bigBoxSize_18:{
            timeNeed:4,
            require:{"part":448,'wood':448},
            science:'bigBoxSize_17'
        },
        bigBoxSize_19:{
            timeNeed:4,
            require:{"part":480,'wood':480},
            science:'bigBoxSize_18'
        },
        bigBoxSize_20:{
            timeNeed:4,
            require:{"part":512,'wood':512},
            science:'bigBoxSize_19'
        },
        bigBoxSize_21:{
            timeNeed:4,
            require:{"part":544,'wood':544},
            science:'bigBoxSize_20'
        },
        bigBoxSize_22:{
            timeNeed:4,
            require:{"part":576,'wood':576},
            science:'bigBoxSize_21'
        },
    },
    toiletUpdate:{
        showerPlace:{
            timeNeed:4,
            require:{"wood":30},
        },
        marshGasTank:{
            timeNeed:4,
            require:{"wood":100},
            science:'showerPlace',
        },
    },
    sleepPlaceUpdate:{
        bed_1:{
            timeNeed:4,
            require:{"wood":20},
        },
        bed_2:{
            timeNeed:4,
            require:{"hay":30},
            science:'bed_1'
        },
        bed_3:{
            timeNeed:4,
            require:{"fur":10,"silk":2},
            science:'bed_2'
        },
        bed_4:{
            timeNeed:4,
            require:{"feather":20,"silk":2},
            science:'bed_3'
        },
    }
}
var TRAP_DATA = {
    antiRogue:{
        desc:'[防盗]',
        require:{gold:1,teeth:2},
        itemGet:{
            'humanMeat':2,
        },
        chance:0,
        science:'antiRogue',
    },
    meatTrap:{
        desc:'[生肉]',
        require:{'meat':1},
        itemGet:{
            'meat':2,
            'teeth':2,
        },
        chance:0.2,
    },
    fruitTrap:{
        desc:'[浆果]',
        require:{'fruit':2},
        itemGet:{
            'meat':2,
            'feather':2,
        },
        chance:0.3,
    },
    vegTrap:{
        desc:'[生菜]',
        require:{'veg':2},
        itemGet:{
            'meat':2,
            'shit':2,
        },
        chance:0.3,
    },
    carrotTrap:{
        desc:'[胡萝]',
        require:{'carrot':2},
        itemGet:{
            'meat':2,
            'fur':2,
        },
        chance:0.3,
    },
    seedTrap:{
        desc:'[种子]',
        require:{'seed':2},
        itemGet:{
            'meat':2,
            'wing':2,
        },
        chance:0.1,
    }
}
var CROP_DATA = {
    wheatCrop:{
        desc:'[小麦]',
        timeMax:96,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'wheat',
        itemAmount:24,
    },
    fruitCrop:{
        desc:'[浆果]',
        timeMax:96,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'fruit',
        itemAmount:24,
    },
    vegCrop:{
        desc:'[生菜]',
        timeMax:96,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'veg',
        itemAmount:24,
    },
    carrotCrop:{
        desc:'[胡萝]',
        timeMax:96,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'carrot',
        itemAmount:24,
    },
    herbCrop:{
        desc:'[草药]',
        timeMax:88,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'herb',
        itemAmount:24,
    },
    hayCrop:{
        desc:'[牧草]',
        timeMax:88,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'hoe':1},
        itemGet:'hay',
        itemAmount:30,
    },
    iceCrop:{
        desc:'[冰露]',
        timeMax:72,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'ice',
        itemAmount:20,
    },
    fireCrop:{
        desc:'[火草]',
        timeMax:72,
        timeNeed:1,
        require:{'fertilizer':4,'seed':10,'water':2,'hoe':1},
        itemGet:'fire',
        itemAmount:20,
    },
    wood:{
        desc:'[榕树]',
        timeMax:178,
        timeNeed:1,
        require:{'wood':5,'water':20},
        itemGet:'wood',
        itemAmount:80,
    },
}
var ALCO_DATA = {
    fruitAlco:{
        desc:'[果酒]',
        timeMax:72,
        timeNeed:1,
        require:{'fruit':6,'water':6},
        itemGet:'fruitAlco',
        itemAmount:4,
    },
    beer:{
        desc:'[麦酒]',
        timeMax:72,
        timeNeed:1,
        require:{'wheat':6,'water':6},
        itemGet:'beer',
        itemAmount:4,
    },
    alco_beer:{
        desc:'[纯化]',
        timeMax:72,
        timeNeed:1,
        require:{'beer':4},
        itemGet:'alco',
        itemAmount:4,
    },
    alco_fruitAlco:{
        desc:'[纯化]',
        timeMax:72,
        timeNeed:1,
        require:{'fruitAlco':4},
        itemGet:'alco',
        itemAmount:4,
    },
}
var STATE_DATA = {
    temp:{
        name:'体温',
    },
    full:{
        name:'满腹',
        desc:'饮食一直是冒险者们头疼的问题。满腹度会随着时间的流逝慢慢下降。',
    },
    moist:{
        name:'水分',
        desc:'饮食一直是冒险者们头疼的问题。水分会随着时间的流逝慢慢下降。',
    },
    hp:{
        name:'生命',
        desc:'只要进行战斗，就很难避免受伤，出门在外可以多准备一些药剂。',
    },
    ps:{
        name:'体力',
        desc:'从户外获取资源几乎都需要体力的消耗。回家睡一觉就能很快恢复体力。',
    },
    san:{
        name:'精神',
        desc:'精神影响着你的战斗士气。在外熬夜或者状态低下均容易造成精神萎靡。',
    },
}
var COOK_DATA = [
    {name:"magicBread",require:["bread","dust"]},

    {name:"iceWater",require:["water","ice"]},
    {name:"fireWater",require:["water","fire"]},

    {name:"hotWater",require:["water","wood"]},
    {name:"hotCoffee",require:["coffee","wood"]},
    {name:"salad",require:["flower","seed"]},
    {name:"salad",require:["veg","seed"]},
    {name:"salad",require:["veg","flower"]},
    {name:"salad",require:["veg","jam"]},
    {name:"salad",require:["veg","seed"]},
    {name:"salad",require:["seed","jam"]},


    {name:"vegMeat",require:["meat","veg"]},
    {name:"vegMeat",require:["meat","carrot"]},

    {name:"vegSalad",require:["veg","carrot"]},
    {name:"vegSalad",require:["salad","carrot"]},
    {name:"vegSalad",require:["salad","veg"]},
    {name:"vegSalad",require:["fruit","veg"]},

    {name:"meatSoap",require:["meat","water"]},

    {name:"vegSoap",require:["veg","water"]},
    {name:"vegSoap",require:["carrot","water"]},

    {name:"coffee",require:["water","seed"]},
    {name:"vodka",require:["water","alco"]},
    {name:"cocktail",require:["fruit","alco"]},
    {name:"juice",require:["water","fruit"]},
    {name:"juice",require:["water","jam"]},

    {name:"jam",require:["flower","fruit"]},
    {name:"jam",require:["seed","fruit"]},
    {name:"jam",require:["salad","fruit"]},
    {name:"jam",require:["ice","fruit"]},
    {name:"jam",require:["wheat","fruit"]},

    {name:"flowerTea",require:["water","flower"]},
    {name:"hotFlowerTea",require:["flowerTea","wood"]},
    {name:"jamBread",require:["jam","flour"]},
    {name:"jamBread",require:["jam","bread"]},

    {name:"fruitAlco",require:["juice","alco"]},
    {name:"fruitAlco",require:["juice","vodka"]},
    {name:"fruitAlco",require:["jam","alco"]},
    {name:"fruitAlco",require:["jam","vodka"]},

    {name:"mixJuice",require:["carrot","fruit"]},

    {name:"bread",require:["wheat","water"]},
    {name:"woodBread",require:["wood","bread"]},
    {name:"fruitBread",require:["fruit","bread"]},
    {name:"seedBread",require:["seed","bread"]},
    {name:"seedBread",require:["seed","flour"]},
    {name:"sandwich",require:["bread","veg"]},
    {name:"flowerBread",require:["bread","flower"]},
    {name:"hamburger",require:["bread","meat"]},
    {name:"fishHamburger",require:["bread","fish"]},
    {name:"bigHamburger",require:["hamburger","meat"]},
    {name:"hornBread",require:["horn","bread"]},
    {name:"boneMeat",require:["bone","meat"]},
    {name:"fullFamilyTong",require:["wing","meat"]},
    {name:"beanJelly",require:["herb","water"]},
    {name:"bakeWing",require:["wing","wood"]},
    {name:"boilEgg",require:["spiderEgg","water"]},
    {name:"hotWater",require:["wood","water"]},

    {name:"fishMeat",require:["fish","meat"]},
    {name:"woodFish",require:["fish","wood"]},
    {name:"woodMeat",require:["meat","wood"]},
    {name:"fishSoap",require:["fish","water"]},
    {name:"seafood",require:["fish","jellyfish"]},


    {name:"iceAlco",require:["ice","beer"]},
    {name:"iceAlco",require:["ice","fruitAlco"]},
    {name:"iceAlco",require:["ice","vodka"]},

    {name:"warmAlco",require:["wood","beer"]},
    {name:"warmAlco",require:["wood","fruitAlco"]},
    {name:"warmAlco",require:["wood","vodka"]},

    {name:"humanCook",require:["humanMeat"]},
    {name:"dragonScaleSoap",require:["dragonScale"]},
    {name:"dragonBoneSoap",require:["dragonBone",'water']},

    {name:"rowFish",require:["fish",'knife']},
    {name:"rowJellyfish",require:["jellyfish",'knife']},
    {name:"fishBall",require:["fish",'stick']},
    {name:"meatBall",require:["meat",'stick']},
]
var TRADE_DATA = {
                    gold:{
                        name:'商队',
                        give:'gold',
                        max:200,
                        time:24,
                        day:24,
                    },
                    gold_2:{
                        name:'商船',
                        give:'gold',
                        max:400,
                        time:48,
                        day:48,
                    },
                    gold_3:{
                        name:'巨型商船',
                        give:'gold',
                        max:2000,
                        time:60,
                        day:96,
                    },
                    winterWood:{
                        name:'冬季救援队',
                        give:'wood',
                        season:'winter',
                        max:50,
                        time:24
                    },
                    winterWater:{
                        name:'冬季救援队',
                        give:'hotWater',
                        season:'winter',
                        max:50,
                        time:24
                    },
                    healer:{
                        name:'治疗师',
                        give:'healPotion',
                        max:10,
                        time:24
                    },
                    wood:{
                        name:'伐木工',
                        give:'wood',
                        max:40,
                        time:96
                    },
                    wheat:{
                        name:'农民',
                        give:'wheat',
                        max:40,
                        time:24
                    },
                    carrot:{
                        name:'农民',
                        give:'carrot',
                        max:40,
                        time:24
                    },
                    veg:{
                        name:'农民',
                        give:'veg',
                        max:40,
                        time:24
                    },
                    seed:{
                        name:'种子商贩',
                        give:'seed',
                        max:100,
                        time:96
                    },
                    water:{
                        name:'卖水者',
                        give:'water',
                        max:40,
                        time:96
                    },
                    iron:{
                        name:'矿工',
                        give:'iron',
                        max:40,
                        time:48
                    },
                    crystal:{
                        name:'矿工',
                        give:'crystal',
                        max:6,
                        time:48
                    },
                    gem:{
                        name:'矿工',
                        give:'gem',
                        max:3,
                        time:48
                    },
                    powder:{
                        name:'火药商',
                        give:'powder',
                        max:100,
                        time:48
                    },
                    bullet:{
                        name:'军火商',
                        give:'bullet',
                        max:100,
                        time:48
                    },
                    arrow:{
                        name:'贩箭者',
                        give:'arrow',
                        max:80,
                        time:48
                    },
                    part:{
                        name:'工匠',
                        give:'part',
                        max:40,
                        time:72
                    },
                    meat:{
                        name:'猎人',
                        give:'meat',
                        max:40,
                        time:24
                    },
                    fur:{
                        name:'猎人',
                        give:'fur',
                        max:10,
                        time:24
                    },
                    wing:{
                        name:'猎人',
                        give:'wing',
                        max:40,
                        time:24
                    },
                    farmUpgrade:{
                        name:'种植大师',
                        give:'farmUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    strUpgrade:{
                        name:'击剑教头',
                        give:'strUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    shootUpgrade:{
                        name:'王牌猎人',
                        give:'shootUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    defUpgrade:{
                        name:'防御大师',
                        give:'defUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    agileUpgrade:{
                        name:'迅捷忍者',
                        give:'agileUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    alcoUpgrade:{
                        name:'酿酒大师',
                        give:'alcoUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },
                    magicUpgrade:{
                        name:'黑衣贤者',
                        give:'magicUpgrade',
                        max:1,
                        time:24,
                        day:50,
                        type:'upgrade',
                    },

                    scroll:{
                        name:'卷轴商人',
                        give:'scroll',
                        max:2,
                        type:'dungeon',
                    },
                    hpPotion:{
                        name:'药剂师',
                        give:'hpPotion',
                        max:10,
                        type:'dungeon',
                    },
                    healPotion:{
                        name:'药剂师',
                        give:'healPotion',
                        max:10,
                        type:'dungeon',
                    },
                    psPotion:{
                        name:'药剂师',
                        give:'psPotion',
                        max:10,
                        type:'dungeon',
                    },
}
var SKILL_DATA = {
    greedy:{
        isTalent:true,
        name:"拾荒者",
        desc:'每一级使得拾荒以及采集获得的物品增加(100%)。',
        buff:1,
        cost:1,
        costInc:2,
    },
    lucky:{
        isTalent:true,
        name:"幸运儿",
        desc:'每一级使得敌人材料掉落增加(50%)。',
        buff:0.5,
        cost:2,
        costInc:2,
    },
    durable:{
        isTalent:true,
        name:"耐久强化",
        desc:'每一级使得精神和体力的最大值提升(100%)。',
        buff:1,
        cost:1,
        costInc:2,
    },
    physique:{
        isTalent:true,
        name:"体能强化",
        desc:'每一级使得生命、水分、满腹的最大值各提升(100%)。',
        buff:1,
        cost:2,
        costInc:2,
    },
    seller:{
        isTalent:true,
        name:"商业大亨",
        desc:'每一级使得商人最大交易量增加(100%)。',
        buff:1,
        cost:1,
        costInc:2,
    },
    manage:{
        isTalent:true,
        name:"经营手腕",
        desc:'每一级使得建筑产出速度加快(100%)。',
        buff:1,
        cost:2,
        costInc:2,
    },
    fighter:{
        isTalent:true,
        name:"战斗专家",
        desc:'每一级使得伤害额外增加(100%)。',
        buff:1,
        cost:3,
        costInc:2,
    },

    blood:{
        name:'嗜血',
        desc:'当你获得胜利时，将恢复20%的生命。',
        buff:0.2,
        one:true,
    },
    absorb:{
        name:'吸收',
        desc:'当你获得胜利时，将恢复20%的精神。',
        buff:0.2,
        one:true,
    },
    melee:{
        name:'格斗技巧',
        desc:'每一级使你的近战伤害增加15%。',
        buff:0.15,
    },
    shoot:{
        name:'射击技巧',
        desc:'每一级使你的远程伤害增加15%。',
        buff:0.15,
    },
    def:{
        name:'防御技巧',
        desc:'每一级使你所受的伤害减少10%。',
        buff:0.9,
    },
    agile:{
        name:'敏捷技巧',
        desc:'每一级使你的射程加成1。',
        buff:1,
    },
    farm:{
        name:'耕种技巧',
        desc:'每一级使你的农作物额外获得10%的产量。',
        buff:0.1,
    },
    alco:{
        name:'酿酒技巧',
        desc:'每一级使你的酿酒额外获得15%的产量。',
        buff:0.15,
    },
    magic:{
        name:'魔法技巧',
        desc:'每一级使你的魔法伤害增加15%。',
        buff:0.15,
    },
}
var TEMP_DATA = {
        veryHot :{name:'酷暑',desc:'迅速地流失大量水分。'},
        hot     :{name:'炎热',desc:'轻易地流失水分。'},
        warm    :{name:'温暖',desc:'开始感觉到温热了。'},
        nice    :{name:'舒适',desc:'这是最为舒适的温度。'},
        cool    :{name:'微凉',desc:'开始感觉到凉意了。'},
        cold    :{name:'寒冷',desc:'开始流失体力值，之后便会侵蚀生命。'},
        veryCold:{name:'极寒',desc:'迅速流失体力值，之后便会侵蚀生命。'},
}
var EQUIP_TYPE_DATA = {
    body:'身体',
    hand:'手',
    foot:'足',
    head:'头',
    neck:'颈',
}

//游戏剧本初始化数据//////////////////////////////////////////////////////////////////////

//建筑数据的初始化1
var BUILDING_INIT = {
    build:{
        own:true
    },
    sleepPlace:{
    },
    bigBox:{
    },
    makeTable:{
    },
    alchemyTable:{
    },
    magicTable:{
    },
    scienceTable:{
    },
    trap:{
        list:[
        ],
        size:2,
        hint:false,
    },
    farm:{
        list:[
        ],
        size:2,
        hint:false,
    },
    alco:{
        list:[
        ],
        size:2,
        hint:false,
    },
    cooker:{
    },
    well:{
    },
    toilet:{
    },
}
for(var attr in BUILDING_INIT){
    if(BUILDING_INIT[attr].own == undefined){
        BUILDING_INIT[attr].own = MODE=='DEBUG'?true : false;
        // BUILDING_INIT[attr].own =  false;
    }
}
//物品初始化
var BOX_INIT = {
    bag:{
        things:{
            axe     :1,
            water   :2,
            bread   :2,
        },
        size:BAG_BASE_SIZE
    },
    makeTable:{
        things:{
        },
        size:1,
        isDone:true,
    },
    scienceTable:{
        things:{
        },
        size:1000,
        isDone:true,
    },
    alchemyTable:{
        things:{
        },
        size:1,
        isDone:true,
    },
    magicTable:{
        things:{
        },
        size:1,
        isDone:true,
    },
    cooker:{
        things:{
        },
        size:2
    },
    cooked:{
        things:{
        },
        size:1,
        isDone:true,
    },
    well:{
        things:{
            water:10,
        },
        size:1,
        isDone:true,
    },
    bigBox:{
        things:{
        },
        size:BIG_BOX_BASE_SIZE
    },
    register:{
        things:{
        },
        size:100
    },
    shit:{
        things:{
        },
        size:1,
        isDone:true,
    },
    wellUpdate:{
        things:{
        },
        size:100,
        isDone:true,
    },
    cookerUpdate:{
        things:{
        },
        size:100,
        isDone:true,
    },
    toiletUpdate:{
        things:{
        },
        size:100,
        isDone:true,
    },
    bigBoxUpdate:{
        things:{
        },
        size:100,
        isDone:true,
    },
    sleepPlaceUpdate:{
        things:{
        },
        size:100,
        isDone:true,
    },
    marshGasTank:{
        things:{
        },
        size:4,
    },
}
//获取所有科技
if(MODE == 'DEBUG'){
    for(var attr in SCIENCE_DATA){
        BOX_INIT.scienceTable.things[attr] = 1;
    }
    BOX_INIT.bag.things.iron        = 1001;
    BOX_INIT.bag.things.herb        = 1001;
    BOX_INIT.bag.things.water       = 1001;
    BOX_INIT.bag.things.scroll      = 1001;
    BOX_INIT.bag.things.dungeonKey  = 1001;
    BOX_INIT.bag.things.dungeonRope = 1001;
    BOX_INIT.bag.things.poizon      = 1001;
    BOX_INIT.bag.things.spiderHead  = 1001;
    BOX_INIT.bag.things.wood        = 1001;
    BOX_INIT.bag.things.gold        = 1001;
    BOX_INIT.bag.things.rope        = 1001;
    BOX_INIT.bag.things.hoe         = 1001;
    BOX_INIT.bag.things.testWeapon  = 1001;
    BOX_INIT.bag.things.mithril     = 1001;
    BOX_INIT.bag.things.reiPart     = 1001;
    BOX_INIT.bag.things.blood       = 1001;
}
//角色状态初始化
var PLAYER_STATE_INIT = {
    temp:{
        amount:0
    },
    hp:{
        amount:100
    },
    full:{
        amount:100
    },
    moist:{
        amount:100
    },
    ps:{
        amount:100
    },
    san:{
        amount:100
    },
}
//道具耐久度初始化
var DURABLE_INIT = {}
for(var attr in ITEM_DATA){
    if(ITEM_DATA[attr].durable){
        DURABLE_INIT[attr] = 0;
    }
}
//集市商人初始化
var TRADE_INIT = [
    {
        trade:'wood',
        time:200
    },
    {
        trade:'iron',
        time:200
    },
    {
        trade:'part',
        time:200
    }
]
//行动冷却初始化
var COOL_DOWN_INIT = {
    shit:0,
    shower:0,
}
//游戏事件初始化
var EVENT_INIT = {
    tramp:{
        foodGot:0
    },
    townEvent:{
        level:0
    },
}
for (var attr in EVENT_DATA) {
    if(EVENT_INIT[attr] == undefined){
        EVENT_INIT[attr] = {experienced:false}
    }else{
        EVENT_INIT[attr].experienced = false;
    }
};
//地点数据初始化
var PLACE_INIT = {}
for(var attr in PLACE_DATA){
    PLACE_INIT[attr] = {visited:false}
    if(PLACE_DATA[attr].mst){
        PLACE_INIT[attr].mst = {};
        for(var attr_2 in PLACE_DATA[attr].mst){
            PLACE_INIT[attr].mst[attr_2] = {};
            PLACE_INIT[attr].mst[attr_2].amount = PLACE_DATA[attr].mst[attr_2].balancedAmount;
            PLACE_INIT[attr].mst[attr_2].count = 0;
        }
    }
    if(PLACE_DATA[attr].things){
        PLACE_INIT[attr].things = clone(PLACE_DATA[attr].things);
    }
    if(PLACE_DATA[attr].resource){
        PLACE_INIT[attr].resource = {};
        for(var attr_2 in PLACE_DATA[attr].resource){
            PLACE_INIT[attr].resource[attr_2] = {};
            PLACE_INIT[attr].resource[attr_2].amount = PLACE_DATA[attr].resource[attr_2].initAmount;
            PLACE_INIT[attr].resource[attr_2].count = 0;
        }
    }
}
//调试模式
if(MODE == 'DEBUG'){
    for(var attr in PLACE_DATA){
        delete PLACE_DATA[attr].science;
        delete PLACE_DATA[attr].season;
    }
}

var ROBBER_DATA = {
    _robber:{
        hpInc:2,
        dmgInc:0.2,
        stole:0.5,
    },
}
var ROBBER_INIT = {
                lastDate:50,
                stoled:{},
                stoledAll:{},
                robber:false,
            };
var DEBUG_SKILL = {
                def:0,
                melee:0,
                magic:0,
            }
