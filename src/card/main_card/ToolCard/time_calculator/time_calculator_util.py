from datetime import datetime, timedelta
from PySide6.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QComboBox, QGroupBox, QScrollArea, QSpinBox)
from PySide6.QtCore import QTimer
import pytz

from src.module import dialog_module
from src.ui import style_util

timezones = [
    "UTC+00:00 Africa/Abidjan - 阿比让",
    "UTC+00:00 Africa/Accra - 阿克拉",
    "UTC+00:00 Africa/Bamako - 巴马科",
    "UTC+00:00 Africa/Banjul - 班珠尔",
    "UTC+00:00 Africa/Bissau - 比绍",
    "UTC+00:00 Africa/Conakry - 科纳克里",
    "UTC+00:00 Africa/Dakar - 达喀尔",
    "UTC+00:00 Africa/Freetown - 弗里敦",
    "UTC+00:00 Africa/Lome - 洛美",
    "UTC+00:00 Africa/Monrovia - 蒙罗维亚",
    "UTC+00:00 Africa/Nouakchott - 努瓦克肖特",
    "UTC+00:00 Africa/Ouagadougou - 瓦加杜古",
    "UTC+00:00 Africa/Sao_Tome - 圣多美",
    "UTC+00:00 America/Danmarkshavn - 丹马沙文",
    "UTC+00:00 Atlantic/Azores - 亚速尔群岛",
    "UTC+00:00 Atlantic/Reykjavik - 雷克雅未克",
    "UTC+00:00 Atlantic/St_Helena - 圣赫勒拿",
    "UTC+00:00 Etc/UTC - 协调世界时UTC",
    "UTC+01:00 Africa/Algiers - 阿尔及尔",
    "UTC+01:00 Africa/Bangui - 班吉",
    "UTC+01:00 Africa/Brazzaville - 布拉柴维尔",
    "UTC+01:00 Africa/Casablanca - 卡萨布兰卡",
    "UTC+01:00 Africa/Douala - 杜阿拉",
    "UTC+01:00 Africa/El_Aaiun - 阿尤恩",
    "UTC+01:00 Africa/Kinshasa - 金沙萨",
    "UTC+01:00 Africa/Lagos - 拉各斯",
    "UTC+01:00 Africa/Libreville - 利伯维尔",
    "UTC+01:00 Africa/Luanda - 罗安达",
    "UTC+01:00 Africa/Malabo - 马拉博",
    "UTC+01:00 Africa/Ndjamena - 恩贾梅纳",
    "UTC+01:00 Africa/Niamey - 尼亚美",
    "UTC+01:00 Africa/Porto-Novo - 波多诺伏",
    "UTC+01:00 Africa/Tunis - 突尼斯",
    "UTC+01:00 Atlantic/Canary - 加那利",
    "UTC+01:00 Atlantic/Faeroe - 法罗",
    "UTC+01:00 Atlantic/Madeira - 马德拉",
    "UTC+01:00 Europe/Dublin - 都柏林",
    "UTC+01:00 Europe/Guernsey - 根西岛",
    "UTC+01:00 Europe/Isle_of_Man - 曼岛",
    "UTC+01:00 Europe/Jersey - 泽西岛",
    "UTC+01:00 Europe/Lisbon - 里斯本",
    "UTC+01:00 Europe/London - 伦敦",
    "UTC+02:00 Africa/Blantyre - 布兰太尔",
    "UTC+02:00 Africa/Bujumbura - 布琼布拉",
    "UTC+02:00 Africa/Ceuta - 休达",
    "UTC+02:00 Africa/Gaborone - 哈博罗内",
    "UTC+02:00 Africa/Harare - 哈拉雷",
    "UTC+02:00 Africa/Johannesburg - 约翰内斯堡",
    "UTC+02:00 Africa/Juba - 朱巴",
    "UTC+02:00 Africa/Khartoum - 喀土穆",
    "UTC+02:00 Africa/Kigali - 基加利",
    "UTC+02:00 Africa/Lubumbashi - 卢本巴希",
    "UTC+02:00 Africa/Lusaka - 卢萨卡",
    "UTC+02:00 Africa/Maputo - 马普托",
    "UTC+02:00 Africa/Maseru - 马塞卢",
    "UTC+02:00 Africa/Mbabane - 姆巴巴纳",
    "UTC+02:00 Africa/Tripoli - 的黎波里",
    "UTC+02:00 Africa/Windhoek - 温得和克",
    "UTC+02:00 Antarctica/Troll - 特罗尔",
    "UTC+02:00 Arctic/Longyearbyen - 朗伊尔城",
    "UTC+02:00 Europe/Amsterdam - 阿姆斯特丹",
    "UTC+02:00 Europe/Andorra - 安道尔",
    "UTC+02:00 Europe/Belgrade - 贝尔格莱德",
    "UTC+02:00 Europe/Berlin - 柏林",
    "UTC+02:00 Europe/Bratislava - 布拉迪斯拉发",
    "UTC+02:00 Europe/Brussels - 布鲁塞尔",
    "UTC+02:00 Europe/Budapest - 布达佩斯",
    "UTC+02:00 Europe/Busingen - 布辛根",
    "UTC+02:00 Europe/Copenhagen - 哥本哈根",
    "UTC+02:00 Europe/Gibraltar - 直布罗陀",
    "UTC+02:00 Europe/Kaliningrad - 加里宁格勒",
    "UTC+02:00 Europe/Ljubljana - 卢布尔雅那",
    "UTC+02:00 Europe/Luxembourg - 卢森堡",
    "UTC+02:00 Europe/Madrid - 马德里",
    "UTC+02:00 Europe/Malta - 马耳他",
    "UTC+02:00 Europe/Monaco - 摩纳哥",
    "UTC+02:00 Europe/Oslo - 奥斯陆",
    "UTC+02:00 Europe/Paris - 巴黎",
    "UTC+02:00 Europe/Podgorica - 波德戈里察",
    "UTC+02:00 Europe/Prague - 布拉格",
    "UTC+02:00 Europe/Rome - 罗马",
    "UTC+02:00 Europe/San_Marino - 圣马力诺",
    "UTC+02:00 Europe/Sarajevo - 萨拉热窝",
    "UTC+02:00 Europe/Skopje - 斯科普里",
    "UTC+02:00 Europe/Stockholm - 斯德哥尔摩",
    "UTC+02:00 Europe/Tirane - 地拉那",
    "UTC+02:00 Europe/Vaduz - 瓦杜兹",
    "UTC+02:00 Europe/Vatican - 梵蒂冈",
    "UTC+02:00 Europe/Vienna - 维也纳",
    "UTC+02:00 Europe/Warsaw - 华沙",
    "UTC+02:00 Europe/Zagreb - 萨格勒布",
    "UTC+02:00 Europe/Zurich - 苏黎世",
    "UTC+03:00 Africa/Addis_Ababa - 亚的斯亚贝巴",
    "UTC+03:00 Africa/Asmera - 阿斯马拉",
    "UTC+03:00 Africa/Cairo - 开罗",
    "UTC+03:00 Africa/Dar_es_Salaam - 达累斯萨拉姆",
    "UTC+03:00 Africa/Djibouti - 吉布提",
    "UTC+03:00 Africa/Kampala - 坎帕拉",
    "UTC+03:00 Africa/Mogadishu - 摩加迪沙",
    "UTC+03:00 Africa/Nairobi - 内罗毕",
    "UTC+03:00 Antarctica/Syowa - 昭和",
    "UTC+03:00 Asia/Aden - 亚丁",
    "UTC+03:00 Asia/Amman - 安曼",
    "UTC+03:00 Asia/Baghdad - 巴格达",
    "UTC+03:00 Asia/Bahrain - 巴林",
    "UTC+03:00 Asia/Beirut - 贝鲁特",
    "UTC+03:00 Asia/Damascus - 大马士革",
    "UTC+03:00 Asia/Famagusta - 法马古斯塔",
    "UTC+03:00 Asia/Gaza - 加沙",
    "UTC+03:00 Asia/Hebron - 希伯伦",
    "UTC+03:00 Asia/Jerusalem - 耶路撒冷",
    "UTC+03:00 Asia/Kuwait - 科威特",
    "UTC+03:00 Asia/Nicosia - 尼科西亚",
    "UTC+03:00 Asia/Qatar - 卡塔尔",
    "UTC+03:00 Asia/Riyadh - 利雅得",
    "UTC+03:00 Europe/Athens - 雅典",
    "UTC+03:00 Europe/Bucharest - 布加勒斯特",
    "UTC+03:00 Europe/Chisinau - 基希讷乌",
    "UTC+03:00 Europe/Helsinki - 赫尔辛基",
    "UTC+03:00 Europe/Istanbul - 伊斯坦布尔",
    "UTC+03:00 Europe/Kiev - 基辅",
    "UTC+03:00 Europe/Kirov - 基洛夫",
    "UTC+03:00 Europe/Mariehamn - 玛丽港",
    "UTC+03:00 Europe/Minsk - 明斯克",
    "UTC+03:00 Europe/Moscow - 莫斯科",
    "UTC+03:00 Europe/Riga - 里加",
    "UTC+03:00 Europe/Simferopol - 辛菲罗波尔",
    "UTC+03:00 Europe/Sofia - 索非亚",
    "UTC+03:00 Europe/Tallinn - 塔林",
    "UTC+03:00 Europe/Uzhgorod - 乌日哥罗德",
    "UTC+03:00 Europe/Vilnius - 维尔纽斯",
    "UTC+03:00 Europe/Volgograd - 伏尔加格勒",
    "UTC+03:00 Europe/Zaporozhye - 扎波罗热",
    "UTC+03:00 Indian/Antananarivo - 安塔那那利佛",
    "UTC+03:00 Indian/Comoro - 科摩罗",
    "UTC+03:00 Indian/Mayotte - 马约特",
    "UTC+03:30 Asia/Tehran - 德黑兰",
    "UTC+04:00 Asia/Baku - 巴库",
    "UTC+04:00 Asia/Dubai - 迪拜",
    "UTC+04:00 Asia/Muscat - 马斯喀特",
    "UTC+04:00 Asia/Tbilisi - 第比利斯",
    "UTC+04:00 Asia/Yerevan - 埃里温",
    "UTC+04:00 Europe/Astrakhan - 阿斯特拉罕",
    "UTC+04:00 Europe/Samara - 萨马拉",
    "UTC+04:00 Europe/Saratov - 萨拉托夫",
    "UTC+04:00 Europe/Ulyanovsk - 乌里扬诺夫斯克",
    "UTC+04:00 Indian/Mahe - 马埃岛",
    "UTC+04:00 Indian/Mauritius - 毛里求斯",
    "UTC+04:00 Indian/Reunion - 留尼汪",
    "UTC+04:30 Asia/Kabul - 喀布尔",
    "UTC+05:00 Antarctica/Mawson - 莫森",
    "UTC+05:00 Antarctica/Vostok - 沃斯托克",
    "UTC+05:00 Asia/Almaty - 阿拉木图",
    "UTC+05:00 Asia/Aqtau - 阿克套",
    "UTC+05:00 Asia/Aqtobe - 阿克托别",
    "UTC+05:00 Asia/Ashgabat - 阿什哈巴德",
    "UTC+05:00 Asia/Atyrau - 阿特劳",
    "UTC+05:00 Asia/Dushanbe - 杜尚别",
    "UTC+05:00 Asia/Karachi - 卡拉奇",
    "UTC+05:00 Asia/Oral - 乌拉尔",
    "UTC+05:00 Asia/Qyzylorda - 克孜洛尔达",
    "UTC+05:00 Asia/Samarkand - 撒马尔罕",
    "UTC+05:00 Asia/Tashkent - 塔什干",
    "UTC+05:00 Asia/Yekaterinburg - 叶卡捷琳堡",
    "UTC+05:00 Indian/Kerguelen - 凯尔盖朗",
    "UTC+05:00 Indian/Maldives - 马尔代夫",
    "UTC+05:30 Asia/Calcutta - 加尔各答",
    "UTC+05:30 Asia/Colombo - 科伦坡",
    "UTC+05:45 Asia/Katmandu - 加德满都",
    "UTC+06:00 Asia/Bishkek - 比什凯克",
    "UTC+06:00 Asia/Dhaka - 达卡",
    "UTC+06:00 Asia/Omsk - 鄂木斯克",
    "UTC+06:00 Asia/Thimphu - 廷布",
    "UTC+06:00 Asia/Urumqi - 乌鲁木齐",
    "UTC+06:00 Indian/Chagos - 查戈斯",
    "UTC+06:30 Asia/Rangoon - 仰光",
    "UTC+06:30 Indian/Cocos - 可可斯",
    "UTC+07:00 Antarctica/Davis - 戴维斯",
    "UTC+07:00 Asia/Bangkok - 曼谷",
    "UTC+07:00 Asia/Barnaul - 巴尔瑙尔",
    "UTC+07:00 Asia/Hovd - 科布多",
    "UTC+07:00 Asia/Jakarta - 雅加达",
    "UTC+07:00 Asia/Krasnoyarsk - 克拉斯诺亚尔斯克",
    "UTC+07:00 Asia/Novokuznetsk - 新库兹涅茨克",
    "UTC+07:00 Asia/Novosibirsk - 诺沃西比尔斯克",
    "UTC+07:00 Asia/Phnom_Penh - 金边",
    "UTC+07:00 Asia/Pontianak - 坤甸",
    "UTC+07:00 Asia/Saigon - 胡志明市",
    "UTC+07:00 Asia/Tomsk - 托木斯克",
    "UTC+07:00 Asia/Vientiane - 万象",
    "UTC+07:00 Indian/Christmas - 圣诞岛",
    "UTC+08:00 Antarctica/Casey - 卡塞",
    "UTC+08:00 Asia/Brunei - 文莱",
    "UTC+08:00 Asia/Choibalsan - 乔巴山",
    "UTC+08:00 Asia/Hong_Kong - 香港",
    "UTC+08:00 Asia/Irkutsk - 伊尔库茨克",
    "UTC+08:00 Asia/Kuala_Lumpur - 吉隆坡",
    "UTC+08:00 Asia/Kuching - 古晋",
    "UTC+08:00 Asia/Macau - 澳门",
    "UTC+08:00 Asia/Makassar - 望加锡",
    "UTC+08:00 Asia/Manila - 马尼拉",
    "UTC+08:00 Asia/Shanghai - 上海",
    "UTC+08:00 Asia/Singapore - 新加坡",
    "UTC+08:00 Asia/Taipei - 台北",
    "UTC+08:00 Asia/Ulaanbaatar - 乌兰巴托",
    "UTC+08:00 Australia/Perth - 珀斯",
    "UTC+08:45 Australia/Eucla - 尤克拉",
    "UTC+09:00 Asia/Chita - 赤塔",
    "UTC+09:00 Asia/Dili - 帝力",
    "UTC+09:00 Asia/Jayapura - 查亚普拉",
    "UTC+09:00 Asia/Khandyga - 汉德加",
    "UTC+09:00 Asia/Pyongyang - 平壤",
    "UTC+09:00 Asia/Seoul - 首尔",
    "UTC+09:00 Asia/Tokyo - 东京",
    "UTC+09:00 Asia/Yakutsk - 雅库茨克",
    "UTC+09:00 Pacific/Palau - 帕劳",
    "UTC+09:30 Australia/Adelaide - 阿德莱德",
    "UTC+09:30 Australia/Broken_Hill - 布罗肯希尔",
    "UTC+09:30 Australia/Darwin - 达尔文",
    "UTC+10:00 Antarctica/DumontDUrville - 迪蒙迪尔维尔",
    "UTC+10:00 Antarctica/Macquarie - 麦格理",
    "UTC+10:00 Asia/Ust-Nera - 乌斯内拉",
    "UTC+10:00 Asia/Vladivostok - 符拉迪沃斯托克",
    "UTC+10:00 Australia/Brisbane - 布里斯班",
    "UTC+10:00 Australia/Currie - 库利",
    "UTC+10:00 Australia/Hobart - 霍巴特",
    "UTC+10:00 Australia/Lindeman - 林德曼",
    "UTC+10:00 Australia/Melbourne - 墨尔本",
    "UTC+10:00 Australia/Sydney - 悉尼",
    "UTC+10:00 Pacific/Guam - 关岛",
    "UTC+10:00 Pacific/Port_Moresby - 莫尔兹比港",
    "UTC+10:00 Pacific/Saipan - 塞班",
    "UTC+10:00 Pacific/Truk - 特鲁克群岛",
    "UTC+10:30 Australia/Lord_Howe - 豪勋爵",
    "UTC+11:00 Asia/Magadan - 马加丹",
    "UTC+11:00 Asia/Sakhalin - 萨哈林",
    "UTC+11:00 Asia/Srednekolymsk - 中科雷姆斯克",
    "UTC+11:00 Pacific/Bougainville - 布干维尔",
    "UTC+11:00 Pacific/Efate - 埃法特",
    "UTC+11:00 Pacific/Guadalcanal - 瓜达尔卡纳尔",
    "UTC+11:00 Pacific/Kosrae - 库赛埃",
    "UTC+11:00 Pacific/Norfolk - 诺福克",
    "UTC+11:00 Pacific/Noumea - 努美阿",
    "UTC+11:00 Pacific/Ponape - 波纳佩岛",
    "UTC+12:00 Antarctica/McMurdo - 麦克默多",
    "UTC+12:00 Asia/Anadyr - 阿纳德尔",
    "UTC+12:00 Asia/Kamchatka - 堪察加",
    "UTC+12:00 Pacific/Auckland - 奥克兰",
    "UTC+12:00 Pacific/Fiji - 斐济",
    "UTC+12:00 Pacific/Funafuti - 富纳富提",
    "UTC+12:00 Pacific/Kwajalein - 夸贾林",
    "UTC+12:00 Pacific/Majuro - 马朱罗",
    "UTC+12:00 Pacific/Nauru - 瑙鲁",
    "UTC+12:00 Pacific/Tarawa - 塔拉瓦",
    "UTC+12:00 Pacific/Wake - 威克",
    "UTC+12:00 Pacific/Wallis - 瓦利斯",
    "UTC+12:45 Pacific/Chatham - 查塔姆",
    "UTC+13:00 Pacific/Apia - 阿皮亚",
    "UTC+13:00 Pacific/Enderbury - 恩德伯里",
    "UTC+13:00 Pacific/Fakaofo - 法考福",
    "UTC+13:00 Pacific/Tongatapu - 东加塔布",
    "UTC+14:00 Pacific/Kiritimati - 基里地马地岛",
    "UTC-01:00 America/Godthab - 努克",
    "UTC-01:00 America/Scoresbysund - 斯科列斯比桑德",
    "UTC-01:00 Atlantic/Cape_Verde - 佛得角",
    "UTC-02:00 America/Miquelon - 密克隆",
    "UTC-02:00 America/Noronha - 洛罗尼亚",
    "UTC-02:00 Atlantic/South_Georgia - 南乔治亚",
    "UTC-02:30 America/St_Johns - 圣约翰斯",
    "UTC-03:00 America/Araguaina - 阿拉瓜伊纳",
    "UTC-03:00 America/Argentina/La_Rioja - 拉里奥哈",
    "UTC-03:00 America/Argentina/Rio_Gallegos - 里奥加耶戈斯",
    "UTC-03:00 America/Argentina/Salta - 萨尔塔",
    "UTC-03:00 America/Argentina/San_Juan - 圣胡安",
    "UTC-03:00 America/Argentina/San_Luis - 圣路易斯",
    "UTC-03:00 America/Argentina/Tucuman - 图库曼",
    "UTC-03:00 America/Argentina/Ushuaia - 乌斯怀亚",
    "UTC-03:00 America/Asuncion - 亚松森",
    "UTC-03:00 America/Bahia - 巴伊亚",
    "UTC-03:00 America/Belem - 贝伦",
    "UTC-03:00 America/Buenos_Aires - 布宜诺斯艾利斯",
    "UTC-03:00 America/Catamarca - 卡塔马卡",
    "UTC-03:00 America/Cayenne - 卡宴",
    "UTC-03:00 America/Cordoba - 科尔多瓦",
    "UTC-03:00 America/Fortaleza - 福塔雷萨",
    "UTC-03:00 America/Glace_Bay - 格莱斯贝",
    "UTC-03:00 America/Goose_Bay - 古斯湾",
    "UTC-03:00 America/Halifax - 哈利法克斯",
    "UTC-03:00 America/Jujuy - 胡胡伊",
    "UTC-03:00 America/Maceio - 马塞约",
    "UTC-03:00 America/Mendoza - 门多萨",
    "UTC-03:00 America/Moncton - 蒙克顿",
    "UTC-03:00 America/Montevideo - 蒙得维的亚",
    "UTC-03:00 America/Paramaribo - 帕拉马里博",
    "UTC-03:00 America/Punta_Arenas - 蓬塔阿雷纳斯",
    "UTC-03:00 America/Recife - 累西腓",
    "UTC-03:00 America/Santarem - 圣塔伦",
    "UTC-03:00 America/Sao_Paulo - 圣保罗",
    "UTC-03:00 America/Thule - 图勒",
    "UTC-03:00 Antarctica/Palmer - 帕默尔",
    "UTC-03:00 Antarctica/Rothera - 罗瑟拉",
    "UTC-03:00 Atlantic/Bermuda - 百慕大",
    "UTC-03:00 Atlantic/Stanley - 斯坦利",
    "UTC-04:00 America/Anguilla - 安圭拉",
    "UTC-04:00 America/Antigua - 安提瓜",
    "UTC-04:00 America/Aruba - 阿鲁巴",
    "UTC-04:00 America/Barbados - 巴巴多斯",
    "UTC-04:00 America/Blanc-Sablon - 布兰克萨布隆",
    "UTC-04:00 America/Boa_Vista - 博阿维斯塔",
    "UTC-04:00 America/Campo_Grande - 大坎普",
    "UTC-04:00 America/Caracas - 加拉加斯",
    "UTC-04:00 America/Cuiaba - 库亚巴",
    "UTC-04:00 America/Curacao - 库拉索",
    "UTC-04:00 America/Detroit - 底特律",
    "UTC-04:00 America/Dominica - 多米尼加",
    "UTC-04:00 America/Grand_Turk - 大特克",
    "UTC-04:00 America/Grenada - 格林纳达",
    "UTC-04:00 America/Guadeloupe - 瓜德罗普",
    "UTC-04:00 America/Guyana - 圭亚那",
    "UTC-04:00 America/Havana - 哈瓦那",
    "UTC-04:00 America/Indiana/Marengo - 印第安纳州马伦戈",
    "UTC-04:00 America/Indiana/Petersburg - 印第安纳州彼得斯堡",
    "UTC-04:00 America/Indiana/Vevay - 印第安纳州维维市",
    "UTC-04:00 America/Indiana/Vincennes - 印第安纳州温森斯",
    "UTC-04:00 America/Indiana/Winamac - 印第安纳州威纳马克",
    "UTC-04:00 America/Indianapolis - 印第安纳波利斯",
    "UTC-04:00 America/Iqaluit - 伊魁特",
    "UTC-04:00 America/Kentucky/Monticello - 肯塔基州蒙蒂塞洛",
    "UTC-04:00 America/Kralendijk - 克拉伦代克",
    "UTC-04:00 America/La_Paz - 拉巴斯",
    "UTC-04:00 America/Louisville - 路易斯维尔",
    "UTC-04:00 America/Lower_Princes - 下太子区",
    "UTC-04:00 America/Manaus - 马瑙斯",
    "UTC-04:00 America/Marigot - 马里戈特",
    "UTC-04:00 America/Martinique - 马提尼克",
    "UTC-04:00 America/Montserrat - 蒙特塞拉特",
    "UTC-04:00 America/Nassau - 拿骚",
    "UTC-04:00 America/New_York - 纽约",
    "UTC-04:00 America/Nipigon - 尼皮贡",
    "UTC-04:00 America/Pangnirtung - 旁涅唐",
    "UTC-04:00 America/Port-au-Prince - 太子港",
    "UTC-04:00 America/Port_of_Spain - 西班牙港",
    "UTC-04:00 America/Porto_Velho - 波多韦柳",
    "UTC-04:00 America/Puerto_Rico - 波多黎各",
    "UTC-04:00 America/Santiago - 圣地亚哥",
    "UTC-04:00 America/Santo_Domingo - 圣多明各",
    "UTC-04:00 America/St_Barthelemy - 圣巴泰勒米岛",
    "UTC-04:00 America/St_Kitts - 圣基茨",
    "UTC-04:00 America/St_Lucia - 圣卢西亚",
    "UTC-04:00 America/St_Thomas - 圣托马斯",
    "UTC-04:00 America/St_Vincent - 圣文森特",
    "UTC-04:00 America/Thunder_Bay - 桑德贝",
    "UTC-04:00 America/Toronto - 多伦多",
    "UTC-04:00 America/Tortola - 托尔托拉",
    "UTC-05:00 America/Bogota - 波哥大",
    "UTC-05:00 America/Cancun - 坎昆",
    "UTC-05:00 America/Cayman - 开曼",
    "UTC-05:00 America/Chicago - 芝加哥",
    "UTC-05:00 America/Coral_Harbour - 阿蒂科肯",
    "UTC-05:00 America/Eirunepe - 依伦尼贝",
    "UTC-05:00 America/Guayaquil - 瓜亚基尔",
    "UTC-05:00 America/Indiana/Knox - 印第安纳州诺克斯",
    "UTC-05:00 America/Indiana/Tell_City - 印第安纳州特尔城",
    "UTC-05:00 America/Jamaica - 牙买加",
    "UTC-05:00 America/Lima - 利马",
    "UTC-05:00 America/Matamoros - 马塔莫罗斯",
    "UTC-05:00 America/Menominee - 梅诺米尼",
    "UTC-05:00 America/North_Dakota/Beulah - 北达科他州比尤拉",
    "UTC-05:00 America/North_Dakota/Center - 北达科他州申特",
    "UTC-05:00 America/North_Dakota/New_Salem - 北达科他州新塞勒姆",
    "UTC-05:00 America/Ojinaga - 奥希纳加",
    "UTC-05:00 America/Panama - 巴拿马",
    "UTC-05:00 America/Rainy_River - 雷尼河",
    "UTC-05:00 America/Rankin_Inlet - 兰今湾",
    "UTC-05:00 America/Resolute - 雷索卢特",
    "UTC-05:00 America/Rio_Branco - 里奥布郎库",
    "UTC-05:00 America/Winnipeg - 温尼伯",
    "UTC-06:00 America/Bahia_Banderas - 巴伊亚班德拉斯",
    "UTC-06:00 America/Belize - 伯利兹",
    "UTC-06:00 America/Boise - 博伊西",
    "UTC-06:00 America/Cambridge_Bay - 剑桥湾",
    "UTC-06:00 America/Chihuahua - 奇瓦瓦",
    "UTC-06:00 America/Costa_Rica - 哥斯达黎加",
    "UTC-06:00 America/Denver - 丹佛",
    "UTC-06:00 America/Edmonton - 埃德蒙顿",
    "UTC-06:00 America/El_Salvador - 萨尔瓦多",
    "UTC-06:00 America/Guatemala - 危地马拉",
    "UTC-06:00 America/Inuvik - 伊努维克",
    "UTC-06:00 America/Managua - 马那瓜",
    "UTC-06:00 America/Merida - 梅里达",
    "UTC-06:00 America/Mexico_City - 墨西哥城",
    "UTC-06:00 America/Monterrey - 蒙特雷",
    "UTC-06:00 America/Regina - 里贾纳",
    "UTC-06:00 America/Swift_Current - 斯威夫特卡伦特",
    "UTC-06:00 America/Tegucigalpa - 特古西加尔巴",
    "UTC-06:00 America/Yellowknife - 耶洛奈夫",
    "UTC-06:00 Pacific/Easter - 复活节岛",
    "UTC-06:00 Pacific/Galapagos - 加拉帕戈斯",
    "UTC-07:00 America/Creston - 克雷斯顿",
    "UTC-07:00 America/Dawson - 道森",
    "UTC-07:00 America/Dawson_Creek - 道森克里克",
    "UTC-07:00 America/Fort_Nelson - 纳尔逊堡",
    "UTC-07:00 America/Hermosillo - 埃莫西约",
    "UTC-07:00 America/Los_Angeles - 洛杉矶",
    "UTC-07:00 America/Mazatlan - 马萨特兰",
    "UTC-07:00 America/Phoenix - 凤凰城",
    "UTC-07:00 America/Santa_Isabel - 圣伊萨贝尔",
    "UTC-07:00 America/Tijuana - 蒂华纳",
    "UTC-07:00 America/Vancouver - 温哥华",
    "UTC-07:00 America/Whitehorse - 怀特霍斯",
    "UTC-08:00 America/Anchorage - 安克雷奇",
    "UTC-08:00 America/Juneau - 朱诺",
    "UTC-08:00 America/Metlakatla - 梅特拉卡特拉",
    "UTC-08:00 America/Nome - 诺姆",
    "UTC-08:00 America/Sitka - 锡特卡",
    "UTC-08:00 America/Yakutat - 亚库塔特",
    "UTC-08:00 Pacific/Pitcairn - 皮特凯恩",
    "UTC-09:00 America/Adak - 埃达克",
    "UTC-09:00 Pacific/Gambier - 甘比尔",
    "UTC-09:30 Pacific/Marquesas - 马克萨斯",
    "UTC-10:00 Pacific/Honolulu - 檀香山",
    "UTC-10:00 Pacific/Johnston - 约翰斯顿",
    "UTC-10:00 Pacific/Rarotonga - 拉罗汤加",
    "UTC-10:00 Pacific/Tahiti - 塔希提",
    "UTC-11:00 Pacific/Midway - 中途岛",
    "UTC-11:00 Pacific/Niue - 纽埃",
    "UTC-11:00 Pacific/Pago_Pago - 帕果帕果"
]


class TimeCalculatorApp(QWidget):
    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)

        self.main_object = main_object

        # 存储当前选择的时区
        self.current_timezone = pytz.timezone('Asia/Shanghai')

        self.setStyleSheet("background: transparent; border: none; padding: 0px;")

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建主选项卡
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        # 创建当前时间选项卡
        self.current_time_tab = QWidget()
        self.setup_current_time_tab()
        self.tab_widget.addTab(self.current_time_tab, "当前时间")

        # 创建计算器选项卡
        self.calculator_tab = QWidget()
        self.setup_calculator_tab()
        self.tab_widget.addTab(self.calculator_tab, "计算器")

        # 初始化时间更新定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(100)  # 每100毫秒更新一次

        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

        # 设置字体
        style_util.set_font_and_right_click_style(self.main_object, self)

    def setup_current_time_tab(self):
        # 创建滚动区域以适应竖向布局
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 上半部分 - 当前时间展示
        top_group = QGroupBox("当前时间")
        top_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        top_layout = QVBoxLayout()  # 改为垂直布局
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(5, 0, 5, 0)

        # 创建时间显示和按钮 - 改为垂直排列
        self.time_labels = []
        self.copy_buttons = []
        self.load_buttons = []

        labels = ["时间(秒)", "时间(毫秒)", "时间戳(秒)", "时间戳(毫秒)"]
        for i, label in enumerate(labels):
            # 为每个时间类型创建一个水平布局
            time_layout = QHBoxLayout()
            time_layout.setSpacing(3)
            time_layout.setContentsMargins(0, 0, 0, 0)

            # 时间标签
            title_label = QLabel(label)
            title_label.setMaximumWidth(75)
            time_layout.addWidget(title_label)

            # 时间显示标签
            time_label = QLabel()
            time_label.setMinimumHeight(25)
            time_label.setMaximumWidth(150)
            self.time_labels.append(time_label)
            time_layout.addWidget(time_label)

            # 按钮布局
            button_layout = QHBoxLayout()

            # 复制按钮
            copy_btn = QPushButton("复制")
            copy_btn.setMinimumHeight(25)
            copy_btn.setMaximumWidth(50)
            copy_btn.clicked.connect(lambda checked=False, idx=i: self.copy_time_value(idx))
            self.copy_buttons.append(copy_btn)
            button_layout.addWidget(copy_btn)

            # 加载按钮
            load_btn = QPushButton("加载")
            load_btn.setMinimumHeight(25)
            load_btn.setMaximumWidth(50)
            load_btn.clicked.connect(lambda checked=False, idx=i: self.load_time_value(idx))
            self.load_buttons.append(load_btn)
            button_layout.addWidget(load_btn)

            time_layout.addLayout(button_layout)
            top_layout.addLayout(time_layout)

        top_group.setLayout(top_layout)
        layout.addWidget(top_group)

        # 下半部分 - 时间转换
        bottom_group = QGroupBox("时间转换")
        bottom_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        bottom_layout = QVBoxLayout()  # 改为垂直布局
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(10, 0, 10, 0)

        # 时区选择
        timezone_layout = QHBoxLayout()
        timezone_layout.setSpacing(0)
        timezone_layout.setContentsMargins(0, 0, 0, 0)
        timezone_label = QLabel("时区选择")
        timezone_label.setMaximumWidth(50)
        timezone_layout.addWidget(timezone_label)
        timezone_layout.addStretch()
        self.timezone_combo = QComboBox()
        self.timezone_combo.setMinimumHeight(25)
        self.timezone_combo.setMaximumWidth(230)

        for tz in timezones:
            self.timezone_combo.addItem(tz)

        # 设置默认时区为上海
        shanghai_index = [i for i, tz in enumerate(timezones) if "Asia/Shanghai" in tz][0]
        self.timezone_combo.setCurrentIndex(shanghai_index)
        self.timezone_combo.currentIndexChanged.connect(self.on_timezone_changed)
        timezone_layout.addWidget(self.timezone_combo)
        bottom_layout.addLayout(timezone_layout)

        # 输入时间
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addWidget(QLabel("输入时间"))
        input_layout.addStretch()
        self.time_input = QLineEdit()
        self.time_input.setMinimumHeight(25)
        self.time_input.setMinimumWidth(175)
        self.time_input.textChanged.connect(self.auto_detect_time_format)
        input_layout.addWidget(self.time_input)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(25)
        self.clear_btn.setMinimumWidth(50)
        self.clear_btn.clicked.connect(self.time_input.clear)
        input_layout.addWidget(self.clear_btn)
        bottom_layout.addLayout(input_layout)

        # 转换结果显示 - 改为垂直排列
        result_labels = ["时间(秒)", "时间(毫秒)", "时间戳(秒)", "时间戳(毫秒)"]
        self.result_labels = []
        self.result_copy_buttons = []

        for i, label in enumerate(result_labels):
            # 每个结果一行
            result_row = QHBoxLayout()

            # 时间标签
            title_label = QLabel(label)
            title_label.setMinimumWidth(120)
            result_row.addWidget(title_label)

            result_label = QLabel()
            result_label.setMinimumHeight(25)
            result_label.setMaximumWidth(150)
            self.result_labels.append(result_label)
            result_row.addWidget(result_label)
            result_row.addStretch()

            copy_btn = QPushButton("复制")
            copy_btn.setMinimumWidth(50)
            copy_btn.setMinimumHeight(25)
            copy_btn.clicked.connect(lambda checked=False, idx=i: self.copy_result_value(idx))
            self.result_copy_buttons.append(copy_btn)
            result_row.addWidget(copy_btn)

            bottom_layout.addLayout(result_row)

        bottom_group.setLayout(bottom_layout)
        layout.addWidget(bottom_group)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 设置当前时间选项卡的布局
        tab_layout = QVBoxLayout(self.current_time_tab)
        tab_layout.setSpacing(0)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)

    def setup_calculator_tab(self):
        # 创建滚动区域以适应竖向布局
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # 差值计算器
        diff_group = QGroupBox("差值计算器")
        diff_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        diff_layout = QVBoxLayout()  # 改为垂直布局

        # 时间输入1
        time1_layout = QHBoxLayout()
        time1_layout.addWidget(QLabel("时间1:"))
        self.time1_input = QLineEdit()
        self.time1_input.setMinimumHeight(25)
        self.time1_input.setPlaceholderText("YYYY-MM-DD HH:MM:SS")
        time1_layout.addWidget(self.time1_input)
        diff_layout.addLayout(time1_layout)

        # 时间输入2
        time2_layout = QHBoxLayout()
        time2_layout.addWidget(QLabel("时间2:"))
        self.time2_input = QLineEdit()
        self.time2_input.setMinimumHeight(25)
        self.time2_input.setPlaceholderText("YYYY-MM-DD HH:MM:SS")
        time2_layout.addWidget(self.time2_input)
        diff_layout.addLayout(time2_layout)

        # 计算按钮和差值单位
        calc_layout = QHBoxLayout()
        self.calc_diff_btn = QPushButton("计算差值")
        self.calc_diff_btn.setMinimumHeight(25)
        self.calc_diff_btn.clicked.connect(self.calculate_difference)
        calc_layout.addWidget(self.calc_diff_btn)

        calc_layout.addWidget(QLabel("差值单位:"))
        self.diff_unit_combo = QComboBox()
        self.diff_unit_combo.setMinimumHeight(25)
        self.diff_unit_combo.addItems(["秒", "分钟", "小时", "日", "周", "月", "年"])
        calc_layout.addWidget(self.diff_unit_combo)
        diff_layout.addLayout(calc_layout)

        # 差值结果
        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel("差值结果:"))
        self.diff_result = QLabel()
        self.diff_result.setMinimumHeight(25)
        result_layout.addWidget(self.diff_result)

        # 添加复制按钮
        self.copy_diff_btn = QPushButton("复制")
        self.copy_diff_btn.setMinimumHeight(25)
        self.copy_diff_btn.clicked.connect(self.copy_diff_result)
        result_layout.addWidget(self.copy_diff_btn)

        diff_layout.addLayout(result_layout)

        diff_group.setLayout(diff_layout)
        layout.addWidget(diff_group)

        # 时间操作
        operation_group = QGroupBox("时间操作")
        operation_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        operation_layout = QVBoxLayout()  # 改为垂直布局

        # 基础时间输入
        base_time_layout = QHBoxLayout()
        base_time_layout.addWidget(QLabel("基础时间:"))
        self.base_time_input = QLineEdit()
        self.base_time_input.setMinimumHeight(25)
        self.base_time_input.setPlaceholderText("YYYY-MM-DD HH:MM:SS")
        base_time_layout.addWidget(self.base_time_input)
        operation_layout.addLayout(base_time_layout)

        # 操作类型
        op_type_layout = QHBoxLayout()
        op_type_layout.addWidget(QLabel("操作:"))
        self.operation_combo = QComboBox()
        self.operation_combo.setMinimumHeight(25)
        self.operation_combo.addItems(["添加", "减少"])
        op_type_layout.addWidget(self.operation_combo)
        operation_layout.addLayout(op_type_layout)

        # 差值输入和单位
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("差值:"))
        self.offset_input = QSpinBox()
        self.offset_input.setMinimumHeight(25)
        offset_layout.addWidget(self.offset_input)

        offset_layout.addWidget(QLabel("单位:"))
        self.offset_unit_combo = QComboBox()
        self.offset_unit_combo.setMinimumHeight(25)
        self.offset_unit_combo.addItems(["秒", "分钟", "小时", "日", "周", "月", "年"])
        offset_layout.addWidget(self.offset_unit_combo)
        operation_layout.addLayout(offset_layout)

        # 计算按钮
        calc_op_layout = QHBoxLayout()
        self.calc_op_btn = QPushButton("计算")
        self.calc_op_btn.setMinimumHeight(25)
        self.calc_op_btn.clicked.connect(self.calculate_operation)
        calc_op_layout.addWidget(self.calc_op_btn)
        operation_layout.addLayout(calc_op_layout)

        # 结果
        op_result_layout = QHBoxLayout()
        op_result_layout.addWidget(QLabel("结果:"))
        self.op_result = QLabel()
        self.op_result.setMinimumHeight(25)
        op_result_layout.addWidget(self.op_result)

        # 添加复制按钮
        self.copy_op_btn = QPushButton("复制")
        self.copy_op_btn.setMinimumHeight(25)
        self.copy_op_btn.clicked.connect(self.copy_op_result)
        op_result_layout.addWidget(self.copy_op_btn)

        operation_layout.addLayout(op_result_layout)

        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 设置计算器选项卡的布局
        tab_layout = QVBoxLayout(self.calculator_tab)
        tab_layout.addWidget(scroll_area)

    def update_current_time(self):
        # 获取当前UTC时间
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        # 转换为选择的时区
        current_time = utc_now.astimezone(self.current_timezone)
        timestamp_sec = int(current_time.timestamp())
        timestamp_ms = int(current_time.timestamp() * 1000)

        # 更新标准时间(秒)
        self.time_labels[0].setText(current_time.strftime("%Y-%m-%d %H:%M:%S"))

        # 更新标准时间(毫秒)
        self.time_labels[1].setText(current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

        # 更新时间戳(秒)
        self.time_labels[2].setText(str(timestamp_sec))

        # 更新时间戳(毫秒)
        self.time_labels[3].setText(str(timestamp_ms))

    def copy_time_value(self, index):
        text = self.time_labels[index].text()
        QApplication.clipboard().setText(text)
        dialog_module.box_information(self.main_object, "提醒", "成功，已复制到剪贴板")

    def load_time_value(self, index):
        text = self.time_labels[index].text()
        self.time_input.setText(text)

    def on_timezone_changed(self):
        # 从下拉框获取时区信息
        tz_text = self.timezone_combo.currentText()
        tz_name = tz_text.split()[1]  # 获取时区名称，如 "Asia/Shanghai"
        self.current_timezone = pytz.timezone(tz_name)

        # 当时区改变时，如果输入框有内容，重新计算时间
        if self.time_input.text():
            self.auto_detect_time_format(self.time_input.text())

    def auto_detect_time_format(self, text):
        if not text:
            for label in self.result_labels:
                label.clear()
            return

        try:
            # 获取选中的时区
            tz = self.current_timezone

            # 尝试解析时间戳(秒)
            if text.isdigit() and len(text) == 10:
                timestamp = int(text)
                dt = datetime.fromtimestamp(timestamp, tz)
                self.update_result_labels(dt, timestamp, timestamp * 1000)
                return

            # 尝试解析时间戳(毫秒)
            if text.isdigit() and len(text) == 13:
                timestamp_ms = int(text)
                timestamp = timestamp_ms / 1000
                dt = datetime.fromtimestamp(timestamp, tz)
                self.update_result_labels(dt, int(timestamp), timestamp_ms)
                return

            # 尝试解析标准时间格式
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S.%f"
            ]

            for fmt in formats:
                try:
                    # 先解析为无时区的时间
                    dt_naive = datetime.strptime(text, fmt)
                    # 然后添加时区信息
                    dt = tz.localize(dt_naive)
                    timestamp = int(dt.timestamp())
                    timestamp_ms = int(dt.timestamp() * 1000)
                    self.update_result_labels(dt, timestamp, timestamp_ms)
                    return
                except ValueError:
                    continue

            # 如果所有格式都不匹配，清空结果
            for label in self.result_labels:
                label.clear()

        except Exception as e:
            for label in self.result_labels:
                label.clear()

    def update_result_labels(self, dt, timestamp, timestamp_ms):
        self.result_labels[0].setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
        self.result_labels[1].setText(dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
        self.result_labels[2].setText(str(timestamp))
        self.result_labels[3].setText(str(timestamp_ms))

    def copy_result_value(self, index):
        text = self.result_labels[index].text()
        QApplication.clipboard().setText(text)
        dialog_module.box_information(self.main_object, "提醒", "成功，已复制到剪贴板")

    def calculate_difference(self):
        try:
            time1_str = self.time1_input.text()
            time2_str = self.time2_input.text()

            if not time1_str or not time2_str:
                self.diff_result.setText("请输入两个时间")
                return

            # 解析时间
            dt1 = self.parse_datetime(time1_str)
            dt2 = self.parse_datetime(time2_str)

            if not dt1 or not dt2:
                self.diff_result.setText("时间格式错误")
                return

            # 计算差值（秒）
            diff_seconds = abs((dt2 - dt1).total_seconds())
            unit = self.diff_unit_combo.currentText()

            # 根据选择的单位转换差值
            if unit == "秒":
                result = diff_seconds
            elif unit == "分钟":
                result = diff_seconds / 60
            elif unit == "小时":
                result = diff_seconds / 3600
            elif unit == "日":
                result = diff_seconds / 86400
            elif unit == "周":
                result = diff_seconds / (86400 * 7)
            elif unit == "月":
                result = diff_seconds / (86400 * 30.44)  # 近似值
            elif unit == "年":
                result = diff_seconds / (86400 * 365.25)  # 近似值

            self.diff_result.setText(f"{result:.0f} {unit}")

        except Exception as e:
            self.diff_result.setText(f"计算错误: {str(e)}")

    def copy_diff_result(self):
        """复制差值计算结果"""
        text = self.diff_result.text()
        if text and text != "请输入两个时间" and text != "时间格式错误" and not text.startswith("计算错误"):
            QApplication.clipboard().setText(text)
            dialog_module.box_information(self.main_object, "提醒", "成功，已复制到剪贴板")

    def calculate_operation(self):
        try:
            base_time_str = self.base_time_input.text()
            offset_str = self.offset_input.text()

            if not base_time_str or not offset_str:
                self.op_result.setText("请输入基础时间和差值")
                return

            # 解析基础时间
            base_dt = self.parse_datetime(base_time_str)
            if not base_dt:
                self.op_result.setText("基础时间格式错误")
                return

            # 解析偏移量
            offset = float(offset_str)
            unit = self.offset_unit_combo.currentText()
            operation = self.operation_combo.currentText()

            # 根据单位和操作计算新时间
            if unit == "秒":
                delta = timedelta(seconds=offset)
            elif unit == "分钟":
                delta = timedelta(minutes=offset)
            elif unit == "小时":
                delta = timedelta(hours=offset)
            elif unit == "日":
                delta = timedelta(days=offset)
            elif unit == "周":
                delta = timedelta(weeks=offset)
            elif unit == "月":
                # 月份的加减需要特殊处理
                if operation == "添加":
                    new_year = base_dt.year
                    new_month = base_dt.month + int(offset)
                    if new_month > 12:
                        new_year += new_month // 12
                        new_month = new_month % 12
                    result_dt = base_dt.replace(year=new_year, month=new_month)
                else:  # 减少
                    new_year = base_dt.year
                    new_month = base_dt.month - int(offset)
                    if new_month < 1:
                        new_year -= abs(new_month) // 12 + 1
                        new_month = 12 - (abs(new_month) % 12)
                    result_dt = base_dt.replace(year=new_year, month=new_month)
                self.op_result.setText(result_dt.strftime("%Y-%m-%d %H:%M:%S"))
                return
            elif unit == "年":
                if operation == "添加":
                    result_dt = base_dt.replace(year=base_dt.year + int(offset))
                else:  # 减少
                    result_dt = base_dt.replace(year=base_dt.year - int(offset))
                self.op_result.setText(result_dt.strftime("%Y-%m-%d %H:%M:%S"))
                return

            # 应用操作
            if operation == "添加":
                result_dt = base_dt + delta
            else:  # 减少
                result_dt = base_dt - delta

            self.op_result.setText(result_dt.strftime("%Y-%m-%d %H:%M:%S"))

        except Exception as e:
            self.op_result.setText(f"计算错误: {str(e)}")

    def copy_op_result(self):
        """复制时间操作结果"""
        text = self.op_result.text()
        if text and text != "请输入基础时间和差值" and text != "基础时间格式错误" and not text.startswith("计算错误"):
            QApplication.clipboard().setText(text)
            dialog_module.box_information(self.main_object, "提醒", "成功，已复制到剪贴板")

    def parse_datetime(self, datetime_str):
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S.%f"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue

        # 尝试解析时间戳
        if datetime_str.isdigit():
            timestamp = int(datetime_str)
            if len(datetime_str) == 10:  # 秒级时间戳
                return datetime.fromtimestamp(timestamp)
            elif len(datetime_str) == 13:  # 毫秒级时间戳
                return datetime.fromtimestamp(timestamp / 1000)

        return None

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)
