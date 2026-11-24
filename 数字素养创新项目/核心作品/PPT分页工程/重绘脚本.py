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

def base(num, eyebrow, title, sub=None, tsize=76, ssize=33):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), eyebrow, font=F(30), fill=ORD)
    pn = "%d / 10" % num
    d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    d.text((L, 108), title, font=F(tsize, True), fill=GREEN)
    y = 108 + int(tsize*1.30)
    if sub:
        d.text((L, y), sub, font=F(ssize), fill=DGREY)
        y += int(ssize*1.62)
    d.line([(L, y+6), (R, y+6)], fill=LINE, width=2)
    return cv, d, y+38

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
    al = (np.clip(fy*0.80+fx*0.80, 0, 1)**1.30*225).astype(np.uint8)
    lay = Image.new("RGBA", (W, H), (9, 40, 34, 255))
    lay.putalpha(Image.fromarray(al))
    cv = Image.alpha_composite(cv.convert("RGBA"), lay).convert("RGB")
    d = ImageDraw.Draw(cv)
    # 顶部：活动名
    d.text((L, 96), "河北省高校人工智能赋能教师教学创新展示活动", font=F(30), fill=(238, 234, 226))
    # 中部：作品名 + 一句话
    d.text((L, 392), "小邮伴学", font=F(132, True), fill=WHITE)
    d.text((L, 560), "把真课堂装进一个文件", font=F(58, True), fill=(246, 243, 237))
    d.text((L, 648), "学生打开就能上课，老师打开就能上课，断网也能上课。", font=F(30), fill=(224, 218, 208))
    # 四真：一条横向色带，铺满整行
    band = 745
    d.line([(L, band-26), (R, band-26)], fill=(255, 255, 255, 60), width=2)
    xs = L
    for i, w_ in enumerate(["真课件", "·", "真任务", "·", "真数据", "·", "真课堂"]):
        f = F(46, True) if w_ != "·" else F(46)
        d.text((xs, band), w_, font=f, fill=OR if w_ != "·" else (200, 150, 110))
        xs += tw(w_, f) + 34
    # 底部：作品信息（左）+ 日期（右）
    d.line([(L, 900), (R, 900)], fill=(255, 255, 255, 70), width=2)
    d.text((L, 926), "教育教学智能体设计作品", font=F(28), fill=(240, 236, 228))
    d.text((L, 972), "石家庄邮电职业技术学院　薛辉", font=F(28), fill=(240, 236, 228))
    d.text((R-tw("2026.11.28", F(32)), 946), "2026.11.28", font=F(32), fill=(226, 222, 214))
    return cv

