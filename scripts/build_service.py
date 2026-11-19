"""Build situ-service static page from the service-description markdown.
usage: python -I build_service.py <md> <brand_source_dir> <out_public_dir>"""
import re, sys, html
md_path, src, out = sys.argv[1:4]
sys.path.insert(0, src)
import markdown
from base import C, logo, mark, TAGLINE, PROMISE, SUBLINE

text = open(md_path, encoding="utf8").read()
meta = re.search(r"版本：(.+)", text).group(1)
body_md = text.split("\n---\n", 1)[1]
foot_note = ""
if "\n---\n" in body_md:
    body_md, foot_note = body_md.rsplit("\n---\n", 1)
h = markdown.markdown(body_md, extensions=["tables"])
h = re.sub(r"【待确认([^】]*)】", lambda m: f'<span class="todo">待确认{html.escape(m.group(1))}</span>', h)
h = re.sub(r"(¥[\d,]+(?:/[月季年])?|\d+(?:[–-]\d+)? ?(?:分钟|天|个)|\d{1,2}:\d{2}–\d{1,2}:\d{2})", r'<span class="num">\1</span>', h)
h = h.replace("<td>无</td>", '<td class="muted">无</td>')
# wrap each h2 section into a card
parts = re.split(r"(?=<h2>)", h)
sec = []
for p in parts:
    if not p.strip():
        continue
    m = re.match(r"<h2>([一二三四五六七八九十]+)、(.+?)</h2>", p)
    if m:
        p = p.replace(m.group(0), f'<h2><span class="no">{m.group(1)}</span>{m.group(2)}</h2>', 1)
    sec.append(f'<section class="card">{p}</section>')
tiers = f"""<div class="tiers">
<div class="tier"><div class="tn">畅享版</div><div class="tp"><span class="num">¥999</span><small>/月</small></div>
<div class="tr">你的<b>高级助理</b></div><p>交代一件，办妥一件，拿来就用。</p>
<ul><li>远程客服 <span class="num">9:00–21:00</span>，<span class="num">3</span> 分钟内响应</li><li>免费试用 <span class="num">14</span> 天</li></ul>
<div class="fine">每月 500 个工作项 · 可同时进行 3 个</div></div>
<div class="tier hi"><span class="badge">主推</span><div class="tn">尊享版</div><div class="tp"><span class="num">¥1,999</span><small>/月</small></div>
<div class="tr">你的<b>特别助理</b></div><p>专人打磨，整件放手，一句办成。</p>
<ul><li>远程客服 <span class="num">9:00–21:00</span>，<span class="num">3</span> 分钟内响应</li><li>专属工作流程，<span class="num">0–1</span> 天交付</li></ul>
<div class="fine">每月 2,000 个工作项 · 可同时进行 5 个</div></div></div>"""
favicon = mark(64, "px").replace('"', "'")
import urllib.parse
fav = "data:image/svg+xml," + urllib.parse.quote(mark(64, "px"))
ink, org, mint, paper, slate, line = C["ink"], C["orange"], C["mint"], C["paper"], C["slate"], C["line"]
css = f"""
@font-face{{font-family:"Resource Han Rounded CN";font-weight:400;src:url(fonts/ResourceHanRoundedCN-Regular.woff2) format("woff2");font-display:swap}}
@font-face{{font-family:"Resource Han Rounded CN";font-weight:500;src:url(fonts/ResourceHanRoundedCN-Medium.woff2) format("woff2");font-display:swap}}
@font-face{{font-family:"Resource Han Rounded CN";font-weight:700;src:url(fonts/ResourceHanRoundedCN-Bold.woff2) format("woff2");font-display:swap}}
@font-face{{font-family:"Resource Han Rounded CN";font-weight:900;src:url(fonts/ResourceHanRoundedCN-Heavy.woff2) format("woff2");font-display:swap}}
@font-face{{font-family:Nunito;font-weight:200 1000;src:url(fonts/Nunito-VF.woff2) format("woff2");font-display:swap}}
*{{box-sizing:border-box}}
body{{margin:0;background:{paper};color:{ink};font-family:"Resource Han Rounded CN","Noto Sans CJK SC","PingFang SC",sans-serif;font-weight:400;line-height:1.8;font-size:16px}}
.num,.tp{{font-family:Nunito,"Resource Han Rounded CN",sans-serif;font-weight:800}}
.wrap{{max-width:960px;margin:0 auto;padding:0 20px}}
header{{padding:28px 0 8px}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:12px}}
.meta{{font-size:13px;color:{slate}}}
.hero{{padding:44px 0 28px}}
.hero h1{{font-size:44px;line-height:1.2;margin:0 0 10px;font-weight:900;letter-spacing:-.01em}}
.hero h1 em{{font-style:normal;color:{org}}}
.hero .lead{{font-size:20px;font-weight:700;margin:0 0 4px}}
.hero .sub{{color:{slate};margin:0}}
.tiers{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:26px 0 34px}}
.tier{{position:relative;background:#fff;border:1.5px solid {line};border-radius:18px;padding:24px 26px}}
.tier.hi{{border-color:{org}}}
.badge{{position:absolute;top:-12px;right:22px;background:{org};color:#fff;font-size:13px;font-weight:700;border-radius:999px;padding:2px 12px}}
.tn{{font-weight:700;font-size:18px}}
.tp{{font-size:38px;line-height:1.2;margin:6px 0}} .tp small{{font-size:15px;font-weight:600;color:{slate}}}
.tr{{font-size:18px;margin-bottom:4px}} .tr b{{color:{org}}}
.tier p{{margin:0 0 10px;color:{ink}}}
.tier ul{{margin:0 0 12px;padding-left:20px}}
.fine{{font-size:13px;color:{slate};border-top:1px solid {line};padding-top:10px}}
.card{{background:#fff;border-radius:18px;padding:26px 30px;margin-bottom:18px;border:1px solid {line}}}
.card h2{{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:700;margin:0 0 14px}}
.card h2 .no{{flex:none;width:34px;height:34px;border-radius:50%;background:#FFF1E6;color:{org};display:inline-flex;align-items:center;justify-content:center;font-size:15px}}
.card h3{{font-size:17px;margin:22px 0 6px}}
.card p{{margin:8px 0}} .card ul,.card ol{{padding-left:22px;margin:8px 0}} li{{margin:4px 0}}
.card strong{{font-weight:700}}
table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}}
th,td{{text-align:left;vertical-align:top;padding:11px 12px;border-bottom:1px solid {line}}}
th{{background:{paper};font-weight:700;white-space:nowrap}}
th:first-child,td:first-child{{width:26%;color:{slate}}}
td.muted{{color:{slate}}}
.tbl{{overflow-x:auto}}
.todo{{display:inline-block;font-size:12px;font-weight:700;color:{org};background:#FFF1E6;border-radius:6px;padding:0 7px;margin:0 3px;line-height:1.8}}
footer{{padding:20px 0 50px;color:{slate};font-size:13px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center}}
@media (max-width:700px){{.hero h1{{font-size:32px}}.tiers{{grid-template-columns:1fr}}.card{{padding:20px 18px}}th:first-child,td:first-child{{width:auto}}}}
@media print{{body{{background:#fff}}.card,.tier{{break-inside:avoid}}}}
"""
body = "".join(sec).replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
page = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>司徒 服务说明｜畅享版与尊享版</title><meta name="description" content="{TAGLINE}。{PROMISE}。">
<link rel="icon" href="{fav}"><style>{css}</style></head><body>
<header><div class="wrap top">{logo(9)}<span class="meta">服务说明 · {html.escape(meta)}</span></div></header>
<main class="wrap">
<div class="hero"><h1>你的事，<em>司徒</em>来办</h1><p class="lead">{PROMISE}</p><p class="sub">{SUBLINE}。两个版本，按你需要的助理来选。</p></div>
{tiers}
{body}
</main>
<footer class="wrap"><span>{mark(18,"px")}&nbsp; 司徒 Situ · {TAGLINE}</span><span>{html.escape(foot_note.strip())}</span></footer>
</body></html>"""
open(f"{out}/index.html", "w", encoding="utf8").write(page)
print("ok", len(page))
