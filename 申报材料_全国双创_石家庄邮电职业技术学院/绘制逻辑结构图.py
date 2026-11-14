#!/usr/bin/env python3
"""绘制案例协同育人路径图；字体可通过 CJK_FONT 环境变量覆盖。"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get('CJK_FONT', '/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc')
OUT = '申报材料_全国双创_石家庄邮电职业技术学院/配图/逻辑结构示意图.png'
im = Image.new('RGB', (1800, 1500), '#ffffff')
d = ImageDraw.Draw(im)
f_title = ImageFont.truetype(FONT, 58)
f_subtitle = ImageFont.truetype(FONT, 36)
f_label = ImageFont.truetype(FONT, 45)
f_card = ImageFont.truetype(FONT, 45)
f_detail = ImageFont.truetype(FONT, 34)
f_feedback = ImageFont.truetype(FONT, 40)
f_note = ImageFont.truetype(FONT, 32)

def centered(text, x, y, font, fill):
    d.text((x, y), text, font=font, fill=fill, anchor='mm')

centered('财税知识库驱动的协同育人路径', 900, 58, f_title, '#183c60')
centered('以企业真需求为牵引，以知识库实践为载体，以学生能力培养为目标', 900, 120, f_subtitle, '#5a6f81')

rows = [
    ('需求牵引', '企业业务场景', '#275887', '#edf4fa', [
        ('政策查询', '高频咨询 · 查找耗时'),
        ('版本辨识', '多级政策 · 新旧交替'),
        ('合规溯源', '明确依据 · 审慎判断'),
    ]),
    ('实践载体', '教师驻企与测试', '#276b78', '#eef7f6', [
        ('资料归集', '12领域 · 651篇文档'),
        ('知识库建设', '分类标注 · 检索规范'),
        ('测试与改进', '问题测试 · 对比复测'),
    ]),
    ('教学转化', '真任务融入教学', '#786138', '#faf6ee', [
        ('毕业设计', '标签体系 · 索引优化'),
        ('课程案例', '政策检索 · 业务判断'),
        ('校企协作', '共同定标 · 沟通反馈'),
    ]),
    ('育人目标', '面向岗位与双创', '#5a618c', '#f2f3fa', [
        ('业务判断', '识别问题 · 核验依据'),
        ('数智素养', '检索溯源 · 审视边界'),
        ('创新创业能力', '需求沟通 · 方案迭代'),
    ]),
]
for i, (label, label2, color, fill, cards) in enumerate(rows):
    y = 180 + i*265
    d.rounded_rectangle((45, y, 1720, y+208), radius=20, fill=fill, outline='#d3dee8', width=2)
    d.rounded_rectangle((45, y, 330, y+208), radius=20, fill=color)
    # cover right-hand rounded corners so the color meets the row cleanly
    d.rectangle((310, y, 330, y+208), fill=color)
    centered(label, 187, y+74, f_label, 'white')
    centered(label2, 187, y+136, f_detail, '#e4eef5')
    for j, (title, detail) in enumerate(cards):
        x = 355 + j*450
        d.rounded_rectangle((x, y+23, x+420, y+185), radius=13, fill='white', outline='#c5d4df', width=2)
        centered(title, x+210, y+77, f_card, color)
        centered(detail, x+210, y+135, f_detail, '#405c70')
    if i < len(rows)-1:
        # One central connector conveys translation between entire layers.
        x = 1030
        d.line((x, y+210, x, y+251), fill='#879eaf', width=5)
        d.polygon([(x, y+261), (x-12, y+243), (x+12, y+243)], fill='#879eaf')

# The feedback is a mechanism for use and improvement, not a claim that all future steps are complete.
d.rounded_rectangle((45, 1260, 1720, 1376), radius=18, fill='#eaf4f0', outline='#78a79b', width=2)
centered('反馈迭代', 185, 1318, f_label, '#356f65')
d.line((325, 1283, 325, 1353), fill='#adcfc4', width=2)
centered('企业反馈与验收  →  学生修改完善  →  成果回流与知识库更新', 1010, 1318, f_feedback, '#285f56')
# Return the feedback to the knowledge-base practice layer.
d.line([(1722, 1318), (1760, 1318), (1760, 549), (1731, 549)], fill='#63988c', width=4)
d.polygon([(1721, 549), (1738, 539), (1738, 559)], fill='#63988c')
centered('注：图示为案例实施路径与培养目标；反馈验收和持续更新按实际进度推进。', 900, 1430, f_note, '#687986')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT, dpi=(300, 300), optimize=True)
print(OUT)
