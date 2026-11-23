# VR 页面 + 短视频融合方案（面向 11-27 现场展示）

> 对象：`校园快递驿站-VR情景导入-v37.html`
> 活动硬约束：**展示 7 分钟 + 互动 3 分钟**，要求"现场演示教育教学智能体，并阐述应用场景与功能"
> 主题：河北省高校人工智能赋能教师教学创新展示活动 —— **教育教学智能体设计**

---

## 一、先说结论

1. **不要用视频去"演一遍全景"**。全景你已经能转、能推、能点，视频重复它 = 白花 30 秒。视频唯一的价值是呈现**全景图做不到的事：时间**。
2. 最合适的视频内容是一句话就能讲清的设定：**"全景是空间，视频是时间 —— 我们让这张静止的桌子活了过来。"**
3. 落地形态建议做成 **"AR 空间锚定层（Video-as-AR-Layer）"**：不是弹窗放视频，而是让视频**贴在桌面/账本/屏幕上，随你转头而透视变化、边缘羽化融入场景**。这样"VR + AR 结合"这句话才有代码证据支撑，而不是口头包装。

---

## 二、一个必须先想清楚的战略判断

你报名的是 **"教育教学智能体设计"**，不是"VR 技术展示"。评委打分看的是：

> 这个智能体**在真实课堂里替师生解决了什么问题**，以及**人和 AI 的分工是否清晰**。

所以 VR 页面在这 7 分钟里的定位应该是 **"智能体的情境入口"**，不是炫技主体。建议时间分配：

| 环节 | 时长 | 内容 |
|---|---|---|
| 门框动画 + 全景自转 | 5 s | 一句话定性：真实岗位情境，不是虚构实训 |
| 点亮 AR 层 + 播放视频 | 20 s | 呈现"实物→数字"的跃迁 |
| 5 步闯关快走 | 40 s | 学生先手算 11 元 → 机器人 0.8 秒对平 327 笔 → **1 笔争议单进教师终审** |
| 切到"小邮伴学"主体 | 45 s | 八功能 + 真实课堂数据 |
| 收尾 | 20 s | 四真 + 可复制性 |
| **合计** | **≈ 2 分 10 秒** | 余下时间留给互动答辩 |

⚠️ 关键：VR 段控制在 **100 秒内**。它是"钩子"，不是"主菜"。

---

## 三、代码与视频的分工（为什么这样最划算）

| 维度 | 代码（HTML/Canvas）能做 | 只有视频能做 |
|---|---|---|
| 空间 | 360° 环绕、变焦推近、热点定位 | — |
| 交互 | 点击、答题、步骤解锁、语音 | — |
| **时间** | 只能做"关键帧式"动画，做不出质的连续变化 | **物体形变、粒子流动、光照溢出、镜头运动** |
| **"看不见的东西"** | 只能贴标签 | **数据流、AI 判断过程、账目对平的那一瞬** |

结论：**视频负责"看不见的过程"，代码负责"可操作的现在"。** 这也是你答辩时最省力的一句分工说明。

---

## 四、推荐方案：AR 空间锚定层

### 4.1 三层递进结构

```
① 静态热点（v37 已有）      → 告诉学生"这里有什么"
② 追踪环 AR-Target（新增）   → 点击后出现脉冲准星 + 连接线，3D 贴附在实物上
③ 视频卡 AR-Layer（新增）    → 准星展开为视频，跟随视角透视缩放、边缘羽化融入场景
```

第 ②③ 层用的就是 v37 里那套 `lon / lat / fov` 投影公式 —— **改动量约 60 行，不动主渲染循环**。

### 4.2 四个可锚定的"舞台"（都在同一张桌面上，这是你的天赋条件）

| 锚点 | 坐标参考（v37 现值） | 视频内容 | 说服力 |
|---|---|---|---|
| **红皮账本** | lon 187 / lat -50 | 数字孪生：手写行下方"长"出 328 行数据，逐行打勾 | ★★★★★ |
| **扫码枪** | lon 151 / lat -50 | 红色扫描光柱扫过面单，数据流沿桌面流向账本 | ★★★★★ |
| **笔记本屏幕** | lon 230 / lat -36 | 镜头推进屏幕：327 行滚过变绿，1 行变红飞走 | ★★★★★ |
| **皮箱** | lon 284 / lat -38 | 锁扣弹开、金光溢出（收尾帧） | ★★★☆ |

> 强在哪：全景图是**AI 生成的 4K 实拍级画面**，桌面上的物体位置固定已知，所以"锚定"是**天然成立**的——不需要 SLAM，不会飘。

### 4.3 可直接嵌入 v38 的代码骨架

