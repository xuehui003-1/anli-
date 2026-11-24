# -*- coding: utf-8 -*-
"""
小邮伴学 · 10 页 PPT 重绘脚本
--------------------------------
用法：python3 重绘脚本.py
读取本目录下 第01页…第10页 每个文件夹里的 图1/图2/图3…，重绘成 1920×1080 的成品图，
输出到 本目录/成品/P01.png … P10.png

换图规则：改名成 图1、图2… 放进对应页文件夹，重跑本脚本即可，版式不用动。
"""
import os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
L, R = 96, 1824
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIRS = ["/tmp/source-han-sans-release/OTF/SimplifiedChinese",
             os.path.join(HERE, "字体")]

GREEN  = (14, 59, 51)
BG     = (246, 243, 237)
WHITE  = (255, 255, 255)
OR     = (232, 114, 42)
ORD    = (192, 85, 20)
DGREY  = (74, 84, 96)
LGREY  = (140, 148, 158)
LINE   = (222, 212, 197)
LGREEN = (240, 246, 243)
GBOX   = (233, 227, 216)

_fc = {}
def _fontfile(bold):
    for d in FONT_DIRS:
        p = os.path.join(d, "SourceHanSansSC-Bold.otf" if bold else "SourceHanSansSC-Regular.otf")
        if os.path.exists(p): return p
    return None
def F(px, bold=False):
    k = (px, bold)
    if k not in _fc:
        f = _fontfile(bold)
        _fc[k] = ImageFont.truetype(f, px) if f else ImageFont.load_default()
    return _fc[k]
def tw(t, f):
    b = f.getbbox(t); return b[2]-b[0]
_NOS = "、。，）」』】！？：；…—·%”’"
def wrap(t, f, maxw):
    out, cur = [], ""
    for ch in t:
        if ch == "\n":
            out.append(cur); cur = ""; continue
        if tw(cur+ch, f) > maxw and cur:
            if ch in _NOS:            # 行首禁则：标点不留行首
                cur += ch
                out.append(cur); cur = ""
            else:
                out.append(cur); cur = ch
        else:
            cur += ch
    if cur: out.append(cur)
    # 避免行末孤零零的开引号
    fixed = []
    for ln in out:
        while ln and ln[0] in _NOS and fixed:
            fixed[-1] += ln[0]; ln = ln[1:]
        fixed.append(ln)
    return [x for x in fixed if x]
def rr(d, box, r, fill=None, outline=None, w=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)
def para(d, xy, t, f, fill, maxw, lh=1.55, maxline=99, align="l"):
    x, y = xy
    lines = wrap(t, f, maxw)[:maxline]
    step = int(f.size*lh)
    for i, ln in enumerate(lines):
        if align == "c":
            d.text((x + (maxw-tw(ln, f))//2, y + i*step), ln, font=f, fill=fill)
        else:
            d.text((x, y + i*step), ln, font=f, fill=fill)
    return y + len(lines)*step

def cover(im, w, h):
    im = im.convert("RGB")
    s = max(w/im.width, h/im.height)
    im2 = im.resize((max(w, int(im.width*s+0.5)), max(h, int(im.height*s+0.5))), Image.LANCZOS)
    x = (im2.width-w)//2; y = (im2.height-h)//2
    return im2.crop((x, y, x+w, y+h))

def img_at(cv, path, box, r=0):
    x0, y0, x1, y1 = box
    w, h = x1-x0, y1-y0
    if not os.path.exists(path):
        d = ImageDraw.Draw(cv)
        rr(d, box, r, fill=(237, 234, 227))
        return False
    ic = cover(Image.open(path), w, h)
    if r > 0:
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w-1, h-1], radius=r, fill=255)
        cv.paste(ic, (x0, y0), m)
    else:
        cv.paste(ic, (x0, y0))
    return True

def base(num, eyebrow, title, sub=None, tsize=76):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), eyebrow, font=F(30), fill=ORD)
    pn = "%d / 10" % num
    d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    d.text((L, 108), title, font=F(tsize, True), fill=GREEN)
    y = 108 + int(tsize*1.30)
    if sub:
        d.text((L, y), sub, font=F(33), fill=DGREY)
        y += 62
    d.line([(L, y+6), (R, y+6)], fill=LINE, width=2)
    return cv, d, y+40

def footer(d, text, y=1000, size=20):
    d.text((L, y), text, font=F(size), fill=LGREY)

def quote(d, text, y=930, size=46, note=None, notew=None):
    d.text((L, y), text, font=F(size, True), fill=OR)
    if note:
        d.text((L, y+int(size*1.55)), note, font=F(20), fill=LGREY)

def find_img(folder, n):
    for ext in (".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".webp"):
        p = os.path.join(HERE, folder, "图%d%s" % (n, ext))
        if os.path.exists(p): return p
    g = sorted(glob.glob(os.path.join(HERE, folder, "图%d.*" % n)))
    g = [x for x in g if not x.endswith(".txt")]
    return g[0] if g else os.path.join(HERE, folder, "图%d_缺失" % n)

# ---------------------------------------------------------------- P1 封面
def p1(folder="第01页_封面"):
    cv = Image.new("RGB", (W, H), GREEN)
    img_at(cv, find_img(folder, 1), (0, 0, W, H))
    ov = Image.new("RGBA", (W, H), (14, 59, 51, 158))   # 62%
    cv = Image.alpha_composite(cv.convert("RGBA"), ov)
    gr = Image.new("L", (1, H))
    for y in range(H):
        t = max(0.0, (y-420)/660.0)
        gr.putpixel((0, y), int(210*min(1.0, t**1.5)))
    gr = gr.resize((W, H))
    gree = Image.new("RGBA", (W, H), (10, 44, 38, 255))
    gree.putalpha(gr)
    cv = Image.alpha_composite(cv, gree)
    cv = cv.convert("RGB")
    # 左下角再加一层渐变压暗，保证标题压得住画面里的招牌字
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fy = np.clip((yy-380)/520.0, 0, 1)
    fx = np.clip(1.0-xx/1250.0, 0, 1)
    al = (np.clip(fy*0.85+fx*0.45, 0, 1)**1.35*205).astype(np.uint8)
    lay = Image.new("RGBA", (W, H), (9, 40, 34, 255))
    lay.putalpha(Image.fromarray(al))
    cv = Image.alpha_composite(cv.convert("RGBA"), lay).convert("RGB")
    d = ImageDraw.Draw(cv)
    d.text((L, 92), "河北省高校人工智能赋能教师教学创新展示活动", font=F(30), fill=(238, 234, 226))
    d.text((L, 612), "小邮伴学", font=F(126, True), fill=WHITE)
    d.text((L, 782), "把真课堂装进一个文件", font=F(56, True), fill=(246, 243, 237))
    xs = L
    for i, w_ in enumerate(["真课件", "·", "真任务", "·", "真数据", "·", "真课堂"]):
        f = F(40, True) if w_ != "·" else F(40)
        d.text((xs, 884), w_, font=f, fill=OR if w_ != "·" else (200, 150, 110))
        xs += tw(w_, f) + 16
    d.line([(L, 962), (L+380, 962)], fill=(255, 255, 255, 90), width=2)
    d.text((L, 986), "教育教学智能体设计作品", font=F(28), fill=(240, 236, 228))
    d.text((L, 1026), "石家庄邮电职业技术学院  薛辉", font=F(28), fill=(240, 236, 228))
    d.text((1640, 1006), "2026.11.28", font=F(30), fill=(226, 222, 214))
    return cv

# ---------------------------------------------------------------- P2 初衷（四个老问题）
def p2(folder="第02页_初衷"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), "P2 · 初衷", font=F(30), fill=ORD)
    pn = "2 / 10"; d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    d.text((L, 104), "这四件事，以前一直没人管", font=F(74, True), fill=GREEN)
    d.text((L, 202), "不是新问题，是老问题：一个没人管，一个看不见，一个说不准，一个忙不过来。", font=F(30), fill=DGREY)
    d.line([(L, 266), (R, 266)], fill=LINE, width=2)

    cards = [
        (1, "①", "没人管", "问题", "没人管",
         [("以前", "课件 154 页，讲到第 38 页该停了，只有我记得。"),
          ("当时", "学生指着第 12 页问，我一说就下课了；下节课又从头讲。")],
         "课讲到哪儿，只有我记得。"),
        (2, "②", "看不见", "问题", "看不见",
         [("以前", "一个班 41 本、74 本笔记，收上来摞在桌上。"),
          ("当时", "一学期翻不了几遍：写得乱、抄得对不对、谁没交，都看不出来。")],
         "写得对不对，没人给学生一句话。"),
        (3, "③", "说不准", "问题", "说不准",
         [("以前", "谁平时认真、谁在混，凭印象记。到期末，印象早糊了。"),
          ("当时", "加多少分、扣多少分，学生不知道，我也不知道凭什么叫人服。")],
         "平时分，凭的是印象。"),
        (4, "④", "忙不过来", "问题", "忙不过来",
         [("以前", "课堂是老师讲、学生听，讲完就散。"),
          ("当时", "点名、批作业、记分、判过关，全是老师一个人的活，忙不过来就省了。")],
         "一节课能干的事，只有讲课。"),
    ]
    gap = 26
    cw = (R-L-3*gap)//4
    top = 292
    chh = 585
    for i, (n, idx, tag, _, _, rows, small) in enumerate(cards):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+150), 12)
        # 编号 + 判断词
        d.text((x0+22, top+172), idx, font=F(30, True), fill=ORD)
        d.text((x0+58, top+174), tag, font=F(38, True), fill=GREEN)
        yy = top+234
        for lab, txt in rows:
            d.text((x0+22, yy), lab, font=F(19, True), fill=OR)
            yy = para(d, (x0+22, yy+26), txt, F(23), DGREY, cw-44, 1.42, 3) + 8
        d.text((x0+22, top+chh-92), small, font=F(20, True), fill=GREEN)
        d.line([(x0+22, top+chh-40), (x0+cw-22, top+chh-40)], fill=LINE, width=1)
        d.text((x0+22, top+chh-32), ["→ 第 5 页 新形态", "→ 第 7、8 页 新证据·新分工",
                                    "→ 第 7 页 新证据", "→ 第 8 页 新分工"][i],
               font=F(19), fill=LGREY)
    by = top + chh + 26
    rr(d, [L, by, R, by+70], 6, fill=GREEN)
    t = "这四件事，就是我们做小邮的全部理由。"
    d.text((L+(R-L-tw(t, F(42, True)))//2, by+12), t, font=F(42, True), fill=WHITE)
    return cv

# ---------------------------------------------------------------- P3 四真四新（四行对账表）
def p3(folder="第03页_四真四新"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 56), "P3 · 四真 · 四新", font=F(30), fill=ORD)
    pn = "3 / 10"; d.text((R-tw(pn, F(30)), 56), pn, font=F(30), fill=LGREY)
    d.text((L, 100), "四真 · 四新", font=F(62, True), fill=GREEN)
    d.text((L+392, 128), "四真是现场（不是我编的）　四新是改法（换了怎么干）", font=F(29), fill=DGREY)
    d.line([(L, 200), (R, 200)], fill=GREEN, width=3)

    cols = [192, 392, 148, 452, 386, 118]
    xs = [L]
    for c in cols: xs.append(xs[-1]+c)
    head = ["四真", "现场摆着什么（数字）", "配哪一新", "这一新，新在哪", "能当场拿出来的东西", "页码"]
    top = 214
    hh = 62
    d.rectangle([L, top, R, top+hh], fill=GREEN)
    for i, h in enumerate(head):
        d.text((xs[i]+22, top+16), h, font=F(25, True), fill=WHITE)

    rows = [
        ("真课件", "154 页互动课件；学生自己写的记录册",
         "新形态", "知识长什么样？\n课件能点、能藏、能判，还能被问、被念（6 种）",
         "6 张现场截屏；651 篇政策库", "P5"),
        ("真任务", "驿站桌上 5 件实物；九站任务图；企业真题",
         "新场景", "任务在哪发生？\n从纸上搬到 5 个现场：驿站、展厅、车间、手势、九站",
         "驻企 42 天；3 名学生打标，企业验收", "P6"),
        ("真数据", "13 堂课、115 人、1,093 条记分明细",
         "新证据", "凭什么信你？\n每一分都带秒，翻得回是哪次课、哪个人",
         "柱图、明细表、67 本册子、两轮体检", "P7"),
        ("真课堂", "42 次抽人、82 次改分、9 站判过关",
         "新分工", "这些活谁干？\n学生做、小邮干、老师审——六张工牌，各有边界",
         "六个数字，每个都能翻回那一条", "P8"),
    ]
    rh = 168
    for r, (a, b, c, dnew, e, pg) in enumerate(rows):
        ty = top + hh + 6 + r*(rh+10)
        bg = WHITE if r % 2 == 0 else (250, 248, 243)
        d.rectangle([L, ty, R, ty+rh], fill=bg)
        d.line([(L, ty+rh), (R, ty+rh)], fill=LINE, width=2)
        d.text((xs[0]+22, ty+56), a, font=F(40, True), fill=GREEN)
        para(d, (xs[1]+22, ty+40), b, F(24), DGREY, cols[1]-44, 1.45, 3)
        d.text((xs[2]+22, ty+56), c, font=F(38, True), fill=OR)
        lines = dnew.split("\n")
        d.text((xs[3]+22, ty+30), lines[0], font=F(26, True), fill=GREEN)
        para(d, (xs[3]+22, ty+70), lines[1], F(24), DGREY, cols[3]-44, 1.45, 3)
        para(d, (xs[4]+22, ty+48), e, F(22), (96, 104, 114), cols[4]-44, 1.5, 3)
        d.text((xs[5]+34, ty+60), pg, font=F(30, True), fill=LGREY)
        # 竖向分隔
        for x in xs[1:-1]:
            d.line([(x, ty+14), (x, ty+rh-14)], fill=(238, 232, 222), width=1)
    d.line([(L, top+hh+6+4*(rh+10)-10), (R, top+hh+6+4*(rh+10)-10)], fill=GREEN, width=3)

    fy = top+hh+6+4*(rh+10)+14
    d.text((L, fy), "一行一条链：现场是我拍的　→　新在哪儿一句话说得清　→　东西当场能拿出来　→　在后面那页。",
           font=F(27, True), fill=GREEN)
    return cv

# ---------------------------------------------------------------- P4 一堂课怎么走
def p4(folder="第04页_一堂课怎么走"):
    cv, d, y = base(4, "P4 · 一堂课怎么走", "四新不是四个功能，是同一堂课的四层",
                    "一节 85 分钟的课，四段时间，每一段都有小邮在干活", 70)
    gap = 26
    cw = (R-L-3*gap)//4
    axis = 352
    top = 372
    chh = 522
    d.line([(L, axis), (R-40, axis)], fill=GREEN, width=2)
    cards = [
        (1, "0–15 分", "课前导入", "驿站全景里找五件实物，找到就进任务",
         "小邮在门口迎你，念一遍今天的任务", "新场景 · 4K 全景 VR 驿站"),
        (2, "15–40 分", "课中讲", "原页课件一页页讲；讲到第 38 页全班停下写",
         "小邮按页守着，到点提醒「该写记录册了」", "新形态 · 互动课件 / 知识星图"),
        (3, "40–65 分", "课中练", "手势答题、车间先押再跑、九站一个个点亮",
         "小邮看得见你的手，当场判、当场亮站", "新场景 · 3D 手部骨骼识别"),
        (4, "65–85 分", "课后复盘", "大屏一拉：谁加了几分、哪一站没亮，当场点人",
         "小邮把这一节的分记完，只从举了册子的人里抽", "新证据 · 13 堂课的成绩单"),
    ]
    for i, (n, tm, name, desc, duty, tag) in enumerate(cards):
        x0 = L + i*(cw+gap)
        cx = x0 + cw//2
        d.line([(cx, axis-18), (cx, axis)], fill=GREEN, width=2)
        d.ellipse([cx-9, axis-9, cx+9, axis+9], fill=OR)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+168), 12)
        d.text((x0+24, top+190), tm, font=F(30, True), fill=ORD)
        d.text((x0+24, top+228), name, font=F(52, True), fill=GREEN)
        para(d, (x0+24, top+294), desc, F(24), DGREY, cw-48, 1.45, 2)
        rr(d, [x0+18, top+366, x0+cw-18, top+chh-66], 8, fill=LGREEN)
        d.text((x0+34, top+380), "小邮这一段的活", font=F(20, True), fill=GREEN)
        para(d, (x0+34, top+406), duty, F(21), GREEN, cw-70, 1.35, 2)
        d.line([(x0+24, top+chh-52), (x0+cw-24, top+chh-52)], fill=LINE, width=1)
        d.text((x0+24, top+chh-44), tag, font=F(20), fill=LGREY)
    quote(d, "同一个班、同一节课、没加一分钟课时。", top+chh+40, 48,
          "课前导入、课中讲、课中练、课后复盘——四段时间各用一种技术组合，不是四个并列的功能。")
    return cv

# ---------------------------------------------------------------- P5 新形态
def p5(folder="第05页_新形态"):
    cv, d, y = base(5, "P5 · 真课件 · 新形态", "知识长什么样？六种活着的东西",
                    "过去是一个 PPT 文件；现在课件能点、能藏、能判，还能被问、被念", 70)
    cells = [
        (1, "互动课件", "154 页", "那 154 页还是那 154 页，但每页都活了：能点、能藏、能判", False),
        (2, "交互页面", "1 个文件", "整堂课是一个点哪都响应的网页", False),
        (3, "知识星图", "11 点", "11 个知识点连成一张图，点一下就跳到那一页", False),
        (4, "立体知识大厦", "3D", "课件摞成一座能转的楼，底层基础、顶层素养", False),
        (5, "问小邮，答政策", "651 篇", "651 篇政策，一句话问到，还能追到原文", False),
        (6, "小邮念给你听", "8 段", "8 段语音就在文件里，断网、机房静音也能念", True),
    ]
    gap = 26
    cw = (R-L-2*gap)//3
    chh = 300
    for i, (n, name, num, desc, miss) in enumerate(cells):
        row, col = i//3, i%3
        x0 = L + col*(cw+gap)
        t0 = y + row*(chh+34)
        rr(d, [x0+4, t0+8, x0+cw+4, t0+chh+8], 12, fill=(233, 227, 216))
        rr(d, [x0, t0, x0+cw, t0+chh], 12, fill=WHITE, outline=LINE, w=2)
        ok = img_at(cv, find_img(folder, n), (x0+2, t0+2, x0+cw-2, t0+150), 10)
        if not ok or miss:
            if not ok:
                d.rounded_rectangle([x0+2, t0+2, x0+cw-2, t0+150], radius=10, fill=(237, 234, 227))
                t1 = "待补：小邮说「我念给你听」的对话截图"
                d.text((x0+2+(cw-tw(t1, F(22)))//2, t0+52), t1, font=F(22), fill=(150, 146, 138))
                t2 = "（源码原话，学生真听过）"
                d.text((x0+2+(cw-tw(t2, F(22)))//2, t0+94), t2, font=F(22), fill=(175, 171, 163))
        nf = F(44, True)
        d.text((x0+24, t0+168), name, font=nf, fill=GREEN)
        d.text((x0+cw-24-tw(num, nf), t0+168), num, font=nf, fill=ORD)
        para(d, (x0+24, t0+232), desc, F(25), DGREY, cw-48, 1.5, 2)
    quote(d, "六格里只有两格带「小邮」：名字要用在它干活的地方，不是撒满一页。",
          y+2*(chh+34)+18, 40,
          "知识星图一共 11 个知识点、12 条关系；政策库 651 篇，来自企业真实文档；语音 8 段，全部内置在同一个文件里。")
    return cv

# ---------------------------------------------------------------- P6 新场景
def p6(folder="第06页_新场景"):
    cv, d, y = base(6, "P6 · 真任务 · 新场景", "任务在哪发生？五个现场，一个真题",
                    "过去是一道题；现在是能转头的驿站、能转身的展厅、能跑起来的车间", 70)
    # 大卡：图1
    bx0, by0, bx1 = L, y+4, L+1112
    bh = 372
    rr(d, [bx0+4, by0+8, bx1+4, by0+bh+8], 14, fill=(233, 227, 216))
    rr(d, [bx0, by0, bx1, by0+bh], 14, fill=WHITE, outline=LINE, w=2)
    img_at(cv, find_img(folder, 1), (bx0+2, by0+2, bx1-2, by0+248), 12)
    f = F(40, True)
    d.text((bx0+26, by0+266), "4K 全景 VR 驿站", font=f, fill=GREEN)
    n1 = "5 件"
    d.text((bx1-26-tw(n1, f), by0+266), n1, font=f, fill=ORD)
    d.text((bx0+26, by0+318), "学校真驿站拍成 360°，桌上五件实物都是按钮", font=F(24), fill=DGREY)
    # 右高卡：图2
    rx0, rx1 = bx1+26, R
    rr(d, [rx0+4, by0+8, rx1+4, by0+bh+8], 14, fill=(233, 227, 216))
    rr(d, [rx0, by0, rx1, by0+bh], 14, fill=WHITE, outline=LINE, w=2)
    img_at(cv, find_img(folder, 2), (rx0+2, by0+2, rx1-2, by0+248), 12)
    d.text((rx0+24, by0+266), "3D 环幕虚拟展厅", font=f, fill=GREEN)
    n2 = "4 面"
    d.text((rx1-24-tw(n2, f), by0+266), n2, font=f, fill=ORD)
    d.text((rx0+24, by0+318), "四面墙围成一圈，拖动就转身，点墙就进课", font=F(24), fill=DGREY)
    # 下排三小卡
    ty = by0 + bh + 34
    gap = 24
    cw = (R-L-2*gap)//3
    small = [(3, "财务机器人车间", "3 个", "三个真业务，改个数先押再跑（跑的是 RPA）",
              "车间里跑的是财务机器人，教的内容；小邮在旁边出题、判分、记分"),
             (4, "3D 手部骨骼识别", "21 点", "21 个骨骼点，手一比就能答题",
              "小邮看得见你的手，但看不见你的脸"),
             (5, "九站任务地图 + 企业真题", "9 站", "九个任务串成一条路；真题来自驻企 42 天",
              "企业真题：3 名学生打标 651 篇，企业验收")]
    for i, (n, name, num, desc, note) in enumerate(small):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, ty+8, x0+cw+4, ty+246+8], 12, fill=(233, 227, 216))
        rr(d, [x0, ty, x0+cw, ty+246], 12, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, ty+2, x0+cw-2, ty+150), 10)
        nf = F(34, True)
        d.text((x0+22, ty+166), name, font=nf, fill=GREEN)
        d.text((x0+cw-22-tw(num, nf), ty+166), num, font=nf, fill=ORD)
        d.text((x0+22, ty+212), desc, font=F(21), fill=DGREY)
    quote(d, "任务不是老师编的，是企业给的；不是纸上的，是桌上摆着的。",
          ty+266, 42,
          "第五格把「九站地图」和「企业真题」合成一格——地图是学生走的路，真题是路的起点。")
    return cv

# ---------------------------------------------------------------- P7 新证据
def p7(folder="第07页_新证据"):
    cv, d, y = base(7, "P7 · 真数据 · 新证据", "凭什么信你？六种能当场验的东西",
                    "115 名学生、13 堂课、1,093 条记分明细——每一个数都翻得回底账", 70)
    lx0, lx1 = L, L+566
    lh = y + 4 + 470
    rr(d, [lx0+4, y+12, lx1+4, lh+8], 14, fill=(233, 227, 216))
    rr(d, [lx0, y+4, lx1, lh], 14, fill=WHITE, outline=LINE, w=2)
    img_at(cv, find_img(folder, 1), (lx0+22, y+24, lx1-22, lh-56), 8)
    d.text((lx0+22, lh-46), "点开大屏，每个数字都能下钻到这一条。", font=F(22), fill=DGREY)
    rx = lx1 + 32
    gap = 16
    cw = (R-rx-gap)//2
    small = [(2, "67 本手写记录册", "67 本", "笔迹、涂改、日期都在，能发到评委手里翻"),
             (3, "13 堂课的成绩单", "1,093 条", "在册、加分、累计、最高分，每个数能下钻到明细"),
             (4, "每一分都有时间戳", "42 次", "42 次抽人，几点几分抽到谁，都查得到"),
             (5, "给小邮做了两轮体检", "5 类", "19 题，查出 5 类毛病——毛病成了下一届的毕设题")]
    ch = 262
    for i, (n, name, num, desc) in enumerate(small):
        row, col = i//2, i%2
        x0 = rx + col*(cw+gap)
        t0 = y + 4 + row*(ch+22)
        rr(d, [x0, t0, x0+cw, t0+ch], 12, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, t0+2, x0+cw-2, t0+126), 10)
        nf = F(31, True)
        d.text((x0+20, t0+142), name, font=nf, fill=GREEN)
        d.text((x0+cw-20-tw(num, nf), t0+144), num, font=nf, fill=ORD)
        para(d, (x0+20, t0+198), desc, F(21), DGREY, cw-40, 1.42, 3)
    quote(d, "这不是 PPT 上画的图，是 13 堂课一节课一节课跑出来的记录。",
          y+4+2*ch+22+34, 46,
          "另外两项在纸质材料里：三份原始 Excel、两段带原声的课堂实录（3'24\" / 4'06\"）。")
    return cv

# ---------------------------------------------------------------- P8 六张工牌
def p8(folder="第08页_新分工"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), "P8 · 真课堂 · 新分工", font=F(30), fill=ORD)
    pn = "8 / 10"; d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    x = L
    for seg, c in [("课堂里多了一个 AI 助教，它叫 ", GREEN), ("小邮", OR), ("。", GREEN)]:
        d.text((x, 104), seg, font=F(74, True), fill=c); x += tw(seg, F(74, True))
    d.text((L, 216), "小邮在课堂里干六个岗——每个岗都有边界。", font=F(33), fill=DGREY)
    d.line([(L, 274), (R, 274)], fill=LINE, width=2)
    badges = [
        ("①", "小邮点名", "不是老师挑人，是算法抽", "已落到底账", "42", "次"),
        ("②", "小邮秒批", "41 份一起批，批完老师还能改", "老师可复核", "273", "次"),
        ("③", "小邮防代写", "问三次也不给答案", "设计即约束", "0", "次"),
        ("④", "小邮不代劳", "67 本手写，它一个字不碰", "边界即态度", "67", "本"),
        ("⑤", "小邮记账", "1,093 条，条条带秒", "条条可追溯", "1,093", "条"),
        ("⑥", "小邮判过关", "做完才亮，没过重来", "判定非手点", "9", "站"),
    ]
    gap = 26
    cw = (R-L-2*gap)//3
    ch = 264
    top = 300
    for i, (idx, name, edge, tag, num, unit) in enumerate(badges):
        row, col = i//3, i%3
        x0 = L + col*(cw+gap)
        t0 = top + row*(ch+30)
        rr(d, [x0+4, t0+8, x0+cw+4, t0+ch+8], 14, fill=(233, 227, 216))
        rr(d, [x0, t0, x0+cw, t0+ch], 14, fill=WHITE, outline=LINE, w=2)
        lab = "小邮 · 工牌" + idx
        lf = F(21, True)
        wlab = tw(lab, lf) + 28
        rr(d, [x0+24, t0+22, x0+24+wlab, t0+56], 6, fill=GREEN)
        d.text((x0+38, t0+27), lab, font=lf, fill=WHITE)
        d.text((x0+24, t0+74), name, font=F(56, True), fill=GREEN)
        d.text((x0+24, t0+152), edge, font=F(24), fill=DGREY)
        d.text((x0+24, t0+206), tag, font=F(18), fill=(168,172,178))
        un = F(22); nn = F(54, True)
        d.text((x0+cw-24-tw(unit, un)-tw(num, nn)-6, t0+ch-74), num, font=nn, fill=ORD)
        d.text((x0+cw-24-tw(unit, un), t0+ch-56), unit, font=un, fill=ORD)
    d.line([(L, 892), (R, 892)], fill=LINE, width=1)
    a = "小邮批的分，"
    b = "老师改过 82 次"
    c = "；67 本手写册，小邮一个字没碰。"
    x = L
    for seg, col in [(a, GREEN), (b, OR), (c, GREEN)]:
        d.text((x, 916), seg, font=F(44, True), fill=col); x += tw(seg, F(44, True))
    d.text((L, 986), "——六个岗，六个数字；每个数字都能翻回「哪次课、哪个人、几点几分」。",
           font=F(21), fill=LGREY)
    return cv

# ---------------------------------------------------------------- P9 效果
def p9(folder="第09页_效果"):
    cv, d, y = base(9, "P9 · 效果", "三样东西同时变了", "不是「效果显著」四个字——三个方向，每条都有数字")
    gap = 30
    cw = (R-L-2*gap)//3
    top = y + 4
    chh = 560
    cols = [(1, "学生变了", "5 → 73", ["加分人数：从 5 人爬到 73 人",
                                   "财务机器人班 8 → 39 人（占 95%）",
                                   "一次没被点到的人，明显少了",
                                   "学生开始盯自己今天加到分没有"]),
            (2, "老师变了", "82 次", ["42 次抽人不用凭记忆了",
                                   "1,093 条分不用拿笔记了",
                                   "判完的分，老师改过 82 次",
                                   "不用为 AI 另做一套课件"]),
            (3, "课堂变了", "67 本", ["67 本手写册当堂写完",
                                    "九个站做完才亮",
                                    "41 台老机器同时开，没装一个软件",
                                    "任务不再是纸上的，是桌上摆的"])]
    for i, (n, name, num, items) in enumerate(cols):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 16, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 16, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+178), 14)
        d.text((x0+26, top+206), name, font=F(50, True), fill=GREEN)
        nn = F(54, True)
        d.text((x0+cw-26-tw(num, nn), top+204), num, font=nn, fill=ORD)
        d.line([(x0+26, top+286), (x0+cw-26, top+286)], fill=LINE, width=1)
        yy = top+312
        for it in items:
            d.ellipse([x0+26, yy+13, x0+37, yy+24], fill=OR)
            lines = wrap(it, F(25), cw-86)
            for j, ln in enumerate(lines):
                d.text((x0+52, yy+j*34), ln, font=F(25), fill=DGREY)
            yy += 34*len(lines) + 20
    by = top + chh + 30
    rr(d, [L, by, R, by+72], 6, fill=GREEN)
    t = "最大的变化不在系统里，在学生那只手上。"
    d.text((L+(R-L-tw(t, F(46, True)))//2, by+14), t, font=F(46, True), fill=WHITE)
    footer(d, "（「5 → 73」是《基础会计》10 堂课里加分人数的变化；82 次是老师改分次数；67 本是手写记录册数量。）",
           by+90, 19)
    return cv

# ---------------------------------------------------------------- P10 三个身份
def p10(folder="第10页_三个身份"):
    cv, d, y = base(10, "P10 · 一个作品，三个身份", "它能不能被搬走？",
                    "同一个东西，在课堂、在毕设、在企业，各是一样东西")
    top = y + 2
    gap = 96
    cw = (R-L-2*gap)//3
    chh = 210
    ids = [("身份 ①", "教学工具", ["小邮在课堂上干六个岗", "41 台老机器照样开"]),
           ("身份 ②", "毕设真题", ["651 篇打标、标签体系", "3 名学生做，企业验收"]),
           ("身份 ③", "企业交付物", ["6 组合规分析", "已进审计部日常作业"])]
    for i, (idx, name, lines) in enumerate(ids):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        d.text((x0+26, top+22), idx, font=F(22), fill=LGREY)
        d.text((x0+26, top+56), name, font=F(54, True), fill=GREEN)
        for j, ln in enumerate(lines):
            d.text((x0+26, top+130+j*34), ln, font=F(25), fill=DGREY)
        if i < 2:
            ax = x0 + cw + 28
            ay = top + chh//2
            d.line([(ax, ay), (ax+40, ay)], fill=OR, width=5)
            d.polygon([(ax+40, ay-11), (ax+58, ay), (ax+40, ay+11)], fill=OR)
    d.line([(L, top+chh+34), (R, top+chh+34)], fill=LINE, width=2)
    d.text((L, top+chh+50), "要换一门课，换的是这三样——程序不动一行：",
           font=F(36, True), fill=GREEN)
    ty = top+chh+104
    fw2, fh2 = 150, 150          # 文件图标预留宽度
    gap2 = 30
    iw = (R-L-fw2-2*gap2)//3
    for i in range(3):
        x0 = L + i*(iw+gap2)
        rr(d, [x0+3, ty+6, x0+iw+3, ty+286], 12, fill=(233, 227, 216))
        rr(d, [x0, ty, x0+iw, ty+280], 12, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, i+1), (x0+2, ty+2, x0+iw-2, ty+180), 10)
        d.text((x0+22, ty+198), ["① 一张全景照片", "② 一份任务清单", "③ 一套课件"][i],
               font=F(28, True), fill=GREEN)
        d.text((x0+22, ty+242), ["换场地", "换任务", "换内容"][i], font=F(22), fill=LGREY)
    # 文件图标（与三张图并列，不重叠）
    fx = L + 3*(iw+gap2) + 12
    fy = ty + 6
    p = find_img(folder, 4)
    if os.path.exists(p):
        img_at(cv, p, (fx, fy, fx+fw2, fy+fh2))
    else:
        d.polygon([(fx, fy), (fx+fw2-38, fy), (fx+fw2, fy+38), (fx+fw2, fy+fh2), (fx, fy+fh2)],
                  fill=WHITE, outline=GREEN)
        d.text((fx+18, fy+56), "HTML", font=F(24), fill=DGREY)
        d.text((fx+14, fy+92), "13 MB", font=F(38, True), fill=ORD)
    d.text((fx-10, fy+fh2+16), "整个课堂 =", font=F(26, True), fill=GREEN)
    d.text((fx-10, fy+fh2+50), "一个 13 MB 文件", font=F(26, True), fill=GREEN)
    quote(d, "能被复制的东西才叫方法，只能演示的只算案例。", ty+326, 42,
          "（「换三样」指：全景照片、任务清单、课件可以换掉重配；页面程序本身不用改。）")
    return cv

PAGES = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

def main():
    out = os.path.join(HERE, "成品")
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate(PAGES, 1):
        cv = fn()
        cv.save(os.path.join(out, "P%02d.png" % i))
        print("saved P%02d.png" % i)

if __name__ == "__main__":
    main()
