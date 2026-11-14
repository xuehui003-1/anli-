#!/usr/bin/env python3
"""绘制实施路线图，CJK_FONT 环境变量可指定中文字体。"""
import os
from PIL import Image, ImageDraw, ImageFont

font_path = os.environ.get('CJK_FONT', '/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc')
output = '申报材料_全国双创_石家庄邮电职业技术学院/配图/实施路线图.png'
im = Image.new('RGB', (1800, 1450), 'white')
d = ImageDraw.Draw(im)
title = ImageFont.truetype(font_path, 57)
subtitle = ImageFont.truetype(font_path, 36)
head = ImageFont.truetype(font_path, 37)
number = ImageFont.truetype(font_path, 40)
phase = ImageFont.truetype(font_path, 43)
text = ImageFont.truetype(font_path, 37)
note = ImageFont.truetype(font_path, 32)

def c(s, x, y, f, color):
    d.text((x, y), s, font=f, fill=color, anchor='mm')

def l(s, x, y, f, color):
    d.text((x, y), s, font=f, fill=color, anchor='lm')

c('财税知识库协同育人实施路线', 900, 60, title, '#173d62')
c('围绕真实任务，明确参与主体、实施行动与阶段产出', 900, 125, subtitle, '#64798a')
# Distinct column headings make it clear this is an execution map, not a second conceptual model.
d.rounded_rectangle((45, 183, 1750, 249), 10, fill='#244f75')
c('阶段', 230, 216, head, 'white')
c('参与主体与主要行动', 855, 216, head, 'white')
c('主要产出 / 预期产出', 1500, 216, head, 'white')
rows = [
    ('01', '驻企调研', '教师、企业', '走访座谈，梳理高频业务痛点', '需求与任务清单'),
    ('02', '建库与标注', '教师、企业', '归集资料，设计分类与检索规范', '知识库与使用规范'),
    ('03', '测试与改进', '教师及测试团队', '开展问题测试，对比复测结果', '测试记录与问题清单'),
    ('04', '教学转化', '教师、学生', '将真实任务融入毕设与课程', '毕设任务与课程案例'),
    ('05', '反馈与迭代', '企业、教师、学生（后续推进）', '反馈、修改、验收与成果回流', '优化方案（预期）'),
]
for i, (n, stage, who, action, out) in enumerate(rows):
    y = 265+i*189
    d.rounded_rectangle((45, y, 1750, y+160), 13, fill=('#f2f6fa' if i%2 == 0 else '#f8fafb'), outline='#d0dce5', width=2)
    d.rounded_rectangle((65, y+29, 150, y+130), 12, fill='#34739c')
    c(n, 107, y+80, number, 'white')
    l(stage, 172, y+81, phase, '#193f61')
    d.line((415, y+20, 415, y+140), fill='#d4e1e8', width=2)
    l(who, 445, y+52, text, '#225e7a')
    l(action, 445, y+111, text, '#344e60')
    d.line((1280, y+20, 1280, y+140), fill='#d4e1e8', width=2)
    c(out, 1515, y+80, text, '#2d655e')
    if i < 4:
        d.line((107, y+162, 107, y+179), fill='#7d9cb2', width=4)
        d.polygon([(107, y+188), (97, y+174), (117, y+174)], fill='#7d9cb2')
# Link the return loop without asserting that the final step is already completed.
d.rounded_rectangle((45, 1240, 1750, 1325), 13, fill='#e9f3ef', outline='#a5c8bb', width=2)
c('持续反馈：发现问题 → 调整标签与问法 → 复测验证 → 再应用', 897, 1282, text, '#2f6c60')
c('注：实施路径及阶段产出为案例归纳；反馈、验收与成果回流以实际进度为准。', 900, 1382, note, '#607580')
os.makedirs(os.path.dirname(output), exist_ok=True)
im.save(output, dpi=(300, 300), optimize=True)
print(output)
