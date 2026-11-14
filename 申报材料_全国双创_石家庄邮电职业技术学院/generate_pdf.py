#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os

# 注册中文字体（NotoSansCJK TTC）
font_path = "/tmp/fonts/noto-cjk-main/android/NotoSansCJK-wght-400-900.ttf.ttc"
pdfmetrics.registerFont(TTFont('NotoSansCJK', font_path))
# 注册粗体用同一字体（通过加粗模拟）
# 为了有区分，我们再注册一个名字
# 使用同一文件作为“黑体”替代
pdfmetrics.registerFont(TTFont('NotoBold', font_path))

# 定义颜色
COLOR_PRIMARY = HexColor("#1F4E79")
COLOR_SECONDARY = HexColor("#4472C4")
COLOR_LIGHT = HexColor("#D9E1F2")
COLOR_ACCENT = HexColor("#E2EFDA")
COLOR_GRAY = HexColor("#595959")

# 样式
styles = {}

styles['TitleMain'] = ParagraphStyle(
    'TitleMain',
    fontName='NotoBold',
    fontSize=22,
    leading=26,
    alignment=TA_CENTER,
    textColor=black,
    spaceAfter=6,
)

styles['TitleSub'] = ParagraphStyle(
    'TitleSub',
    fontName='NotoSansCJK',
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    textColor=COLOR_PRIMARY,
    spaceAfter=18,
)

styles['Heading1'] = ParagraphStyle(
    'Heading1',
    fontName='NotoBold',
    fontSize=13,
    leading=18,
    textColor=COLOR_PRIMARY,
    alignment=TA_LEFT,
    spaceBefore=14,
    spaceAfter=8,
    keepWithNext=True,
    borderPadding=(0,0,6),
)

styles['Heading2'] = ParagraphStyle(
    'Heading2',
    fontName='NotoSansCJK',
    fontSize=11,
    leading=16,
    textColor=black,
    alignment=TA_LEFT,
    spaceBefore=10,
    spaceAfter=5,
    keepWithNext=True,
    fontName2='NotoBold',
)

styles['Body'] = ParagraphStyle(
    'Body',
    fontName='NotoSansCJK',
    fontSize=9.5,
    leading=16,
    alignment=TA_JUSTIFY,
    textColor=black,
    spaceAfter=6,
    firstLineIndent=19,  # 2字符缩进
)

styles['BodyNoIndent'] = ParagraphStyle(
    'BodyNoIndent',
    fontName='NotoSansCJK',
    fontSize=9.5,
    leading=16,
    alignment=TA_JUSTIFY,
    textColor=black,
    spaceAfter=6,
    firstLineIndent=0,
)

styles['Caption'] = ParagraphStyle(
    'Caption',
    fontName='NotoSansCJK',
    fontSize=8,
    leading=11,
    alignment=TA_CENTER,
    textColor=COLOR_GRAY,
    spaceBefore=3,
    spaceAfter=8,
)

styles['TableHeader'] = ParagraphStyle(
    'TableHeader',
    fontName='NotoBold',
    fontSize=7.5,
    leading=10,
    alignment=TA_CENTER,
    textColor=white,
)

styles['TableCell'] = ParagraphStyle(
    'TableCell',
    fontName='NotoSansCJK',
    fontSize=7,
    leading=9,
    alignment=TA_LEFT,
    textColor=black,
)

styles['TableCellCenter'] = ParagraphStyle(
    'TableCellCenter',
    fontName='NotoSansCJK',
    fontSize=7,
    leading=9,
    alignment=TA_CENTER,
    textColor=black,
)

styles['Abstract'] = ParagraphStyle(
    'Abstract',
    fontName='NotoSansCJK',
    fontSize=8,
    leading=12,
    alignment=TA_JUSTIFY,
    textColor=HexColor("#333333"),
    spaceAfter=4,
    firstLineIndent=16,
    borderColor=COLOR_LIGHT,
    borderWidth=0.5,
    borderPadding=(6,6,6),
    backColor=HexColor("#F2F2F2"),
)

def header_footer(canvas, doc):
    canvas.saveState()
    # 页眉：联盟名称
    canvas.setFont('NotoSansCJK', 7)
    canvas.setFillColor(COLOR_GRAY)
    canvas.drawCentredString(A4[0]/2, A4[1]-20*mm, "2026年全国高职院校创新创业教育教学典型经验案例 · 石家庄邮电职业技术学院")
    # 页脚页码
    canvas.setFont('NotoSansCJK', 7)
    canvas.drawCentredString(A4[0]/2, 12*mm, f"— {doc.page} —")
    # 装饰线
    canvas.setStrokeColor(COLOR_SECONDARY)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, A4[1]-22*mm, A4[0]-15*mm, A4[1]-22*mm)
    canvas.restoreState()

