#!/usr/bin/python
# -*- coding: UTF-8 -*-
import traceback
"""
    name:       获取信息
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 获取信息
"""
import urllib

# 处理成可以展示的html
def get_html(data_list, type_name, logger):
    try:
        # result = '<table><thead><tr class="thead_tr"><th class="th-01">序号</th><th class="th-02">关键词</th><th class="th-03"></th></tr></thead><tbody>'
        space_str = ("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                     "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        result = '<table><thead><tr class="thead_tr"><th class="th-01"></th><th class="th-02">' + space_str + '</th><th class="th-03"></th></tr></thead><tbody>'
        # result = '<table><tbody>'
        index = 0
        for data_item in data_list:
            # 热搜排名
            search_item_index = data_item['i']
            # 热搜标题
            search_item_title = data_item['t']
            # 热搜地址
            if type_name == "weibo":
                search_item_url = "https://s.weibo.com/weibo?q=" + urllib.parse.quote("#" + str(search_item_title) + "#")
            else:
                search_item_url = data_item['u']
            # 热搜火爆度
            search_item_count = data_item['n']
            # 热搜图标
            if 'c' in data_item:
                search_item_icon = data_item['c']
            else:
                search_item_icon = None
            # 组合数据
            result = result + '<tr class="">'
            if index < 3:
                result = result + '<td class="td-01 ranktop ranktop' + str(index) + '" style="line-height:25px;color: #f26d5f;font-weight: bold;"> ' + search_item_index + '  </td>'
            else:
                result = result + '<td class="td-01 ranktop ranktop' + str(index) + '" style="line-height:25px;color: #ff8200;"> ' + search_item_index + '  </td>'
            result = result + '<td class="td-02" style="line-height:25px;"><a href="' + search_item_url + '" target="_blank">' + search_item_title + '</a><span> ' + search_item_count + '</span></td>'
            if search_item_icon is not None:
                if search_item_icon == "new":
                    result = result + ('<td class="td-03" style="border-bottom:1px solid #ff3852;line-height:25px;">'
                                       '<i class="icon-txt icon-txt-len-1" style="background-color:#ff3852;margin-left: 4px;display: inline-block;width: 16px;height: 16px;'
                                       'line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font-style: normal;">新</i></td>')
                elif search_item_icon == "hot":
                    result = result + ('<td class="td-03" style="border-bottom:1px solid #ff9406;line-height:25px;">'
                                       '<i class="icon-txt icon-txt-len-1" style="background-color:#ff9406;margin-left: 4px;display: inline-block;width: 16px;height: 16px;'
                                       'line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font-style: normal;">热</i></td>')
                elif search_item_icon == "boil":
                    result = result + ('<td class="td-03" style="border-bottom:1px solid #f86400;line-height:25px;">'
                                       '<i class="icon-txt icon-txt-len-1" style="background-color:#f86400;margin-left: 4px;display: inline-block;width: 16px;height: 16px;'
                                       'line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font-style: normal;">沸</i></td>')
                elif search_item_icon == "warm":
                    result = result + ('<td class="td-03" style="border-bottom:1px solid #ffab5a;line-height:25px;">'
                                       '<i class="icon-txt icon-txt-len-1" style="background-color:#ffab5a;margin-left: 4px;display: inline-block;width: 16px;height: 16px;'
                                       'line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font-style: normal;">暖</i></td>')
                elif search_item_icon == "boom":
                    result = result + ('<td class="td-03" style="border-bottom:1px solid #bd0000;line-height:25px;">'
                                       '<i class="icon-txt icon-txt-len-1" style="background-color:#bd0000;margin-left: 4px;display: inline-block;width: 16px;height: 16px;'
                                       'line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font-style: normal;">爆</i></td>')
            result = result + '</tr>'
            if index == 0:
                result = result.replace("25px", "16px")
            index = index + 1
        result = result + '</tbody></table>'
        return result
    except Exception as e:
        traceback.print_exc()
        logger.info("获取热搜错误:{0}".format(e))
    return ""
