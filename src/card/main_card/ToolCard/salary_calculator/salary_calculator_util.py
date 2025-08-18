from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QGroupBox, QLabel, QLineEdit, QComboBox,
                               QRadioButton, QCheckBox, QScrollArea, QGridLayout)
from PySide6.QtGui import QFont

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util

# PPP转换因子映射表
PPP_FACTORS = {
    'AF': 18.71, 'AO': 167.66, 'AL': 41.01, 'AR': 28.67, 'AM': 157.09, 'AG': 2.06,
    'AU': 1.47, 'AT': 0.76, 'AZ': 0.50, 'BI': 680.41, 'BE': 0.75, 'BJ': 211.97,
    'BF': 209.84, 'BD': 32.81, 'BG': 0.70, 'BH': 0.18, 'BS': 0.88, 'BA': 0.66,
    'BY': 0.77, 'BZ': 1.37, 'BO': 2.60, 'BR': 2.36, 'BB': 2.24, 'BN': 0.58,
    'BT': 20.11, 'BW': 4.54, 'CF': 280.19, 'CA': 1.21, 'CH': 1.14, 'CL': 418.43,
    'CN': 4.19, 'CI': 245.25, 'CM': 228.75, 'CD': 911.27, 'CG': 312.04, 'CO': 1352.79,
    'KM': 182.34, 'CV': 46.51, 'CR': 335.86, 'CY': 0.61, 'CZ': 12.66, 'DE': 0.75,
    'DJ': 105.29, 'DM': 1.69, 'DK': 6.60, 'DO': 22.90, 'DZ': 37.24, 'EC': 0.51,
    'EG': 4.51, 'ES': 0.62, 'EE': 0.53, 'ET': 12.11, 'FI': 0.84, 'FJ': 0.91,
    'FR': 0.73, 'GA': 265.46, 'GB': 0.70, 'GE': 0.90, 'GH': 2.33, 'GN': 4053.64,
    'GM': 17.79, 'GW': 214.86, 'GQ': 229.16, 'GR': 0.54, 'GD': 1.64, 'GT': 4.01,
    'GY': 73.60, 'HK': 6.07, 'HN': 10.91, 'HR': 3.21, 'HT': 40.20, 'HU': 148.01,
    'ID': 4673.65, 'IN': 21.99, 'IE': 0.78, 'IR': 30007.63, 'IQ': 507.58, 'IS': 145.34,
    'IL': 3.59, 'IT': 0.66, 'JM': 72.03, 'JO': 0.29, 'JP': 102.84, 'KZ': 139.91,
    'KE': 43.95, 'KG': 18.28, 'KH': 1400.09, 'KI': 1.00, 'KN': 1.92, 'KR': 861.82,
    'LA': 2889.36, 'LB': 1414.91, 'LR': 0.41, 'LY': 0.48, 'LC': 1.93, 'LK': 51.65,
    'LS': 5.90, 'LT': 0.45, 'LU': 0.86, 'LV': 0.48, 'MO': 5.18, 'MA': 3.92,
    'MD': 6.06, 'MG': 1178.10, 'MV': 8.35, 'MX': 9.52, 'MK': 18.83, 'ML': 211.41,
    'MT': 0.57, 'MM': 417.35, 'ME': 0.33, 'MN': 931.67, 'MZ': 24.05, 'MR': 12.01,
    'MU': 16.52, 'MW': 298.82, 'MY': 1.57, 'NA': 7.40, 'NE': 257.60, 'NG': 144.27,
    'NI': 11.75, 'NL': 0.77, 'NO': 10.03, 'NP': 33.52, 'NZ': 1.45, 'PK': 38.74,
    'PA': 0.46, 'PE': 1.80, 'PH': 19.51, 'PG': 2.11, 'PL': 1.78, 'PR': 0.92,
    'PT': 0.57, 'PY': 2575.54, 'PS': 0.57, 'QA': 2.06, 'RO': 1.71, 'RU': 25.88,
    'RW': 339.88, 'SA': 1.61, 'SD': 21.85, 'SN': 245.98, 'SG': 0.84, 'SB': 7.08,
    'SL': 2739.26, 'SV': 0.45, 'SO': 9107.78, 'RS': 41.13, 'ST': 10.94, 'SR': 3.55,
    'SK': 0.53, 'SI': 0.56, 'SE': 8.77, 'SZ': 6.36, 'SC': 7.82, 'TC': 1.07,
    'TD': 220.58, 'TG': 236.83, 'TH': 12.34, 'TJ': 2.30, 'TL': 0.41, 'TT': 4.15,
    'TN': 0.91, 'TR': 2.13, 'TV': 1.29, 'TW': 13.85, 'TZ': 888.32, 'UG': 1321.35,
    'UA': 7.69, 'UY': 28.45, 'US': 1.00, 'UZ': 2297.17, 'VC': 1.54, 'VN': 7473.67,
    'VU': 110.17, 'XK': 0.33, 'ZA': 6.93, 'ZM': 5.59, 'ZW': 24.98
}