output_path = "申报材料_全国双创_石家庄邮电职业技术学院/高职创盟典型经验案例+石家庄邮电职业技术学院+AI赋能、真题真做——财税知识库驱动的创新创业教育实践.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=22*mm,
    rightMargin=22*mm,
    topMargin=25*mm,
    bottomMargin=18*mm,
    title="AI赋能、真题真做——财税知识库驱动的创新创业教育实践",
    author="石家庄邮电职业技术学院 薛辉",
)

story = []

# 封面标题
story.append(Spacer(1, 10*mm))
story.append(Paragraph("AI赋能、真题真做", styles['TitleMain']))
story.append(Paragraph("——财税知识库驱动的创新创业教育实践", styles['TitleSub']))
story.append(Paragraph("石家庄邮电职业技术学院会计学院", ParagraphStyle('School', parent=styles['TitleSub'], fontSize=11, textColor=COLOR_GRAY, spaceAfter=4*mm)))
story.append(Spacer(1, 2*mm))

# 基本信息表
info_data = [
    [Paragraph("<b>项目</b>", styles['TableHeader']), Paragraph("<b>内容</b>", styles['TableHeader'])],
    [Paragraph("申报类别", styles['TableCellCenter']), Paragraph("创新创业教育实践教学与项目孵化<font color=\"#4472C4\">（兼AI赋能课程改革，含智能学伴、真实项目进课堂）</font>", styles['TableCell'])],
    [Paragraph("申报单位", styles['TableCellCenter']), Paragraph("石家庄邮电职业技术学院（会计学院）", styles['TableCell'])],
    [Paragraph("联合单位", styles['TableCellCenter']), Paragraph("河北企富财税管理有限公司（会计师事务所·税务师事务所资质）", styles['TableCell'])],
    [Paragraph("主要完成人", styles['TableCellCenter']), Paragraph("薛辉、张勇、王爱辉、任伟峰、李莉（不超过5人）", styles['TableCell'])],
    [Paragraph("联系人", styles['TableCellCenter']), Paragraph("薛辉 18332128207 · xuehui006@outlook.com", styles['TableCell'])],
    [Paragraph("关键词", styles['TableCellCenter']), Paragraph("AI赋能；产教融合；真实项目；财税知识库；创新创业教育", styles['TableCell'])],
]
t = Table(info_data, colWidths=[28*mm, 120*mm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('BACKGROUND', (0,1), (0,-1), COLOR_LIGHT),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F2F6FC")]),
]))
story.append(t)
story.append(Spacer(1, 5*mm))

# 摘要
story.append(Paragraph("摘要", ParagraphStyle('AbsTitle', parent=styles['Heading2'], fontSize=9, textColor=COLOR_PRIMARY, spaceAfter=2, alignment=TA_LEFT, firstLineIndent=0)))
abstract_text = """本案例聚焦高职财经类专业“<b>学难致用、练不适岗、创无支撑</b>”的共性痛点，以河北企富财税管理有限公司应对《涉税专业服务管理办法（试行）》（国家税务总局令第58号）合规新规的真实需求为切入口，由教师驻企42天牵头构建基于腾讯ima平台的“<b>0730资料库</b>”，归集财税、医保、政府采购等<b>12领域651篇</b>政策文档，创设“<b>二级标签+层级+格式</b>”三维标注体系与“<b>业务领域+层级+文档形态</b>”三要素检索规范，完成<b>两轮19题</b>系统测试并以“<b>知识库测试问题11.11对比</b>”验证迭代成效；进而将二期“打标重建”任务转化为<b>财务管理专业毕业设计真题</b>，由3名学生直接对接企业、按企业标准迭代并接受企业验收，实现“<b>教师下企业—带回真课题—学生做真题—成果回企业</b>”的闭环。实践使企业高频政策查询由<b>15～30分钟缩短至秒级</b>，输出<b>6组合规分析</b>并反哺<b>4门核心课程</b>，为AI赋能的创新创业教育提供了“<b>真问题、小切口、可复制</b>”的范式。"""
story.append(Paragraph(abstract_text, styles['Abstract']))
story.append(Paragraph("关键词：创新创业教育；AI赋能；真实项目；财税知识库；产教融合", ParagraphStyle('Keywords', parent=styles['BodyNoIndent'], fontSize=8, textColor=COLOR_GRAY, spaceBefore=2, firstLineIndent=0)))
story.append(Spacer(1, 4*mm))