```js
/* ============ AR 锚定层：与 hotspots 共用同一套经纬度投影 ============ */
const AR_ANCHORS = [
  { id:'flow',  lon:186, lat:-48, w:0.34, label:'AR·数据流层',  src:'ar_flow.mp4',  poster:'ar_flow.jpg'  },
  { id:'audit', lon:230, lat:-36, w:0.30, label:'AR·AI对账',    src:'ar_audit.mp4' },
  { id:'chest', lon:284, lat:-38, w:0.26, label:'AR·结算结果',  src:'ar_chest.mp4' },
];

AR_ANCHORS.forEach(a => {
  const el = document.createElement('div');
  el.className = 'ar-anchor';
  el.id = 'ar-' + a.id;
  el.innerHTML = `
    <div class="ar-reticle"><i></i><i></i><i></i><i></i></div>
    <div class="ar-card">
      <div class="ar-tag">${a.label}</div>
      <video src="${a.src}" ${a.poster ? `poster="${a.poster}"` : ''}
             playsinline muted loop preload="metadata"></video>
    </div>`;
  // 点击放大会带声音播完整版
  el.onclick = () => openARFullscreen(a);
  document.getElementById('hotspot-layer').appendChild(el);
  a.el = el;
});

// 在主渲染循环里追加（v37 的 hotspots.forEach 之后）
AR_ANCHORS.forEach(a => {
  const dLon = ((a.lon - lon + 540) % 360) - 180;
  const dLat = a.lat - lat;
  const halfView = fov * 0.55;
  if (Math.abs(dLon) > halfView) { a.el.style.display = 'none'; return; }
  a.el.style.display = 'block';

  const px = innerWidth  / 2 + (dLon / fov) * innerWidth;
  const py = innerHeight / 2 - (dLat / (fov * innerHeight / innerWidth)) * innerHeight;
  const scale = 150 / fov;          // 拉近(fov↓) → 变大
  const rotY  = -dLon * 0.55;       // ★关键：随视角偏转 → 产生"贴在空间里"的3D感
  const fade  = 1 - Math.abs(dLon) / halfView;

  a.el.style.left = px + 'px';
  a.el.style.top  = py + 'px';
  a.el.style.opacity = fade.toFixed(2);
  a.el.style.transform =
    `translate(-50%,-50%) perspective(900px) rotateY(${rotY}deg) scale(${scale.toFixed(3)})`;
});
```

配套 CSS（**羽化是"不像贴纸"的命门**）：

```css
.ar-anchor { position:absolute; pointer-events:auto; cursor:pointer;
             transition:opacity .15s linear; will-change:transform,opacity; }
.ar-card   { position:relative; width:420px; border-radius:14px; overflow:hidden;
             /* 边缘羽化：让它和全景融为一体，而不是一张浮在上面的图 */
             -webkit-mask-image:radial-gradient(ellipse 88% 82% at 50% 50%, #000 62%, transparent 100%);
                     mask-image:radial-gradient(ellipse 88% 82% at 50% 50%, #000 62%, transparent 100%); }
.ar-card video { width:100%; display:block; }
.ar-tag    { position:absolute; top:8px; left:10px; font-size:12px; letter-spacing:.5px;
             color:#5eead4; background:rgba(2,6,23,.6); border:1px solid rgba(94,234,212,.5);
             padding:2px 8px; border-radius:99px; backdrop-filter:blur(6px); }
.ar-reticle{ position:absolute; inset:-14px; display:grid; place-items:center; pointer-events:none; }
.ar-reticle i { position:absolute; width:18px; height:18px; border:2px solid rgba(94,234,212,.9);
                animation:arPulse 2.2s ease-out infinite; }
.ar-reticle i:nth-child(1){ top:0; left:0;  border-right:0; border-bottom:0; }
.ar-reticle i:nth-child(2){ top:0; right:0; border-left:0;  border-bottom:0; }
.ar-reticle i:nth-child(3){ bottom:0; left:0;  border-right:0; border-top:0; }
.ar-reticle i:nth-child(4){ bottom:0; right:0; border-left:0; border-top:0; }
@keyframes arPulse { 0%{opacity:.25; transform:scale(1.15)} 60%{opacity:1; transform:scale(1)} 100%{opacity:.25; transform:scale(1.15)} }
```

**为什么 `rotateY` 这四个字值是方案核心**：全景旋转时，视频卡的左右边缘会产生透视变形，视觉上"贴"在那面墙/那张桌上，而不是像 HUD 一样悬在屏幕上。这就是观众感知到"AR"的心理学开关。

### 4.4 备用低成本版（半天可完成，效果 ~80%）

时间实在紧的话，**不做 MP4，只做锚定层**：
- 追踪环脉冲 + 数据层用 Canvas 画（数字计数器 + 逐行打勾 + 扫描光柱）
- 零加载成本、零文件、投影仪绝不卡
- 缺点：没有"物体形变"的奇观感

建议：**先用豪华版视频，同时内置这个降级路径**（视频加载失败 `onerror` 自动回落到 Canvas 版）——答辩现场网络不可控，这是保险丝。

---

## 五、视频内容：4 个候选，按"全景做不到"排序

### 候选 A（首推）· 20 秒主视频《让这张桌子活过来》

一句话设定：**静态全景是空间，视频是时间。**