# ---------------------------------------------------------------- P2 初衷（四个老问题）
def p2(folder="第02页_初衷"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), "P2 · 初衷", font=F(30), fill=ORD)
    pn = "2 / 10"; d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    d.text((L, 104), "一节课里，有四件事一直没人管", font=F(72, True), fill=GREEN)
    d.text((L, 204), "这四件事都不新，全出在同一个地方：全靠老师一个人记、一个人看、一个人算、一个人干。",
           font=F(34), fill=DGREY)
    d.line([(L, 270), (R, 270)], fill=LINE, width=2)

    cards = [
        (1, "①", "讲到第几页，\n没人说得清",
         [("以前", "课件一共 154 页，上节课讲到第 38 页。"),
          ("当时", "下节课只有老师自己记得讲到哪。学生想预习，不知道从哪页看起。")],
         "课件讲到哪一页，全班只有老师一个人知道。",
         "→ 第 5 页 新形态"),
        (2, "②", "笔记写得好不好，\n老师看不见",
         [("以前", "学生用手写记录册，一个班 41 本、74 本，收上来摞一桌。"),
          ("当时", "一学期翻不了几遍：写得乱、抄得对不对、谁没交，都看不出。")],
         "学生写得对不对，没有人当面告诉他一句。",
         "→ 第 7、8 页 新证据·新分工"),
        (3, "③", "平时分给多少，\n说不清凭什么",
         [("以前", "谁平时认真、谁在混，老师凭印象记。"),
          ("当时", "到期末印象早糊了。加多少、扣多少，学生不知道，老师也说不清。")],
         "平时分怎么来的，谁也说不清。",
         "→ 第 7 页 新证据"),
        (4, "④", "点名、批作业、记分，\n一个人干不完",
         [("以前", "课堂就是老师讲、学生听，讲完就散。"),
          ("当时", "点名、批作业、记分、判过关，全是老师一个人的活，忙不过来就省了。")],
         "这些活，一个老师真的忙不过来。",
         "→ 第 8 页 新分工"),
    ]
    gap = 26
    cw = (R-L-3*gap)//4
    top = 294
    chh = 596
    for i, (n, idx, tag, rows, small, goto) in enumerate(cards):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+132), 12)
        d.text((x0+20, top+146), idx, font=F(28, True), fill=ORD)
        yy = top+182
        for ln in tag.split("\n"):
            d.text((x0+20, yy), ln, font=F(29, True), fill=GREEN)
            yy += 40
        yy += 10
        for lab, txt in rows:
            d.text((x0+20, yy), lab, font=F(19, True), fill=OR)
            yy = para(d, (x0+20, yy+24), txt, F(21), DGREY, cw-40, 1.40, 4) + 6
        d.line([(x0+20, top+chh-112), (x0+cw-20, top+chh-112)], fill=LINE, width=1)
        para(d, (x0+20, top+chh-100), small, F(21, True), GREEN, cw-40, 1.32, 2)
        d.text((x0+20, top+chh-32), goto, font=F(19), fill=LGREY)
    by = top + chh + 18
    rr(d, [L, by, R, by+70], 6, fill=GREEN)
    t = "小邮要解决的，就是这四件事。"
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
    d.text((L+392, 128), "四真，就是现场真实存在的东西；四新，就是我们把哪一步换了个干法。", font=F(29), fill=DGREY)
    d.line([(L, 200), (R, 200)], fill=GREEN, width=3)

    cols = [192, 392, 148, 452, 386, 118]
    xs = [L]
    for c in cols: xs.append(xs[-1]+c)
    head = ["四真", "现场有什么（数字）", "四新", "新在哪（一句话）", "当场能拿出什么", "页码"]
    top = 214
    hh = 62
    d.rectangle([L, top, R, top+hh], fill=GREEN)
    for i, h in enumerate(head):
        d.text((xs[i]+22, top+16), h, font=F(25, True), fill=WHITE)

    rows = [
        ("真课件", "154 页互动课件；\n学生手写的记录册",
         "新形态", "知识长什么样？\n课件能点、能藏、能判，还能被问、被念",
         "6 张现场截屏；\n651 篇政策库", "P5"),
        ("真任务", "驿站桌上 5 件实物；\n九站任务；企业真题",
         "新场景", "任务在哪发生？\n从纸上搬到 5 个现场：驿站、展厅、车间、手势、九站",
         "驻企 42 天；\n企业验收的打标成果", "P6"),
        ("真数据", "13 堂课、115 人、\n1,093 条记分明细",
         "新证据", "凭什么信你？\n每一分都写明几点几分，翻得回哪次课、哪个人",
         "柱图、明细表、\n67 本册子、两轮体检", "P7"),
        ("真课堂", "42 次抽人、82 次改分、\n9 站判过关",
         "新分工", "这些活谁干？\n学生做、小邮干、老师审——六张工牌，各有边界",
         "六个数字，\n每一个都翻得回那一条", "P8"),
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
    d.text((L, fy), "四真都有实物，四新都落在一页上——往下四页，一页讲一样。",
           font=F(28, True), fill=GREEN)
    return cv

# ---------------------------------------------------------------- P4 一堂课怎么走（技术怎么运作）
def p4(folder="第04页_一堂课怎么走"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 56), "P4 · 课前导入 · 课中讲 · 课中练 · 课后复盘", font=F(30), fill=ORD)
    pn = "4 / 10"; d.text((R-tw(pn, F(30)), 56), pn, font=F(30), fill=LGREY)
    d.text((L, 100), "这一堂课，小邮在四个环节各干一件活", font=F(72, True), fill=GREEN)
    d.text((L, 204), "同一节课、同一个班、一分钟课时都没加——看看技术在这四段里各干了什么。",
           font=F(40), fill=DGREY)
    d.line([(L, 278), (R, 278)], fill=LINE, width=2)

    cards = [
        (1, "0–15 分 · 课前导入",
         "全景自己会转，不用装插件、不用联网。学生点桌上那五样——信、扫码枪、账本、财务机器人、百宝箱——它一件件讲给他听。",
         "360° 全景 VR ＋ 点击热点 ＋ 内置语音（断网也能转）",
         "过去导入靠老师讲、靠照片；现在是学生在真场地里自己转一圈，五步点完。"),
        (2, "15–40 分 · 课中讲",
         "154 页摊在一个网页里：点知识星图就跳页，点关键词就藏、就判，点小邮就能问，它把 8 段语音念给你听。",
         "互动课件 154 页 ＋ 知识星图 11 点 ＋ 语音朗读 8 段",
         "过去课件是死的，讲哪算哪；现在它自己会跳、会藏、会念。"),
        (3, "40–65 分 · 课中练",
         "手一比就认（21 个骨骼点），不用鼠标；车间里让财务机器人先押再跑，九个站做完一站亮一站。",
         "3D 手部骨骼识别 ＋ 财务机器人 ＋ 九站闯关",
         "过去练是纸上写、下周判；现在当场认、当场判、当场亮。"),
        (4, "65–85 分 · 课后复盘",
         "这一节谁写了、谁加了分、谁卡住，大屏一拉全在；再从举了册子的人里抽一个，当场问。",
         "实时大屏 ＋ 算法抽人 ＋ 1,093 条带时间戳",
         "过去复盘凭记忆、点人凭老师；现在数据点人、算法抽人，学生服。"),
    ]
    gap = 24
    cw = (R-L-3*gap)//4
    top = 312
    chh = 530
    for i, (n, name, duty, tech, newtxt) in enumerate(cards):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+106), 12)
        d.text((x0+22, top+114), name, font=F(26, True), fill=GREEN)
        # 小邮在干什么
        rr(d, [x0+14, top+150, x0+cw-14, top+302], 10, fill=LGREEN)
        d.text((x0+30, top+160), "小邮在这里", font=F(20, True), fill=GREEN)
        para(d, (x0+30, top+188), duty, F(20), GREEN, cw-56, 1.38, 4)
        # 用什么技术
        d.text((x0+22, top+314), "用什么技术", font=F(19, True), fill=OR)
        para(d, (x0+22, top+338), tech, F(22, True), GREEN, cw-44, 1.34, 2)
        # 和过去比
        d.text((x0+22, top+408), "和过去比", font=F(19, True), fill=OR)
        para(d, (x0+22, top+432), newtxt, F(20), DGREY, cw-42, 1.38, 4)
    quote(d, "还是那 85 分钟，只是这四段都有人搭手了。", top+chh+22, 44,
          "技术只有一个用处：把老师一个人干不过来的活接过去。")
    return cv