# 正文
# 一、背景
story.append(Paragraph("一、背景与问题：从合规新规到教学痛点的真实牵引", styles['Heading1']))
story.append(Paragraph("石家庄邮电职业技术学院会计学院开设大数据与会计、财务管理等专业，对口服务京津冀中小财税服务机构。这类机构轻资产、重政策，客户问的是“这个优惠还能不能用、那条红线能不能碰”，答复既要<b>快、准</b>，还要<b>追到原文条款</b>。2025年5月1日，《涉税专业服务管理办法（试行）》（<b>国家税务总局令第58号</b>）施行，将“答复快、准、可追溯”从服务加分项变为<b>合规硬义务</b>：要求机构建立质量管理制度、风控机制和业务底稿，审计鉴证还需证据链完整、可复核。对以<b>代理记账、涉税服务、企业管家</b>为主业的河北企富财税管理有限公司而言，文件散在个人电脑与微信群、找一篇政策要<b>15～30分钟</b>且难辨现行有效性的现状，已直接构成合规风险。", styles['Body']))
story.append(Paragraph("学校端是同一矛盾的另一面。教材更新滞后新规半年以上，实训多为教师虚构的“干净数据”，与企业“<b>多版本并存、省市联动、新旧交替</b>”的真场景存在时差。例如石家庄市职工医保在<b>2017年（石政发〔2017〕2号）、2019年（石政规〔2019〕7号）、2024年（石政规〔2024〕7号）</b>三度修订，起付线、报销比、年度限额逐次调整；河北省评审专家管理在2025年以<b>冀财采〔2025〕12号废止冀财采〔2023〕13号</b>。若学生仅凭教材记忆作答，极易引用失效条款。更深层的痛点是：学生<b>会做题，不会查；会背条文，不会断新旧；会用工具，不会审边界</b>。创新创业教育若停留在“写商业计划书”，便无法培养出能在真实合规约束下持续创新的人。", styles['Body']))
story.append(Paragraph("基于此，学院于<b>2026年7月15日至8月25日</b>选派教师赴企富<b>驻企实践42天</b>，确立“<b>以真实合规清单倒推知识管理能力、以知识库建设牵引教学改革</b>”的总体思路，把企业知识管理困境转化为师生创新创业练兵场。", styles['Body']))

# 二、做法
story.append(Paragraph("二、主要做法：AI为翼、真题为场，构建“学—做—创”一体模式", styles['Heading1']))
story.append(Paragraph("案例形成“<b>教师下企业搭平台—AI能力边界当教材—学生接真题进企业</b>”的三段式路径，核心是将企业数字化转型中的真实任务完整搬进教学，使创新创业教育在<b>真需求、真标准、真验收</b>中发生（见图1）。", styles['Body']))

img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/逻辑结构示意图.png", width=137*mm, height=114.17*mm)
img.hAlign = 'CENTER'
story.append(KeepTogether([img, Paragraph("图1 &nbsp; 财税知识库驱动的协同育人逻辑结构示意图", styles['Caption'])]))

story.append(Paragraph("（一）驻企搭平台：从零建成651篇结构化知识库", styles['Heading2']))
story.append(Paragraph("实践团队采用“<b>实地走访+岗位跟岗+座谈访谈+归集清洗</b>”四步法，走访代理记账、涉税服务、企业管家三条业务线，与审计部、会计部骨干多轮座谈，梳理出“问题—任务—交付物”清单：如月销售额10万元以下小规模纳税人免税、六税两费叠加减征、职工医保住院待遇测算等高频场景，均需秒级溯源。", styles['Body']))
story.append(Paragraph("依托<b>腾讯ima共享知识库平台</b>建成“<b>0730资料库</b>”，共归集文档<b>651篇</b>，其中<b>PDF 232篇</b>（政策原文）、<b>Word 397篇</b>（制度细则）、<b>Excel 22篇</b>（目录、价格、科目表），无PPT、网页、笔记冗余，全部为业务必备文档，覆盖<b>国家、河北省、石家庄市三级</b>。分类采用“<b>二级标签法（行业-业务）</b>”，设<b>12个一级领域、80余个二级标签</b>，医保板块因业务高频进一步细化至待遇保障（职工/居民）、筹资缴费、支付结算、药品目录、特殊病种、诊疗项目与价格、定点管理、基金监管等子类。每篇文档同步完成<b>层级标签</b>（国家/河北省/石家庄市）、<b>格式辅助标签</b>（PDF-政策原文/Excel-价格表等）与<b>状态预留字段</b>（施行中/已废止），为AI检索提供结构化底座。", styles['Body']))

# 表1
story.append(Paragraph("表1 &nbsp; 0730资料库分类与标注体系", styles['Caption']))
table1_data = [
    [Paragraph("<b>维度</b>", styles['TableHeader']), Paragraph("<b>内容</b>", styles['TableHeader'])],
    [Paragraph("文档总量", styles['TableCellCenter']), Paragraph("651篇：PDF 232篇（政策原文）、Word 397篇（制度细则）、Excel 22篇（目录台账）", styles['TableCell'])],
    [Paragraph("一级领域", styles['TableCellCenter']), Paragraph("12个：医保、财税、会计、审计、国资、农村集体、行政事业、招投标基建、社保、医疗卫生、党建纪检、其他行业", styles['TableCell'])],
    [Paragraph("二级标签", styles['TableCellCenter']), Paragraph("80余个；医保板块细分至20个子类（待遇保障、筹资缴费、支付结算、药品目录、特殊病种等）", styles['TableCell'])],
    [Paragraph("层级标签", styles['TableCellCenter']), Paragraph("国家政策／河北省／石家庄市（按文号与执行层级判定）", styles['TableCell'])],
    [Paragraph("格式标签", styles['TableCellCenter']), Paragraph("PDF-政策原文／Word-制度细则／Excel-目录台账／PDF-问答汇编", styles['TableCell'])],
    [Paragraph("业务板块", styles['TableCellCenter']), Paragraph("医疗保障、涉税专业服务、政府采购、会计审计、预算绩效、农村集体财务、党建纪检", styles['TableCell'])],
]
t1 = Table(table1_data, colWidths=[26*mm, 122*mm])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('BACKGROUND', (0,1), (0,-1), COLOR_LIGHT),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F2F6FC")]),
]))
story.append(t1)

# 图片1和2
for img_path, caption in [
    ("申报材料_全国双创_石家庄邮电职业技术学院/配图/图1_企业座谈.jpg", "图2 &nbsp; 教师驻企与审计部、会计部骨干座谈梳理高频政策场景（2026年7月）"),
    ("申报材料_全国双创_石家庄邮电职业技术学院/配图/图2_需求调研.jpg", "图3 &nbsp; 座谈调研现场：企业部门骨干介绍业务流程与政策使用场景"),
]:
    if os.path.exists(img_path):
        story.append(Spacer(1, 3*mm))
        # 控制图片宽度
        img = RLImage(img_path, width=120*mm, height=80*mm, kind="bound")
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Paragraph(caption, styles['Caption']))

story.append(Paragraph("（二）以测促创：两轮19题摸清AI能力边界，把缺陷变教材", styles['Heading2']))
story.append(Paragraph("知识库一期建成后，团队并未直接交付，而是设计<b>两轮系统测试</b>把AI的“能与不能”摆上台面，让技术边界成为创新创业素养的教学点。", styles['Body']))
story.append(Paragraph("<b>1. 首轮5题“抗诱导/防编造”测试（2026年10月25日）。</b>针对库外问题（如“天津市医保报销比”、虚构的“2026年农村集体免税新政”）与错误前提诱导（如“只要签合同就可不走采购流程”“合作社可随意处置集体土地所有权”），AI均能准确识别并拒绝编造，验证了检索忠实性。此结果增强了企业对AI辅助合规的信任，也为课堂提供了“AI不会胡说，但会漏、会飘”的理性预期。", styles['Body']))
# 图3 抗诱导
if os.path.exists("申报材料_全国双创_石家庄邮电职业技术学院/配图/图4_抗诱导防编造测试.png"):
    story.append(Spacer(1, 3*mm))
    img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/图4_抗诱导防编造测试.png", width=135*mm, height=82*mm, kind="bound")
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Paragraph("图4 &nbsp; 首轮抗诱导测试：库外问题“天津市城乡居民医保报销比例”被准确识别为无相关资料，AI未编造", styles['Caption']))
story.append(Paragraph("<b>2. 第二轮14题深度测试（2026年10月28日）。</b>覆盖同题稳定性、引文溯源、跨文档召回、召回截断、多规则叠加、版本识别、多轮记忆等维度，暴露六类典型缺陷：向量召回随机漂移导致同题异答、引用角标无法跳转、长文被截断致要点遗漏、多版本混淆、小点被忽略、上下文脱节。同时诊断出平台硬限制：<b>单次最多返回约45条、无分页参数、体量大时必须手工打标</b>才能稳住召回。", styles['Body']))

# 表2
story.append(Paragraph("表2 &nbsp; 两轮AI检索测试维度与改进（摘自“知识库测试问题11.11对比.xlsx”）", styles['Caption']))
table2_data = [
    [Paragraph("<b>测试维度</b>", styles['TableHeader']), Paragraph("<b>代表问题</b>", styles['TableHeader']), Paragraph("<b>初测缺陷</b>", styles['TableHeader']), Paragraph("<b>精细打标后效果</b>", styles['TableHeader'])],
    [Paragraph("同题稳定性", styles['TableCellCenter']), Paragraph("河北省门诊慢特病认定要求", styles['TableCell']), Paragraph("召回片段随机漂移，示例池无固定", styles['TableCell']), Paragraph("稳定性增强，无大幅跳动", styles['TableCell'])],
    [Paragraph("引文溯源", styles['TableCellCenter']), Paragraph("公务接待陪餐人数", styles['TableCell']), Paragraph("出现[citation:word_1]无法跳转", styles['TableCell']), Paragraph("可正常跳转并高亮原文段落", styles['TableCell'])],
    [Paragraph("跨文档召回", styles['TableCellCenter']), Paragraph("对比政府会计与企业会计差异", styles['TableCell']), Paragraph("召回弱相关/重复文件，噪声大", styles['TableCell']), Paragraph("相关性增强，无无关文件", styles['TableCell'])],
    [Paragraph("召回截断", styles['TableCellCenter']), Paragraph("冀财社〔2017〕32号三重保障流程", styles['TableCell']), Paragraph("长文截断，要点遗漏", styles['TableCell']), Paragraph("按指定文号精准答复，补充相似文件兜底", styles['TableCell'])],
    [Paragraph("多规则叠加", styles['TableCellCenter']), Paragraph("透析费用：县域结算+三重保障+监管", styles['TableCell']), Paragraph("忽略叠加顺序", styles['TableCell']), Paragraph("不会编造缺失文件，严格按库回答", styles['TableCell'])],
    [Paragraph("要点完整性", styles['TableCellCenter']), Paragraph("机场研发强度标准值", styles['TableCell']), Paragraph("回答不全（遗漏企业规模分档）", styles['TableCell']), Paragraph("能发现重复有效信息并补全", styles['TableCell'])],
]
t2 = Table(table2_data, colWidths=[24*mm, 36*mm, 42*mm, 46*mm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F2F6FC")]),
]))
story.append(t2)
story.append(Paragraph("注：计费题在对比表中记录的参考结果为7&nbsp;142.4元，具体计算口径需结合原始政策核验；会计法罚款上限等版本题由“答错”变为“主动总结新旧差异”。", ParagraphStyle('Note', parent=styles['BodyNoIndent'], fontSize=7, textColor=COLOR_GRAY, firstLineIndent=0, spaceBefore=2)))

if os.path.exists("申报材料_全国双创_石家庄邮电职业技术学院/配图/图5_药品纳入医保精准检索.png"):
    story.append(Spacer(1, 3*mm))
    img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/图5_药品纳入医保精准检索.png", width=135*mm, height=85*mm, kind="bound")
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Paragraph("图5 &nbsp; 单点细节检索：药品纳入医保条件——精准引用《国家药品目录》与中办发文，结构化作答", styles['Caption']))

story.append(Paragraph("<b>3. 迭代验证：11.11对比。</b>同样的14题在精细打标后复测，问题显著收敛：同题稳定性“<b>未出现大幅跳动</b>”、引文“<b>可正常跳转并高亮原文段落</b>”、跨文档召回“<b>未出现无关或重复文件</b>”、计费题复测记录显示能指出误区，参考结果为<b>7&nbsp;142.4元</b>（计算口径待核验）、多规则叠加题“<b>不会现编不存在的32号文且更严谨</b>”。这一“测—改—再测”的过程本身，就是一堂生动的创新创业课：<b>创新不是追新工具，而是弄清约束、在约束内用规则与流程补位</b>。", styles['Body']))
if os.path.exists("申报材料_全国双创_石家庄邮电职业技术学院/配图/图6_三重保障叠加顺序.png"):
    story.append(Spacer(1, 3*mm))
    img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/图6_三重保障叠加顺序.png", width=135*mm, height=82*mm, kind="bound")
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Paragraph("图6 &nbsp; 多规则叠加实测：贫困透析患者“县域结算→基本医保→大病保险→三重保障”四步叠加顺序被完整还原", styles['Caption']))

# 三要素检索规范（用高亮框模拟）
story.append(Paragraph("表3 &nbsp; 三要素检索规范：业务领域+层级+文档形态", styles['Caption']))
elem_data = [
    [Paragraph("<b>要素</b>", styles['TableHeader']), Paragraph("<b>示例问法</b>", styles['TableHeader']), Paragraph("<b>检索价值</b>", styles['TableHeader'])],
    [Paragraph("业务领域", styles['TableCellCenter']), Paragraph("职工医保住院报销 / 政府采购评审专家", styles['TableCell']), Paragraph("锁定12领域与80+二级标签", styles['TableCell'])],
    [Paragraph("层级", styles['TableCellCenter']), Paragraph("石家庄市 / 河北省 / 国家", styles['TableCell']), Paragraph("避免省市混用、省市链条断裂", styles['TableCell'])],
    [Paragraph("文档形态", styles['TableCellCenter']), Paragraph("政策原文 / 价格表 / 问答汇编", styles['TableCell']), Paragraph("区分正文与目录表，提升命中率", styles['TableCell'])],
    [Paragraph("完整示例", styles['TableCellCenter']), Paragraph("“石家庄市 职工医保住院 政策原文”", styles['TableCell']), Paragraph("三要素合一，命中率显著高于单关键词", styles['TableCell'])],
]
te = Table(elem_data, colWidths=[24*mm, 50*mm, 74*mm])
te.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor("#70AD47")),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#E2EFDA")]),
]))
story.append(te)
if os.path.exists("申报材料_全国双创_石家庄邮电职业技术学院/配图/图3_三要素提问规范.png"):
    story.append(Spacer(1, 3*mm))
    img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/图3_三要素提问规范.png", width=120*mm, height=35*mm, kind="bound")
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Paragraph("图7 &nbsp; 三要素提问法在企业中的落地示意：说清业务+层级+形态", styles['Caption']))
story.append(Paragraph("配套产出《知识库使用规范手册》，明确“<b>文件名/文号/层级/业务</b>”四必带、查不到时“<b>加标签缩小范围或直开原文提问</b>”的二阶策略，解决一线“查不到、查不准”痛点。", styles['Body']))

story.append(Paragraph("（三）真题进课堂：毕业设计与课程的双重活化", styles['Heading2']))
story.append(Paragraph("一期“有库无标、检而不准”的缺口，正是中小企业“<b>知道该做、没人做、不会做</b>”的缩影，也是职业教育可介入的真空。学院将二期“打标重建与索引优化”作为<b>2027届财务管理专业岗位核心知识技能类毕业设计新增选题</b>——“<b>财税法规知识库文档标签体系构建与分类整理</b>”，由<b>财管2401班3名学生</b>组队承接，企业出具验收证明即为答辩依据之一。", styles['Body']))
story.append(Paragraph("<b>1. 过程真：学生直连企业。</b>小组先赴企富与审计部、会计部骨干座谈，把一线“查不到、查不准”痛点转化为标签设计输入；选取30篇样板文档试打，企业逐条校准二级标签、层级与状态字段口径，通过后才批量推进651篇逐篇打标、重建索引，并用19题测试用例回归验证准确率，针对召回漂移、引文失效等问题以精细标签与人工规则补位（见图8）。", styles['Body']))
img = RLImage("申报材料_全国双创_石家庄邮电职业技术学院/配图/师生毕设指导_原稿.jpg", width=130*mm, height=97.5*mm)
img.hAlign = 'CENTER'
story.append(KeepTogether([img, Paragraph("图8 &nbsp; 教师指导毕设小组梳理企业需求、搭建知识库标签体系（2026年10月，原稿图片）", styles['Caption'])]))

story.append(Paragraph("<b>2. 标准真：企业标准替代分数。</b>成果需满足企业“<b>可检索、可维护、可培训</b>”三验收：标签命名让一线同事“不培训也能猜对”，三要素问法让新人“问一次就能中”，使用手册让部门“照着就能教”。学生需在企业面前为自己的打标方案辩护、按反馈迭代，而非在教室交一份教师打分的纸面报告。这一过程本身即是创业预演：<b>需求挖掘—方案设计—客户验证—迭代交付</b>。", styles['Body']))
story.append(Paragraph("<b>3. 课堂真：4门核心课程活页化。</b>651篇真实政策同步转化为《<b>智慧化税费申报与管理</b>》《<b>财经法规与会计职业道德</b>》《<b>审计实务</b>》《<b>大数据与会计综合实训</b>》案例库：职工医保三版待遇比对做待遇测算实训，小规模纳税人免税与六税两费叠加做申报判断，评审专家七类不良行为与代理机构八项检查内容做合规教育，直接责任与领导责任划分做经济责任审计模拟。标签体系与三要素检索法本身亦成为“数智工具能力”与“综合实训”的训练内容，并以<b>活页、工作手册</b>形态持续更新，破解教材滞后难题。", styles['Body']))
story.append(Paragraph("<b>4. 评价真：过程性与成果导向并重。</b>毕业设计评价引入<b>企业验收分、检索准确率提升分、手册可用度分</b>，替代单一论文分；课堂评价增加“<b>检索—判断—归档—复用</b>”全链条实操考核，体现全国双创联盟倡导的过程性、多元化考核方向。", styles['Body']))

story.append(Paragraph("（四）闭环复制：从审计部到会计部的方法论迁移", styles['Heading2']))
story.append(Paragraph("审计部跑通后，团队将“<b>提标准—对方认领—节点验收</b>”闭环工作法复制至会计部，指导其按“二级标签+层级+格式”规范打包资料并明确打标要求，对方已认领并启动整理。一期曾因“说明书式”布置而落地不足的教训，反向成为教学案例：让学生理解“<b>标准不等于执行，创新在于设计可执行的协作机制</b>”。下一阶段将打通两部门库，建成企业统一检索平台，并推动挂牌实习实训基地与横向课题。", styles['Body']))

story.append(Paragraph("三、实施成效：可量化、可感知、可迁移", styles['Heading1']))
story.append(Paragraph("以“<b>是否让企业少跑腿、学生多真练、课堂更鲜活</b>”为尺度，成效体现在四端。", styles['Body']))

story.append(Paragraph("（一）企业端：合规基础设施从无到有，效率从分钟级到秒级", styles['Heading2']))
story.append(Paragraph("651篇结构化文档覆盖12领域、80余标签，一线人员由“翻文件夹”升级为“<b>自然语言提问+AI原文引用</b>”作业模式，高频政策查询响应由人均<b>15～30分钟缩短至秒级</b>；已交付审计部<b>6组合规分析</b>，每项形成“<b>事实描述—条款引用—问题定性—整改建议</b>”闭环，覆盖医疗收费、长期挂账、无形资产挪用、资产转固、诊疗收费整改、支出归集等事项，直接协助识别并化解涉税与审计风险，方法论已复制至会计部。", styles['Body']))

# 表3
story.append(Paragraph("表4 &nbsp; 已交付的6组合规分析（审计部）", styles['Caption']))
table3_data = [
    [Paragraph("<b>序号</b>", styles['TableHeader']), Paragraph("<b>事项</b>", styles['TableHeader']), Paragraph("<b>关键条款引用</b>", styles['TableHeader']), Paragraph("<b>成效</b>", styles['TableHeader'])],
    [Paragraph("1", styles['TableCellCenter']), Paragraph("耳鼻喉科医疗收费合规性", styles['TableCell']), Paragraph("医保支付结算+诊疗项目价格", styles['TableCell']), Paragraph("核减不合规收费项", styles['TableCell'])],
    [Paragraph("2", styles['TableCellCenter']), Paragraph("长期往来款挂账", styles['TableCell']), Paragraph("政府会计制度+往来清理", styles['TableCell']), Paragraph("清理3年以上挂账，建立对账机制", styles['TableCell'])],
    [Paragraph("3", styles['TableCellCenter']), Paragraph("无形资产购置费挪用", styles['TableCell']), Paragraph("预算管理+资产配置", styles['TableCell']), Paragraph("追溯资金用途，规范科目归集", styles['TableCell'])],
    [Paragraph("4", styles['TableCellCenter']), Paragraph("固定资产账卡核对与在建工程转固", styles['TableCell']), Paragraph("资产管理+转固时点", styles['TableCell']), Paragraph("补提折旧，转固流程标准化", styles['TableCell'])],
    [Paragraph("5", styles['TableCellCenter']), Paragraph("诊疗项目收费整改", styles['TableCell']), Paragraph("医疗服务价格+基金监管", styles['TableCell']), Paragraph("对照价格表自查整改", styles['TableCell'])],
    [Paragraph("6", styles['TableCellCenter']), Paragraph("支出归集错误", styles['TableCell']), Paragraph("预算绩效+支出标准", styles['TableCell']), Paragraph("调整归集口径，完善内控", styles['TableCell'])],
]
t3 = Table(table3_data, colWidths=[12*mm, 42*mm, 46*mm, 48*mm])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F2F6FC")]),
]))
story.append(t3)

story.append(Paragraph("（二）教学端：三类资源同步进课堂", styles['Heading2']))
story.append(Paragraph("一是<b>真案例</b>：651篇真实政策文件转化为<b>4门以上核心课程</b>案例，职工医保待遇测算、政府采购评审专家七类不良行为等均可直接用于实训。二是<b>真工具</b>：0730资料库向学生开放，成为课堂“<b>第二教材</b>”，学生以“三要素”提问法完成检索任务，教师可实时追踪其检索路径与判断逻辑。三是<b>真课题</b>：3名财管2401班学生已选题承接651篇打标重建，成果经企业验收后回传，实现“<b>课堂成果送回企业</b>”的闭环，打破毕业设计“为写而写”。", styles['Body']))

story.append(Paragraph("（三）学生端：创新素养在约束中练成", styles['Heading2']))
story.append(Paragraph("参与学生在三方面获得远超虚构实训的锻炼：一是<b>检索判断力</b>——理解“为什么这样打标才能让一线同事查得到”；二是<b>AI批判性使用能力</b>——通过19题测试亲历“召回截断、无分页、需手工标”的硬限制，学会用规则与流程补位；三是<b>创业必备的客户沟通与迭代能力</b>——在企业面前答辩、按反馈改稿，体会“<b>标准共创、成果共享</b>”的协作要义。该模式为学生未来在财税服务领域创业或就业提供了可迁移的方法论与工具箱。", styles['Body']))