# 货币符号映射表
CURRENCY_SYMBOLS = {
    'AF': '؋', 'AL': 'L', 'DZ': 'د.ج', 'AO': 'Kz', 'AR': '$', 'AM': '֏',
    'AU': 'A$', 'AT': '€', 'AZ': '₼', 'BI': 'FBu', 'BE': '€', 'BJ': 'CFA',
    'BF': 'CFA', 'BD': '৳', 'BG': 'лв', 'BH': '.د.ب', 'BS': 'B$', 'BA': 'KM',
    'BY': 'Br', 'BZ': 'BZ$', 'BO': 'Bs', 'BR': 'R$', 'BB': 'Bds$', 'BN': 'B$',
    'BT': 'Nu.', 'BW': 'P', 'CA': 'C$', 'CH': 'CHF', 'CL': 'CLP$', 'CN': '¥',
    'CI': 'CFA', 'CM': 'FCFA', 'CD': 'FC', 'CG': 'FCFA', 'CO': 'Col$', 'CR': '₡',
    'CY': '€', 'CZ': 'Kč', 'DE': '€', 'DK': 'kr', 'DO': 'RD$', 'EC': '$',
    'EG': 'E£', 'ES': '€', 'EE': '€', 'ET': 'Br', 'FI': '€', 'FJ': 'FJ$',
    'FR': '€', 'GB': '£', 'GE': '₾', 'GH': '₵', 'GR': '€', 'GT': 'Q',
    'HK': 'HK$', 'HN': 'L', 'HR': '€', 'HU': 'Ft', 'ID': 'Rp', 'IN': '₹',
    'IE': '€', 'IR': '﷼', 'IQ': 'ع.د', 'IS': 'kr', 'IL': '₪', 'IT': '€',
    'JM': 'J$', 'JO': 'JD', 'JP': '¥', 'KE': 'KSh', 'KR': '₩', 'KW': 'د.ك',
    'LB': 'L£', 'LK': 'Rs', 'LT': '€', 'LU': '€', 'LV': '€', 'MA': 'د.م.',
    'MX': 'Mex$', 'MY': 'RM', 'NG': '₦', 'NL': '€', 'NO': 'kr', 'NP': 'रू',
    'NZ': 'NZ$', 'PK': '₨', 'PA': 'B/.', 'PE': 'S/.', 'PH': '₱', 'PL': 'zł',
    'PT': '€', 'QA': 'ر.ق', 'RO': 'lei', 'RU': '₽', 'SA': 'ر.س', 'SG': 'S$',
    'SK': '€', 'SI': '€', 'SE': 'kr', 'TH': '฿', 'TR': '₺', 'TW': 'NT$',
    'UA': '₴', 'US': '$', 'UY': '$U', 'VN': '₫', 'ZA': 'R'
}

# 国家名称映射（中文）
COUNTRY_NAMES = {
    'AF': '阿富汗', 'AO': '安哥拉', 'AL': '阿尔巴尼亚', 'AR': '阿根廷', 'AM': '亚美尼亚',
    'AG': '安提瓜和巴布达', 'AU': '澳大利亚', 'AT': '奥地利', 'AZ': '阿塞拜疆', 'BI': '布隆迪',
    'BE': '比利时', 'BJ': '贝宁', 'BF': '布基纳法索', 'BD': '孟加拉国', 'BG': '保加利亚',
    'BH': '巴林', 'BS': '巴哈马', 'BA': '波黑', 'BY': '白俄罗斯', 'BZ': '伯利兹',
    'BO': '玻利维亚', 'BR': '巴西', 'BB': '巴巴多斯', 'BN': '文莱', 'BT': '不丹',
    'BW': '博茨瓦纳', 'CF': '中非', 'CA': '加拿大', 'CH': '瑞士', 'CL': '智利',
    'CN': '中国', 'CI': '科特迪瓦', 'CM': '喀麦隆', 'CD': '刚果(金)', 'CG': '刚果(布)',
    'CO': '哥伦比亚', 'KM': '科摩罗', 'CV': '佛得角', 'CR': '哥斯达黎加', 'CY': '塞浦路斯',
    'CZ': '捷克', 'DE': '德国', 'DJ': '吉布提', 'DM': '多米尼克', 'DK': '丹麦',
    'DO': '多米尼加', 'DZ': '阿尔及利亚', 'EC': '厄瓜多尔', 'EG': '埃及', 'ES': '西班牙',
    'EE': '爱沙尼亚', 'ET': '埃塞俄比亚', 'FI': '芬兰', 'FJ': '斐济', 'FR': '法国',
    'GA': '加蓬', 'GB': '英国', 'GE': '格鲁吉亚', 'GH': '加纳', 'GN': '几内亚',
    'GM': '冈比亚', 'GW': '几内亚比绍', 'GQ': '赤道几内亚', 'GR': '希腊', 'GD': '格林纳达',
    'GT': '危地马拉', 'GY': '圭亚那', 'HK': '中国香港', 'HN': '洪都拉斯', 'HR': '克罗地亚',
    'HT': '海地', 'HU': '匈牙利', 'ID': '印度尼西亚', 'IN': '印度', 'IE': '爱尔兰',
    'IR': '伊朗', 'IQ': '伊拉克', 'IS': '冰岛', 'IL': '以色列', 'IT': '意大利',
    'JM': '牙买加', 'JO': '约旦', 'JP': '日本', 'KZ': '哈萨克斯坦', 'KE': '肯尼亚',
    'KG': '吉尔吉斯斯坦', 'KH': '柬埔寨', 'KI': '基里巴斯', 'KN': '圣基茨和尼维斯', 'KR': '韩国',
    'LA': '老挝', 'LB': '黎巴嫩', 'LR': '利比里亚', 'LY': '利比亚', 'LC': '圣卢西亚',
    'LK': '斯里兰卡', 'LS': '莱索托', 'LT': '立陶宛', 'LU': '卢森堡', 'LV': '拉脱维亚',
    'MO': '中国澳门', 'MA': '摩洛哥', 'MD': '摩尔多瓦', 'MG': '马达加斯加', 'MV': '马尔代夫',
    'MX': '墨西哥', 'MK': '北马其顿', 'ML': '马里', 'MT': '马耳他', 'MM': '缅甸',
    'ME': '黑山', 'MN': '蒙古', 'MZ': '莫桑比克', 'MR': '毛里塔尼亚', 'MU': '毛里求斯',
    'MW': '马拉维', 'MY': '马来西亚', 'NA': '纳米比亚', 'NE': '尼日尔', 'NG': '尼日利亚',
    'NI': '尼加拉瓜', 'NL': '荷兰', 'NO': '挪威', 'NP': '尼泊尔', 'NZ': '新西兰',
    'PK': '巴基斯坦', 'PA': '巴拿马', 'PE': '秘鲁', 'PH': '菲律宾', 'PG': '巴布亚新几内亚',
    'PL': '波兰', 'PR': '波多黎各', 'PT': '葡萄牙', 'PY': '巴拉圭', 'PS': '巴勒斯坦',
    'QA': '卡塔尔', 'RO': '罗马尼亚', 'RU': '俄罗斯', 'RW': '卢旺达', 'SA': '沙特阿拉伯',
    'SD': '苏丹', 'SN': '塞内加尔', 'SG': '新加坡', 'SB': '所罗门群岛', 'SL': '塞拉利昂',
    'SV': '萨尔瓦多', 'SO': '索马里', 'RS': '塞尔维亚', 'ST': '圣多美和普林西比', 'SR': '苏里南',
    'SK': '斯洛伐克', 'SI': '斯洛文尼亚', 'SE': '瑞典', 'SZ': '斯威士兰', 'SC': '塞舌尔',
    'TC': '特克斯和凯科斯群岛', 'TD': '乍得', 'TG': '多哥', 'TH': '泰国', 'TJ': '塔吉克斯坦',
    'TL': '东帝汶', 'TT': '特立尼达和多巴哥', 'TN': '突尼斯', 'TR': '土耳其', 'TV': '图瓦卢',
    'TW': '中国台湾', 'TZ': '坦桑尼亚', 'UG': '乌干达', 'UA': '乌克兰', 'UY': '乌拉圭',
    'US': '美国', 'UZ': '乌兹别克斯坦', 'VC': '圣文森特和格林纳丁斯', 'VN': '越南', 'VU': '瓦努阿图',
    'XK': '科索沃', 'ZA': '南非', 'ZM': '赞比亚', 'ZW': '津巴布韦'
}