# ---------------------------------------------------------------- P5 新形态
def p5(folder="第05页_新形态"):
    cv, d, y = base(5, "P5 · 新形态", "真课件 · 新形态",
                    "知识长什么样？它不再是死的一页一页：能点、能藏、能判、能问、能念。", 72, 40)
    cells = [
        (1, "互动课件", "154 页", "每页都能点、能藏、能判——讲到哪、藏什么、判对错，页面自己说了算", False),
        (2, "交互页面", "1 个文件", "整堂课是一个网页：双击就开、断网能用，不装任何软件", False),
        (3, "知识星图", "11 点", "11 个知识点连成一张图，点哪个点就跳到哪一页", False),
        (4, "立体知识大厦", "3D", "把课件摞成一座能转的楼：底层是基础，顶层是素养", False),
        (5, "问小邮，答政策", "651 篇", "651 篇政策文档装在文件里，一句话问到，还能点开原文", False),
        (6, "小邮念给你听", "8 段", "8 段语音内置在同一个文件里，断网、静音机房也能念", True),
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
    quote(d, "以前的课件是老师放给学生看的；现在学生点哪儿，它就应哪儿。",
          y+2*(chh+34)+16, 40,
          "知识星图一共 11 个知识点、12 条关系；政策库 651 篇，来自企业真实文档；语音 8 段，全部内置在同一个文件里。")
    return cv

# ---------------------------------------------------------------- P6 新场景
def p6(folder="第06页_新场景"):
    cv, d, y = base(6, "P6 · 新场景", "真任务 · 新场景",
                    "任务在哪发生？从纸上搬到五个真现场——能转头、能转身、能跑起来", 72, 40)
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
    d.text((bx0+26, by0+318), "学校真驿站拍成 360°，能一直转；桌上五件实物都是按钮", font=F(24), fill=DGREY)
    # 右高卡：图2
    rx0, rx1 = bx1+26, R
    rr(d, [rx0+4, by0+8, rx1+4, by0+bh+8], 14, fill=(233, 227, 216))
    rr(d, [rx0, by0, rx1, by0+bh], 14, fill=WHITE, outline=LINE, w=2)
    img_at(cv, find_img(folder, 2), (rx0+2, by0+2, rx1-2, by0+248), 12)
    d.text((rx0+24, by0+266), "3D 环幕虚拟展厅", font=f, fill=GREEN)
    n2 = "4 面"
    d.text((rx1-24-tw(n2, f), by0+266), n2, font=f, fill=ORD)
    d.text((rx0+24, by0+318), "四面墙围成一圈，拖动就转身，点哪面墙就进哪一课", font=F(24), fill=DGREY)
    # 下排三小卡
    ty = by0 + bh + 34
    gap = 24
    cw = (R-L-2*gap)//3
    small = [(3, "财务机器人车间", "3 个", "三个真业务，改个数先押再跑",
              "跑的是财务机器人；小邮在旁边出题、判分、记分"),
             (4, "3D 手部骨骼识别", "21 点", "21 个骨骼点，手一比就答题",
              "小邮看得见你的手，但看不见你的脸"),
             (5, "九站任务地图", "9 站", "九个任务串成一条路，做完一站亮一站",
              "真题来自驻企 42 天，3 名学生打标 651 篇")]
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
          ty+262, 42,
          "五格连成一条线：真场地（驿站、展厅）→ 真业务（车间）→ 真动作（手势）→ 真任务链（九站）。")
    return cv

# ---------------------------------------------------------------- P7 新证据
def p7(folder="第07页_新证据"):
    cv, d, y = base(7, "P7 · 新证据", "真数据 · 新证据",
                    "凭什么信你？不靠一句「效果显著」——六个东西当场就能验", 72, 40)
    lx0, lx1 = L, L+566
    lh = y + 4 + 470
    rr(d, [lx0+4, y+12, lx1+4, lh+8], 14, fill=(233, 227, 216))
    rr(d, [lx0, y+4, lx1, lh], 14, fill=WHITE, outline=LINE, w=2)
    img_at(cv, find_img(folder, 1), (lx0+22, y+24, lx1-22, lh-56), 8)
    d.text((lx0+22, lh-46), "点开大屏，每个数都能翻到具体那一条。", font=F(22), fill=DGREY)
    rx = lx1 + 32
    gap = 16
    cw = (R-rx-gap)//2
    small = [(2, "67 本手写记录册", "67 本", "笔迹、涂改、日期全在，能发到评委手里翻"),
             (3, "13 堂课的成绩单", "1,093 条", "在册、加分、累计、最高分，每一条能下钻"),
             (4, "每一分都有时间戳", "42 次", "42 次抽人，几点几分抽到谁，都查得到"),
             (5, "给小邮做了两轮体检", "5 类", "19 题查出 5 类毛病，成了下一届的毕设题")]
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
    quote(d, "这些图不是画出来的，是 13 堂课一节一节记下来的。",
          y+4+2*ch+22+30, 44,
          "115 名学生、13 堂课、1,093 条明细；另有三份原始 Excel、两段课堂实录（3'24\" / 4'06\"）。")
    return cv

# ---------------------------------------------------------------- P8 六张工牌
def p8(folder="第08页_新分工"):
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 0, 26, H], fill=GREEN)
    d.text((L, 62), "P8 · 新分工", font=F(30), fill=ORD)
    pn = "8 / 10"; d.text((R-tw(pn, F(30)), 62), pn, font=F(30), fill=LGREY)
    x = L
    for seg, c in [("真课堂 · ", GREEN), ("新分工", OR)]:
        d.text((x, 104), seg, font=F(84, True), fill=c); x += tw(seg, F(84, True))
    x = L
    for seg, c in [("课堂里多了一个助教，它叫 ", GREEN), ("小邮", OR), ("；六个岗，各有边界。", GREEN)]:
        d.text((x, 226), seg, font=F(40), fill=c); x += tw(seg, F(40))
    d.line([(L, 296), (R, 296)], fill=LINE, width=2)
    badges = [
        ("①", "小邮点名", "不是老师挑人，是算法抽", "抽了谁，查得到", "42", "次"),
        ("②", "小邮秒批", "41 份一起批，批完老师还能改", "最后仍是老师说了算", "273", "次"),
        ("③", "小邮防代写", "问三次也不给答案", "这条规矩写进了程序", "0", "次"),
        ("④", "小邮不代劳", "67 本手写，它一个字不碰", "它不替学生写字", "67", "本"),
        ("⑤", "小邮记账", "1,093 条，每条都写几点几分", "每一分都翻得回去", "1,093", "条"),
        ("⑥", "小邮判过关", "做完才亮，没过重来", "机器判，不是手点", "9", "站"),
    ]
    gap = 26
    cw = (R-L-2*gap)//3
    ch = 258
    top = 318
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
    d.line([(L, 902), (R, 902)], fill=LINE, width=1)
    a = "小邮批的分，"
    b = "老师改过 82 次"
    c = "；67 本手写册，小邮一个字没碰。"
    x = L
    for seg, col in [(a, GREEN), (b, OR), (c, GREEN)]:
        d.text((x, 926), seg, font=F(44, True), fill=col); x += tw(seg, F(44, True))
    d.text((L, 992), "六个岗，六个数字；每一个数字都能翻回：哪次课、哪个人、几点几分。",
           font=F(21), fill=LGREY)
    return cv

# ---------------------------------------------------------------- P9 效果（数字从哪来）
def p9(folder="第09页_效果"):
    cv, d, y = base(9, "P9 · 效果", "效果 · 三样东西同时变了",
                    "这些数不是统计出来的，是小邮每干一件活，自己顺手记下来的。", 72, 40)

    # ---- 数字从哪来：一条流水线
    by = y + 2
    rr(d, [L, by, R, by+78], 8, fill=LGREEN)
    d.text((L+22, by+26), "数字从哪来", font=F(24, True), fill=GREEN)
    steps = ["① 小邮干一件活", "② 文件自己记一条，几点几分都写上", "③ 13 堂课攒成 1,093 条，汇成大屏"]
    x = L + 214
    for i, t in enumerate(steps):
        d.text((x, by+24), t, font=F(24, True), fill=DGREY)
        x += tw(t, F(24, True)) + 18
        if i < 2:
            d.text((x, by+24), "→", font=F(24, True), fill=OR); x += 40

    cards = [
        (1, "学生变了", "5 → 73",
         "每节课点名抽人，抽到、答对，当场加一条分。",
         "13 堂课下来，加分的人从 5 个涨到 73 个。",
         "以前只有几个尖子举手；现在几乎全班在等被抽。"),
        (2, "老师变了", "82 次",
         "41 份作业一起批完，把分推给老师，老师再改。",
         "82 次改动，每次都记下原判几分、改成几分。",
         "判分的是老师，不是 AI——这 82 次就是证据。"),
        (3, "课堂变了", "67 本",
         "把该写的那几格推上大屏、念一遍要求，但不碰笔。",
         "67 本手写册，当堂写完、当堂收上来。",
         "小邮干得越多，学生手上越不能停。"),
    ]
    gap = 30
    cw = (R-L-2*gap)//3
    top = by + 84
    chh = 552
    for i, (n, name, num, duty, made, meaning) in enumerate(cards):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, n), (x0+2, top+2, x0+cw-2, top+176), 12)
        d.text((x0+26, top+192), name, font=F(44, True), fill=GREEN)
        nn = F(46, True)
        d.text((x0+cw-26-tw(num, nn), top+190), num, font=nn, fill=ORD)
        d.line([(x0+26, top+258), (x0+cw-26, top+258)], fill=LINE, width=1)
        blocks = [("小邮干了什么", duty, GREEN), ("记下什么", made, DGREY), ("说明什么", meaning, OR)]
        yy = top+280
        for lab, txt, col in blocks:
            d.text((x0+26, yy), lab, font=F(20, True), fill=ORD if lab != "小邮干了什么" else GREEN)
            yy = para(d, (x0+26, yy+32), txt, F(23), col, cw-52, 1.42, 3) + 16
    quote(d, "最大的变化不在系统里，在学生那只手上。", top+chh+16, 42)
    return cv

# ---------------------------------------------------------------- P10 被用了三次
def p10(folder="第10页_三个身份"):
    cv, d, y = base(10, "P10 · 可复制", "同一个文件，被用了三次",
                    "先在课堂上教 → 用出 5 类毛病 → 毛病变成毕设真题 → 毕设成果交到企业手上", 72, 40)

    steps = [
        ("用第 1 次", "在课堂上用", "115 名学生、13 堂课，六个岗天天转：点名、秒批、记账、判过关",
         "用出 5 类毛病（做了 19 题体检）"),
        ("用第 2 次", "在毕设里用", "那 5 类毛病成了 3 名学生的毕设真题：给 651 篇政策打标、建标签体系",
         "企业验收"),
        ("用第 3 次", "在企业里用", "毕设做出来的 6 组合规分析，直接进了审计部日常作业",
         "已经天天在用"),
    ]
    gap = 56
    cw = (R-L-2*gap)//3
    top = y + 2
    chh = 262
    for i, (idx, who, duty, endtxt) in enumerate(steps):
        x0 = L + i*(cw+gap)
        rr(d, [x0+4, top+8, x0+cw+4, top+chh+8], 14, fill=(233, 227, 216))
        rr(d, [x0, top, x0+cw, top+chh], 14, fill=WHITE, outline=LINE, w=2)
        lab = "同一份课件 · " + idx
        lf = F(21, True)
        wlab = tw(lab, lf) + 26
        rr(d, [x0+22, top+20, x0+22+wlab, top+54], 6, fill=GREEN)
        d.text((x0+35, top+25), lab, font=lf, fill=WHITE)
        d.text((x0+22, top+70), who, font=F(44, True), fill=GREEN)
        para(d, (x0+22, top+132), duty, F(22), DGREY, cw-44, 1.42, 3)
        d.line([(x0+22, top+chh-52), (x0+cw-22, top+chh-52)], fill=LINE, width=1)
        d.text((x0+22, top+chh-42), "→ " + endtxt, font=F(21, True), fill=ORD)
        if i < 2:
            ax = x0 + cw + 12
            ay = top + chh//2
            d.line([(ax, ay), (ax+32, ay)], fill=OR, width=5)
            d.polygon([(ax+32, ay-10), (ax+48, ay), (ax+32, ay+10)], fill=OR)
    # 第一二步之间的交接说明
    ay = top + chh + 22
    d.text((L, ay), "课堂用出来的毛病，就是毕设的题；毕设做出来的东西，交到企业手里——同一条线，不是三件不相干的事。",
           font=F(24), fill=DGREY)

    # ---- 下半区：换一门课只换三样
    ly = ay + 56
    d.line([(L, ly), (R, ly)], fill=LINE, width=2)
    d.text((L, ly+16), "要换一门课，换的是这三样——页面程序不动一行：", font=F(34, True), fill=GREEN)
    ty = ly + 74
    fw2, fh2 = 140, 140
    gap2 = 26
    iw = (R-L-fw2-2*gap2)//3
    ch2 = 236
    for i in range(3):
        x0 = L + i*(iw+gap2)
        rr(d, [x0+3, ty+6, x0+iw+3, ty+ch2+6], 12, fill=(233, 227, 216))
        rr(d, [x0, ty, x0+iw, ty+ch2], 12, fill=WHITE, outline=LINE, w=2)
        img_at(cv, find_img(folder, i+1), (x0+2, ty+2, x0+iw-2, ty+150), 10)
        d.text((x0+20, ty+164), ["① 一张全景照片", "② 一份任务清单", "③ 一套课件"][i],
               font=F(27, True), fill=GREEN)
        d.text((x0+20, ty+200), ["换场地", "换任务", "换内容"][i], font=F(21), fill=LGREY)
    fx = L + 3*(iw+gap2) + 10
    fyv = ty + 4
    pth = find_img(folder, 4)
    if os.path.exists(pth):
        img_at(cv, pth, (fx, fyv, fx+fw2, fyv+fh2))
    else:
        rr(d, [fx, fyv, fx+fw2, fyv+fh2], 8, fill=WHITE, outline=GREEN, w=2)
        d.text((fx+14, fyv+40), "HTML", font=F(22), fill=DGREY)
        d.text((fx+8, fyv+74), "13 MB", font=F(34, True), fill=ORD)
    d.text((fx-6, fyv+fh2+14), "整个课堂 =", font=F(23, True), fill=GREEN)
    d.text((fx-6, fyv+fh2+44), "一个 13 MB 文件", font=F(23, True), fill=GREEN)
    quote(d, "别人也照着做得出来，这才叫方法；只能演一遍的，只是个案例。", ty+ch2+22, 40)
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
