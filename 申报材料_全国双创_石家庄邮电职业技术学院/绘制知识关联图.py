#!/usr/bin/env python3
"""绘制三个示例场景的知识与教学关联示意图。"""
import os
from PIL import Image, ImageDraw, ImageFont

font_path = os.environ.get('CJK_FONT', '/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc')
out = '申报材料_全国双创_石家庄邮电职业技术学院/配图/业务知识关联图.png'
im = Image.new('RGB', (1800, 1500), '#ffffff')
d = ImageDraw.Draw(im)
title = ImageFont.truetype(font_path, 54)
small = ImageFont.truetype(font_path, 33)
main = ImageFont.truetype(font_path, 42)
sub = ImageFont.truetype(font_path, 34)
link = ImageFont.truetype(font_path, 30)
foot = ImageFont.truetype(font_path, 30)

def center(s, x, y, f, color):
    d.text((x, y), s, font=f, fill=color, anchor='mm')

def arrow(x, y1, y2):
    d.line((x, y1, x, y2-12), fill='#91aab8', width=4)
    d.polygon([(x,y2),(x-10,y2-15),(x+10,y2-15)], fill='#91aab8')

center('业务场景—政策资料—教学任务关联图', 900, 55, title, '#183c60')
center('以“0730资料库”为载体，选取三个典型场景说明知识如何服务教学', 900, 118, small, '#617889')
# Central source node branches into three concrete business-scenario nodes.
d.rounded_rectangle((580, 166, 1220, 265), radius=30, fill='#224e73')
center('0730资料库', 900, 215, main, 'white')
xs = [300, 900, 1500]
d.line((900, 265, 900, 307), fill='#91aab8', width=4)
d.line((300, 307, 1500, 307), fill='#91aab8', width=4)
for x in xs: arrow(x, 307, 350)
rows = [
    [('医保待遇', '职工医保住院待遇'), ('涉税服务', '小规模纳税人免税'), ('政府采购', '采购评审专家管理')],
    [('多级医保政策', '国家、省市待遇相关规定'), ('税费优惠政策', '免税规定及配套政策文件'), ('政府采购规定', '评审专家管理办法等文件')],
    [('待遇测算与核验', '比较版本并核对政策依据'), ('税费申报判断', '识别适用条件与政策依据'), ('采购合规分析', '辨识版本与分析管理要求')],
]
colors = [('#edf4fa','#275887'),('#edf7f6','#276c77'),('#faf6ee','#80673d')]
for row, entries in enumerate(rows):
    y = 350 + row*240
    bg, color = colors[row]
    for j, (name, detail) in enumerate(entries):
        x = xs[j]
        d.rounded_rectangle((x-245,y,x+245,y+150), radius=26, fill=bg, outline='#bdcfd9', width=3)
        center(name, x, y+52, main, color)
        center(detail, x, y+110, sub, '#435e6e')
        if row < 2:
            arrow(x,y+153,y+235)
            center('查找' if row == 0 else '转化',x+47,y+192,link,'#718b9a')

# Legend and common retrieval dimensions help distinguish node types.
for j, (label, color) in enumerate([('业务场景','#275887'),('关联资料','#276c77'),('教学任务示例','#80673d')]):
    x = 345+j*525
    d.ellipse((x-145,1126,x-125,1146),fill=color)
    center(label,x,1136,small,color)
d.rounded_rectangle((55,1180,1745,1304), radius=15, fill='#eef4f2', outline='#b8d0c7', width=2)
center('共同检索维度：业务领域  ·  政策层级  ·  文档形态', 900, 1220, sub, '#2e6a61')
center('政策有效状态仍需核验，避免混用新旧版本', 900, 1270, sub, '#41675f')
center('注：本图为三个场景的概念性关联示例，不代表已建成图数据库或完整知识图谱。', 900, 1377, foot, '#5e7382')
center('教学任务用于说明转化方向，实际应用与成果以相关材料和实施进度为准。', 900, 1431, foot, '#5e7382')
os.makedirs(os.path.dirname(out), exist_ok=True)
im.save(out, dpi=(300, 300), optimize=True)
print(out)
