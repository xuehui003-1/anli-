#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def add_paragraph(doc, text, font_name="仿宋_GB2312", font_size=16, bold=False, italic=False, color=None, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=28, first_line_indent=32, space_after=0, space_before=0, keep_with_next=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = Pt(line_spacing)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.alignment = alignment
    if first_line_indent is not None and first_line_indent>0:
        p.paragraph_format.first_line_indent = Pt(first_line_indent)
    p.paragraph_format.widow_control = True
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return p

def set_cell_text(cell, text, font_name="仿宋_GB2312", font_size=9, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, shading=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.add_run(text)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    cell.vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    if shading:
        tblCell = cell._tc
        tblCellProperties = tblCell.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), shading)
        shd.set(qn('w:val'), 'clear')
        tblCellProperties.append(shd)

def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top','left','bottom','right','insideH','insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '6')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_page_number(doc):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)
    run2 = p.add_run()
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'PAGE'
    run2._r.append(instr)
    run3 = p.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run3._r.append(fldChar2)
    run4 = p.add_run(' / ')
    run4.font.size = Pt(9)
    run4.font.name = '仿宋_GB2312'
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'begin')
    run5 = p.add_run()
    run5._r.append(fldChar3)
    run6 = p.add_run()
    instr2 = OxmlElement('w:instrText')
    instr2.set(qn('xml:space'), 'preserve')
    instr2.text = 'NUMPAGES'
    run6._r.append(instr2)
    run7 = p.add_run()
    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')
    run7._r.append(fldChar4)

def add_figure(doc, img_path, caption, width_inches=5.5):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.first_line_indent = Pt(0)
        p_img.paragraph_format.keep_with_next = True
        p_img.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        p_cap = add_paragraph(doc, caption, font_name="楷体_GB2312", font_size=8, bold=False, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6, line_spacing=13)
        return True
    else:
        print(f"缺图 {img_path}")
        return False

doc = Document()
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.5)

style = doc.styles['Normal']
style.font.name = '仿宋_GB2312'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
style.font.size = Pt(16)
style.paragraph_format.line_spacing = Pt(28)
style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
style.paragraph_format.first_line_indent = Pt(32)

# 封面
add_paragraph(doc, "", font_size=16, space_after=12, first_line_indent=0)
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(6)
p_title.paragraph_format.space_before = Pt(24)
run = p_title.add_run("AI赋能、真题真做")
run.font.name = "方正小标宋简体"
run._element.rPr.rFonts.set(qn('w:eastAsia'), "方正小标宋简体")
run.font.size = Pt(22)
run.font.bold = True
p_title2 = doc.add_paragraph()
p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title2.paragraph_format.space_after = Pt(18)
run = p_title2.add_run("——财税知识库驱动的创新创业教育实践")
run.font.name = "方正小标宋简体"
run._element.rPr.rFonts.set(qn('w:eastAsia'), "方正小标宋简体")
run.font.size = Pt(22)
run.font.bold = True
p_school = doc.add_paragraph()
p_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_school.paragraph_format.space_after = Pt(24)
run = p_school.add_run("（石家庄邮电职业技术学院）")
run.font.name = "楷体_GB2312"
run._element.rPr.rFonts.set(qn('w:eastAsia'), "楷体_GB2312")
run.font.size = Pt(14)

info_data = [
    ["项目", "内容"],
    ["申报类别", "创新创业教育实践教学与项目孵化（兼AI赋能课程改革）"],
    ["申报单位", "石家庄邮电职业技术学院（会计学院）"],
    ["联合单位", "河北企富财税管理有限公司（会计师事务所·税务师事务所）"],
    ["主要完成人", "薛辉、张勇、王爱辉、任伟峰、李 莉"],
    ["联系人", "薛辉  18332128207  xuehui006@outlook.com"],
    ["关键词", "创新创业教育；AI赋能；产教融合；真实项目；财税知识库"],
]
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.columns[0].width = Inches(1.6)
table.columns[1].width = Inches(4.9)
hdr_cells = table.rows[0].cells
set_cell_text(hdr_cells[0], info_data[0][0], font_size=10, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(hdr_cells[1], info_data[0][1], font_size=10, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
for row_data in info_data[1:]:
    cells = table.add_row().cells
    set_cell_text(cells[0], row_data[0], font_size=9, bold=True, shading="D9E1F2", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(cells[1], row_data[1], font_size=9, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT)
set_table_borders(table)
add_paragraph(doc, "", font_size=6, space_after=6, first_line_indent=0)
add_paragraph(doc, "【摘要】", font_name="黑体", font_size=11, bold=True, first_line_indent=0, space_after=4, space_before=6)
add_paragraph(doc, "本案例聚焦高职财经类专业“学难致用、练不适岗、创无支撑”的共性痛点，以河北企富财税管理有限公司应对《涉税专业服务管理办法（试行）》（国家税务总局令第58号）合规新规的真实需求为切入口，由教师驻企42天牵头构建基于腾讯ima平台的“0730资料库”，归集财税、医保、政府采购等12领域651篇政策文档，创设“二级标签+层级+格式”三维标注体系与“业务领域+层级+文档形态”三要素检索规范，完成两轮19题系统测试并以“知识库测试问题11.11对比”验证迭代成效；进而将知识库二期“打标重建”任务转化为财务管理专业毕业设计真题，由3名学生直接对接企业、按企业标准迭代并接受企业验收，实现“教师下企业—带回真课题—学生做真题—成果回企业”的闭环。实践使企业高频政策查询由15～30分钟缩短至秒级，输出6组合规分析并反哺4门核心课程，为AI赋能的创新创业教育提供了“真问题、小切口、可复制”的范式。", font_size=10, first_line_indent=32, line_spacing=18, space_after=2)
add_paragraph(doc, "关键词：创新创业教育；AI赋能；真实项目；财税知识库；产教融合", font_size=10, bold=False, first_line_indent=0, space_after=12, line_spacing=18)

# 一
add_paragraph(doc, "一、背景与问题：从合规新规到教学痛点的真实牵引", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "石家庄邮电职业技术学院会计学院开设大数据与会计、财务管理等专业，对口服务京津冀中小财税服务机构。这类机构轻资产、重政策，客户问的是“这个优惠还能不能用、那条红线能不能碰”，答复既要快、准，还要追到原文条款。2025年5月1日，《涉税专业服务管理办法（试行）》（国家税务总局令第58号）施行，将“答复快、准、可追溯”从服务加分项变为合规硬义务：要求机构建立质量管理制度、风控机制和业务底稿，审计鉴证还需证据链完整、可复核。对以代理记账、涉税服务、企业管家为主业的河北企富财税管理有限公司而言，文件散在个人电脑与微信群、找一篇政策要15～30分钟且难辨现行有效性的现状，已直接构成合规风险。", font_size=16, line_spacing=28)
add_paragraph(doc, "学校端是同一矛盾的另一面。教材更新滞后新规半年以上，实训多为教师虚构的“干净数据”，与企业“多版本并存、省市联动、新旧交替”的真场景存在时差。例如石家庄市职工医保在2017年（石政发〔2017〕2号）、2019年（石政规〔2019〕7号）、2024年（石政规〔2024〕7号）三度修订，起付线、报销比、年度限额逐次调整；河北省评审专家管理在2025年以冀财采〔2025〕12号废止冀财采〔2023〕13号。若学生仅凭教材记忆作答，极易引用失效条款。更深层的痛点是：学生会做题，不会查；会背条文，不会断新旧；会用工具，不会审边界。创新创业教育若停留在“写商业计划书”，便无法培养出能在真实合规约束下持续创新的人。", font_size=16, line_spacing=28)
add_paragraph(doc, "基于此，学院于2026年7月15日至8月25日选派教师赴企富驻企实践42天，确立“以真实合规清单倒推知识管理能力、以知识库建设牵引教学改革”的总体思路，把企业知识管理困境转化为师生创新创业练兵场。", font_size=16, line_spacing=28)

# 二
add_paragraph(doc, "二、主要做法：AI为翼、真题为场，构建“学—做—创”一体模式", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "案例形成“教师下企业搭平台—AI能力边界当教材—学生接真题进企业”的三段式路径，核心是将企业数字化转型中的真实任务完整搬进教学，使创新创业教育在真需求、真标准、真验收中发生（见图1）。", font_size=16, line_spacing=28)

add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/逻辑结构示意图.png", "图1  财税知识库驱动的协同育人逻辑结构示意图", width_inches=5.4)

add_paragraph(doc, "具体实施遵循驻企调研、建库标注、测试改进、教学转化和反馈迭代五个环节，明确教师、企业和学生的参与方式及各阶段产出；后续验收与成果回流按实际进度推进（见图2）。", font_size=16, line_spacing=28)
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/实施路线图.png", "图2  财税知识库协同育人实施路线图", width_inches=5.4)

# （一）
add_paragraph(doc, "（一）驻企搭平台：从零建成651篇结构化知识库", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=10, space_after=4)
add_paragraph(doc, "实践团队采用“实地走访+岗位跟岗+座谈访谈+归集清洗”四步法，走访代理记账、涉税服务、企业管家三条业务线，与审计部、会计部骨干多轮座谈，梳理出“问题—任务—交付物”清单：如月销售额10万元以下小规模纳税人免税、六税两费叠加减征、职工医保住院待遇测算等高频场景，均需秒级溯源。", font_size=16, line_spacing=28)
add_paragraph(doc, "依托腾讯ima共享知识库平台建成“0730资料库”，共归集文档651篇，其中PDF232篇（政策原文）、Word397篇（制度细则）、Excel22篇（目录、价格、科目表），无PPT、网页、笔记冗余，全部为业务必备文档，覆盖国家、河北省、石家庄市三级。分类采用“二级标签法（行业-业务）”，设12个一级领域、80余个二级标签，医保板块因业务高频进一步细化至待遇保障（职工/居民）、筹资缴费、支付结算、药品目录、特殊病种、诊疗项目与价格、定点管理、基金监管等子类（见表1）。每篇文档同步完成层级标签（国家/河北省/石家庄市）、格式辅助标签（PDF-政策原文/Excel-价格表等）与状态预留字段（施行中/已废止），为AI检索提供结构化底座。", font_size=16, line_spacing=28)
add_paragraph(doc, "表1  0730资料库分类与标注体系", font_name="黑体", font_size=10, bold=True, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
table1_data = [
    ["维度", "内容"],
    ["文档总量", "651篇：PDF 232篇（政策原文）、Word 397篇（制度细则）、Excel 22篇（目录台账）"],
    ["一级领域", "12个：医保、财税、会计、审计、国资、农村集体、行政事业、招投标基建、社保、医疗卫生、党建纪检、其他行业"],
    ["二级标签", "80余个；医保板块细分至20个子类（待遇保障、筹资缴费、支付结算、药品目录、特殊病种等）"],
    ["层级标签", "国家政策／河北省／石家庄市（按文号与执行层级判定）"],
    ["格式标签", "PDF-政策原文／Word-制度细则／Excel-目录台账／PDF-问答汇编"],
    ["业务板块", "医疗保障、涉税专业服务、政府采购、会计审计、预算绩效、农村集体财务、党建纪检"],
]
table1 = doc.add_table(rows=1, cols=2)
table1.style = 'Table Grid'
table1.columns[0].width = Inches(1.5)
table1.columns[1].width = Inches(5.0)
hdr = table1.rows[0].cells
set_cell_text(hdr[0], table1_data[0][0], font_size=9, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(hdr[1], table1_data[0][1], font_size=9, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
for row in table1_data[1:]:
    cells = table1.add_row().cells
    set_cell_text(cells[0], row[0], font_size=8, bold=True, shading="D9E1F2", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(cells[1], row[1], font_size=8, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT)
set_table_borders(table1)
add_paragraph(doc, "以医保待遇、涉税服务和政府采购三个场景为例，可将业务问题、关联政策资料与教学任务对应起来，供政策检索和案例设计参考（见图3）。该图为概念性示意，实际资料适用性及教学应用情况须结合原文和实施进度核验。", font_size=16, line_spacing=28)
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/业务知识关联图.png", "图3  业务场景、政策资料与教学任务关联示意图", width_inches=5.4)

# 图1 图2
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图1_企业座谈.jpg", "图4  教师驻企与审计部、会计部骨干座谈梳理高频政策场景（2026年7月）", width_inches=5.4)
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图2_需求调研.jpg", "图5  座谈调研现场：企业部门骨干介绍业务流程与政策使用场景", width_inches=5.4)

# （二）
add_paragraph(doc, "（二）以测促创：两轮19题摸清AI能力边界，把缺陷变教材", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=10, space_after=4)
add_paragraph(doc, "知识库一期建成后，团队并未直接交付，而是设计两轮系统测试把AI的“能与不能”摆上台面，让技术边界成为创新创业素养的教学点。", font_size=16, line_spacing=28)
add_paragraph(doc, "1.首轮5题“抗诱导/防编造”测试（2026年10月25日）。针对库外问题（如“天津市医保报销比”、虚构的“2026年农村集体免税新政”）与错误前提诱导（如“只要签合同就可不走采购流程”“合作社可随意处置集体土地所有权”），AI均能准确识别并拒绝编造，验证了检索忠实性（见图6）。此结果增强了企业对AI辅助合规的信任，也为课堂提供了“AI不会胡说，但会漏、会飘”的理性预期。", font_size=16, line_spacing=28, first_line_indent=32)

# 图3 抗诱导
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图4_抗诱导防编造测试.png", "图6  首轮抗诱导测试：库外问题“天津市城乡居民医保报销比例”被准确识别为无相关资料，AI未编造", width_inches=5.6)

add_paragraph(doc, "2.第二轮14题深度测试（2026年10月28日）。覆盖同题稳定性、引文溯源、跨文档召回、召回截断、多规则叠加、版本识别、多轮记忆等维度，暴露六类典型缺陷：向量召回随机漂移导致同题异答、引用角标无法跳转、长文被截断致要点遗漏、多版本混淆、小点被忽略、上下文脱节（见表2）。测试同步诊断出平台硬限制：单次最多返回约45条、无分页参数、体量大时必须手工打标才能稳住召回。", font_size=16, line_spacing=28, first_line_indent=32)

# 表2
add_paragraph(doc, "表2  两轮AI检索测试维度与改进（摘自“知识库测试问题11.11对比.xlsx”）", font_name="黑体", font_size=10, bold=True, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
table2_data = [
    ["测试维度", "代表问题", "初测缺陷", "精细打标后效果"],
    ["同题稳定性", "河北省门诊慢特病认定要求", "召回片段随机漂移，示例池无固定", "稳定性增强，无大幅跳动"],
    ["引文溯源", "公务接待陪餐人数", "出现[citation:word_1]无法跳转", "可正常跳转并高亮原文段落"],
    ["跨文档召回", "对比政府会计与企业会计差异", "召回弱相关/重复文件，噪声大", "相关性增强，无无关文件"],
    ["召回截断", "冀财社〔2017〕32号三重保障流程", "长文截断，要点遗漏", "按指定文号精准答复，补充相似文件兜底"],
    ["多规则叠加", "透析费用：县域结算+三重保障+监管", "忽略叠加顺序", "不会编造缺失文件，严格按库回答"],
    ["要点完整性", "机场研发强度标准值", "回答不全（遗漏企业规模分档）", "能发现重复有效信息并补全"],
]
table2 = doc.add_table(rows=1, cols=4)
table2.style = 'Table Grid'
table2.columns[0].width = Inches(1.0)
table2.columns[1].width = Inches(1.8)
table2.columns[2].width = Inches(1.8)
table2.columns[3].width = Inches(1.9)
hdr = table2.rows[0].cells
for i, h in enumerate(table2_data[0]):
    set_cell_text(hdr[i], h, font_size=8, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
for row in table2_data[1:]:
    cells = table2.add_row().cells
    for i, txt in enumerate(row):
        set_cell_text(cells[i], txt, font_size=7.5, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT)
set_table_borders(table2)
add_paragraph(doc, "注：计费题在对比表中记录的参考结果为7 142.4元，具体计算口径需结合原始政策核验；会计法罚款上限等版本题由“答错”变为“主动总结新旧差异”。", font_name="楷体_GB2312", font_size=9, bold=False, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=6, line_spacing=14)

# 图4 单点检索
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图5_药品纳入医保精准检索.png", "图7  单点细节检索：药品纳入医保条件——精准引用《国家药品目录》与中办发文，结构化作答", width_inches=5.6)

add_paragraph(doc, "3.迭代验证：11.11对比。同样的14题在精细打标后复测，问题显著收敛：同题稳定性“未出现大幅跳动”、引文“能正常跳转并标示原文段落”、跨文档召回“未出现无关或重复文件”、计费题复测记录显示能指出误区，参考结果为7 142.4元（计算口径待核验）、多规则叠加题“不会现编不存在的32号文且更严谨”。这一“测—改—再测”的过程本身，就是一堂生动的创新创业课：创新不是追新工具，而是弄清约束、在约束内用规则与流程补位。", font_size=16, line_spacing=28, first_line_indent=32)

# 图5 三重保障叠加
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图6_三重保障叠加顺序.png", "图8  多规则叠加实测：贫困透析患者“县域结算→基本医保→大病保险→三重保障”四步叠加顺序被完整还原", width_inches=5.6)

# 三要素
add_paragraph(doc, "表3  三要素检索规范：业务领域+层级+文档形态", font_name="黑体", font_size=10, bold=True, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4)
elem_table_data = [
    ["要素", "示例问法", "检索价值"],
    ["业务领域", "职工医保住院报销 / 政府采购评审专家", "锁定12领域与80+二级标签"],
    ["层级", "石家庄市 / 河北省 / 国家", "避免省市混用、省市链条断裂"],
    ["文档形态", "政策原文 / 价格表 / 问答汇编", "区分正文与目录表，提升命中率"],
    ["完整示例", "“石家庄市 职工医保住院 政策原文”", "三要素合一，命中率显著高于单关键词"],
]
elem_table = doc.add_table(rows=1, cols=3)
elem_table.style = 'Table Grid'
elem_table.columns[0].width = Inches(1.2)
elem_table.columns[1].width = Inches(2.3)
elem_table.columns[2].width = Inches(3.0)
hdr = elem_table.rows[0].cells
for i, h in enumerate(elem_table_data[0]):
    set_cell_text(hdr[i], h, font_size=8, bold=True, shading="E2EFDA", alignment=WD_ALIGN_PARAGRAPH.CENTER)
for row in elem_table_data[1:]:
    cells = elem_table.add_row().cells
    for i, txt in enumerate(row):
        set_cell_text(cells[i], txt, font_size=8, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT)
set_table_borders(elem_table)
# 三要素真图补充
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/图3_三要素提问规范.png", "图9  三要素提问法在企业中的落地示意：说清业务+层级+形态", width_inches=5.0)
add_paragraph(doc, "配套产出《知识库使用规范手册》，明确“文件名/文号/层级/业务”四必带、查不到时“加标签缩小范围或直开原文提问”的二阶策略，解决一线“查不到、查不准”痛点。", font_size=16, line_spacing=28, first_line_indent=32)

# （三）
add_paragraph(doc, "（三）真题进课堂：毕业设计与课程的双重活化", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=10, space_after=4)
add_paragraph(doc, "一期“有库无标、检而不准”的缺口，正是中小企业“知道该做、没人做、不会做”的缩影，也是职业教育可介入的真空。学院将二期“打标重建与索引优化”作为2027届财务管理专业岗位核心知识技能类毕业设计新增选题——“财税法规知识库文档标签体系构建与分类整理”，由财管2401班3名学生组队承接，企业出具验收证明即为答辩依据之一。", font_size=16, line_spacing=28)
add_paragraph(doc, "1.过程真：学生直连企业。小组先赴企富与审计部、会计部骨干座谈，把一线“查不到、查不准”痛点转化为标签设计输入；选取30篇样板文档试打，企业逐条校准二级标签、层级与状态字段口径，通过后才批量推进651篇逐篇打标、重建索引，并用19题测试用例回归验证准确率，针对召回漂移、引文失效等问题以精细标签与人工规则补位（见图10）。", font_size=16, line_spacing=28, first_line_indent=32)
add_figure(doc, "申报材料_全国双创_石家庄邮电职业技术学院/配图/师生毕设指导_原稿.jpg", "图10  教师指导毕设小组梳理企业需求、搭建知识库标签体系（2026年10月，原稿图片）", width_inches=5.1)

add_paragraph(doc, "2.标准真：企业标准替代分数。成果需满足企业“可检索、可维护、可培训”三验收：标签命名让一线同事“不培训也能猜对”，三要素问法让新人“问一次就能中”，使用手册让部门“照着就能教”。学生需在企业面前为自己的打标方案辩护、按反馈迭代，而非在教室交一份教师打分的纸面报告。这一过程本身即是创业预演：需求挖掘—方案设计—客户验证—迭代交付。", font_size=16, line_spacing=28, first_line_indent=32)
add_paragraph(doc, "3.课堂真：4门核心课程活页化。651篇真实政策同步转化为《智慧化税费申报与管理》《财经法规与会计职业道德》《审计实务》《大数据与会计综合实训》案例库：职工医保三版待遇比对做待遇测算实训，小规模纳税人免税与六税两费叠加做申报判断，评审专家七类不良行为与代理机构八项检查内容做合规教育，直接责任与领导责任划分做经济责任审计模拟。标签体系与三要素检索法本身亦成为“数智工具能力”与“综合实训”的训练内容，并以活页、工作手册形态持续更新，破解教材滞后难题。", font_size=16, line_spacing=28, first_line_indent=32)
add_paragraph(doc, "4.评价真：过程性与成果导向并重。毕业设计评价引入企业验收分、检索准确率提升分、手册可用度分，替代单一论文分；课堂评价增加“检索—判断—归档—复用”全链条实操考核，体现全国双创联盟倡导的过程性、多元化考核方向。", font_size=16, line_spacing=28, first_line_indent=32)

# （四）
add_paragraph(doc, "（四）闭环复制：从审计部到会计部的方法论迁移", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=10, space_after=4)
add_paragraph(doc, "审计部跑通后，团队将“提标准—对方认领—节点验收”闭环工作法复制至会计部，指导其按“二级标签+层级+格式”规范打包资料并明确打标要求，对方已认领并启动整理。一期曾因“说明书式”布置而落地不足的教训，反向成为教学案例：让学生理解“标准不等于执行，创新在于设计可执行的协作机制”。下一阶段将打通两部门库，建成企业统一检索平台，并推动挂牌实习实训基地与横向课题。", font_size=16, line_spacing=28)

# 三
add_paragraph(doc, "三、实施成效：可量化、可感知、可迁移", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "以“是否让企业少跑腿、学生多真练、课堂更鲜活”为尺度，成效体现在四端。", font_size=16, line_spacing=28)
add_paragraph(doc, "（一）企业端：合规基础设施从无到有，效率从分钟级到秒级", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "651篇结构化文档覆盖12领域、80余标签，一线人员由“翻文件夹”升级为“自然语言提问+AI原文引用”作业模式，高频政策查询响应由人均15～30分钟缩短至秒级；已交付审计部6组合规分析，每项形成“事实描述—条款引用—问题定性—整改建议”闭环，覆盖医疗收费、长期挂账、无形资产挪用、资产转固、诊疗收费整改、支出归集等事项，直接协助识别并化解涉税与审计风险，方法论已复制至会计部。", font_size=16, line_spacing=28)
add_paragraph(doc, "表4  已交付的6组合规分析（审计部）", font_name="黑体", font_size=10, bold=True, first_line_indent=0, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
table3_data = [
    ["序号", "事项", "关键条款引用", "成效"],
    ["1", "耳鼻喉科医疗收费合规性", "医保支付结算+诊疗项目价格", "核减不合规收费项"],
    ["2", "长期往来款挂账", "政府会计制度+往来清理", "清理3年以上挂账，建立对账机制"],
    ["3", "无形资产购置费挪用", "预算管理+资产配置", "追溯资金用途，规范科目归集"],
    ["4", "固定资产账卡核对与在建工程转固", "资产管理+转固时点", "补提折旧，转固流程标准化"],
    ["5", "诊疗项目收费整改", "医疗服务价格+基金监管", "对照价格表自查整改"],
    ["6", "支出归集错误", "预算绩效+支出标准", "调整归集口径，完善内控"],
]
table3 = doc.add_table(rows=1, cols=4)
table3.style = 'Table Grid'
table3.columns[0].width = Inches(0.5)
table3.columns[1].width = Inches(2.0)
table3.columns[2].width = Inches(2.0)
table3.columns[3].width = Inches(2.0)
hdr = table3.rows[0].cells
for i, h in enumerate(table3_data[0]):
    set_cell_text(hdr[i], h, font_size=7.5, bold=True, shading="4472C4", alignment=WD_ALIGN_PARAGRAPH.CENTER)
for row in table3_data[1:]:
    cells = table3.add_row().cells
    for i, txt in enumerate(row):
        set_cell_text(cells[i], txt, font_size=7.5, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT)
set_table_borders(table3)
add_paragraph(doc, "（二）教学端：三类资源同步进课堂", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "一是真案例：651篇真实政策文件转化为4门以上核心课程案例，职工医保待遇测算、政府采购评审专家七类不良行为等均可直接用于实训。二是真工具：0730资料库向学生开放，成为课堂“第二教材”，学生以“三要素”提问法完成检索任务，教师可实时追踪其检索路径与判断逻辑。三是真课题：3名财管2401班学生已选题承接651篇打标重建，成果经企业验收后回传，实现“课堂成果送回企业”的闭环，打破毕业设计“为写而写”。", font_size=16, line_spacing=28)
add_paragraph(doc, "（三）学生端：创新素养在约束中练成", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "参与学生在三方面获得远超虚构实训的锻炼：一是检索判断力——理解“为什么这样打标才能让一线同事查得到”；二是AI批判性使用能力——通过19题测试亲历“召回截断、无分页、需手工标”的硬限制，学会用规则与流程补位；三是创业必备的客户沟通与迭代能力——在企业面前答辩、按反馈改稿，体会“标准共创、成果共享”的协作要义。该模式为学生未来在财税服务领域创业或就业提供了可迁移的方法论与工具箱。", font_size=16, line_spacing=28)
add_paragraph(doc, "（四）教师与社会服务：双师能力与协同格局同步提升", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "参与教师在政策应用、数智工具运用、企业业务诊断三方面获实质性提升，由“知识讲授者”转向“项目组织者、标准制定者、成果验收者”。横向课题、社会培训、实习就业合作空间已打开，与同期协作的新道科技（数智财务应用）、河北云匙科技（ERP实施）形成“政策+流程+系统”互补，为共同体成员单位推广复制奠定基础。", font_size=16, line_spacing=28)

# 四
add_paragraph(doc, "四、特色创新：小切口、真缺陷、可复制", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "（一）切口小但问题真：从一份合规清单倒推育人改革", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "不贪大求全，不空谈“双创”。从58号令的一条合规要求出发，聚焦“找得快、判得准、追得到”真问题，教师上得了手、企业验得了收，合作才有落点。小切口背后是完整的政策链与业务流，具备向其他政策密集型行业迁移的通用性。", font_size=16, line_spacing=28)
add_paragraph(doc, "（二）把AI缺陷变成教材：创新创业教育的理性养成", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "首创“两轮19题+11.11对比”教学实验：让学生亲见AI的随机漂移、引文失效、召回截断与多版本混淆，再亲手通过精细打标、规则设计与话术规范去弥补。这比单纯炫技更能培养创新创业所需的批判性思维——知道工具边界，才敢在边界内创新。", font_size=16, line_spacing=28)
add_paragraph(doc, "（三）标准共建、成果回流：产教融合的可复制闭环", font_name="楷体_GB2312", font_size=16, bold=True, first_line_indent=0, space_before=8, space_after=4)
add_paragraph(doc, "校企共定“二级标签+层级+格式”规范，共建检索口径；学生按企业标准交付、企业验收即评价。42天驻企带回的不是一份调研报告，而是12领域、80余标签、19题题库构成的可执行任务清单。该“教师下企业—带回真课题—学生做真题—成果回企业”闭环，投入小、周期短、验收可见，已具备向共同体200余家成员单位推广的条件。", font_size=16, line_spacing=28)

# 五
add_paragraph(doc, "五、反思与展望：从文件仓库到创业支撑", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "当前仍有五方面不足：一是首期仅3名学生承接，与651篇持续维护及场景化政策包组装的工作量相比需扩大至5～8人小组并轮岗；二是版本管理未闭环，失效文件“已废止”状态字段需本轮毕设补全并建立主版本关联；三是常态更新机制待制度化，拟由企业指定专人按季巡检、学院派驻学生接力，形成“校企共维”协议；四是AI召回漂移等6类缺陷需通过持续打标与问答对训练再优化；五是场景化政策包（小规模纳税人优惠包、医保待遇测算包、政府采购合规包等）尚在组装，从“仓库”到“作业支撑系统”仍需一学期。", font_size=16, line_spacing=28)
add_paragraph(doc, "下一步将完成知识库二期建设并签订共维协议、挂牌实习实训基地，将模式固化为《财税合规AI应用》活页教材与1+X证书培训包，并依托全国双创联盟与河北省财经行业产教融合共同体双平台，向成员单位分享“提问速查卡”“打标口径模板”“19题测试题库”三件套，推动更多院校用真项目练真创新。", font_size=16, line_spacing=28)
add_paragraph(doc, "结语", font_name="黑体", font_size=16, bold=True, first_line_indent=0, space_before=12, space_after=6)
add_paragraph(doc, "本案例的价值不在“存了多少”而在“能不能被准确、及时地用起来”——既让企业合规跑得快，也让学生在真标准下练出创新判断力与工具驾驭力。当AI成为标配，职业教育的竞争力将体现在“设计规则、组织协作、持续让工具更懂业务”的人才能力上。这正是创新创业教育的应有之义。", font_size=16, line_spacing=28)

add_page_number(doc)
output_dir = "申报材料_全国双创_石家庄邮电职业技术学院"
os.makedirs(output_dir, exist_ok=True)
docx_path = os.path.join(output_dir, "高职创盟典型经验案例+石家庄邮电职业技术学院+AI赋能、真题真做——财税知识库驱动的创新创业教育实践.docx")
doc.save(docx_path)
print(f"已生成 Word: {docx_path}")
full_text = "\n".join([p.text for p in doc.paragraphs])
print(f"段落数: {len(doc.paragraphs)} 表格数: {len(doc.tables)} 图像数: {len([r for r in doc.part.rels.values() if 'image' in r.target_ref])}")
print(f"字符数（去空白）: {len([c for c in full_text if c.strip()])} 总字符: {len(full_text)}")