class SalaryCalculator(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(1600, 950)
        # 设置链接
        self.standard_title_bar.setLink("https://github.com/Zippland/worth-calculator/")
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 初始化默认值
        self.default_values = {
            "salary": "",
            "work_days_per_week": "5",
            "wfh_days_per_week": "0",
            "annual_leave": "5",
            "public_holidays": "13",
            "paid_sick_leave": "3",
            "work_hours": "8",
            "commute_hours": "2",
            "rest_time": "2",
            "city_factor": "1.0",
            "work_environment": "1.0",
            "leadership": "1.0",
            "teamwork": "1.0",
            "home_town": "no",
            "degree_type": "bachelor",
            "school_type": "firstTier",
            "bachelor_type": "firstTier",
            "work_years": "0",
            "shuttle": "1.0",
            "canteen": "1.0",
            "job_stability": "private",
            "education": "1.0",
            "has_shuttle": False,
            "has_canteen": False,
            "selected_country": "CN"
        }

        # 主部件和布局
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(15)
        self.widget_base.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建左侧区域（薪资信息 + 工作时间）
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setSpacing(20)

        # 创建中间区域（环境系数）
        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.setSpacing(20)

        # 创建右侧区域（计算结果）
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setSpacing(20)

        # 添加到主布局
        self.main_layout.addWidget(self.left_widget, 2)  # 左侧占2份
        self.main_layout.addWidget(self.center_widget, 4)  # 中间占3份
        self.main_layout.addWidget(self.right_widget, 2)  # 右侧占2份

        # 创建左侧滚动区域
        self.left_scroll_area = QScrollArea()
        self.left_scroll_area.setWidgetResizable(True)
        self.left_scroll_content = QWidget()
        self.left_scroll_content.setStyleSheet("border: none;")
        self.left_scroll_layout = QVBoxLayout(self.left_scroll_content)
        self.left_scroll_layout.setSpacing(20)
        self.left_scroll_area.setWidget(self.left_scroll_content)
        self.left_scroll_area.setStyleSheet("border: 2px solid rgba(13, 202, 75, 125);")
        self.left_layout.addWidget(self.left_scroll_area)

        # 创建中间滚动区域
        self.center_scroll_area = QScrollArea()
        self.center_scroll_area.setWidgetResizable(True)
        self.center_scroll_content = QWidget()
        self.center_scroll_content.setStyleSheet("border: none;")
        self.center_scroll_layout = QVBoxLayout(self.center_scroll_content)
        self.center_scroll_layout.setSpacing(20)
        self.center_scroll_area.setWidget(self.center_scroll_content)
        self.center_scroll_area.setStyleSheet("border: 2px solid rgba(13, 202, 75, 125);")
        self.center_layout.addWidget(self.center_scroll_area)

        # 创建表单区域（布局调整）
        self.create_salary_section()  # 左侧：薪资信息
        self.create_time_section()  # 左侧：工作时间
        self.create_environment_section()  # 中间：环境系数
        self.create_results_section()  # 右侧：计算结果

        # 加载保存的设置
        self.load_settings()

        # 初始计算
        self.calculate_value()

    def create_salary_section(self):
        group = QGroupBox("薪资信息")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        group.setFont(QFont("", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(15)

        # 国家选择
        self.country_label = QLabel("国家/地区:")
        self.country_combo = QComboBox()

        # 按国家名称排序
        sorted_countries = sorted(PPP_FACTORS.keys(),
                                  key=lambda code: COUNTRY_NAMES.get(code, code))

        for code in sorted_countries:
            country_name = COUNTRY_NAMES.get(code, code)
            ppp_factor = PPP_FACTORS[code]
            self.country_combo.addItem(f"{country_name} (PPP: {ppp_factor:.2f})", code)

        self.country_combo.currentIndexChanged.connect(self.calculate_value)

        # 薪资输入
        self.salary_label = QLabel("年薪:")
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("请输入您的年薪")
        self.salary_input.textChanged.connect(self.calculate_value)

        # 添加到布局
        layout.addWidget(self.country_label, 0, 0)
        layout.addWidget(self.country_combo, 0, 1)
        layout.addWidget(self.salary_label, 1, 0)
        layout.addWidget(self.salary_input, 1, 1)

        group.setLayout(layout)
        self.left_scroll_layout.addWidget(group, 1)

    def create_time_section(self):
        group = QGroupBox("工作时间")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        group.setFont(QFont("", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(10)

        # 每周工作天数
        self.work_days_label = QLabel("每周工作天数:")
        self.work_days_input = QLineEdit()
        self.work_days_input.textChanged.connect(self.calculate_value)

        # 在家工作天数
        self.wfh_days_label = QLabel("在家工作天数:")
        self.wfh_days_input = QLineEdit()
        self.wfh_days_input.textChanged.connect(self.calculate_value)

        # 年假
        self.annual_leave_label = QLabel("年假天数:")
        self.annual_leave_input = QLineEdit()
        self.annual_leave_input.textChanged.connect(self.calculate_value)

        # 公共假期
        self.public_holidays_label = QLabel("公共假期天数:")
        self.public_holidays_input = QLineEdit()
        self.public_holidays_input.textChanged.connect(self.calculate_value)

        # 带薪病假
        self.sick_leave_label = QLabel("带薪病假天数:")
        self.sick_leave_input = QLineEdit()
        self.sick_leave_input.textChanged.connect(self.calculate_value)

        # 工作时间
        self.work_hours_label = QLabel("每日工作时间,不含通勤(小时):")
        self.work_hours_input = QLineEdit()
        self.work_hours_input.textChanged.connect(self.calculate_value)

        # 通勤时间
        self.commute_hours_label = QLabel("每日总通勤时间(小时):")
        self.commute_hours_input = QLineEdit()
        self.commute_hours_input.textChanged.connect(self.calculate_value)

        # 休息时间
        self.rest_time_label = QLabel("每日休息&摸鱼时间(小时):")
        self.rest_time_input = QLineEdit()
        self.rest_time_input.textChanged.connect(self.calculate_value)

        # 添加到布局
        layout.addWidget(self.work_days_label, 0, 0)
        layout.addWidget(self.work_days_input, 0, 1)
        layout.addWidget(self.wfh_days_label, 1, 0)
        layout.addWidget(self.wfh_days_input, 1, 1)

        layout.addWidget(self.annual_leave_label, 2, 0)
        layout.addWidget(self.annual_leave_input, 2, 1)
        layout.addWidget(self.public_holidays_label, 3, 0)
        layout.addWidget(self.public_holidays_input, 3, 1)

        layout.addWidget(self.sick_leave_label, 4, 0)
        layout.addWidget(self.sick_leave_input, 4, 1)

        layout.addWidget(self.work_hours_label, 5, 0)
        layout.addWidget(self.work_hours_input, 5, 1)
        layout.addWidget(self.commute_hours_label, 6, 0)
        layout.addWidget(self.commute_hours_input, 6, 1)

        layout.addWidget(self.rest_time_label, 7, 0)
        layout.addWidget(self.rest_time_input, 7, 1)

        group.setLayout(layout)
        self.left_scroll_layout.addWidget(group, 2)

    def create_environment_section(self):
        group = QGroupBox("环境系数")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        group.setFont(QFont("", 10, QFont.Bold))
        layout = QVBoxLayout()

        # 学历背景 & 工作年限
        self.create_education_and_work_years_group(layout)

        # 工作类型
        self.create_job_type_group(layout)

        # 城市系数
        self.create_city_factor_group(layout)

        # 工作环境
        self.create_work_environment_group(layout)

        # 领导团队
        self.create_leadership_group(layout)

        # 班车食堂
        self.create_shuttle_canteen_group(layout)

        group.setLayout(layout)
        self.center_scroll_layout.addWidget(group)

    def create_education_and_work_years_group(self, parent_layout):
        group = QGroupBox("学历背景和工作年限")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        layout = QGridLayout()

        # 学历类型
        self.degree_label = QLabel("学历类型:")
        self.degree_combo = QComboBox()
        self.degree_combo.addItem("专科及以下", "belowBachelor")
        self.degree_combo.addItem("本科", "bachelor")
        self.degree_combo.addItem("硕士", "masters")
        self.degree_combo.addItem("博士", "phd")
        self.degree_combo.currentIndexChanged.connect(self.calculate_value)

        # 学校类型
        self.school_label = QLabel("学校类型:")
        self.school_combo = QComboBox()
        self.school_combo.addItem("二本/三本", "secondTier")
        self.school_combo.addItem("双非/QS100/USnews50", "firstTier")
        self.school_combo.addItem("985/211/QS30/USnews20", "elite")
        self.school_combo.currentIndexChanged.connect(self.calculate_value)

        # 本科背景（仅硕士显示）
        self.bachelor_label = QLabel("本科背景:")
        self.bachelor_combo = QComboBox()
        self.bachelor_combo.addItem("二本/三本", "secondTier")
        self.bachelor_combo.addItem("双非/QS100/USnews50", "firstTier")
        self.bachelor_combo.addItem("985/211/QS30/USnews20", "elite")
        self.bachelor_combo.currentIndexChanged.connect(self.calculate_value)
        self.bachelor_label.setVisible(False)
        self.bachelor_combo.setVisible(False)

        # 连接信号
        self.degree_combo.currentIndexChanged.connect(self.update_education_visibility)

        layout.addWidget(self.degree_label, 0, 0)
        layout.addWidget(self.degree_combo, 0, 1)
        layout.addWidget(self.school_label, 1, 0)
        layout.addWidget(self.school_combo, 1, 1)
        layout.addWidget(self.bachelor_label, 2, 0)
        layout.addWidget(self.bachelor_combo, 2, 1)

        # 工作年限
        self.work_years_label = QLabel("工作经验:")
        self.work_years_combo = QComboBox()
        self.work_years_combo.addItem("应届生", "0")
        self.work_years_combo.addItem("1-3年", "1")
        self.work_years_combo.addItem("3-5年", "2")
        self.work_years_combo.addItem("5-8年", "4")
        self.work_years_combo.addItem("8-10年", "6")
        self.work_years_combo.addItem("10-12年", "10")
        self.work_years_combo.addItem("12年以上", "15")
        self.work_years_combo.currentIndexChanged.connect(self.calculate_value)

        layout.addWidget(self.work_years_label, 3, 0)
        layout.addWidget(self.work_years_combo, 3, 1)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def calculate_education_factor(self):
        """
        根据学位类型和学校类型计算教育系数
        """
        degree_type = self.degree_combo.currentData()
        school_type = self.school_combo.currentData()
        bachelor_type = self.bachelor_combo.currentData()

        factor = 1.0  # 默认值

        # 专科及以下固定为0.8
        if degree_type == 'belowBachelor':
            factor = 0.8
        # 本科学历
        elif degree_type == 'bachelor':
            if school_type == 'secondTier':
                factor = 0.9  # 二本三本
            elif school_type == 'firstTier':
                factor = 1.0  # 双非/QS100/USnews50
            elif school_type == 'elite':
                factor = 1.2  # 985/211/QS30/USnews20
        # 硕士学历 - 考虑本科背景
        elif degree_type == 'masters':
            # 先获取本科背景的基础系数
            bachelor_base_coefficient = 0
            if bachelor_type == 'secondTier':
                bachelor_base_coefficient = 0.9  # 二本三本
            elif bachelor_type == 'firstTier':
                bachelor_base_coefficient = 1.0  # 双非/QS100/USnews50
            elif bachelor_type == 'elite':
                bachelor_base_coefficient = 1.2  # 985/211/QS30/USnews20

            # 再计算硕士学校的加成系数
            masters_bonus = 0
            if school_type == 'secondTier':
                masters_bonus = 0.4  # 二本三本硕士
            elif school_type == 'firstTier':
                masters_bonus = 0.5  # 双非/QS100/USnews50硕士
            elif school_type == 'elite':
                masters_bonus = 0.6  # 985/211/QS30/USnews20硕士

            # 最终学历系数 = 本科基础 + 硕士加成
            factor = bachelor_base_coefficient + masters_bonus
        # 博士学历
        elif degree_type == 'phd':
            if school_type == 'secondTier':
                factor = 1.6  # 二本三本博士
            elif school_type == 'firstTier':
                factor = 1.8  # 双非/QS100/USnews50博士
            elif school_type == 'elite':
                factor = 2.0  # 985/211/QS30/USnews20博士

        return factor

    def update_education_visibility(self):
        degree_type = self.degree_combo.currentData()
        is_masters = degree_type == "masters"
        self.bachelor_label.setVisible(is_masters)
        self.bachelor_combo.setVisible(is_masters)
        self.calculate_value()

    def create_job_type_group(self, parent_layout):
        group = QGroupBox("工作类型")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        layout = QGridLayout()

        self.job_type_buttons = []
        job_types = [
            ("体制内", "government"),
            ("央/国企", "state"),
            ("外企", "foreign"),
            ("私企", "private"),
            ("派遣", "dispatch"),
            ("自由职业", "freelance")
        ]

        for i, (name, value) in enumerate(job_types):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.job_type_buttons.append(btn)
            layout.addWidget(btn, i // 3, i % 3)

        # 默认选择私企
        self.job_type_buttons[3].setChecked(True)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_city_factor_group(self, parent_layout):
        group = QGroupBox("城市系数")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        layout = QGridLayout()

        self.city_factor_buttons = []
        city_factors = [
            ("一线城市(北上广深)", "0.70"),
            ("新一线城市", "0.80"),
            ("二线城市", "1.0"),
            ("三线城市", "1.10"),
            ("四线城市", "1.25"),
            ("县城", "1.40"),
            ("乡镇", "1.50")
        ]

        for i, (name, value) in enumerate(city_factors):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.city_factor_buttons.append(btn)
            layout.addWidget(btn, i // 3, i % 3)

        # 默认选择二线城市
        self.city_factor_buttons[2].setChecked(True)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_work_environment_group(self, parent_layout):
        group = QGroupBox("工作环境")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125);}")
        layout = QGridLayout()

        self.env_buttons = []
        env_options = [
            ("远程办公", "0.8"),
            ("工厂/工地", "0.9"),
            ("普通办公室", "1.0"),
            ("CBD写字楼", "1.1")
        ]

        for i, (name, value) in enumerate(env_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.env_buttons.append(btn)
            layout.addWidget(btn, i // 2, i % 2)

        # 默认选择普通办公室
        self.env_buttons[2].setChecked(True)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_leadership_group(self, parent_layout):
        group = QGroupBox("领导与团队")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        layout = QGridLayout()

        # 领导风格
        leadership_group = QGroupBox("领导风格")
        leadership_layout = QGridLayout()

        self.leadership_buttons = []
        leadership_options = [
            ("糟糕的领导", "0.7"),
            ("严厉的领导", "0.9"),
            ("普通领导", "1.0"),
            ("好领导", "1.1"),
            ("贵人领导", "1.3")
        ]

        for i, (name, value) in enumerate(leadership_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.leadership_buttons.append(btn)
            leadership_layout.addWidget(btn, i // 3, i % 3)

        # 默认选择普通领导
        self.leadership_buttons[2].setChecked(True)
        leadership_group.setLayout(leadership_layout)

        # 团队氛围
        teamwork_group = QGroupBox("团队氛围")
        teamwork_layout = QGridLayout()

        self.teamwork_buttons = []
        teamwork_options = [
            ("糟糕的团队", "0.9"),
            ("普通团队", "1.0"),
            ("好的团队", "1.1"),
            ("优秀的团队", "1.2")
        ]

        for i, (name, value) in enumerate(teamwork_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.teamwork_buttons.append(btn)
            teamwork_layout.addWidget(btn, i // 2, i % 2)

        # 默认选择普通团队
        self.teamwork_buttons[1].setChecked(True)
        teamwork_group.setLayout(teamwork_layout)

        # 家乡
        hometown_group = QGroupBox("是否在家乡工作")
        hometown_layout = QGridLayout()

        self.hometown_buttons = []
        hometown_options = [
            ("不在家乡", "no"),
            ("在家乡", "yes")
        ]

        for i, (name, value) in enumerate(hometown_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.hometown_buttons.append(btn)
            hometown_layout.addWidget(btn, i // 2, i % 2)

        # 默认选择不在家乡
        self.hometown_buttons[0].setChecked(True)
        hometown_group.setLayout(hometown_layout)

        # 添加到主布局
        layout.addWidget(leadership_group, 0, 0)
        layout.addWidget(teamwork_group, 0, 1)
        layout.addWidget(hometown_group, 1, 0, 1, 2)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_shuttle_canteen_group(self, parent_layout):
        group = QGroupBox("班车与食堂")
        group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        layout = QGridLayout()

        # 班车
        self.shuttle_check = QCheckBox("公司提供班车")
        self.shuttle_check.toggled.connect(self.calculate_value)

        self.shuttle_group = QGroupBox("班车便利程度")
        shuttle_layout = QGridLayout()

        self.shuttle_buttons = []
        shuttle_options = [
            ("无班车", "1.0"),
            ("不太便利", "0.9"),
            ("比较便利", "0.7"),
            ("直达", "0.5")
        ]

        for i, (name, value) in enumerate(shuttle_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.shuttle_buttons.append(btn)
            shuttle_layout.addWidget(btn, i // 2, i % 2)

        # 默认选择无班车
        self.shuttle_buttons[0].setChecked(True)
        self.shuttle_group.setLayout(shuttle_layout)
        self.shuttle_group.setEnabled(False)

        # 食堂
        self.canteen_check = QCheckBox("公司提供食堂")
        self.canteen_check.toggled.connect(self.calculate_value)

        self.canteen_group = QGroupBox("食堂质量")
        canteen_layout = QGridLayout()

        self.canteen_buttons = []
        canteen_options = [
            ("无食堂", "1.0"),
            ("普通食堂", "1.05"),
            ("良好食堂", "1.1"),
            ("优秀食堂", "1.15")
        ]

        for i, (name, value) in enumerate(canteen_options):
            btn = QRadioButton(name)
            btn.value = value
            btn.toggled.connect(self.calculate_value)
            self.canteen_buttons.append(btn)
            canteen_layout.addWidget(btn, i // 2, i % 2)

        # 默认选择无食堂
        self.canteen_buttons[0].setChecked(True)
        self.canteen_group.setLayout(canteen_layout)
        self.canteen_group.setEnabled(False)

        # 连接信号
        self.shuttle_check.toggled.connect(lambda checked: self.shuttle_group.setEnabled(checked))
        self.canteen_check.toggled.connect(lambda checked: self.canteen_group.setEnabled(checked))

        # 添加到布局
        layout.addWidget(self.shuttle_check, 0, 0)
        layout.addWidget(self.shuttle_group, 1, 0)
        layout.addWidget(self.canteen_check, 0, 1)
        layout.addWidget(self.canteen_group, 1, 1)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_results_section(self):
        group = QGroupBox("计算结果")
        group.setStyleSheet("QGroupBox{border: 2px solid rgba(13, 139, 201, 125);}")
        group.setFont(QFont("", 10, QFont.Bold))
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 添加顶部空间
        layout.addStretch(6)

        # 年工作天数
        days_layout = QVBoxLayout()
        self.working_days_label = QLabel("年工作天数:")
        self.working_days_label.setFont(QFont("", 10))
        self.working_days_value = QLabel("0天")
        self.working_days_value.setFont(QFont("", 12, QFont.Bold))
        days_layout.addWidget(self.working_days_label)
        days_layout.addWidget(self.working_days_value)
        layout.addLayout(days_layout)
        layout.addStretch(1)

        # 平均日薪
        salary_layout = QVBoxLayout()
        self.daily_salary_label = QLabel("平均日薪:")
        self.daily_salary_label.setFont(QFont("", 10))
        self.daily_salary_value = QLabel("¥0.00")
        self.daily_salary_value.setFont(QFont("", 12, QFont.Bold))
        salary_layout.addWidget(self.daily_salary_label)
        salary_layout.addWidget(self.daily_salary_value)
        layout.addLayout(salary_layout)
        layout.addStretch(1)

        # 工作价值指数
        value_layout = QVBoxLayout()
        self.job_value_label = QLabel("工作价值指数:")
        self.job_value_label.setFont(QFont("", 10))
        self.job_value_value = QLabel("0.00")
        self.job_value_value.setFont(QFont("", 24, QFont.Bold))
        self.job_value_value.setStyleSheet("color: #3498db;")
        value_layout.addWidget(self.job_value_label)
        value_layout.addWidget(self.job_value_value)
        layout.addLayout(value_layout)
        layout.addStretch(1)

        # 价值评估
        assessment_layout = QVBoxLayout()
        self.assessment_label = QLabel("价值评估:")
        self.assessment_label.setFont(QFont("", 10))
        self.assessment_value = QLabel("请输入薪资数据")
        self.assessment_value.setFont(QFont("", 16, QFont.Bold))
        self.assessment_value.setStyleSheet("color: gray;")
        assessment_layout.addWidget(self.assessment_label)
        assessment_layout.addWidget(self.assessment_value)
        layout.addLayout(assessment_layout)

        # 添加底部空间
        layout.addStretch(6)

        group.setLayout(layout)
        self.right_layout.addWidget(group)

    def calculate_working_days(self):
        try:
            weeks_per_year = 52
            work_days_per_week = float(self.work_days_input.text() or 0)
            total_work_days = weeks_per_year * work_days_per_week
            annual_leave = float(self.annual_leave_input.text() or 0)
            public_holidays = float(self.public_holidays_input.text() or 0)
            paid_sick_leave = float(self.sick_leave_input.text() or 0)

            total_leaves = annual_leave + public_holidays + paid_sick_leave * 0.6
            return max(total_work_days - total_leaves, 0)
        except:
            return 0

    def calculate_daily_salary(self):
        try:
            salary = float(self.salary_input.text() or 0)
            if salary <= 0:
                return 0

            working_days = self.calculate_working_days()
            if working_days <= 0:
                return 0

            country_code = self.country_combo.currentData()
            ppp_factor = PPP_FACTORS.get(country_code, 4.19)
            standardized_salary = salary * (4.19 / ppp_factor)

            return standardized_salary / working_days
        except:
            return 0

    def calculate_value(self):
        # 检查必要属性是否存在
        if not hasattr(self, 'working_days_value') or not hasattr(self, 'daily_salary_value'):
            return  # 如果属性不存在，直接返回

        # 获取当前国家
        country_code = self.country_combo.currentData()
        currency_symbol = CURRENCY_SYMBOLS.get(country_code, "$")

        # 计算年工作天数和日薪
        working_days = self.calculate_working_days()
        daily_salary = self.calculate_daily_salary()

        # 更新UI
        self.working_days_value.setText(f"{working_days:.0f}天")
        self.daily_salary_value.setText(f"{currency_symbol}{daily_salary:.2f}")

        # 计算工作价值指数
        if daily_salary <= 0:
            self.job_value_value.setText("0.00")
            self.assessment_value.setText("请输入薪资数据")
            self.assessment_value.setStyleSheet("color: gray;")
            return

        try:
            # 获取环境系数
            city_factor = self.get_selected_radio_value(self.city_factor_buttons, default=1.0)
            work_environment = self.get_selected_radio_value(self.env_buttons, default=1.0)
            leadership = self.get_selected_radio_value(self.leadership_buttons, default=1.0)
            teamwork = self.get_selected_radio_value(self.teamwork_buttons, default=1.0)

            # 获取班车和食堂系数
            shuttle_factor = self.get_selected_radio_value(self.shuttle_buttons,
                                                           default=1.0) if self.shuttle_check.isChecked() else 1.0
            canteen_factor = self.get_selected_radio_value(self.canteen_buttons,
                                                           default=1.0) if self.canteen_check.isChecked() else 1.0

            # 计算教育系数
            education = self.calculate_education_factor()

            # 计算综合环境系数
            environment_factor = city_factor * work_environment * leadership * teamwork * canteen_factor / education

            # 获取时间参数
            work_hours = float(self.work_hours_input.text() or 0)
            commute_hours = float(self.commute_hours_input.text() or 0)
            rest_time = float(self.rest_time_input.text() or 0)
            work_days_per_week = float(self.work_days_input.text() or 0)
            wfh_days_per_week = float(self.wfh_days_input.text() or 0)

            # 计算通勤效率
            office_days_ratio = (
                                        work_days_per_week - wfh_days_per_week) / work_days_per_week if work_days_per_week > 0 else 0
            effective_commute_hours = commute_hours * office_days_ratio * shuttle_factor

            # 获取工作年限和类型
            work_years = float(self.work_years_combo.currentData() or 0)
            job_stability = self.get_selected_radio_value(self.job_type_buttons, "private")

            # 经验薪资倍数
            experience_salary_multiplier = 1.0
            if work_years == 0:  # 应届生
                if job_stability == "government":
                    experience_salary_multiplier = 0.8
                elif job_stability == "state":
                    experience_salary_multiplier = 0.9
                elif job_stability == "foreign":
                    experience_salary_multiplier = 0.95
                elif job_stability == "private":
                    experience_salary_multiplier = 1.0
                elif job_stability in ["dispatch", "freelance"]:
                    experience_salary_multiplier = 1.1
            else:
                # 工作经验薪资模型
                if work_years == 1:
                    base_multiplier = 1.5
                elif work_years <= 3:
                    base_multiplier = 2.2
                elif work_years <= 5:
                    base_multiplier = 2.7
                elif work_years <= 8:
                    base_multiplier = 3.2
                elif work_years <= 10:
                    base_multiplier = 3.6
                else:
                    base_multiplier = 3.9

                # 工作类型调整
                growth_factor = 1.0
                if job_stability == "foreign":
                    growth_factor = 0.8
                elif job_stability == "state":
                    growth_factor = 0.4
                elif job_stability == "government":
                    growth_factor = 0.2
                elif job_stability in ["dispatch", "freelance"]:
                    growth_factor = 1.2

                experience_salary_multiplier = 1 + (base_multiplier - 1) * growth_factor

            # 最终价值计算
            value = (daily_salary * environment_factor) / (
                    35 * (work_hours + effective_commute_hours - 0.5 * rest_time) * experience_salary_multiplier)

            # 更新UI
            self.job_value_value.setText(f"{value:.2f}")

            # 评估结果
            if value < 0.6:
                assessment = "血亏！快跑！"
                color = "#c0392b"  # 红色
            elif value < 1.0:
                assessment = "不太划算"
                color = "#e74c3c"  # 浅红色
            elif value <= 1.8:
                assessment = "平均水平"
                color = "#f39c12"  # 橙色
            elif value <= 2.5:
                assessment = "还不错"
                color = "#3498db"  # 蓝色
            elif value <= 3.2:
                assessment = "很值！"
                color = "#2ecc71"  # 绿色
            elif value <= 4.0:
                assessment = "超值！"
                color = "#9b59b6"  # 紫色
            else:
                assessment = "人生赢家！"
                color = "#f1c40f"  # 黄色

            self.assessment_value.setText(assessment)
            self.assessment_value.setStyleSheet(f"color: {color}; font-weight: bold;")

        except Exception as e:
            print(f"计算错误: {e}")
            self.job_value_value.setText("0.00")
            self.assessment_value.setText("计算错误")
            self.assessment_value.setStyleSheet("color: #c0392b;")

    def get_selected_radio_value(self, radio_buttons, default=None):
        for btn in radio_buttons:
            if btn.isChecked():
                try:
                    return float(btn.value)
                except:
                    return btn.value
        return default

    def load_settings(self):
        settings = self.default_values

        # 应用设置
        self.salary_input.setText(settings.get("salary", self.default_values["salary"]))

        # 设置国家
        country_code = settings.get("selected_country", self.default_values["selected_country"])
        index = self.country_combo.findData(country_code)
        if index >= 0:
            self.country_combo.setCurrentIndex(index)

        # 设置其他输入字段
        self.work_days_input.setText(settings.get("work_days_per_week", self.default_values["work_days_per_week"]))
        self.wfh_days_input.setText(settings.get("wfh_days_per_week", self.default_values["wfh_days_per_week"]))
        self.annual_leave_input.setText(settings.get("annual_leave", self.default_values["annual_leave"]))
        self.public_holidays_input.setText(settings.get("public_holidays", self.default_values["public_holidays"]))
        self.sick_leave_input.setText(settings.get("paid_sick_leave", self.default_values["paid_sick_leave"]))
        self.work_hours_input.setText(settings.get("work_hours", self.default_values["work_hours"]))
        self.commute_hours_input.setText(settings.get("commute_hours", self.default_values["commute_hours"]))
        self.rest_time_input.setText(settings.get("rest_time", self.default_values["rest_time"]))

        # 设置学历
        self.degree_combo.setCurrentIndex(
            self.degree_combo.findData(settings.get("degree_type", self.default_values["degree_type"])))
        self.school_combo.setCurrentIndex(
            self.school_combo.findData(settings.get("school_type", self.default_values["school_type"])))
        self.bachelor_combo.setCurrentIndex(
            self.bachelor_combo.findData(settings.get("bachelor_type", self.default_values["bachelor_type"])))
        self.update_education_visibility()

        # 设置工作年限
        self.work_years_combo.setCurrentIndex(
            self.work_years_combo.findData(settings.get("work_years", self.default_values["work_years"])))

        # 设置单选按钮
        self.set_radio_buttons(self.job_type_buttons,
                               settings.get("job_stability", self.default_values["job_stability"]))
        self.set_radio_buttons(self.city_factor_buttons,
                               settings.get("city_factor", self.default_values["city_factor"]))
        self.set_radio_buttons(self.env_buttons,
                               settings.get("work_environment", self.default_values["work_environment"]))
        self.set_radio_buttons(self.leadership_buttons, settings.get("leadership", self.default_values["leadership"]))
        self.set_radio_buttons(self.teamwork_buttons, settings.get("teamwork", self.default_values["teamwork"]))
        self.set_radio_buttons(self.hometown_buttons, settings.get("home_town", self.default_values["home_town"]))

        # 设置班车和食堂
        has_shuttle = settings.get("has_shuttle", self.default_values["has_shuttle"])
        self.shuttle_check.setChecked(has_shuttle)
        self.shuttle_group.setEnabled(has_shuttle)
        self.set_radio_buttons(self.shuttle_buttons, settings.get("shuttle", self.default_values["shuttle"]))

        has_canteen = settings.get("has_canteen", self.default_values["has_canteen"])
        self.canteen_check.setChecked(has_canteen)
        self.canteen_group.setEnabled(has_canteen)
        self.set_radio_buttons(self.canteen_buttons, settings.get("canteen", self.default_values["canteen"]))

    def set_radio_buttons(self, buttons, value):
        for btn in buttons:
            if str(btn.value) == str(value):
                btn.setChecked(True)
                break


def show_salary_calculator_dialog(main_object, title, content):
    """显示这班上得值不值对话框"""
    dialog = SalaryCalculator(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog