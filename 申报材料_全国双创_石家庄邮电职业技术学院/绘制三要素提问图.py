#!/usr/bin/env python3
"""绘制三要素检索与原文核验示意图。CJK_FONT 可指定中文字体。"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get('CJK_FONT', '/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc')
OUT = '申报材料_全国双创_石家庄邮电职业技术学院/配图/三要素提问与核验示意图.png'
im = Image.new('RGB', (1800, 1170), 'white')
d = ImageDraw.Draw(im)
ftitle = ImageFont.truetype(FONT, 58)
fsub = ImageFont.truetype(FONT, 36)
fnum = ImageFont.truetype(FONT, 31)
fhead = ImageFont.truetype(FONT, 48)
fbody = ImageFont.truetype(FONT, 38)
fplus = ImageFont.truetype(FONT, 58)
fquery = ImageFont.truetype(FONT, 40)
fnote = ImageFont.truetype(FONT, 31)

def c(text, x, y, font, color):
    d.text((x, y), text, font=font, fill=color, anchor='mm')

def l(text, x, y, font, color):
    d.text((x, y), text, font=font, fill=color, anchor='lm')

c('三要素提问与原文核验', 900, 55, ftitle, '#173d60')
c('把业务问题说清楚，把政策范围和资料类型说具体', 900, 120, fsub, '#627989')

cards = [
    (65, '01', '业务领域', '职工医保住院待遇', '#275887', '#edf4fa'),
    (650, '02', '政策层级', '石家庄市', '#286c78', '#edf7f6'),
    (1235, '03', '文档形态', '政策原文', '#80673d', '#faf6ee'),
]
for x, num, name, value, color, bg in cards:
    d.rounded_rectangle((x, 180, x+500, 418), radius=24, fill=bg, outline='#c7d8e1', width=3)
    d.rounded_rectangle((x+22, 202, x+77, 251), radius=10, fill=color)
    c(num, x+49, 227, fnum, 'white')
    c(name, x+250, 270, fhead, color)
    d.line((x+47, 309, x+453, 309), fill='#c2d3dc', width=2)
    c(value, x+250, 359, fbody, '#304f61')
c('+', 607, 299, fplus, '#9baeb8')
c('+', 1192, 299, fplus, '#9baeb8')
# The three inputs combine into a question, not a claimed actual query result.
d.line((900, 425, 900, 476), fill='#86a0af', width=5)
d.polygon([(900,490),(887,471),(913,471)], fill='#86a0af')
d.rounded_rectangle((65, 500, 1735, 750), radius=22, fill='#f7f9fb', outline='#b9ccd9', width=3)
d.rounded_rectangle((96, 526, 332, 584), radius=10, fill='#244f75')
c('组合问法示例', 214, 555, fsub, 'white')
l('请依据石家庄市职工医保政策原文，说明职工医保住院待遇', 122, 640, fquery, '#233f54')
l('的主要规定，并标明文件名称和相关条款。', 122, 704, fquery, '#233f54')
# Verification step emphasizes that the method does not guarantee an answer.
d.rounded_rectangle((65, 790, 1735, 995), radius=22, fill='#eaf4f0', outline='#a8ccbf', width=3)
c('检索后核验', 900, 843, fhead, '#316b61')
c('对照原文  →  核实层级与现行有效性  →  结合具体业务判断', 900, 920, fbody, '#315f58')
c('注：示例用于说明提问结构；实际检索效果取决于资料覆盖与内容质量。', 900, 1070, fnote, '#627989')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT, dpi=(300, 300), optimize=True)
print(OUT)