| # | 时长 | 画面 | 屏显数据 |
|---|---|---|---|
| 1 | 0–3 s | 桌面近景，扫码枪红光扫过牛皮纸信封与面单，尘埃在光柱中浮动 | `328 面单` |
| 2 | 3–8 s | 数据从扫码枪沿桌面"流"进红皮账本；账本原有手写行下方逐行"长出"新行并高亮 | `实物 → 数字` |
| 3 | 8–13 s | 镜头推入笔记本屏幕，327 行流水高速滚过、逐行打勾变绿 | `AI 0.8 s · 327 笔对平` |
| 4 | 13–17 s | 1 行数据变红、抬起、飞向画面边缘的"教师终审"卡片，其余全绿 | `1 笔争议 → 教师终审` |
| 5 | 17–20 s | 皮箱锁扣"咔哒"弹开、金光溢出，画面拉回全景 | `3,420.00 元` |

**这段视频真正的分量在第 4 镜**：它把"学生先判断、AI 只辅助、教师做终审"这条教学机制，用 4 秒画面讲完了。评委记住的会是这个，而不是全景旋转。

### 候选 B · 账本"数字孪生"（8–12 s，最省事）
账本翻页，纸上的手写行被"扫描"成规整表格，学生手算的 `11 元` 与系统 `11.00` 逐位对齐闪一下。适合放在第 3 步"人工算账"里。

### 候选 C · 信封展开成全息卡片（6–10 s）
牛皮纸信封拆开的瞬间，信纸内容"溢出"成立体全息卡，围绕桌子悬浮。视觉奇观强，教学含量低 → 只适合做开场 3 秒钩子。

### 候选 D · 争议单追踪（10 s）
红框从桌面账本一路追到右上角的教师台，形成"数据找人"的动线。适合做答辩互动时的回放素材。

> **不建议**：把视频贴成全景图里的一面"电视墙"随视角转动。4K 全景里插一段低分辨率视频，会因为清晰度落差立刻露出"贴图感"，反而掉分。

---

## 六、汇报话术：VR+AR 怎么说才不被问倒

### ✅ 推荐说法（每句都有代码兜底）

> "我们做了三层：**全景是 VR 层**，解决'在哪里'；**锚定叠加是 AR 层**，把数据流、AI 判断这些看不见的东西钉在桌面的实物上，随视角做透视贴合与缩放，属于 **marker-less 的固定空间锚定**；**短视频承载时间维度**，呈现动态过程。三者合起来，才让'实物—数字—AI 决策'这条链路在课堂里可看见、可操作。"

### ⚠️ 三个高危追问 + 标准答法

| 评委可能问 | 别这样答 | 这样答 |
|---|---|---|
| "这是真 AR 吗？用什么追踪？" | "是 AR"（一问就穿） | "我们没有用 SLAM/标记识别，而是在已知的 360° 场景坐标系（经度/纬度/视场角）里做固定锚点叠加。理由很实际：教室电脑、投影仪、断网环境都要一键可用，SLAM 反而飘。教学场景里稳定 > 炫技。" |
| "视频是 AI 生成的吧？和真实课堂什么关系？" | 含糊过去 | "视频只承担**看不见的过程**（数据流、判断），不替代真实。真实部分由 19 题检索测试报告、课堂记分原始表、三次课堂实录佐证。" |
| "为什么不直接 3D 建模？" | "太重了" | "成本与稳定性。AI 全景 + 锚定层改一版 40 分钟，3D 建模要两周且教室机器跑不动。我们要的是能复制到其他课程，不是一次性的展示品。" |

> 记住：**主动说清边界，比被追问出来可信十倍。**

---

## 七、工程与现场风险

| 风险 | 现象 | 处置 |
|---|---|---|
| **文件体积** | v37 已 13 MB（base64 全景），再塞视频 → 25 MB+，投影仪首屏卡 10 秒 | 视频**必须外链本地文件**，不进 base64；全景也抽成 `station_pano.png` 外链，可瘦身 90% |
| **自动播放** | Chrome 静音策略拦截带声视频 | 内嵌层用 `muted loop` 自动播；点击放大后才 `play()` 带声音 |
| **分辨率** | 4K 全景在 1080p 投影上重采样发糊 | 演示版准备 1920 宽全景，`image-rendering` 保持默认平滑 |
| **网络** | 现场 WiFi 不可靠 | 全部本地文件；视频码率 4–6 Mbps，20 s ≈ 10–14 MB 可接受 |
| **时间超支** | 一激动讲 3 分钟 | 页面上做一个 100 秒倒计时 HUD（按 `T` 切换），只你自己看得见 |

---

## 八、我现在就能替你做的 4 件事

1. **出一版 `v38`**：把 AR 锚定层 + 视频热点 + 全屏播放器写进代码（含视频加载失败自动回落 Canvas 版），可直接双击运行。
2. **出 4 张关键帧分镜图**：以你真实全景裁切图为参考图生成，作为视频模型（可灵/即梦/Veo）的 **image-to-video 种子图**，保证画面和你页面同源。
3. **出 20 秒中文旁白 + 字幕时间轴**（或纯字幕无人声版，现场你自己讲）。
4. **做一次瘦身**：base64 全景抽成外链 + 生成 1920 宽演示版，体积降到原来 1/10。

---

*方案基于 v37 源码实测：投影公式、热点坐标、FOV 区间（70–145）、语音片段时长（welcome 3.2s / letter 7.4s）均已核对。*
