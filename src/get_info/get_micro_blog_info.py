#!/usr/bin/python
# -*- coding: UTF-8 -*-
import traceback
"""
    name:       获取微博信息
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 获取微博信息，例如热搜榜等
"""
import re


# 处理成可以展示的html
def change_css(html_content):
    # 热度标签样式
    # html_content = html_content.replace("background-color:#bd0000;",
    #                     'background-color:#bd0000;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    # html_content = html_content.replace("background-color:#ff3852;",
    #                     'background-color:#ff3852;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    # html_content = html_content.replace("background-color:#ffab5a;",
    #                     'background-color:#ffab5a;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    # html_content = html_content.replace("background-color:#ff9406;",
    #                     'background-color:#ff9406;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    # html_content = html_content.replace("background-color:#f86400;",
    #                     'background-color:#f86400;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace('>新<', '>&nbsp;新&nbsp;<')
    html_content = html_content.replace('>热<', '>&nbsp;热&nbsp;<')
    html_content = html_content.replace('>暖<', '>&nbsp;暖&nbsp;<')
    html_content = html_content.replace('>沸<', '>&nbsp;沸&nbsp;<')
    html_content = html_content.replace('>爆<', '>&nbsp;爆&nbsp;<')
    # 去掉顶部热搜
    matches = re.findall('<tr class="">\n.*<td class="td-01"><i class="icon-top">.*\n.*\n.*\n.*\n.*\n.*</tr>', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 去掉广告
    matches = re.findall('<tr class="">\n.*<td class="td-01 ranktop".*\n.*\n.*\n.*\n.*\n.*\n.*</tr>', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 去掉图片
    matches = re.findall('<img src.*">', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 热搜文字样式
    for index in range(51):
        if index == 1:
            html_content = html_content.replace('class="td-01 ranktop ranktop' + str(index) + '"',
                                                'class="td-01 ranktop ranktop' + str(index) + '" style="border-bottom:0px solid #f9f9f9;line-height:16px;color: #f26d5f;"')
        if index <= 3:
            html_content = html_content.replace('class="td-01 ranktop ranktop' + str(index) + '"',
                                                'class="td-01 ranktop ranktop' + str(index) + '" style="border-bottom:0px solid #f9f9f9;line-height:25px;color: #f26d5f;"')
        else:
            html_content = html_content.replace('class="td-01 ranktop ranktop' + str(index) + '"',
                                                'class="td-01 ranktop ranktop' + str(index) + '" style="border-bottom:0px solid #f9f9f9;line-height:25px;color: #ff8200;"')
    html_content = html_content.replace('class="td-02"',
                                        'class="td-02" style="border-bottom:0px solid #f9f9f9;line-height:25px;"')
    html_content = html_content.replace('class="td-03"',
                                        'class="td-03" style="border-bottom:0px solid #f9f9f9;line-height:25px;"')
    html_content = html_content.replace('target="_blank">',
                                        'target="_blank" style="text-decoration:none;color:#0078b6;">')
    html_content = html_content.replace('class="th-02"',
                                        'class="th-02" style="width:1000px;min-width:1000px;"')
    # html_content = html_content.replace('</tbody>',
    #                                     '<tr style="line-height:1px;height: 1px;"><td></td><td><span style="color:white">'
    #                                     '———————————————————————————'
    #                                     '</span></td><td></td></tr></tbody>')
    return html_content
