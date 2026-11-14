#!/usr/bin/env python3
"""绘制案例逻辑结构示意图；字体路径可通过 CJK_FONT 环境变量覆盖。"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get('CJK_FONT', '/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc')
OUT = '申报材料_全国双创_石家庄邮电职业技术学院/配图/逻辑结构示意图.png'
im = Image.new('RGB', (1800, 620), '#ffffff')
d = ImageDraw.Draw(im)
f_title = ImageFont.truetype(FONT, 45)
f_main = ImageFont.truetype(FONT, 38)
f_sub = ImageFont.truetype(FONT, 28)
f_note = ImageFont.truetype(FONT, 27)

def center(text, xy, font, color):
    d.text(xy, text, font=font, fill=color, anchor='mm')

center('财税知识库驱动的协同育人逻辑', (900, 55), f_title, '#17385b')
boxes = [
    ('企业真实需求', '驻企调研  ·  业务痛点', '教师与企业共同梳理'),
    ('知识库建设', '归集资料  ·  分类标注', '形成政策检索底座'),
    ('测试与改进', '发现缺陷  ·  对比复测', '明确AI能力边界'),
    ('教学实践', '毕业设计  ·  课程案例', '学生围绕真任务训练'),
]
for i, (title, sub, desc) in enumerate(boxes):
    x = 45 + i * 440
    d.rounded_rectangle((x, 135, x+385, 370), 20, fill='#f1f6fb', outline='#396b98', width=3)
    center(title, (x+192, 196), f_main, '#163b62')
    d.line((x+38, 234, x+347, 234), fill='#aac2d6', width=2)
    center(sub, (x+192, 275), f_sub, '#234c6e')
    center(desc, (x+192, 327), f_sub, '#234c6e')
    if i < 3:
        d.line((x+390, 252, x+423, 252), fill='#396b98', width=5)
        d.polygon([(x+432,252),(x+414,241),(x+414,263)], fill='#396b98')
# feedback loop: training -> enterprise requirements, expressing a process rather than a claimed result
d.line([(1540, 380), (1540, 455), (235, 455), (235, 387)], fill='#54877f', width=4)
d.polygon([(235, 377),(224, 396),(246, 396)], fill='#54877f')
d.rounded_rectangle((600, 427, 1160, 484), 12, fill='white')
center('企业反馈与验收  ·  成果回流  ·  持续迭代', (880, 454), f_note, '#315e58')
center('注：示意图概括案例路径；反馈验收和持续迭代按正文所述推进。', (900, 559), f_note, '#5b6671')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT, dpi=(300, 300), optimize=True)
print(OUT)