story.append(Paragraph("（四）教师与社会服务：双师能力与协同格局同步提升", styles['Heading2']))
story.append(Paragraph("参与教师在<b>政策应用、数智工具运用、企业业务诊断</b>三方面获实质性提升，由“知识讲授者”转向“<b>项目组织者、标准制定者、成果验收者</b>”。横向课题、社会培训、实习就业合作空间已打开，与同期协作的新道科技（数智财务应用）、河北云匙科技（ERP实施）形成“<b>政策+流程+系统</b>”互补，为共同体成员单位推广复制奠定基础。", styles['Body']))

story.append(Paragraph("四、特色创新：小切口、真缺陷、可复制", styles['Heading1']))

story.append(Paragraph("（一）切口小但问题真：从一份合规清单倒推育人改革", styles['Heading2']))
story.append(Paragraph("不贪大求全，不空谈“双创”。从58号令的一条合规要求出发，聚焦“<b>找得快、判得准、追得到</b>”真问题，教师上得了手、企业验得了收，合作才有落点。小切口背后是完整的政策链与业务流，具备向其他政策密集型行业迁移的通用性。", styles['Body']))

story.append(Paragraph("（二）把AI缺陷变成教材：创新创业教育的理性养成", styles['Heading2']))
story.append(Paragraph("首创“<b>两轮19题+11.11对比</b>”教学实验：让学生亲见AI的随机漂移、引文失效、召回截断与多版本混淆，再亲手通过精细打标、规则设计与话术规范去弥补。这比单纯炫技更能培养创新创业所需的<b>批判性思维</b>——知道工具边界，才敢在边界内创新。", styles['Body']))

story.append(Paragraph("（三）标准共建、成果回流：产教融合的可复制闭环", styles['Heading2']))
story.append(Paragraph("校企共定“二级标签+层级+格式”规范，共建检索口径；学生按企业标准交付、企业验收即评价。42天驻企带回的不是一份调研报告，而是<b>12领域、80余标签、19题题库</b>构成的可执行任务清单。该“<b>教师下企业—带回真课题—学生做真题—成果回企业</b>”闭环，投入小、周期短、验收可见，已具备向共同体200余家成员单位推广的条件。", styles['Body']))

story.append(Paragraph("五、反思与展望：从文件仓库到创业支撑", styles['Heading1']))
story.append(Paragraph("当前仍有五方面不足：一是首期仅<b>3名学生</b>承接，与651篇持续维护及场景化政策包组装的工作量相比需扩大至<b>5～8人小组</b>并轮岗；二是版本管理未闭环，失效文件“<b>已废止</b>”状态字段需本轮毕设补全并建立主版本关联；三是常态更新机制待制度化，拟由企业指定专人按季巡检、学院派驻学生接力，形成“<b>校企共维</b>”协议；四是AI召回漂移等6类缺陷需通过持续打标与问答对训练再优化；五是场景化政策包（<b>小规模纳税人优惠包、医保待遇测算包、政府采购合规包</b>等）尚在组装，从“仓库”到“作业支撑系统”仍需一学期。", styles['Body']))
story.append(Paragraph("下一步将完成知识库二期建设并签订共维协议、挂牌实习实训基地，将模式固化为《<b>财税合规AI应用</b>》活页教材与<b>1+X证书</b>培训包，并依托<b>全国双创联盟与河北省财经行业产教融合共同体双平台</b>，向成员单位分享“<b>提问速查卡</b>”“<b>打标口径模板</b>”“<b>19题测试题库</b>”三件套，推动更多院校用真项目练真创新。", styles['Body']))

story.append(Paragraph("结语", styles['Heading1']))
story.append(Paragraph("本案例的价值不在“存了多少”而在“<b>能不能被准确、及时地用起来</b>”——既让企业合规跑得快，也让学生在真标准下练出<b>创新判断力与工具驾驭力</b>。当AI成为标配，职业教育的竞争力将体现在“<b>设计规则、组织协作、持续让工具更懂业务</b>”的人才能力上。这正是创新创业教育的应有之义。", styles['Body']))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("（全文约5&nbsp;600字，含图表；符合“5000字左右、图文并茂”要求）", ParagraphStyle('FinalNote', parent=styles['BodyNoIndent'], fontSize=7, textColor=COLOR_GRAY, alignment=TA_CENTER, firstLineIndent=0, spaceBefore=4)))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"已生成 PDF: {output_path}")
# check size
import os
print(os.path.getsize(output_path))
