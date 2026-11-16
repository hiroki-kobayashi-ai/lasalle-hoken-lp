import re
src = open('/tmp/orig.html', encoding='utf8').read()
head_css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
body = src[src.find('<body>'):]
def cut(a, b):
    i = body.find(a); j = body.find(b, i + 1)
    assert i > -1 and j > -1, (a, b)
    return body[i:j]
SC = cut('<section class="info sc" id="selfcheck"', '<section class="info tr"')
TR = cut('<section class="info tr"', '<section class="info" aria-label="数字で見る介護">')
NUM = cut('<section class="info" aria-label="数字で見る介護">', '<section class="info" aria-label="公的介護保険だけでは足りないところ">')
PUB = cut('<section class="info" aria-label="公的介護保険だけでは足りないところ">', '<section class="info" aria-label="認知症保険を選ぶときに見る5つのポイント">')
PTS = cut('<section class="info" aria-label="認知症保険を選ぶときに見る5つのポイント">', '<section class="info gan"')
GAN = cut('<section class="info gan"', '<section class="info faq"')
FAQ = cut('<section class="info faq"', '<section class="contact-options"')
LEGAL = cut('<section class="legal-intro"', '<footer>')
FOOT = body[body.find('<footer>'):body.find('</footer>') + 9]
scripts = re.findall(r'<script>.*?</script>', body, re.S)
SC_JS = [s for s in scripts if 'sc-go' in s][0]
EV_JS = [s for s in scripts if 'data-ev' in s][0]
# がんセクションからボタン（第一ネオ・LINE）を除き、図と表だけ使う
GAN_INFO = re.sub(r'<a class="banner[^>]*>.*?</a>', '', GAN, flags=re.S)
GAN_INFO = GAN_INFO.replace('<h2>がんへの備えも、あわせて</h2>', '<h2>がんは身近な病気です</h2>').replace(' id="gan"', '')
# 認知症のセルフチェック結果の下にある LINE ボタンはそのまま残す

NEO_N = 'https://neofirst.co.jp/sim/simulation?sid=agent=6155300000&amp;branch=0000&amp;index=0000&amp;type=014014'
NEO_G = 'https://neofirst.co.jp/sim/simulation?sid=agent=6155300000&amp;branch=0000&amp;index=0000&amp;type=014015'
NEO_ALL = 'https://neofirst.co.jp/ent2/?param=6155300000'
NEO_K = 'https://neofirst.co.jp/sim/simulation?sid=agent=6155300000&amp;branch=0000&amp;index=0000&amp;type=014002'
LINE = 'https://lin.ee/5gJWVqG'
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSccRHCt5AheXYdAuCldzdOeVagka3Cl97rLjJFDbVRP67sg_A/viewform'
TEL = 'tel:05036964531'

CSS = r'''
body{font-size:20px;background:#f5f6f3}
.top{position:sticky;top:0;z-index:60;margin:0 -16px;padding:8px 10px 10px;background:#ffffffee;backdrop-filter:blur(6px);border-bottom:1px solid #e3e7e2}
.brand{display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#4f5c57;margin:0 2px 6px}
.brand b{display:block;color:#1f5c4a;font-size:19px;letter-spacing:.02em}
.brand a{font-weight:700;color:#1f5c4a;text-decoration:none;font-size:15px}
.tabs6{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}
.tabs6 a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;min-height:46px;padding:3px 1px;border-radius:12px;background:#f1f4f0;color:#18221f;text-decoration:none;font-size:14px;font-weight:700;line-height:1.2;text-align:center;border:2px solid transparent}
.tabs6 a .ic{font-size:18px;line-height:1}
.tabs6.closed{display:none}
.tabtg{display:block;width:100%;margin:6px 0 0;padding:9px;border:0;border-radius:12px;background:#1f5c4a;color:#fff;font-size:16px;font-weight:800;font-family:inherit;cursor:pointer}
.tabtg.open{background:#f1f4f0;color:#1f5c4a;border:2px solid #1f5c4a}
.tabs6 a.wide{grid-column:1/-1;flex-direction:row;gap:8px;min-height:40px;background:#eaf3ef;border-color:#1f5c4a;color:#1f5c4a}
.tabs6 a.wide .ic{font-size:20px}
.tabs6 a.wide[aria-current="page"]{background:#1f5c4a;color:#fff}
.deskband{display:flex;align-items:center;gap:10px;background:#eaf3ef;border:2px solid #1f5c4a;border-radius:16px;padding:12px 14px;margin:8px 0 16px;color:#18221f;text-decoration:none;line-height:1.6}
.deskband b{color:#1f5c4a}.deskband .ar{margin-left:auto;font-weight:800;color:#1f5c4a;white-space:nowrap}
.telrow{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 12px;margin:0 0 6px;border:2px solid #d6ded9;border-radius:12px;text-decoration:none;color:#18221f;background:#fff}.telrow span{display:flex;flex-direction:column;line-height:1.35}.telrow small{font-size:13px;color:#4f5c57}.telrow em{font-style:normal;font-weight:800;color:#1f5c4a;white-space:nowrap;font-size:16px}
.tkband{display:block;margin:10px 0 12px;padding:10px 12px;border-radius:12px;background:#fff6ec;border:2px solid #d9822b;color:#18221f;text-decoration:none;font-size:15px;line-height:1.5}.tkband span{font-weight:800;color:#b5651d;white-space:nowrap}
.o70 h2{font-size:24px}.o70lead{font-weight:700;margin:0 0 10px}.o70stats{display:grid;grid-template-columns:1fr;gap:8px;margin:8px 0 14px}.o70stats div{background:#fff6ec;border:2px solid #d9822b;border-radius:14px;padding:10px 12px;line-height:1.5}.o70stats b{display:block;font-size:30px;color:#b5651d;line-height:1.2}.o70stats span{display:block;font-weight:700}.o70stats i{display:block;font-style:normal;font-size:14px;color:#4f5c57}.talk{margin:6px 0 10px}.tk{display:flex;align-items:flex-end;gap:8px;margin:8px 0}.tk.r{justify-content:flex-end}.tk .av{font-size:34px;line-height:1}.tk p{margin:0;padding:10px 14px;border-radius:18px;background:#eaf3ef;max-width:78%;line-height:1.6;position:relative}.tk.r p{background:#fdf0e1}.o70why{margin:6px 0 10px;padding-left:1.2em;line-height:1.7}.o70why li{margin:4px 0}.o70now{text-align:center;font-size:21px;line-height:1.6;margin:12px 0 8px}.o70now b{color:#b5651d;font-size:24px}.o70who{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}.o70who a{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:64px;border-radius:14px;background:#1f5c4a;color:#fff;font-weight:800;font-size:15px;line-height:1.35;text-decoration:none;padding:6px}.o70who small{font-size:12px;font-weight:400}.ng-bg{position:fixed;inset:0;background:#18221f99;z-index:10000;display:flex;align-items:flex-end;justify-content:center}.ng{background:#fff;max-width:640px;width:100%;max-height:92vh;overflow:auto;border-radius:18px 18px 0 0;padding:18px 16px 22px;position:relative;line-height:1.65}.ng h3{font-size:22px;margin:0 36px 6px 0}.ng .ngkey{background:#fff6ec;border:2px solid #d9822b;border-radius:12px;padding:8px 12px;font-weight:700;margin:6px 0 10px}.ng ol{padding-left:1.3em;margin:6px 0}.ng li{margin:6px 0}.ng .pos{display:inline-block;background:#1f5c4a;color:#fff;border-radius:8px;padding:0 8px;font-weight:800}.ng .ngx{position:absolute;top:8px;right:8px;width:44px;height:44px;border:0;background:none;font-size:28px;cursor:pointer;color:#4f5c57}.ng .nglist{margin:4px 0 6px;padding-left:1.4em}.ng .nglist li{margin:2px 0}.ng a.nggo{display:flex;justify-content:center;align-items:center;min-height:58px;border-radius:14px;background:#d9822b;color:#fff;font-size:20px;font-weight:800;text-decoration:none;margin:12px 0 6px}.ng a.ngline{display:flex;justify-content:center;align-items:center;min-height:50px;border-radius:14px;background:#06c755;color:#fff;font-size:18px;font-weight:700;text-decoration:none}.neopos{display:block;font-size:13px;font-weight:700;opacity:.95;margin-top:2px}
.top:has(#tabs-nav:not(.closed)){position:relative}
.desk3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:10px 0}.desk3 div{background:#f1f4f0;border-radius:14px;padding:10px 6px;text-align:center;line-height:1.4}.desk3 b{display:block;font-size:19px;color:#1f5c4a}.desk3 span{font-size:13px;color:#4f5c57}
.tabs6 a[aria-current="page"],.tabs6 a.small[aria-current="page"]{background:#1f5c4a;color:#fff}
.tabs6 a.small{font-size:14px;color:#4f5c57}
.tabs6 a.hot{position:relative;border-color:#d9822b;background:#fff6ec}
.tabs6 a.hot[aria-current="page"]{background:#1f5c4a;border-color:#d9822b}
.tabs6 a .badge{position:absolute;top:-8px;right:-2px;background:#d9482b;color:#fff;font-style:normal;font-size:11px;font-weight:800;padding:1px 6px;border-radius:9px;line-height:1.5}
.toc ol{margin:6px 0 0;padding-left:1.4em;line-height:2}.toc a{color:#1f5c4a;font-weight:700}
.ch{font-size:19px;margin:16px 2px 6px;color:#1f5c4a}
.cmp td{padding:6px 2px;border-bottom:1px solid #e3e9e6}
.calc .row{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:8px 0;font-size:16px}
.calc .row input,.calc .row select{width:9.5em;font-size:18px;padding:8px;border:1px solid #c9d3cf;border-radius:10px;text-align:right}
.calc .row select{text-align:left}
.calc .res{background:#f1f4f0;border-radius:14px;padding:12px;margin-top:10px;font-size:16px;line-height:1.7}
.calc .res b{font-size:22px;color:#1f5c4a}
.story{border-left:4px solid #d9822b;padding:2px 0 2px 12px;margin:10px 0;line-height:1.8}
.story p{margin:6px 0}
.kv{margin:0;padding:0;list-style:none}.kv li{padding:10px 0;border-bottom:1px solid #e3e9e6;line-height:1.7}.kv li b{display:block;color:#1f5c4a;font-size:17px}
.view{display:none;padding-top:14px;animation:slide .35s ease}
.view.on{display:block}
@keyframes slide{from{opacity:0;transform:translateX(24px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.view{animation:none}}
.lead{text-align:center;margin:6px 0 16px}
.lead .kicker{display:inline-block;font-size:15px;font-weight:700;color:#9a5a12;background:#fbeedd;border-radius:999px;padding:3px 14px;margin-bottom:8px}
.lead h1{font-family:"BIZ UDPGothic","Hiragino Sans",sans-serif;font-size:clamp(26px,7vw,34px);line-height:1.4;margin:0 0 6px;font-weight:800}
.lead p{margin:0;color:#4f5c57;font-size:18px}
.big3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 6px}
.big3 div{background:#fff;border-radius:18px;padding:14px 4px;text-align:center;box-shadow:0 2px 10px #18221f12}
.big3 b{display:block;font-size:clamp(21px,6vw,28px);color:#1f5c4a;line-height:1.2}
.big3 span{display:block;font-size:14px;line-height:1.4;margin-top:4px}
.srcs{font-size:13px;color:#6b7772;text-align:center;margin:4px 0 18px}
.box{background:#fff;border-radius:22px;padding:18px 16px;margin:0 0 16px;box-shadow:0 2px 14px #18221f14}
.box h2{font-size:23px;line-height:1.45;margin:0 0 10px;color:#18221f}
.box p{margin:0 0 10px}
.cta{display:block;text-decoration:none;text-align:center;border-radius:18px;padding:16px 12px;margin:12px 0 6px;font-weight:800;font-size:22px;line-height:1.4;background:#1f5c4a;color:#fff;box-shadow:0 5px 0 #123a2f}
.cta small{display:block;font-size:15px;font-weight:400;opacity:.92;margin-top:2px}
button.cta{color:#fff;width:100%}.cta:active{transform:translateY(4px);box-shadow:0 1px 0 #123a2f}
.cta.sub{background:#fff;color:#1f5c4a;border:2px solid #1f5c4a;box-shadow:0 5px 0 #1f5c4a33}
.cta.line{background:#06c755;box-shadow:0 5px 0 #04913d}
.cta.amber{background:#9a5a12;box-shadow:0 5px 0 #6b3d0b}
.who{display:inline-block;background:#e3f1ea;color:#1f5c4a;border-radius:999px;padding:2px 12px;font-size:16px;font-weight:800;margin-bottom:4px}
.cta .who{background:#ffffff26;color:#fff}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:8px 0 10px}
.steps3 div{background:#f1f4f0;border-radius:16px;padding:12px 4px;text-align:center;font-size:16px;line-height:1.4;position:relative}
.steps3 div b{display:block;font-size:28px;line-height:1.2}
.steps3 div i{font-style:normal;display:block;font-size:13px;color:#1f5c4a;font-weight:800}
.need{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.need div{border:2px dashed #c9d3cd;border-radius:14px;padding:10px 6px;text-align:center;font-size:16px;line-height:1.4}
.need div b{display:block;font-size:26px}
.time{text-align:center;font-weight:800;font-size:20px;margin:6px 0 2px}
.time em{font-style:normal;color:#9a5a12;font-size:26px}
.note{font-size:15px;color:#4f5c57;line-height:1.6}
details.more{background:#fff;border-radius:18px;margin:0 0 10px;box-shadow:0 2px 10px #18221f10}
details.more>summary{list-style:none;cursor:pointer;padding:16px 46px 16px 16px;font-weight:800;font-size:19px;position:relative;line-height:1.45}
details.more>summary::-webkit-details-marker{display:none}
details.more>summary:after{content:"＋";position:absolute;right:16px;top:14px;font-size:24px;color:#1f5c4a}
details.more[open]>summary:after{content:"－"}
details.more>.in{padding:0 12px 12px}
details.more .info{margin:0;border:0;padding:4px}
ol.flow8{margin:4px 0 0;padding:0;list-style:none;counter-reset:s}
ol.flow8 li{counter-increment:s;position:relative;padding:7px 0 7px 38px;border-top:1px dashed #dfe5e1;font-size:18px;line-height:1.5}
ol.flow8 li:first-child{border-top:0}
ol.flow8 li:before{content:counter(s);position:absolute;left:0;top:8px;width:28px;height:28px;border-radius:50%;background:#1f5c4a;color:#fff;text-align:center;line-height:28px;font-weight:700;font-size:15px}
.go-tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:6px 0 16px}
.go-tiles a{display:block;background:#fff;border-radius:18px;padding:14px 10px;text-decoration:none;text-align:center;box-shadow:0 2px 10px #18221f14;font-weight:800;font-size:17px;line-height:1.4}
.go-tiles a span{display:block;font-size:30px}
.go-tiles a small{display:block;font-weight:400;font-size:14px;color:#4f5c57}
.q{margin:0 0 16px}
.q .qt{font-weight:800;font-size:20px;margin:0 0 8px;line-height:1.45}
.q .qt i{font-style:normal;display:inline-block;background:#1f5c4a;color:#fff;border-radius:8px;padding:0 8px;margin-right:6px;font-size:16px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips label{display:flex;align-items:center;gap:6px;border:2px solid #d6ded9;border-radius:999px;padding:10px 14px;background:#fff;font-size:18px;cursor:pointer;line-height:1.3}
.chips input{width:20px;height:20px;accent-color:#1f5c4a}
.chips label:has(input:checked){border-color:#1f5c4a;background:#e3f1ea;font-weight:800}
.q select,.q input[type=text]{width:100%;font-size:19px;padding:12px;border:2px solid #d6ded9;border-radius:14px;background:#fff}
.res2{display:none;background:#fff7e8;border:2px solid #9a5a12;border-radius:18px;padding:14px;margin-top:12px}
.res2.show{display:block;animation:slide .35s ease}
.res2 h3{margin:0 0 8px;font-size:21px;color:#7a430a}
.res2 ul{margin:0 0 8px;padding-left:1.2em}
.res2 li{margin-bottom:4px}
.topics{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.topics a{display:flex;align-items:center;gap:8px;background:#f1f4f0;border-radius:14px;padding:12px 10px;text-decoration:none;font-weight:700;font-size:17px;line-height:1.35}
.topics a span{font-size:26px}
.callrow{text-align:center;margin:8px 0 0;font-size:17px}
.callrow a{display:inline-block;font-size:26px;font-weight:800;color:#1f5c4a;min-height:48px}
.pill-steps{display:flex;flex-direction:column;gap:8px;margin:8px 0}
.pill-steps div{display:flex;gap:10px;align-items:center;background:#f1f4f0;border-radius:16px;padding:10px 12px;font-size:18px;line-height:1.45}
.pill-steps div b{flex:0 0 auto;width:34px;height:34px;border-radius:50%;background:#9a5a12;color:#fff;display:flex;align-items:center;justify-content:center}
.src-hero{border-radius:22px;overflow:hidden;background:#fff;margin:0 0 14px;box-shadow:0 2px 14px #18221f14}.src-hero img{display:block;width:100%;height:auto}.src-hero p{margin:0;padding:14px 16px;font-size:23px;font-weight:800;line-height:1.5;text-align:center}.src-hero p small{display:block;font-size:17px;font-weight:400;color:#4f5c57;margin-top:4px}.src-hero.dark{background:#1d2623;color:#fff}.src-hero.dark p{padding:30px 18px}.src-hero.dark p span{display:block;font-size:44px}.src-hero.dark small{color:#cfd8d3}.keep{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.keep a{display:flex;align-items:center;justify-content:center;text-align:center;min-height:56px;border-radius:14px;font-weight:800;font-size:16px;line-height:1.35;text-decoration:none;padding:6px}.keep .k-line{background:#06c755;color:#fff}.keep .k-fam{background:#fff;border:2px solid #1f5c4a;color:#1f5c4a}
.hf textarea{width:100%;font-size:18px;padding:11px;border:2px solid #d6ded9;border-radius:12px;font-family:inherit;resize:vertical}.fp{margin:10px 0 0;font-size:15px;line-height:1.6;color:#4f5c57}.fp a{color:#1f5c4a;font-weight:700}.brand .telbtn{display:flex;flex-direction:column;align-items:flex-end;line-height:1.2;font-weight:800;color:#1f5c4a;text-decoration:none}.brand .telbtn small{font-size:12px;font-weight:400;color:#4f5c57}.brand .telbtn span{font-size:16px;white-space:nowrap}.brand{align-items:flex-start}.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 16px}.pair a{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:72px;border-radius:16px;font-weight:800;font-size:17px;line-height:1.35;text-decoration:none;padding:8px 6px}.pair a small{font-size:13px;font-weight:400;margin-top:2px}.pair .p1{background:#1f5c4a;color:#fff;box-shadow:0 4px 0 #123a2f}.pair .p2{background:#fff;color:#1f5c4a;border:2px solid #1f5c4a}.kokuchi{background:#f1f4f0;border-radius:14px;padding:12px;margin:8px 0}.kokuchi li{margin:0 0 8px;line-height:1.6}.complist h3{font-size:19px;margin:12px 0 6px}.complist ul{margin:0;padding-left:1.2em;line-height:1.9}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#18221f;color:#fff;padding:12px 18px;border-radius:999px;font-size:17px;z-index:99;display:none}
.toast.show{display:block}
'''

TOP = f'''<div class="top"><div class="brand"><span><b>ラサール＆パートナーズ</b>（保険代理店）</span><a class="telbtn" href="{TEL}" data-ev="tel_top"><small>☎ 電話で相談</small><span>050-3696-4531</span></a></div>
<nav class="tabs6" id="tabs-nav" aria-label="ページの切り替え">
<a href="#ninchi" data-v="ninchi"><span class="ic">🌿</span>認知症の<br>備え</a>
<a href="#gan" data-v="gan"><span class="ic">🎗️</span>がんの<br>備え</a>
<a href="#jibyo" data-v="jibyo"><span class="ic">💊</span>持病が<br>ある方</a>
<a href="#over70" data-v="over70"><span class="ic">🌸</span>70歳<br>以上の方</a>
<a href="#sonpo" data-v="sonpo"><span class="ic">🚗</span>車・家の<br>保険</a>
<a href="#souzoku" data-v="souzoku" class="hot"><em class="badge">相談多数</em><span class="ic">🏠</span>相続の<br>備え</a>
<a href="#soudan" data-v="soudan"><span class="ic">💬</span>保険の<br>相談</a>
<a href="#oya" data-v="oya"><span class="ic">👪</span>親御さんの<br>保険</a>
<a href="#oyanaki" data-v="oyanaki"><span class="ic">🤲</span>障がいと<br>親なきあと</a>
<a href="#desk" data-v="desk" class="wide"><span class="ic">🛡️</span>ご契約後の安心｜ラサール クライアントデスク</a>
</nav><button type="button" class="tabtg" id="tabtg" aria-controls="tabs-nav" aria-expanded="true">▲ メニューをたたんで、下へ読み進める</button></div>'''

GO_TILES = '''<div class="go-tiles">
<a href="#over70" data-v="over70"><span>🌸</span>70歳以上の方<small>お一人ずつお調べします</small></a>
<a href="#soudan" data-v="soudan"><span>💬</span>相談して決めたい<small>どんな保険でもOK</small></a>
<a href="#gan" data-v="gan"><span>🎗️</span>がんの備え<small>治療の種類で選ぶ</small></a>
<a href="#jibyo" data-v="jibyo"><span>💊</span>持病がある方<small>入りやすい保険</small></a>
</div>'''

FLOW_CARD = f'''<section class="box" id="flow-n"><h2>ボタンを押すと、こうなります</h2>
<div class="steps3"><div><i>STEP1</i><b>🧮</b>保険料の<br>試算</div><div><i>STEP2</i><b>✍️</b>入力と<br>健康の質問</div><div><i>STEP3</i><b>💳</b>カード<br>登録で完了</div></div>
<p class="time">かかる時間は <em>約15分</em></p>
<p class="note" style="text-align:center">STEP1の試算だけなら、申込みにはなりません。</p>
<div class="need"><div><b>💳</b>ご本人名義の<br>クレジットカード</div><div><b>🪪</b>運転免許証など<br><span class="note">（あとで写真で送ります）</span></div></div>
<details class="more" style="box-shadow:none;background:#f7f9f6"><summary>くわしい8つの手順を見る</summary><div class="in"><ol class="flow8">
<li>保険料の試算</li><li>申込み前の確認事項を読む</li><li>ご本人の情報（お名前・ご住所など）を入力</li><li>受取人を入力</li><li>健康状態の質問（告知）に答える</li><li>入力内容の確認</li><li>クレジットカードの登録</li><li>控え（PDF）を保存して完了<br><span class="note">後日、メールの案内にそって本人確認書類を写真で送ります。</span></li></ol>
<p class="note">ネットでお申込みできるのは、ご契約者・保険をかける方・カードの名義が同じご本人の場合です。</p></div></details>
<a class="cta js-neo" data-ev="neo_ninchisho" id="banner-ninchisho-flow" href="{NEO_N}" target="_blank" rel="noopener noreferrer"><span class="who">40〜69歳のご本人</span><br>保険料を見てみる<small>第一ネオ生命（第一生命グループ）の画面へ</small></a>
<a class="cta line" data-ev="line_flow" href="{LINE}" target="_blank" rel="noopener noreferrer">途中で迷ったらLINEで聞く</a></section>'''

SONPO_CSS = r'''
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;background:#e9eee9;border-radius:16px;padding:5px;margin:0 0 14px}
.seg button{border:0;border-radius:12px;background:transparent;padding:10px 2px;font:inherit;font-size:17px;font-weight:800;color:#4f5c57;cursor:pointer;line-height:1.3}
.seg button span{display:block;font-size:24px}
.seg button[aria-selected="true"]{background:#fff;color:#1f5c4a;box-shadow:0 2px 8px #18221f1f}
.sub{display:none}.sub.on{display:block;animation:slide .3s ease}.cta.sub{display:block}.sub2{display:none}.sub2.on{display:block;animation:slide .3s ease}
.bring{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:6px 0}
.bring div{background:#f1f4f0;border-radius:14px;padding:10px 6px;text-align:center;font-size:16px;line-height:1.4}
.bring div b{display:block;font-size:26px}
'''
CSS = CSS + SONPO_CSS
HEAR_CSS = r"""
.hear h2 small{display:block;font-size:15px;font-weight:400;color:#4f5c57;margin-top:2px}
.hf{margin:0 0 14px}.hf .ql{font-weight:800;font-size:18px;margin:0 0 6px;line-height:1.45}
.hf .ql i{font-style:normal;font-size:13px;font-weight:700;color:#9a5a12;margin-left:6px}
.hf select,.hf input[type=text]{width:100%;font-size:18px;padding:11px;border:2px solid #d6ded9;border-radius:12px;background:#fff;font-family:inherit}
.hf .chips label{padding:9px 12px;font-size:17px}
.sendrow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px}
.sendrow button{border:0;border-radius:14px;min-height:60px;font:inherit;font-size:18px;font-weight:800;cursor:pointer;line-height:1.3}
.sendrow .s-line{background:#06c755;color:#fff}.sendrow .s-form{background:#fff;color:#1f5c4a;border:2px solid #1f5c4a}
.house-sub{display:none}.house-sub.on{display:block}
"""
CSS = CSS + HEAR_CSS
def opts(name, items, multi=False, other=False):
    typ = "checkbox" if multi else "radio"
    return '<div class="chips">' + ''.join(f'<label><input type="{typ}" name="{name}" value="{x}">{x}</label>' for x in items) + '</div>'
def sel(name, items):
    return f'<select name="{name}"><option value="">えらんでください</option>' + ''.join(f'<option>{x}</option>' for x in items) + '</select>'
def q(label, body, note=""):
    return f'<div class="hf"><p class="ql">{label}{("<i>"+note+"</i>") if note else ""}</p>{body}</div>'
COMMENT = '<div class="hf"><p class="ql">ご質問・ご要望など（自由にどうぞ）</p><textarea name="comment" rows="3" placeholder="例：今の保険料が高いので見直したい／平日の夜に電話がほしい"></textarea></div>'
FPLINE = '<p class="fp">📜 国家資格（FP技能士）をもつファイナンシャルプランナーが担当します。当社は複数の保険会社を扱う乗合代理店です。<a href="#companies" data-v="companies">取扱保険会社一覧 ›</a></p>'
YEARS=[f"{y}年" for y in range(2026,2004,-1)]+["2004年より前"]
CAR_FORM = ('<section class="box hear" id="hear-car" data-title="自動車保険のお見積り依頼"><h2>かんたん見積もりメモ（約2分）<small>わかるところだけでOK。お名前・ご住所は、ここでは入れません。保険証券（または満期案内）と車検証があると、そのまま写せます。</small></h2>'
 + '<p class="ql" style="margin:4px 0 8px;color:#1f5c4a">① お車を主に使用される方</p>'
 + q("年齢", opts("記名被保険者の年齢",["20歳以下","21〜25歳","26〜29歳","30代","40代","50代","60代","70歳以上"]))
 + q("運転免許証の色", opts("免許証の色",["ゴールド","ブルー","グリーン"]))
 + '<p class="ql" style="margin:4px 0 8px;color:#1f5c4a">② 運転される方</p>'
 + q("運転される方の範囲", opts("運転者の範囲",["本人のみ","本人・配偶者","家族","限定なし"]))
 + q("運転される方のうち、いちばん若い方の年齢", opts("運転者年齢条件",["20歳以下","21〜25歳","26〜34歳","35歳以上"]))
 + '<p class="ql" style="margin:4px 0 8px;color:#1f5c4a">③ お車と使い方</p>'
 + q("メーカー・車名", '<input type="text" name="車名" placeholder="例：トヨタ プリウス">', "車検証")
 + q("初度登録年月（年式）", sel("初度登録",YEARS+["わからない"]), "車検証")
 + q("型式（わかれば）", '<input type="text" name="型式" placeholder="例：6AA-MXWH60">', "車検証")
 + q("使用目的", opts("使用目的",["日常・レジャー","通勤・通学","業務"]))
 + q("年間走行距離（これから1年の予想）", opts("年間走行距離",["3,000km以下","5,000km以下","10,000km以下","15,000km以下","15,000km超","わからない"]))
 + q("累計走行距離（メーターの数字）", '<input type="text" name="累計走行距離" placeholder="例：45,000km（わからなければ空でOK）">')
 + '<p class="ql" style="margin:4px 0 8px;color:#1f5c4a">④ 今のご契約</p>'
 + q("今の自動車保険", opts("現在の契約",["他社で契約中","はじめて契約する（新車・中古車）","わからない"]))
 + q("ノンフリート等級", sel("等級",[f"{i}等級" for i in range(1,21)]+["わからない"]), "保険証券")
 + q("事故有係数適用期間", sel("事故有係数適用期間",[f"{i}年" for i in range(0,7)]+["わからない"]), "保険証券")
 + q("この1年の事故（保険を使った事故）", opts("前年の事故",["なし","1件","2件以上"]))
 + q("満期日（はじめての方は納車日）", '<input type="text" name="満期日" placeholder="例：2027年1月15日">')
 + '<p class="ql" style="margin:4px 0 8px;color:#1f5c4a">⑤ ご希望</p>'
 + q("車両保険（ご自分の車の修理代）", opts("車両保険",["付けたい","付けない","相談したい"]))
 + q("今と同じ補償でよい？", opts("補償の希望",["今と同じでよい","見直したい","おまかせ"]))
 + COMMENT + q("ご連絡の方法", opts("連絡方法",["LINE","電話","メール","テレビ電話"]))
 + '<div class="sendrow"><button type="button" class="s-line" data-send="hear-car">LINEで送る</button><button type="button" class="s-form" data-sendform="hear-car">フォームで送る</button></div>'
 + '<p class="note">「フォームで送る」は<b>Googleフォーム</b>が開きます（答えは入った状態）。LINEは送信を押すだけ。保険証券や車検証の写真は、お申込みの前にメールかフォームで送ってください（個人の情報は隠してOK）。</p></section>')
FIRE_FORM = ('<section class="box hear" id="hear-fire" data-title="火災保険のお見積り依頼"><h2>かんたん見積もりメモ（約2分）<small>わかるところだけでOK。お名前・ご住所は、ここでは入れません。</small></h2>'
 + q("お住まい", '<div class="chips" id="house-type">' + ''.join(f'<label><input type="radio" name="住まい" value="{x}">{x}</label>' for x in ["賃貸（アパート・マンション）","持ち家（一戸建て）","持ち家（マンション）"]) + '</div>')
 + '<div class="house-sub" id="hs-rent">'
 + q("借家人賠償責任の保険金額（大家さんへの賠償）", sel("借家人賠償",["1,000万円","2,000万円","3,000万円","指定はない","わからない"]), "賃貸の契約書・重要事項説明書")
 + q("世帯人数", opts("世帯人数",["1人","2人","3人","4人以上"]))
 + q("家財の保険金額（家具・家電・服など）", opts("家財の保険金額",["100万円","200万円","300万円","500万円","おまかせ"]))
 + q("個人賠償責任（自転車事故など）を、ほかの保険で付けている？", opts("個人賠償責任",["付けている","付けていない","わからない"]))
 + q("保険期間", opts("保険期間",["1年","2年","賃貸契約に合わせたい"]))
 + '</div><div class="house-sub" id="hs-own">'
 + q("建築年月", sel("建築年",[f"{y}年" for y in range(2026,1979,-1)]+["1980年より前","わからない"]))
 + q("延床面積（だいたいでOK）", '<input type="text" name="延床面積" placeholder="例：100㎡ ／ 30坪">', "登記簿・パンフレット")
 + q("建物の保険金額（わかれば）／購入・建築のときの価格", '<input type="text" name="建物の評価" placeholder="例：2,000万円（わからなければ空でOK）">')
 + q("家財の補償", opts("家財",["付けたい","付けない","相談したい"]))
 + q("地震保険", opts("地震保険",["付けたい","付けない","相談したい"]))
 + q("水災（大雨・洪水）の補償", opts("水災",["付けたい","付けない","相談したい"]))
 + q("今の火災保険の満期（入っている方）", '<input type="text" name="満期" placeholder="例：2027年3月">')
 + '</div>'
 + q("建物の構造", opts("建物の構造",["木造","鉄骨造","鉄筋コンクリート造","わからない"]), "マンションはたいてい鉄筋コンクリート造")
 + q("所在地（都道府県・市区町村まで）", '<input type="text" name="所在地" placeholder="例：北海道札幌市中央区">')
 + q("専有面積（マンション・アパートの方）", '<input type="text" name="面積" placeholder="例：30㎡（わからなければ空でOK）">')
 + q("補償を始めたい日（入居日など）", '<input type="text" name="開始日" placeholder="例：12月1日">')
 + COMMENT + q("ご連絡の方法", opts("連絡方法",["LINE","電話","メール","テレビ電話"]))
 + '<div class="sendrow"><button type="button" class="s-line" data-send="hear-fire">LINEで送る</button><button type="button" class="s-form" data-sendform="hear-fire">フォームで送る</button></div>'
 + '<p class="note">「フォームで送る」は<b>Googleフォーム</b>が開きます（答えは入った状態）。LINEは送信を押すだけ。</p></section>')


# ===== 追加：返事の目安・各種見積もりメモ・知らないと損・証券診断 =====
REPLY = '<p class="reply">⏱ 受付から遅くとも<b>翌々日まで</b>に、お見積もりをお返事します。</p>'
MAIL = 'info@lasalle2023.com'
def hear(id_, title, cat, body, extra_note=""):
    return (f'<section class="box hear" id="{id_}" data-title="{title}" data-cat="{cat}"><h2>かんたん見積もりメモ<small>わかるところだけでOK。お名前・ご住所は、ここでは入れません。</small></h2>'
            + body + COMMENT + q("ご連絡の方法", opts("連絡方法", ["LINE", "電話", "メール", "テレビ電話"]))
            + f'<div class="sendrow"><button type="button" class="s-line" data-send="{id_}">LINEで送る</button><button type="button" class="s-form" data-sendform="{id_}">フォームで送る</button></div>'
            + '<p class="note">「LINEで送る」はLINEが開くので送信を押すだけ。「フォームで送る」は<b>Googleフォーム</b>（お名前・ご連絡先を入れる画面）が開き、答えは入った状態です。' + extra_note + '</p>' + REPLY + FPLINE + '</section>')
def tips(title, items, src):
    lis = ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in items)
    return f'<section class="box tips"><h2>💡 {title}</h2><ol>{lis}</ol><p class="src2">{src}</p></section>'
MASK = ('<div class="mask"><b>📸 写真を送るときは、ここを隠してください</b>'
        '<div class="mask-grid"><span>お名前</span><span>ご住所</span><span>電話番号</span><span>生年月日の月日</span><span>証券番号</span><span>車台番号</span></div>'
        '<p class="note">付箋や指でかくして撮ればOK。保険会社名・補償の中身・保険料・満期日・等級は見えるままにしてください。</p></div>')
SEND_PHOTO = (MASK + '<div class="sendrow" style="grid-template-columns:1fr">'
              f'<a class="s-mail" data-ev="photo_mail" href="mailto:{MAIL}?subject=%E4%BF%9D%E9%99%BA%E8%A8%BC%E5%88%B8%E3%81%AE%E5%86%99%E7%9C%9F%EF%BC%88%E8%A8%BA%E6%96%AD%E3%83%BB%E3%81%8A%E7%94%B3%E8%BE%BC%E3%81%BF%EF%BC%89&body=%E5%86%99%E7%9C%9F%E3%82%92%E6%B7%BB%E4%BB%98%E3%81%97%E3%81%BE%E3%81%99%E3%80%82%EF%BC%88%E5%80%8B%E4%BA%BA%E6%83%85%E5%A0%B1%E3%81%AF%E9%9A%A0%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%EF%BC%89%0A%E3%81%94%E9%80%A3%E7%B5%A1%E5%85%88%EF%BC%9A">✉️ メールで写真を送る</a>'
                            f'<p class="note">メールのあて先：{MAIL}（ラサール＆パートナーズ）</p>')

MORE_CSS = r"""
.reply{margin:10px 0 0;padding:10px 12px;background:#e3f1ea;border-radius:12px;font-size:17px;line-height:1.5;color:#1f5c4a}
.tips ol{margin:0;padding:0;list-style:none;counter-reset:t}
.tips li{counter-increment:t;position:relative;padding:10px 0 10px 40px;border-top:1px dashed #dfe5e1;line-height:1.65;font-size:18px}
.tips li:first-child{border-top:0}
.tips li:before{content:counter(t);position:absolute;left:0;top:11px;width:30px;height:30px;border-radius:50%;background:#9a5a12;color:#fff;text-align:center;line-height:30px;font-weight:800}
.tips li b{display:block;font-size:19px;color:#18221f;margin-bottom:2px}
.src2{font-size:13px;color:#6b7772;margin:6px 0 0;line-height:1.5}
.mask{background:#fff7e8;border:2px dashed #9a5a12;border-radius:14px;padding:12px;margin:8px 0}
.mask b{display:block;margin-bottom:6px;color:#7a430a}
.mask-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.mask-grid span{background:#18221f;color:#fff;border-radius:6px;text-align:center;font-size:15px;padding:6px 2px}
.sendrow a{display:flex;align-items:center;justify-content:center;border-radius:14px;min-height:60px;font-size:18px;font-weight:800;text-decoration:none;text-align:center;line-height:1.3}
.s-mail{background:#1f5c4a;color:#fff}.s-form2{background:#fff;color:#1f5c4a;border:2px solid #1f5c4a}
.seg4{grid-template-columns:repeat(4,1fr)}
.seg4 button{font-size:15px}
"""
CSS = CSS + MORE_CSS

# --- 生保の見積もりメモ（がん・持病・認知症） ---
def life_form(id_, title, kind_opts, kind_label, extra=""):
    return hear(id_, title, "病気・入院・がんの保険",
        q("お生まれの年", sel("生まれ年", [f"{y}年" for y in range(2006, 1925, -1)]))
        + q("性別", opts("性別", ["男性", "女性"]))
        + q("たばこ", opts("たばこ", ["吸わない", "吸う（電子たばこ含む）"]))
        + q(kind_label, opts(kind_label, kind_opts, multi=True))
        + extra
        + q("毎月の保険料のご予算", opts("予算", ["2,000円くらい", "3,000円くらい", "5,000円くらい", "10,000円くらい", "15,000円くらい", "おまかせ"]))
        + q("今入っている同じ種類の保険", opts("今の保険", ["ある", "ない", "わからない"])),
        "健康状態のことは、お電話でうかがいます（ここでは入れません）。")
GAN_FORM = life_form("hear-gan", "がん保険のお見積り依頼",
    ["診断されたら一時金", "入院", "手術", "放射線", "抗がん剤・ホルモン剤", "先進医療", "休んだ分の収入"], "備えたいこと",
    q("診断一時金のめやす", opts("診断一時金", ["50万円", "100万円", "200万円", "おまかせ"])))
JIBYO_FORM = life_form("hear-jibyo", "持病がある方の医療保険のお見積り依頼",
    ["入院", "手術", "先進医療", "三大疾病の一時金", "通院"], "備えたいこと")
NINCHI_FORM = life_form("hear-ninchi", "認知症保険のお見積り依頼（くらべて選びたい方）",
    ["認知症と診断されたら一時金", "介護が必要になったら", "軽度認知障害（MCI）も", "おまかせ"], "備えたいこと")

# --- その他の損保 ---
BIKE_FORM = hear("hear-bike", "自転車保険のお見積り依頼", "自動車・火災・ケガの保険",
    q("補償する人", opts("補償する人", ["本人だけ", "夫婦", "家族みんな"]))
    + q("自転車に乗る人の年齢（いちばん上の人）", opts("年齢", ["10代以下", "20〜30代", "40〜50代", "60代", "70歳以上"]))
    + q("個人賠償（相手への賠償）を、自動車保険・火災保険などで付けている？", opts("個人賠償", ["付けている", "付けていない", "わからない"]))
    + q("自分のケガの補償も", opts("ケガの補償", ["付けたい", "いらない", "相談したい"])))
TRAVEL_FORM = hear("hear-travel", "海外旅行保険のお見積り依頼", "自動車・火災・ケガの保険",
    q("行き先", '<input type="text" name="行き先" placeholder="例：ハワイ／韓国／ヨーロッパ">')
    + q("出発日と帰国日", '<input type="text" name="日程" placeholder="例：12月20日〜12月27日">')
    + q("行く人数と年齢", '<input type="text" name="人数" placeholder="例：大人2人（50代）・子ども1人（10歳）">')
    + q("目的", opts("目的", ["観光", "出張", "留学・長期滞在"]))
    + q("クレジットカードの旅行保険", opts("カード付帯", ["付いている（自動付帯）", "付いている（利用付帯）", "わからない", "付いていない"])))
INJURY_FORM = hear("hear-injury", "ケガの保険のお見積り依頼", "自動車・火災・ケガの保険",
    q("補償する人", opts("補償する人", ["本人だけ", "夫婦", "家族みんな"]))
    + q("本人の年齢", opts("年齢", ["20代以下", "30代", "40代", "50代", "60代", "70歳以上"]))
    + q("お仕事", opts("職業", ["事務・接客など", "外回り・運転が多い", "建設・工場など体を使う", "学生・主婦・無職"]))
    + q("備えたいこと", opts("備えたいこと", ["入院", "通院", "手術", "後遺障害", "相手への賠償"], multi=True)))
BIZ_FORM = hear("hear-biz", "会社・お店の保険のご相談", "会社・お店の保険",
    q("業種", '<input type="text" name="業種" placeholder="例：飲食店／建設業／美容室">')
    + q("従業員の人数", opts("従業員", ["0人（ひとり）", "1〜5人", "6〜20人", "21人以上"]))
    + q("心配なこと", opts("心配なこと", ["火事・水漏れ", "お客さまへの賠償", "休業したときの売上", "従業員のケガ", "車", "まだわからない"], multi=True))
    + q("今の保険", opts("今の保険", ["入っている", "入っていない", "わからない"])))

# --- 知らないと損（各ページ） ---
TIPS_NINCHI = tips("知らないと損する3つのこと", [
    ("健康なうちしか、入れない", "認知症保険は、加入の前に健康状態を聞かれます。症状が出てからでは選べる保険がぐっと減ります。"),
    ("介護は「長く続く」", "介護が続く期間は平均4年7か月、毎月の費用は平均9.0万円。一時金はその間の生活費にも使えます。"),
    ("家族が困るのは「お金を下ろせない」こと", "本人の判断がむずかしくなると、家族でも本人の口座から自由にお金を下ろせないことがあります。早めに家族と話しておくことが大切です。")],
    "出典：生命保険文化センター（2024年度）")
TIPS_GAN = tips("知らないと損する3つのこと", [
    ("入院は短く、通院が長くなった", "病気やケガの平均入院日数は、1990年の44.9日から2017年には29.3日へ短くなりました。入院だけに備える保険だと、通院の治療で出ないことがあります。"),
    ("古いがん保険は、今の治療に合っていないことも", "放射線や抗がん剤・ホルモン剤の治療を、通院で長く続ける人がふえています。10年以上前の保険は、一度中身を見てみましょう。"),
    ("先進医療は、全額自己負担", "公的な保険がきかないので、費用はそのまま自分持ちです。保険で備えられるかを確かめておくと安心です。")],
    "出典：厚生労働省「患者調査」（平均在院日数）")
TIPS_JIBYO = tips("知らないと損する3つのこと", [
    ("まずは「ふつうの保険」に入れるか確かめる", "持病があっても、ふつうの保険に入れることがあります。ふつうの保険のほうが保険料は安めです。"),
    ("健康状態の質問には、正直に答える", "事実とちがう答えをすると、いざというときに保険金が出ないことがあります。"),
    ("入りやすい保険にも、決まりがある", "商品によっては、入ってすぐの時期は受け取れる額が少ないなどの決まりがあります。くらべて選ぶのが大切です。")],
    "")
TIPS_CAR = tips("知らないと損する3つのこと", [
    ("乗り換えは「満期日」に合わせる", "満期で乗り換えると、事故がなければ等級が1つ上がった状態で始まります。途中で乗り換えると、等級が上がるのは1年先になります。"),
    ("満期を過ぎたら、7日以内に", "前の保険の満期日（または解約日）から7日以内に次の保険を始めないと、等級を引き継げません。"),
    ("車を手放すときは「中断証明書」", "しばらく車に乗らないときは、条件を満たせば今の等級を残しておけます。")],
    "参考：価格.com保険・オリコン顧客満足度ほか各社の解説")
TIPS_FIRE = tips("知らないと損する3つのこと", [
    ("賃貸の保険は、自分で選べる", "不動産会社にすすめられた保険でなくても、必要な補償がそろっていれば入れます（借家人賠償の金額などは契約書で確認）。"),
    ("火災保険は最長5年", "2022年10月から、火災保険を一度に契約できるのは最長5年になりました。更新のときが見直しどきです。"),
    ("水災・地震は、自分で付けるか決める", "大雨・洪水への補償や地震保険は、付けないこともできます。ハザードマップで場所の危険度を見てから決めましょう。")],
    "参考：価格.com保険・SOMPOダイレクトほか")
TIPS_ETC = tips("知らないと損する3つのこと", [
    ("自転車の事故で、約9,500万円の賠償", "11歳の子どもが自転車で女性にけがをさせ、約9,521万円の賠償が命じられた例があります（2013年判決）。"),
    ("相手への賠償は、もう付いているかも", "自動車保険や火災保険に「個人賠償」が付いていることがあります。だぶっていないか、保険証券で確かめましょう。"),
    ("海外の病院代は高い", "海外旅行保険の加入者の22人に1人が旅行中にトラブルにあい、ハワイで2,530万円の治療費が出た例もあります。カード付帯の保険は「使ったときだけ」の場合もあるので確認を。")],
    "出典：判決例（交通事故総合分析センター資料ほか）、ジェイアイ傷害火災保険「2025年度 海外旅行保険事故データ」")
TIPS_SHINDAN = tips("保険証券を見せてもらうと、こんなことがわかります", [
    ("だぶっている補償", "個人賠償や医療の補償が、別々の保険に重なって付いていることがあります。"),
    ("今の治療に合っていない保険", "入院だけ・日額だけの古い保険は、今の通院中心の治療で出ないことがあります。"),
    ("払いすぎている保険料", "等級や年齢の条件、使っていない特約を見直すと、保険料が下がることがあります。")], "")

SHINDAN_BOX = ('<section class="box" id="shindan"><h2>📋 今入っている保険の「無料診断」</h2>'
    '<p>保険証券の写真を送るだけ。生命保険も、車・家の保険も、まとめて見ます。</p>'
    '<div class="pill-steps"><div><b>1</b>保険証券（車は車検証も）を用意</div><div><b>2</b>お名前など個人の情報を隠して写真をとる</div><div><b>3</b>メールかフォームで送る</div><div><b>4</b>診断結果をお返事します</div></div>'
    + SEND_PHOTO + REPLY.replace('お見積もりを','診断結果を') + '</section>')

CAR_FORM = CAR_FORM.replace('</section>', REPLY+FPLINE+'</section>')
FIRE_FORM = FIRE_FORM.replace('</section>', REPLY+FPLINE+'</section>')


LIFE_CO = ["エヌエヌ生命","オリックス生命","アクサ生命","マニュライフ生命","第一ネオ生命","メットライフ生命","日本生命","はなさく生命"]
NONLIFE_CO = ["損保ジャパン","あいおいニッセイ同和損保"]
def pair(first_href, first_label, first_small, neo=True, ev="pair"):
    a1 = (f'<a class="p1 js-neo" data-ev="{ev}_neo" href="{first_href}" target="_blank" rel="noopener noreferrer">{first_label}<small>{first_small}</small></a>' if neo
          else f'<a class="p1" href="{first_href}" data-v="{first_href[1:]}">{first_label}<small>{first_small}</small></a>')
    return f'<div class="pair">{a1}<a class="p2" href="#soudan" data-v="soudan">あらゆる保険の<br>相談をする<small>無料・申し込まなくてOK</small></a></div>'
OVER70_FORM = hear("hear-70", "70歳以上の方のご相談", "家族のための保障",
    q("どなたのためのご相談ですか？", opts("相談の立場", ["ご自分のため","親御さんのため（お子さまから）","今の保険の確認"]))
    + q("どんな保険をお探しですか？（いくつでも）", opts("探している保険", ["認知症","がん","医療・入院","介護","お葬式・死亡","相続","資産形成（資産運用）","まだわからない"], multi=True))
    + q("ご希望の保険会社（いくつでも）", opts("希望の保険会社", ["特にない"] + LIFE_CO + NONLIFE_CO, multi=True)
        + '<input type="text" name="その他の保険会社" placeholder="その他の保険会社（わかれば）" style="margin-top:8px">')
    + q("性別", opts("性別", ["男性","女性"]))
    + q("生年月日", '<div style="display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:6px">' + sel("生年", [f"{y}年（昭和{y-1925}年）" if y>=1926 else f"{y}年" for y in range(1956,1919,-1)]) + sel("生月",[f"{m}月" for m in range(1,13)]) + sel("生日",[f"{d}日" for d in range(1,32)]) + '</div>', "保険料の計算に使います")
    + q("知りたいこと（いくつでも）", opts("知りたいこと", ["保険料の金額","パンフレット（デジタル）","パンフレット（紙）","くわしい説明"], multi=True)))
SOUDAN_FORM = hear("hear-soudan", "保険のご相談", "まだ分からない",
    q("ご相談したいこと（いくつでも）", opts("相談内容", ["今の保険の見直し","保険料を下げたい","がん・医療","認知症・介護","相続","老後・資産形成","車・家の保険","会社・お店の保険","何から聞けばいいかわからない"], multi=True))
    + q("年代", opts("年代", ["20代","30代","40代","50代","60代","70歳以上"]))
    + q("ご家族", opts("ご家族", ["ひとり","夫婦","夫婦と子ども","親と同居"]))
    + q("今入っている保険", opts("今の保険", ["生命保険","医療・がん保険","車の保険","火災保険","入っていない","わからない"], multi=True))).replace("<h2>かんたん見積もりメモ","<h2>かんたん相談メモ")
OYA_FORM = hear("hear-oya", "親御さんの保険のご相談", "家族のための保障",
    q("親御さんのご年齢", opts("親の年齢", ["60代","70代","80代","90歳以上"]))
    + q("気になっていること（いくつでも）", opts("気になること", ["認知症","介護","入院・医療","お葬式の費用","相続","今の保険の中身がわからない"], multi=True))
    + q("親御さんの今の保険", opts("親の保険", ["入っている","入っていない","わからない"]))
    + q("ご相談のしかた", opts("相談のしかた", ["自分だけで先に聞きたい","親と一緒に聞きたい"]))).replace("<h2>かんたん見積もりメモ","<h2>かんたん相談メモ")
SOUZOKU_FORM = hear("hear-souzoku", "相続のご相談", "家族のための保障",
    q("年代", opts("年代", ["50代以下","60代","70代","80歳以上"]))
    + q("ご家族", opts("配偶者", ["配偶者がいる","配偶者はいない"]) + opts("子どもの人数", ["子ども1人","子ども2人","子ども3人以上","子どもはいない"]))
    + q("気になっていること（いくつでも）", opts("気になること", ["相続税","遺産の分け方","税金をはらうお金","自宅・不動産","会社・お店の引き継ぎ","認知症になったとき"], multi=True))
    + q("財産でいちばん多いもの", opts("財産", ["自宅・不動産","預貯金","株・投資信託","会社の株","わからない"]))
    + q("今の生命保険", opts("今の生命保険", ["入っている","入っていない","わからない"]))).replace("<h2>かんたん見積もりメモ","<h2>かんたん相談メモ")
TIPS_SOUZOKU = tips("知らないと損する3つのこと", [
    ("生命保険には「非課税の枠」がある", "死亡保険金のうち「500万円×法定相続人の数」までは、相続税がかかりません。預金のまま残すより、税金が少なくなることがあります。"),
    ("受け取る人を決めておける", "生命保険は受け取る人を指定できるので、遺産の分け方の話し合いとは別に、指定した人へ現金で届きます。"),
    ("認知症になると、対策がむずかしい", "保険の契約や財産の整理には、本人の判断が必要です。元気なうちに考えておくのが大切です。")],
    "出典：国税庁（相続税の基礎控除・生命保険金の非課税限度額）。具体的な税額は、必要に応じて税理士と連携してご案内します。")

AFTER_BOX = ('<section class="box" id="after-care"><h2>🤝 ご契約後のサポート</h2>'
 '<p style="line-height:1.8"><b>保険は、入ってからが本番です。</b>ネットでお申し込みの方も、ご相談から入った方も、同じようにサポートします。</p><ul class="kv">'
 '<li><b>① 変更の手続き</b>住所・お名前・口座・受取人の変更など、手続きのご案内とお手伝いをします。</li>'
 '<li><b>② 給付金・保険金の請求</b>入院・手術・がんの診断などのとき、請求の仕方と必要な書類をご案内します。</li>'
 '<li><b>③ ご契約内容の確認</b>「何に入っていたっけ？」にお答えします。更新・満期の前にもお知らせします。</li>'
 '<li><b>④ 年に1回の保障の点検</b>ご家族やお仕事が変わったら、今の保険で足りているかを無料で点検します。</li>'
 '<li><b>⑤ 車・家の保険の事故のとき</b>事故の連絡窓口になり、保険会社への取り次ぎをします。交通事故や家の事故で、弁護士費用特約を使って弁護士に頼みたいとき、書類づくりを行政書士に頼みたいときなど、ご希望に応じて各士業へ<b>無料でお取り次ぎ</b>します。</li>'
 '<li><b>⑥ もしものとき（お亡くなりになったとき）</b>ご家族からのご連絡で、死亡保険金の請求手続き、必要書類のご案内、各社への連絡の進め方までお手伝いします。ほかの保険会社のご契約や、どこに入っていたか分からないときの調べ方、相続の整理についてもアドバイスします。弁護士・司法書士・税理士・行政書士など、ご希望に応じて各士業へ<b>無料でお取り次ぎ</b>します。</li>'
 '</ul><p class="note">ご連絡はLINE・お電話・フォームから。お手続きは各保険会社の所定の方法で行います。お取り次ぎは無料です。士業に正式にご依頼される場合の報酬は、各事務所との直接のお取り決めになります（弁護士費用特約の対象になる場合があります）。</p>'
 '<div class="pair"><a class="p1" href="'+LINE+'" target="_blank" rel="noopener noreferrer" data-ev="after_line">LINEで<br>相談する<small>契約後のことも何でも</small></a><a class="p2" href="'+TEL+'" data-ev="after_tel">電話で<br>相談する<small>050-3696-4531</small></a></div></section>')
AFTER_MINI = ('<section class="box"><p style="margin:0;line-height:1.8">🤝 <b>ご契約後もサポートします。</b>変更の手続き、給付金・保険金の請求、もしものときのご家族の手続きまでお手伝いします。</p>'
 '<a class="cta sub" href="#soudan" data-v="soudan" data-ev="after_more">ご契約後のサポートを見る</a></section>')

DESK_MINI = ('<section class="box" style="border:2px solid #1f5c4a"><h2>🛡️ ご契約後は「ラサール クライアントデスク」がお守りします</h2>'
 '<p style="line-height:1.8">ネットでお申し込みの方も、ご相談から入った方も、ご契約後のお手続き（保全）は<b>LINEで24時間受付</b>しています。ご自宅の水漏れなどの事故のご連絡から、万一の保険金のお届け、各士業への無料お取り次ぎまで、同じ窓口で承ります。</p>'
 '<a class="cta sub" href="#desk" data-v="desk" data-ev="desk_more">クライアントデスクのくわしい説明を見る</a></section>')
CASES_BOX = '<section class="box" id="cases"><h2>📖 実際にあったお話（契約のあとこそ）</h2><p style="line-height:1.8">代表がこれまでにお預かりしてきたご契約は<b>500件以上</b>。保険金・給付金をお届けしたご家族と、今も長いお付き合いが続いています。</p><ul class="kv"><li><b>Mさん（当時70代の奥さま・仮名）</b>ご主人が長く入院され、入院給付金の支払い日数は上限に。奥さまはパートで病院代を払い続けていました。たまたま伺った際に状況をうかがい、当社募集人が主治医にヒアリングすると<b>高度障害の状態</b>にあたることが分かりました。診断書のお願いの仕方もご案内して請求し、<b>高度障害保険金5,000万円</b>をお届けできました。ご本人もご家族も、保険が出るとは気づいていなかったケースです。</li><li><b>Kさん（50代の男性・仮名）</b>軽度の障がいをお持ちの方でした。お母さまと母一人・子一人のご家庭で、80歳ごろのお母さまがお亡くなりになり、Kさんはお一人になりました。死亡保険金をお届けし、税理士と一緒に相続税の手続きを進め、暮らしに必要な手配もお手伝いしました。その後も寄り添い続け、<b>10年以上のお付き合い</b>になっています。</li></ul><p class="note">※個人が特定されないよう、仮名で紹介しています。保険金・給付金が出るかどうか、その金額は、ご契約の内容と保険会社の審査によります。</p></section>'
TOKUTEN_BOX = ('<section class="box" id="tokuten" style="border:2px solid #d9822b;background:#fffaf3"><h2>🎁 いまだけの特典（どなたでも）</h2>'
 '<p style="line-height:1.8;margin:0 0 8px"><b>11月30日まで、どなたでも無料でダウンロードできます。</b>「お金と制度の早わかり表 2026年版」（入院・介護・年金・相続で国からいくら戻るか、A4・9ページ）。下のボタンを押すとPDFが開きます。LINE登録やお名前の入力はいりません。</p>'
 '<a class="cta sub" href="/tokuten/hayawakari-2026.pdf" target="_blank" rel="noopener" data-ev="tokuten_pdf">📥 早わかり表（PDF）をダウンロードする</a>'
 '<p style="line-height:1.8;margin:10px 0 8px"><b>LINEのお友だち登録をした方全員に</b>、お孫さん・お子さんが主役の<b>20秒程度の紙芝居ドラマ</b>をお作りします。<b>お好きなあらすじ</b>をLINEで送ってください（呼び名と好きなことだけでもOK。ご自身が主役でも）。<br><small>※保険のご相談やご契約とは関係なく、どなたにもお作りします。</small></p>'
 '<a class="cta line" href="'+LINE+'" target="_blank" rel="noopener noreferrer" data-ev="tokuten_line">LINEでお友だち登録する</a></section>')

DESK_BAND = ('<a class="deskband" href="#desk" data-v="desk" data-ev="desk_band"><span style="font-size:26px">🛡️</span>'
 '<span><b>ネットで入っても、ご契約後までしっかりお見守りします。</b><br>ラサール クライアントデスク｜LINEで24時間受付</span><span class="ar">くわしく ›</span></a>')

V_NINCHI = f'''<section class="view" id="v-ninchi" data-name="ninchi">
<div class="src-hero" id="hero-jihyo" hidden><img src="/img/jihyo_hero.jpg" width="540" height="540" alt="机の上に置かれた一通の封筒"><p>あなたは、どうしますか。<small>元気なうちに、決めておけること。</small></p></div>
<div class="src-hero dark" id="hero-soba" hidden><p><span>🍜</span>父は今夜も、そばを打つ。<small>その手が止まる日のことを、少しだけ考えてみませんか。</small></p></div>
<div class="hero-people" id="hero-default"><img src="/img/ninchisho_hero.jpg" width="1086" height="362" alt="穏やかな表情の60代の男性と女性のイラスト"></div>
<div class="lead"><span class="kicker">認知症への備え</span><h1>自分で決める、<br>自分で備える。</h1><p>まずは3つの数字から。</p></div>
<div class="big3"><div><b>3.6人に<br>1人</b><span>65歳以上で認知症か、その手前</span></div><div><b>4年<br>7か月</b><span>介護が続く平均の期間</span></div><div><b>月<br>9.0万円</b><span>介護にかかる毎月の費用の平均</span></div></div>
<p class="srcs">出典：厚生労働省資料（2022年の推計）、生命保険文化センター（2024年度）</p>
<a class="cta js-neo" data-ev="neo_ninchisho" id="banner-ninchisho" href="{NEO_N}" target="_blank" rel="noopener noreferrer"><span class="who">40〜69歳のご本人</span><br>認知症保険を見てみる<small>第一ネオ生命（第一生命グループ）の画面へ・試算だけなら申込みになりません</small></a>
{GO_TILES}
<div class="box" style="padding:6px 6px 2px">{SC}</div>
{FLOW_CARD}
{TIPS_NINCHI}
{pair(NEO_N,'自分で保険料を<br>見てみる','40〜69歳のご本人')}
<h2 style="font-size:21px;margin:22px 4px 10px">ほかの保険会社ともくらべたい方へ</h2>
<p class="note" style="margin:0 4px 10px">第一ネオ生命以外の保険会社の認知症保険も、お調べしてお見積もりします。</p>
{NINCHI_FORM}
<h2 style="font-size:21px;margin:22px 4px 10px">もっと知りたい方へ</h2>
<details class="more"><summary>😟 認知症になると困ること</summary><div class="in">{TR}</div></details>
<details class="more"><summary>📊 数字で見る、介護のお金と期間</summary><div class="in">{NUM}</div></details>
<details class="more"><summary>🏛️ 公的介護保険だけでは足りないところ</summary><div class="in">{PUB}</div></details>
<details class="more"><summary>✅ 認知症保険を選ぶときの5つのポイント</summary><div class="in">{PTS}</div></details>
<details class="more"><summary>❓ よくある質問</summary><div class="in">{FAQ}</div></details>
{AFTER_MINI}
</section>'''

GAN_CHECK = '''<section class="box"><h2>がん保険 かんたんチェック</h2><p>もしものとき、<b>どの治療</b>に備えたいですか？（いくつでも）</p>
<div class="chips" id="gc">
<label><input type="checkbox" value="nyuin">🛏️ 入院</label><label><input type="checkbox" value="shujutsu">🩺 手術</label>
<label><input type="checkbox" value="hoshasen">☢️ 放射線</label><label><input type="checkbox" value="kouganzai">💉 抗がん剤</label>
<label><input type="checkbox" value="horumon">💊 ホルモン剤</label><label><input type="checkbox" value="shindan">📄 診断されたら一時金</label>
<label><input type="checkbox" value="sensin">🔬 先進医療</label><label><input type="checkbox" value="shunyu">👔 休んだ分の収入</label></div>
<button type="button" class="cta" id="gc-go" style="width:100%;border:0;cursor:pointer;font-family:inherit">結果を見る</button>
<div class="res2" id="gc-res"><h3>保険を選ぶときに確かめたいこと</h3><ul id="gc-list"></ul><p class="note">がん保険は、商品によって「どの治療のときにお金が出るか」が違います。選んだ治療が保障の対象かを、試算の画面やご相談で確かめてください。</p><div class="keep"><a href="#" class="k-line" data-keep="gan">📩 この結果を<br>LINEに保存</a><a href="#" class="k-fam" data-share="gan">👪 家族に<br>このページを送る</a></div></div></section>'''

V_GAN = f'''<section class="view" id="v-gan" data-name="gan">
<div class="lead"><span class="kicker">がんへの備え</span><h1>治療は、<br>人によってちがう。</h1><p>だから、備え方も選べます。</p></div>
{pair(NEO_G,'がん保険の<br>保険料を見てみる','試算だけなら申込みになりません',ev='gan_top')}
<div class="box">{GAN_INFO}</div>
{GAN_CHECK}
{TIPS_GAN}
{pair(NEO_G,'自分で保険料を<br>見てみる','第一ネオ生命の画面へ',ev='gan_tips')}
{GAN_FORM}
<a class="cta js-neo" data-ev="neo_gan" href="{NEO_G}" target="_blank" rel="noopener noreferrer">がん保険を見てみる<small>第一ネオ生命（第一生命グループ）の画面へ・試算だけなら申込みになりません</small></a>
<a class="cta sub" href="#soudan" data-v="soudan">相談して決めたい方はこちら</a>
<a class="cta sub" href="#over70" data-v="over70">70歳以上の方はこちら</a>
{AFTER_MINI}
</section>'''

V_JIBYO = f'''<section class="view" id="v-jibyo" data-name="jibyo">
<div class="lead"><span class="kicker">持病がある方へ</span><h1>持病があっても、<br>あきらめないで。</h1><p>入りやすい保険があります。</p></div>
{pair(NEO_K,'入りやすい医療保険の<br>保険料を見てみる','試算だけなら申込みになりません',ev='jibyo_top')}
<section class="box"><h2>あてはまるものはありますか？</h2>
<div class="chips" id="jc">
<label><input type="checkbox">🏥 いま通院している</label><label><input type="checkbox">💊 毎日飲んでいる薬がある</label>
<label><input type="checkbox">🩹 入院・手術をしたことがある</label><label><input type="checkbox">🙅 保険を断られたことがある</label></div>
<button type="button" class="cta" id="jc-go" style="width:100%;border:0;cursor:pointer;font-family:inherit">結果を見る</button>
<div class="res2" id="jc-res"><h3 id="jc-h"></h3><p id="jc-p"></p><div class="keep"><a href="#" class="k-line" data-keep="jibyo">📩 この結果を<br>LINEに保存</a><a href="#" class="k-fam" data-share="jibyo">👪 家族に<br>このページを送る</a></div></div></section>
<section class="box"><h2>入りやすい保険って？</h2>
<p>健康状態の質問が<b>2〜3つと少ない</b>のが特長です。多くの保険会社で、たとえばこんな質問です。</p>
<ol class="kokuchi"><li>最近3か月以内に、医師から入院・手術・検査をすすめられたことがありますか？</li><li>過去1〜2年以内に、病気やケガで入院・手術をしたことがありますか？</li><li>過去5年以内に、がんで入院・手術をしたことがありますか？</li></ol>
<p>ぜんぶ「いいえ」なら、入れる可能性があります。<b>当てはまっても入れる保険があることもある</b>ので、あきらめずにご相談ください。</p>
<p class="note">※質問の内容や年数は、保険会社・商品によってちがいます。そのぶん保険料は、ふつうの保険より高めです。「引受基準緩和型（ひきうけきじゅん かんわがた）」と呼ばれる保険です。</p></section>
{TIPS_JIBYO}
{JIBYO_FORM}
{pair(NEO_K,'入りやすい医療保険の<br>保険料を見てみる','第一ネオ生命の画面へ',ev='jibyo_end')}
{AFTER_MINI}
</section>'''


OVER70_HOOK = ('<section class="box o70"><h2>70歳から、何が変わる？</h2>'
 '<p class="o70lead">保険は「入りたい」と思った時に、入れるとは限りません。数字で見てみましょう。</p>'
 '<div class="o70stats">'
 '<div><b>約3.4倍</b><span>入院する人の割合<br>（50代前半とくらべて70代前半）</span><i>人口10万人あたり 441人→1,502人</i></div>'
 '<div><b>約8倍</b><span>がんと診断される男性の割合<br>（50代前半とくらべて70代前半）</span><i>人口10万人あたり 322人→2,685人（女性は約2.2倍）</i></div>'
 '<div><b>43.4%</b><span>収入が年金だけの<br>高齢者世帯</span><i>入院やがんの費用は、貯金を取り崩すことに</i></div>'
 '</div>'
 '<div class="talk"><div class="tk l"><span class="av">👵</span><p>70を過ぎてから、まわりで「がんが見つかった」って話をよく聞くようになったのよね。</p></div>'
 '<div class="tk r"><p>年金暮らしだと、入院したら貯金から出すしかないんだよな。</p><span class="av">👴</span></div>'
 '<div class="tk l"><span class="av">👩</span><p>元気な今のうちに、一度だけ聞いてみたら？　相談だけならタダなんだし。</p></div>'
 '<p class="note" style="text-align:right">※会話はイメージです</p></div>'
 '<ul class="o70why"><li><b>保険料は、申し込む年齢で決まります。</b>1歳上がるごとに高くなるのが一般的です。</li>'
 '<li><b>一度入院・手術をすると、入れなくなることがあります。</b>告知（健康状態の質問）に当てはまると、お断りや条件付きになることがあります。</li>'
 '<li><b>年齢が上がるほど、選べる保険が減っていきます。</b>入れる年齢に上限がある保険も多いです。</li></ul>'
 '<p class="o70now">思い立った今日が、いちばん若い日です。<br><b>今、相談しちゃいましょう。</b></p>'
 '<div class="o70who"><a href="#hear-70" data-who="ご自分のため" data-ev="o70_self">👤 ご自分のため</a>'
 '<a href="#hear-70" data-who="親御さんのため（お子さまから）" data-ev="o70_parent">👪 親御さんのため<br><small>お子さまから</small></a>'
 '<a href="#hear-70" data-who="今の保険の確認" data-ev="o70_check">📋 今の保険の確認</a></div>'
 '<p class="src2">出典：厚生労働省「令和5年 患者調査」入院受療率、厚生労働省「令和5年 全国がん登録 罹患数・率 報告」年齢階級別罹患率、厚生労働省「2024年 国民生活基礎調査」（公的年金・恩給を受給している高齢者世帯のうち、総所得に占める割合が100%の世帯）</p></section>')
OVER70_NEXT = ('<section class="box"><h2>送ったあと、こう進みます</h2><div class="pill-steps">'
 '<div><b>1</b>担当から、受付から<b>遅くとも翌々日まで</b>にご連絡します</div>'
 '<div><b>2</b>お電話かテレビ電話で、まず<b>「どんなときに・いくら出るか」</b>を一緒に確認します</div>'
 '<div><b>3</b>生年月日と性別をうかがって、<b>保険料をお出しします</b></div>'
 '<div><b>4</b>パンフレットと重要事項説明書をお送りし、ご納得いただけたらお申込みへ</div></div>'
 '<p class="note">ご家族も一緒に聞けます（ご希望の方だけ。ご本人だけでも大丈夫です）。</p></section>')

V_70 = f'''<section class="view" id="v-over70" data-name="over70">
<div class="lead"><span class="kicker">70歳以上の方へ</span><h1>あなたに合う保険を、<br>私たちがお調べします。</h1><p>わかるところだけ答えて、送るだけ。</p></div>
{OVER70_HOOK}
{OVER70_FORM}
{OVER70_NEXT}
<section class="box" hidden><h2>このあとの流れ</h2><div class="pill-steps">
<div><b>1</b>いまの内容を送る</div><div><b>2</b>担当がお客さまに合う保険をお調べします</div><div><b>3</b>保険料やパンフレットを、ご希望の方法でご案内します</div><div><b>4</b>ご納得いただけたら、お手続きをご案内します</div></div>
<p class="callrow">お電話でもどうぞ<br><a href="{TEL}" data-ev="tel_70">050-3696-4531</a><br><span class="note">月〜金 9:00〜18:00</span></p></section>
{AFTER_MINI}
</section>'''

V_SOUDAN = f'''<section class="view" id="v-soudan" data-name="soudan">
<div class="lead"><span class="kicker">無料のご相談</span><h1>どんな保険のことでも、<br>聞いてください。</h1><p>相談しても、申し込まなくて大丈夫です。</p></div>
<section class="box"><h2>🙋 自分で決める方はこちら</h2><p>相談せずに、ご自身で保険料を見て、そのままスマホで申し込むこともできます。</p>
<a class="cta js-neo" data-ev="neo_other" id="banner-other-soudan" href="{NEO_ALL}" target="_blank" rel="noopener noreferrer">自分で決める｜保険を選んで保険料を見る<small>第一ネオ生命（第一生命グループ）の画面へ・試算だけなら申込みになりません</small></a>
<p class="note">迷ったら、下の無料相談からどうぞ。</p></section>
{AFTER_BOX}
{CASES_BOX}
{DESK_MINI}
{SHINDAN_BOX}
{TIPS_SHINDAN}
<section class="box"><h2>こんなご相談、多いです</h2><div class="topics">
<a href="#shindan" data-ev="topic_shindan" data-scroll="shindan"><span>📋</span>今の保険、このままでいい？（無料診断）</a>
<a href="#" data-topic="家族のための保障" data-ev="topic_souzoku"><span>🏠</span>相続のこと</a>
<a href="#" data-topic="病気・入院・がんの保険" data-ev="topic_gan"><span>🎗️</span>がん・病気・入院</a>
<a href="#" data-topic="家族のための保障" data-ev="topic_ninchi"><span>🌿</span>認知症・介護</a>
<a href="#sonpo" data-v="sonpo" data-ev="topic_sonpo"><span>🚗</span>車・家・ケガ</a>
<a href="#" data-topic="会社・お店の保険" data-ev="topic_houjin"><span>🏢</span>会社・お店の保険</a>
<a href="#" data-topic="まだ分からない" data-ev="topic_wakaranai" style="grid-column:1/-1"><span>🤔</span>何から聞けばいいかわからない</a></div>
<p class="note">押すと、相談フォーム（Googleフォーム）が開きます。選んだ内容が入った状態です。</p></section>
{SOUDAN_FORM}
<a class="cta line" data-ev="soudan_line" href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで相談する<small>スマホからかんたん</small></a>
<a class="cta sub" data-ev="soudan_form" href="{FORM}" target="_blank" rel="noopener noreferrer">フォームで相談する</a>
<p class="callrow">お電話でもどうぞ<br><a href="{TEL}" data-ev="tel_soudan">050-3696-4531</a><br><span class="note">月〜金 9:00〜18:00</span></p>
<section class="box"><h2>相談するのは、こんな会社です</h2><p><b>生命保険会社の支社長</b>と<b>信用金庫の支店長</b>が一緒につくった保険代理店です。代表は業歴17年目。国家資格（FP技能士）をもつファイナンシャルプランナーがご相談に乗ります。生命保険も損害保険も扱う乗合代理店なので、あらゆる保険のご相談ができます。<a href="#companies" data-v="companies" class="fp">取扱保険会社一覧 ›</a></p></section>
</section>'''



V_SONPO = f'''<section class="view" id="v-sonpo" data-name="sonpo">
<div class="lead"><span class="kicker">車と家の保険（損害保険）</span><h1>車と家の保険も、<br>スマホで。</h1><p>お店に行かず、見積もりから申込みまでできます。</p></div>
<div class="seg" role="tablist" aria-label="保険の種類">
<button type="button" role="tab" aria-selected="true" data-sub="car"><span>🚗</span>自動車保険</button>
<button type="button" role="tab" aria-selected="false" data-sub="fire"><span>🏠</span>火災保険</button>
<button type="button" role="tab" aria-selected="false" data-sub="etc"><span>🛡️</span>その他</button></div>

<div class="sub on" id="s-car">
<section class="box"><h2>こんなとき、見直しどきです</h2><div class="chips" id="cc">
<label><input type="checkbox" value="満期が近い">📅 満期が近い</label><label><input type="checkbox" value="車を買い替える">🚙 車を買い替える</label>
<label><input type="checkbox" value="家族が免許を取った">🔰 家族が免許を取った</label><label><input type="checkbox" value="運転する人が変わった">👥 運転する人が変わった</label>
<label><input type="checkbox" value="保険料を見直したい">💴 保険料を見直したい</label><label><input type="checkbox" value="補償の中身がわからない">🤔 中身がよくわからない</label></div></section>
<section class="box"><h2>手元にあると早いもの</h2><div class="bring"><div><b>📄</b>車検証</div><div><b>📋</b>今の保険証券<br><span class="note">（入っている方）</span></div><div><b>🪪</b>運転免許証<br><span class="note">（色を確認）</span></div><div><b>📱</b>スマホ</div></div></section>
{TIPS_CAR}
{CAR_FORM}
</div>

<div class="sub" id="s-fire">
<section class="box"><h2>あなたの家、水害は大丈夫？</h2><p>火災保険は、<b>水災（大雨・洪水）</b>を付けるかどうかで中身が大きく変わります。まずは、お住まいの場所の危険度を見てみましょう。</p>
<a class="cta sub" data-ev="hazardmap" href="https://disaportal.gsi.go.jp/" target="_blank" rel="noopener noreferrer">🗺️ ハザードマップで調べる<small>国土交通省「ハザードマップポータルサイト」</small></a>
<p class="note">危険度が低い地域でも、大雨で水があふれたり、土砂崩れが起きたりすることがあります。</p></section>
<section class="box"><h2>こんなとき、見直しどきです</h2><div class="chips" id="fc">
<label><input type="checkbox" value="更新が近い">📅 更新が近い</label><label><input type="checkbox" value="家を買う・建てる">🏡 家を買う・建てる</label>
<label><input type="checkbox" value="引っ越す・賃貸">📦 引っ越す・賃貸</label><label><input type="checkbox" value="地震保険を考えたい">🌏 地震保険を考えたい</label>
<label><input type="checkbox" value="水災を付けるか迷う">🌧️ 水災を付けるか迷う</label><label><input type="checkbox" value="家財も守りたい">🛋️ 家具・家電も守りたい</label></div></section>
<section class="box"><h2>手元にあると早いもの</h2><div class="bring"><div><b>📍</b>住所</div><div><b>🏢</b>戸建て・<br>マンション</div><div><b>📐</b>広さと<br>建てた年</div><div><b>📋</b>今の保険証券<br><span class="note">（入っている方）</span></div></div></section>
{TIPS_FIRE}
{FIRE_FORM}
</div>

<div class="sub" id="s-etc">
{TIPS_ETC}
<div class="seg seg4" role="tablist" aria-label="その他の保険">
<button type="button" aria-selected="true" data-sub2="bike"><span>🚲</span>自転車</button>
<button type="button" aria-selected="false" data-sub2="travel"><span>✈️</span>海外旅行</button>
<button type="button" aria-selected="false" data-sub2="injury"><span>🩹</span>ケガ</button>
<button type="button" aria-selected="false" data-sub2="biz"><span>🏢</span>会社・お店</button></div>
<div class="sub2 on" id="s2-bike">{BIKE_FORM}</div><div class="sub2" id="s2-travel">{TRAVEL_FORM}</div><div class="sub2" id="s2-injury">{INJURY_FORM}</div><div class="sub2" id="s2-biz">{BIZ_FORM}</div>
</div>

<section class="box"><h2>スマホで申込みまで、5ステップ</h2><div class="pill-steps">
<div><b>1</b>見積もりメモを送る（わかるところだけでOK）</div>
<div><b>2</b>担当が見積もりを作り、資料をメールでお送りします<br><span class="note">（いくつかの保険会社でくらべることもできます）</span></div>
<div><b>3</b>大切なことのご説明と、内容に間違いがないかの確認を、お電話でします</div>
<div><b>4</b>お申込みの前に、保険証券・車検証の写真を送ってください（個人の情報は隠してOK）</div><div><b>5</b>スマホで申込みができます。ハンコはいりません</div></div>{REPLY}
<p class="note">お電話でのお申込みや、お会いしてのお手続きもできます。</p><h2 style="margin-top:14px">写真の送り方</h2>{SEND_PHOTO}</section>
<a class="cta line" data-ev="sonpo_line" href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで聞いてみる</a>
<p class="callrow">お電話でもどうぞ<br><a href="{TEL}" data-ev="tel_sonpo">050-3696-4531</a><br><span class="note">月〜金 9:00〜18:00</span></p>
{AFTER_MINI}
</section>'''

V_SOUZOKU = f'''<section class="view" id="v-souzoku" data-name="souzoku">
<div class="lead"><span class="kicker">相続への備え　<span style="color:#d9482b">いまご相談が多いテーマです</span></span><h1>相続を「争族」に<br>しないために。</h1><p>相続税の試算、よくある悩み、一般的な対策をまとめました。</p></div>
<h2 class="ch" id="sz1">📊 1. 相続の基本の数字</h2>
<div class="big3"><div><b style="font-size:18px">3,000万円<br>＋600万円<br>×人数</b><span>相続税がかからない<br>基礎控除</span></div><div><b>500万円<br>×人数</b><span>死亡保険金が<br>非課税になる枠</span></div><div><b>10か月</b><span>相続税の<br>申告・納付の期限</span></div></div>
<p class="srcs">出典：国税庁　※人数は法定相続人の数</p>
<section class="box" style="border:2px solid #1f5c4a"><p style="margin:0;line-height:1.8">📞 <b>電話1本で、相続の窓口がそろいます。</b><br>行政書士資格保有者・国家資格ファイナンシャルプランナー・宅建士（不動産）がご相談をお受けします。ご希望の方には、税理士・弁護士・司法書士・不動産会社・金融機関へのお取り次ぎも行います（無料のサービスです）。<br><b>親御さんからも、お子さまからもご相談いただけます。</b>現在のところ<b>全国対応</b>しています。</p></section>
<nav class="box toc" aria-label="相続ページの目次"><h2>📖 このページの目次</h2><ol>
<li><a href="#sz1" data-scroll="sz1">相続の基本の数字</a></li>
<li><a href="#souzoku-calc" data-scroll="souzoku-calc">相続税のかんたん試算</a></li>
<li><a href="#sz3" data-scroll="sz3">実際に相続が起きると、困ること</a></li>
<li><a href="#sz4" data-scroll="sz4">相続が「争族」になるまで</a></li>
<li><a href="#sz5" data-scroll="sz5">家族の間で、よく困ること</a></li>
<li><a href="#sz6" data-scroll="sz6">一般的な相続対策</a></li>
<li><a href="#sz7" data-scroll="sz7">保険でできる相続対策</a></li>
<li><a href="#sz8" data-scroll="sz8">ご相談の体制（電話1本・全国対応）</a></li>
<li><a href="#hear-souzoku" data-scroll="hear-souzoku">かんたん相談メモ</a></li></ol></nav>
<div class="pair"><a class="p1" href="#hear-souzoku" data-scroll="hear-souzoku">かんたん<br>相談メモへ<small>1分・お名前は不要</small></a><a class="p2" href="#soudan" data-v="soudan">あらゆる保険の<br>相談をする<small>無料・申し込まなくてOK</small></a></div>
{TIPS_SOUZOKU}
<section class="box calc" id="souzoku-calc"><h2>🧮 2. 相続税の「かんたん試算」</h2>
<p>相続税がどう計算されるかを知るための<b>学習用の試算</b>です。数字は「万円」で入れてください。</p>
<div class="row"><label for="c-sp">配偶者（夫・妻）</label><select id="c-sp"><option value="1">いる</option><option value="0">いない</option></select></div>
<div class="row"><label for="c-ch">子どもの人数</label><select id="c-ch"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option></select></div>
<div class="row"><label for="c-dep">預貯金</label><input id="c-dep" type="number" inputmode="numeric" min="0" placeholder="例 2000"></div>
<div class="row"><label for="c-re">自宅・土地など<small style="display:block;font-size:12px;color:#4f5c57">固定資産税の評価額などのめやす</small></label><input id="c-re" type="number" inputmode="numeric" min="0" placeholder="例 3000"></div>
<div class="row"><label for="c-st">株・投資信託など</label><input id="c-st" type="number" inputmode="numeric" min="0" placeholder="例 500"></div>
<div class="row"><label for="c-li">死亡保険金</label><input id="c-li" type="number" inputmode="numeric" min="0" placeholder="例 1000"></div>
<div class="row"><label for="c-db">借入れ・葬儀費用</label><input id="c-db" type="number" inputmode="numeric" min="0" placeholder="例 200"></div>
<button type="button" class="cta" id="c-go" data-ev="souzoku_calc">試算してみる</button>
<div class="res" id="c-res" hidden></div>
<p class="note">※国税庁が公表している計算のしくみ（基礎控除・税率表・生命保険金の非課税枠・配偶者の税額軽減）を、財産を法律で決まった割合（法定相続分）で分けたと仮定して当てはめた<b>一般的な試算</b>です。土地の評価（路線価、小規模宅地等の特例など）や贈与、お子さまがいない場合などは反映していません。個別の税額の計算や税務のご相談ではありません。実際の税額は税理士にご確認ください（税理士・弁護士・司法書士へのお取り次ぎも可能です）。</p>
</section>
<section class="box" id="sz3"><h2>📝 3. 実際に相続が起きると、困ること</h2>
<p>もめていなくても、手続きだけでご家族は大変です。実際によくあるのは、こんなことです。</p><ul class="kv">
<li><b>① 不動産は、すぐには売れない</b>「家を売って分ければいい」と思っても、買い手が見つかるまで数か月〜何年もかかることがあります。地方の土地や古い家は、値段が付きにくいことも。その間も固定資産税や管理の手間はかかり続けます。</li>
<li><b>② 預貯金が凍結される</b>銀行が亡くなったことを知ると、口座は止まります。葬儀代や当面の生活費が引き出せず困るケースは多いです（一定額までは払い戻せる制度がありますが、手続きと書類が必要です）。</li>
<li><b>③ 戸籍集めだけで何週間も</b>相続人を確定するため、亡くなった方の生まれてから亡くなるまでの戸籍が必要です。本籍を何度も移していると、集めるだけで大仕事です。</li>
<li><b>④ 相続登記は「義務」になった</b>2024年4月から、不動産を相続したら3年以内の登記が義務になりました。正当な理由なく放っておくと過料（10万円以下）の対象になることがあります。</li>
<li><b>⑤ 名義変更・解約が、とにかく多い</b>銀行・証券・保険・車・電気ガス水道・携帯・年金…。平日に窓口へ行く必要があるものも多く、仕事をしながらでは大変です。</li>
<li><b>⑥ 期限が次々にやってくる</b>相続放棄は3か月、亡くなった方の所得税の申告（準確定申告）は4か月、相続税の申告・納付は10か月以内です。</li>
<li><b>⑦ 借金やローンも相続される</b>預金だけでなく、借入れ・保証人の立場も引き継ぎます。知らずに財産を使うと、相続放棄ができなくなることがあります。</li>
</ul><p class="srcs">出典：法務省（相続登記の申請義務化）、国税庁、民法</p></section>
<section class="box" id="sz4"><h2>⚠️ 4. 相続が「争族（あらそうぞく）」になるまで</h2>
<div class="big3" style="grid-template-columns:1fr 1fr"><div><b>約3件に<br>1件</b><span>家庭裁判所で争われた遺産分割のうち、遺産1,000万円以下</span></div><div><b>約4分の3</b><span>遺産5,000万円以下のケースの割合</span></div></div>
<p class="srcs">出典：最高裁判所「司法統計年報」（令和4年・遺産分割事件の遺産の価額別）</p>
<div class="story"><p>父が亡くなった。財産は、実家と預金が少し。</p>
<p>実家で同居して介護をしてきた長女は「家は私が住み続けたい」。遠くに住む長男は「法律どおり半分ずつ」。</p>
<p>家を売らなければ半分は払えない。話し合いは平行線のまま、10か月の期限が近づく。</p>
<p>やがて家庭裁判所の調停へ。父の一周忌に、きょうだいがそろうことはなかった。</p></div>
<p>「うちは財産が少ないから大丈夫」が、いちばん危ない。もめる原因はお金の多さではなく、<b>分けにくさ</b>と<b>気持ちのすれ違い</b>です。</p></section>
<section class="box" id="sz5"><h2>😟 5. 家族の間で、よく困ること</h2><ul class="kv">
<li><b>財産が自宅しかなく、分けられない</b>売るのか、誰かが住み続けるのか。住む人が他の兄弟にお金を払えず、もめる原因になります。</li>
<li><b>介護をした人・しなかった人の不公平感</b>「私がずっと面倒を見たのに、同じ割合なの？」は、とても多いご相談です。</li>
<li><b>預金が引き出せず、葬儀代に困る</b>亡くなったことが分かると、口座は止まります。一定額まで払い戻せる制度はありますが、手続きが必要です。</li>
<li><b>相続人が多い・連絡が取れない</b>前の結婚のお子さん、疎遠な兄弟など、全員の同意がないと分け方が決まりません。</li>
<li><b>相続人の中に認知症の方がいる</b>話し合いに参加できず、成年後見人が必要になることがあります。</li>
<li><b>期限に追われる</b>相続放棄は3か月、相続税の申告は10か月。悲しみの中で、手続きが一気に押し寄せます。</li>
</ul></section>
<section class="box" id="sz6"><h2>📌 6. 一般的な相続対策（常識の範囲で）</h2><ul class="kv">
<li><b>① 財産の一覧をつくる</b>預金・保険・不動産・証券・借入れを1枚に。ネット銀行やネット証券は、家族が気づかないことがよくあります。</li>
<li><b>② 遺言書を書いておく</b>公証役場でつくる「公正証書遺言」や、法務局で預かってもらえる「自筆証書遺言の保管制度」があります。</li>
<li><b>③ 生命保険の非課税枠を使う</b>死亡保険金は「500万円×法定相続人の数」まで非課税。受け取る人を指定でき、すぐ現金で届きます。</li>
<li><b>④ 相続税をはらう現金を用意する</b>財産が自宅中心だと、税金や他の家族に渡すお金が足りなくなりがちです。</li>
<li><b>⑤ 生前の贈与を計画的に</b>年110万円までの贈与は贈与税がかかりません（ただし亡くなる前の一定期間の贈与は相続財産に足し戻されます）。</li>
<li><b>⑥ 認知症に備える</b>判断力がなくなると、契約や財産の整理ができなくなります。任意後見や家族信託という方法もあります。</li>
<li><b>⑦ 家族で一度、話しておく</b>「誰が家を継ぐか」「介護をしてくれた人への気持ち」など、元気なうちの一言がいちばんの対策です。</li>
</ul><p class="srcs">出典：国税庁、法務省（自筆証書遺言書保管制度）</p></section>
<section class="box" id="sz7"><h2>🛡️ 7. 保険でできる相続対策</h2>
<p>生命保険は、相続でとても使いやすい道具です。代表的なものをまとめました。</p><ul class="kv">
<li><b>① 非課税の枠がある</b>相続人が受け取る死亡保険金は「500万円×法定相続人の数」まで相続税がかかりません。例：相続人が3人なら1,500万円まで。預金のまま残すより税金が少なくなることがあります。</li>
<li><b>② 受け取る人を指定できる</b>保険金は受取人の固有の財産として扱われ、原則として遺産分割の話し合いを待たずに、指定した人へ届きます。「家を継ぐ子に多めに」「介護してくれた子に」といった気持ちを形にできます。</li>
<li><b>③ すぐに現金が届く</b>請求から数日〜1週間ほどで支払われることが多く、口座が凍結されている間の葬儀代や当面の生活費に使えます。</li>
<li><b>④ 相続税をはらうお金になる</b>財産が自宅中心で現金が少ないと、10か月以内の納税に困ります。保険金で納税資金を用意できます。</li>
<li><b>⑤ 不動産を分けるときの調整に使える</b>家を継ぐ人が、他の兄弟に代わりのお金（代償金）を払う方法があります。その原資を保険で準備しておけます。</li>
<li><b>⑥ 契約の形で、かかる税金が変わる</b>同じ保険金でも、誰が保険料をはらい、誰が受け取るかで「相続税」「所得税」「贈与税」のどれがかかるかが変わります。入っている保険の形を一度確認するのがおすすめです。</li>
<li><b>⑦ 毎年の税金も軽くなる</b>生命保険料は「生命保険料控除」の対象で、所得税は一般・介護医療・個人年金の3つでそれぞれ最大4万円、合計最大12万円まで所得から差し引けます（新制度の場合）。</li>
</ul>
<table class="cmp" style="width:100%;border-collapse:collapse;font-size:15px;margin-top:8px"><tr><th style="text-align:left;border-bottom:1px solid #c9d3cf">保険料をはらう人／亡くなる人／受け取る人</th><th style="border-bottom:1px solid #c9d3cf">かかる税金</th></tr>
<tr><td>父／父／子</td><td style="text-align:center">相続税（非課税枠あり）</td></tr>
<tr><td>子／父／子</td><td style="text-align:center">所得税（一時所得）</td></tr>
<tr><td>母／父／子</td><td style="text-align:center">贈与税</td></tr></table>
<p class="note">※相続人以外の人（例：お孫さん）が受け取る場合は非課税枠の対象外です。お孫さんなどは相続税が2割加算になる場合があります。</p>
<p class="srcs">出典：国税庁（相続税の非課税財産・生命保険料控除・保険金の課税関係）</p>
<div class="pair"><a class="p1" href="#hear-souzoku" data-scroll="hear-souzoku">今の保険で<br>大丈夫か相談<small>無料・お名前は不要</small></a><a class="p2" href="#soudan" data-v="soudan">保険の<br>無料診断へ<small>証券の写真でOK</small></a></div></section>
<div class="pair"><a class="p1" href="#hear-souzoku" data-scroll="hear-souzoku">かんたん<br>相談メモへ<small>1分・お名前は不要</small></a><a class="p2" href="#soudan" data-v="soudan">あらゆる保険の<br>相談をする<small>無料・申し込まなくてOK</small></a></div>
{AFTER_BOX}
{DESK_MINI}
<section class="box" id="sz8"><h2>🤝 8. ご相談の体制</h2>
<p style="line-height:1.8"><b>まずはラサール＆パートナーズに電話を1本ください。</b>お話をうかがい、ご希望の方には専門家や業者へのお取り次ぎを行います（無料のサービスです）。ご家族があちこちに連絡する必要はありません。</p>
<ul class="kv">
<li><b>相続全体・保険・お金の整理</b>行政書士資格保有者、国家資格ファイナンシャルプランナーがお話をうかがいます。</li>
<li><b>不動産（自宅・土地・空き家）</b>宅建士がご相談に乗ります。必要に応じて<b>現地を実際に見に行く</b>ことも可能です。売却・活用はご希望に応じて提携する不動産会社をご紹介します。</li>
<li><b>遺言・登記・税金・もめごと</b>ご希望の方には、当社と提携している各事務所（税理士・弁護士・司法書士・行政書士）へお取り次ぎし、連携して進められます。</li>
<li><b>預金・ローン・資金のこと</b>銀行・信用金庫へお取り次ぎした例もあります。</li>
</ul>
<div class="big3" style="grid-template-columns:1fr 1fr 1fr"><div><b>電話<br>1本</b><span>まずはご相談を</span></div><div><b>全国<br>対応</b><span>現在のところ可能です</span></div><div><b>親から<br>子から</b><span>どちらからでもOK</span></div></div>
<p class="note">※ご相談は無料です。税理士・弁護士・司法書士などの専門家に正式にご依頼される場合の報酬は、各事務所との直接のお取り決めになります。</p>
<a class="cta" href="{TEL}" data-ev="souzoku_tel">☎ 電話で相続の相談をする（050-3696-4531）</a></section>
{SOUZOKU_FORM}
<div class="pair"><a class="p2" href="#" onclick="history.back();return false;">← 前の画面に<br>戻る</a><a class="p1" href="#ninchi" data-v="ninchi">トップに<br>戻る</a></div>
</section>'''

OYANAKI_FORM = hear("hear-oyanaki", "親なきあとのご相談", "家族のための保障",
    q("ご相談される方", opts("相談者", ["親御さん","ご兄弟・ご姉妹","ご本人","その他のご家族","支援者の方"]))
    + q("お子さま（ご本人）の年代", opts("本人の年代", ["未成年","20代","30代","40代","50代以上"]))
    + q("気になっていること（いくつでも）", opts("気になること", ["お金の管理","住まい（グループホーム等）","見守ってくれる人","手続き・書類","保険の入り方・受取人","遺言・相続","ご兄弟・ご姉妹の負担","障害年金・制度"], multi=True))
    + q("今している備え（いくつでも）", opts("今の備え", ["生命保険","扶養共済","信託","遺言","後見","まだ何もしていない","わからない"], multi=True))).replace("<h2>かんたん見積もりメモ","<h2>かんたん相談メモ")

V_OYANAKI = f'''<section class="view" id="v-oyanaki" data-name="oyanaki">
<div class="lead"><span class="kicker">親なきあと安心設計</span><h1>親の愛を、<br>未来の安心へ。</h1><p>親がいなくなっても、愛情が途切れないように。障がいのあるお子さまの「親なきあと」の備えを、ご家族と一緒に考えます。</p></div>
<section class="box" style="border:2px solid #1f5c4a"><p style="margin:0;line-height:1.8">📞 <b>ご家族のどなたからでもご相談いただけます。</b>国家資格ファイナンシャルプランナー・行政書士資格保有者がお話をうかがい、ご希望の方には弁護士・司法書士・税理士などへ<b>無料でお取り次ぎ</b>します。現在のところ<b>全国対応</b>しています。</p></section>
<section class="box"><h2>😟 よくあるご不安</h2><ul class="kv">
<li><b>お金のこと</b>親がいなくなったあと、この子の生活費は足りるのか。お金の管理は誰がするのか。</li>
<li><b>住まいと暮らし</b>今の家に住み続けられるのか。グループホームや施設はどうするのか。</li>
<li><b>見守る人</b>ご兄弟・ご姉妹に負担をかけたくない。でも、誰に頼めばいいのか分からない。</li>
<li><b>手続き</b>障害年金、福祉サービス、契約ごと。親が全部やってきたことを、誰が引き継ぐのか。</li>
<li><b>親が入院・認知症になったら</b>通帳・支払い・契約・連絡先を、誰が把握するのか決まっていない。</li>
<li><b>何から始めればいいか</b>遺言・成年後見・家族信託・生命保険…。福祉だけでは解決できない。でも、どこに聞けばいいのか分からない。</li>
</ul></section>
<section class="box"><h2>🧭 わたしたちの考え方</h2><ul class="kv">
<li><b>本人の暮らしと希望から考える</b>財産や制度から先に決めるのではなく、お子さまの暮らしと希望を出発点にします。</li>
<li><b>「今決めること／後でよいこと」を分ける</b>論点を見える形にして、ご家族で話しやすくします。</li>
<li><b>福祉の支援者とは「横につながる」</b>相談支援専門員さんなど、今の支援者の役割はそのまま。お金・法律・相続・保険の部分だけを一緒に整理します。</li>
</ul></section>
<section class="box"><h2>📌 備えの方法（一般的なしくみ）</h2><ul class="kv">
<li><b>① 家族の情報を1冊にまとめる</b>お子さまの特性・通院先・お薬・支援者・好きなこと・苦手なこと。親が持っている「この子の取扱説明書」を、次に支える人へ残します。</li>
<li><b>② 生命保険で、お金を残す</b>受取人や受け取り方を工夫して、まとまったお金を一度に渡さず、必要な分ずつ届ける方法（生命保険信託など）もあります。</li>
<li><b>③ 心身障害者扶養共済制度</b>親が掛金を払い、親が亡くなったあと、お子さまに年金（1口 月2万円）が一生支払われる、自治体の制度です。</li>
<li><b>④ 特定贈与信託</b>障がいのある方の生活のために信託銀行などへお金を託すと、一定額（特別障害者は6,000万円、その他の特定障害者は3,000万円）まで贈与税がかかりません。</li>
<li><b>⑤ 遺言</b>遺し方を決めておかないと、相続の話し合いに障がいのあるお子さまも加わる必要があり、成年後見人が必要になることがあります。</li>
<li><b>⑥ 成年後見・任意後見・家族信託</b>お金の管理や契約を、誰がどう支えるかを元気なうちに決めておく方法です。</li>
</ul><p class="srcs">出典：国税庁（特定贈与信託）、厚生労働省（心身障害者扶養共済制度）。制度の詳細はお住まいの自治体・各機関でご確認ください。</p></section>
<section class="box"><h2>🤝 ラサール＆パートナーズにできること</h2><ul class="kv">
<li><b>家族の情報の整理</b>何を残せばいいか、一緒に整理します。</li>
<li><b>保険の点検と設計</b>今の保険が、お子さまにきちんと届く形になっているかを点検し、受取人・受け取り方まで一緒に考えます。</li>
<li><b>制度の確認</b>扶養共済・障害年金・信託など、使える制度の確認をお手伝いします。</li>
<li><b>専門家へのお取り次ぎ</b>遺言・後見・信託・税金のことは、ご希望に応じて弁護士・司法書士・税理士・行政書士へ無料でお取り次ぎします。</li>
<li><b>ご契約後の保全</b>ご契約のあとも、受取人の変更・請求・もしものときの手続きまで、ラサール クライアントデスクがLINEで24時間受付してお守りします。</li>
</ul><p class="note">お取り次ぎは無料です。専門家に正式にご依頼される場合の報酬は、各事務所との直接のお取り決めになります。</p></section>
<section class="box"><h2>🏢 相談支援専門員・支援者のみなさまへ</h2><p style="line-height:1.8">「親なきあと」を、ひとりの相談員・ひとつの家庭だけで抱えないために。福祉だけでは解けない論点（お金・法律・相続・保険）を整理する<b>30〜45分のミニ勉強会</b>も承ります。営業・商品説明を目的とした会ではありません。</p></section>
<div class="pair"><a class="p1" href="#hear-oyanaki" data-scroll="hear-oyanaki">かんたん<br>相談メモへ<small>1分・お名前は不要</small></a><a class="p2" href="{TEL}" data-ev="oyanaki_tel">電話で<br>相談する<small>050-3696-4531</small></a></div>
{DESK_MINI}
{OYANAKI_FORM}
<div class="pair"><a class="p2" href="#" onclick="history.back();return false;">← 前の画面に<br>戻る</a><a class="p1" href="#ninchi" data-v="ninchi">トップに<br>戻る</a></div>
</section>'''


V_DESK = f'''<section class="view" id="v-desk" data-name="desk">
<div class="lead"><span class="kicker">ラサール クライアントデスク</span><h1>ご契約のあとも、<br>ずっとお見守りします。</h1><p>保険は、入ってからが本番です。ネットでお申し込みの方も、ご相談から入った方も、同じ窓口でサポートします。</p></div>
<section class="box" style="border:2px solid #1f5c4a"><h2>💚 親身のお見守り活動</h2><p style="line-height:1.8;margin:0"><b>ご自宅の水漏れから、万一の保険金のお届けまで。</b>暮らしの「困った」に、ひとつの窓口で対応します。ご相談はLINEで<b>即時受付</b>しています。</p></section>
<div class="desk3"><div><b>24時間</b><span>LINEで受付</span></div><div><b>無料</b><span>各士業へお取り次ぎ</span></div><div><b>全事業</b><span>同じ窓口で対応</span></div></div>
{CASES_BOX}
<section class="box"><h2>📱 3つの窓口</h2><ul class="kv">
<li><b>ご契約後のお手続き（保全）</b>住所・お名前・口座・受取人の変更、ご契約内容の確認、給付金・保険金の請求のご案内。</li>
<li><b>事故のご連絡</b>ご自宅の水漏れ・雨漏り、車の事故なども、LINEでご連絡を受け付けます。保険会社へのお取り次ぎと、その後の進め方をご案内します。</li>
<li><b>士業へのお取り次ぎ</b>弁護士・司法書士・税理士・行政書士へ、ご希望に応じて無料でお取り次ぎします（弁護士費用特約を使いたいときもご相談ください）。</li>
</ul></section>
<section class="box"><h2>🤝 対応する事業</h2><ul class="kv">
<li><b>生命保険・医療保険・がん保険</b>ネット加入（第一ネオ生命）も、対面でのご契約も。</li>
<li><b>車・家の保険（損害保険）</b>事故のご連絡から保険会社への取り次ぎまで。</li>
<li><b>相続のご相談</b>手続きの整理、専門家・不動産会社・金融機関へのお取り次ぎ。</li>
<li><b>障がいと親なきあと</b>ご家族の情報の整理、保険の受け取り方の点検、制度や専門家へのおつなぎ。</li>
</ul></section>
<section class="box"><h2>🧭 ご利用の流れ</h2><div class="pill-steps"><div><b>1</b>LINEでラサール保険研究所を友だち追加</div><div><b>2</b>トークでご用件を送る（24時間いつでも）</div><div><b>3</b>担当者が確認して、LINE・お電話でご連絡します</div></div>
<p class="note">受付は24時間です。担当者からのご返信は営業時間内に順番に行います。<b>事故でけが人がいる・車が動かせないなど急ぐときは、下の「保険会社の連絡先」から事故受付（24時間）にもあわせてお電話ください。</b>お手続きは各保険会社の所定の方法で行います。士業に正式にご依頼される場合の報酬は、各事務所との直接のお取り決めになります。</p></section>
<section class="box" id="desk-tel"><h2>☎ 保険会社の連絡先（タップで電話）</h2><p style="line-height:1.8">担当者がすぐに動けないときや、夜間・休日に急ぐときは、ご契約の保険会社へ直接お電話ください。</p><h3 style="font-size:18px;margin:14px 0 6px">🚗 車・家の事故（24時間365日受付）</h3><a class="telrow" href="tel:0120256110" data-ev="desk_tel_sonpo"><span><b>損保ジャパン</b><small>自動車の事故</small></span><em>☎ 0120-256-110</em></a><a class="telrow" href="tel:0120727110" data-ev="desk_tel_sonpo"><span><b>損保ジャパン</b><small>火災・家・ケガなど自動車以外の事故</small></span><em>☎ 0120-727-110</em></a><a class="telrow" href="tel:0120024024" data-ev="desk_tel_sonpo"><span><b>あいおいニッセイ同和損保</b><small>自動車の事故</small></span><em>☎ 0120-024-024</em></a><a class="telrow" href="tel:0120985024" data-ev="desk_tel_sonpo"><span><b>あいおいニッセイ同和損保</b><small>火災・家など自動車以外の事故</small></span><em>☎ 0120-985-024</em></a><h3 style="font-size:18px;margin:16px 0 6px">💊 生命保険の給付金・保険金のご請求</h3><a class="telrow" href="tel:0120568093" data-ev="desk_tel_life"><span><b>アクサ生命</b><small>カスタマーサービスセンター</small></span><em>☎ 0120-568-093</em></a><a class="telrow" href="tel:0120521513" data-ev="desk_tel_life"><span><b>エヌエヌ生命</b><small>サービスセンター</small></span><em>☎ 0120-521-513</em></a><a class="telrow" href="tel:0120506053" data-ev="desk_tel_life"><span><b>オリックス生命</b><small>保険金・給付金お問合せ窓口</small></span><em>☎ 0120-506-053</em></a><a class="telrow" href="tel:0120226201" data-ev="desk_tel_life"><span><b>第一ネオ生命</b><small>コンタクトセンター</small></span><em>☎ 0120-226-201</em></a><a class="telrow" href="tel:0120279481" data-ev="desk_tel_life"><span><b>日本生命</b><small>保険金・給付金ダイヤル</small></span><em>☎ 0120-279-481</em></a><a class="telrow" href="tel:0120873917" data-ev="desk_tel_life"><span><b>はなさく生命</b><small>お客様コンタクトセンター</small></span><em>☎ 0120-8739-17</em></a><a class="telrow" href="tel:0120063730" data-ev="desk_tel_life"><span><b>マニュライフ生命</b><small>コールセンター</small></span><em>☎ 0120-063-730</em></a><a class="telrow" href="tel:0120881796" data-ev="desk_tel_life"><span><b>メットライフ生命</b><small>カスタマーサービスセンター（保険金・給付金）</small></span><em>☎ 0120-881-796</em></a><p class="note">生命保険会社の窓口は24時間ではありません（受付時間は各社でご確認ください）。お電話のときは証券番号をお手元にご用意ください。番号は各社・生命保険文化センター等の公表情報（2026年時点）にもとづきます。お電話のあとも、ラサール クライアントデスクにLINEでひと言いただければ、その後の進め方をお手伝いします。</p></section>
<div class="pair"><a class="p1" href="{LINE}" target="_blank" rel="noopener noreferrer" data-ev="desk_line">LINEで<br>連絡する<small>24時間受付</small></a><a class="p2" href="{TEL}" data-ev="desk_tel">電話で<br>相談する<small>050-3696-4531</small></a></div>
<div class="pair"><a class="p2" href="#" onclick="history.back();return false;">← 前の画面に<br>戻る</a><a class="p1" href="#ninchi" data-v="ninchi">トップに<br>戻る</a></div>
</section>'''

V_COMP = f'''<section class="view" id="v-companies" data-name="companies">
<div class="lead"><span class="kicker">ラサール＆パートナーズ</span><h1>取扱保険会社一覧</h1><p>複数の保険会社をくらべてご提案する、乗合代理店です。</p></div>
<section class="box complist"><h3>生命保険</h3><ul>{''.join('<li>'+c+'保険</li>' for c in LIFE_CO)}</ul><h3>損害保険</h3><ul><li>損害保険ジャパン</li><li>あいおいニッセイ同和損害保険</li></ul>
<p class="note">取扱保険会社の商品でも、お取り扱いできない場合があります。ネットでのお申込みは、第一ネオ生命の商品が対象です。</p></section>
<div class="pair"><a class="p2" href="#" onclick="history.back();return false;">← 前の画面に<br>戻る</a><a class="p1" href="#ninchi" data-v="ninchi">トップに<br>戻る</a></div>
</section>'''

V_OYA = f'''<section class="view" id="v-oya" data-name="oya">
<div class="lead"><span class="kicker">親御さんの保険</span><h1>親の保険のこと、<br>一緒に考えます。</h1><p>ご年齢やご希望をうかがって、合う方法をご案内します。</p></div>
<section class="box"><div class="pill-steps"><div><b>1</b>親御さんのご年齢と、気になっていることを教えてください</div><div><b>2</b>担当がお調べして、LINE・お電話でご案内します</div><div><b>3</b>ご家族で話し合ってから決めて大丈夫です</div></div></section>
{OYA_FORM}
<a class="cta line" data-ev="oya_line" href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで相談する</a>
<a class="cta sub" data-ev="oya_form" href="{FORM}" target="_blank" rel="noopener noreferrer">フォームで相談する</a>
<a class="cta sub" href="#over70" data-v="over70">親御さんが70歳以上なら、こちらが早いです</a>
<div class="pair"><a class="p2" href="#" onclick="history.back();return false;">← 前の画面に<br>戻る</a><a class="p1" href="#ninchi" data-v="ninchi">トップに<br>戻る</a></div>
{AFTER_MINI}
</section>'''

JS = r'''<script>(function(){var b=document.getElementById("c-go");if(!b)return;
function v(id){var x=parseFloat(document.getElementById(id).value);return isNaN(x)||x<0?0:x;}
function tx(a){var t=[[1000,.10,0],[3000,.15,50],[5000,.20,200],[10000,.30,700],[20000,.40,1700],[30000,.45,2700],[60000,.50,4200],[1e12,.55,7200]];for(var i=0;i<t.length;i++){if(a<=t[i][0])return Math.max(0,a*t[i][1]-t[i][2]);}return 0;}
function f(n){return Math.round(n).toLocaleString("ja-JP");}
b.addEventListener("click",function(){var sp=+document.getElementById("c-sp").value,ch=+document.getElementById("c-ch").value,n=sp+ch;
var li=v("c-li"),liFree=Math.min(li,500*n),gross=v("c-dep")+v("c-re")+v("c-st")+(li-liFree)-v("c-db");if(gross<0)gross=0;
var base=3000+600*n,taxable=Math.max(0,gross-base),total=0,spShare=sp?0.5:0,chShare=sp?0.5/ch:1/ch;
if(sp)total+=tx(taxable*spShare);for(var i=0;i<ch;i++)total+=tx(taxable*chShare);
var after=sp?total*(1-spShare):total;
var r=document.getElementById("c-res");r.hidden=false;
r.innerHTML="法定相続人："+n+"人<br>課税される財産（保険の非課税枠 "+f(liFree)+"万円を引いた後）："+f(gross)+"万円<br>基礎控除："+f(base)+"万円<br>"+(taxable<=0?"<b>相続税はかからない見込み</b>（基礎控除の範囲内）":"家族全体の相続税の目安：<b>約"+f(after)+"万円</b>"+(sp?"<br><small>（配偶者の税額軽減を使った場合。使わない場合の総額は約"+f(total)+"万円）</small>":""))+"<br><small>※学習用の一般的な試算です。実際の税額は税理士にご確認ください。</small>";
try{if(window.gtag)gtag("event","souzoku_calc");}catch(e){}});})();</script><div class="toast" id="toast"></div><script>
(function(){
var views=["ninchi","gan","jibyo","over70","sonpo","souzoku","soudan","oya","oyanaki","desk","companies"];
function ev(n,p){try{if(window.gtag){var q={transport_type:"beacon",page:"ninchisho_v2"};var s=sessionStorage.getItem("src");if(s)q.src=s;for(var k in(p||{}))q[k]=p[k];gtag("event",n,q);}}catch(e){}}
function show(v,push){if(views.indexOf(v)<0)v="ninchi";views.forEach(function(x){document.getElementById("v-"+x).classList.toggle("on",x===v);});
document.querySelectorAll(".tabs6 a").forEach(function(a){if(a.getAttribute("data-v")===v)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});
if(push)history.pushState(null,"","#"+v);window.scrollTo(0,0);ev("view_"+v);}
var tg=document.getElementById("tabtg"),nv=document.getElementById("tabs-nav");
function fold(c,user){nv.classList.toggle("closed",c);tg.classList.toggle("open",c);tg.setAttribute("aria-expanded",c?"false":"true");tg.textContent=c?"☰ ご相談メニュー（10個）をひらく ▼":"▲ メニューをたたんで、下へ読み進める";try{sessionStorage.setItem("tabfold",c?"1":"0");}catch(e){}if(user)ev(c?"menu_fold":"menu_open");}
if(tg&&nv){tg.addEventListener("click",function(){var c=!nv.classList.contains("closed");fold(c,true);if(c){var m=document.getElementById("main-content");if(m)m.scrollIntoView({behavior:"smooth",block:"start"});}});
try{if(sessionStorage.getItem("tabfold")==="1")fold(true,false);}catch(e){}}
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-v]");if(!a)return;e.preventDefault();if(nv&&a.closest("#tabs-nav"))fold(true,false);show(a.getAttribute("data-v"),true);});
window.addEventListener("popstate",function(){show(location.hash.slice(1),false);});
show(location.hash.slice(1)||"ninchi",false);
// がんチェック
var GC={nyuin:"入院したとき、1日いくら・何日まで出るか",shujutsu:"手術を受けたときにお金が出るか",hoshasen:"放射線治療が対象か",kouganzai:"抗がん剤治療が対象か（通院でも出るか）",horumon:"ホルモン剤の治療が対象か（期間が長くなりやすい治療です）",shindan:"がんと診断されたときに、治療の方法を問わず一時金が出るか",sensin:"先進医療の技術料が対象か（公的保険の対象外です）",shunyu:"仕事を休んだ分の収入の減り方に備えられるか（一時金はそのまま生活費にも使えます）"};
var gb=document.getElementById("gc-go");if(gb)gb.addEventListener("click",function(){var l=document.getElementById("gc-list");l.innerHTML="";var c=[].slice.call(document.querySelectorAll("#gc input:checked"));if(!c.length)c=[].slice.call(document.querySelectorAll("#gc input"));c.forEach(function(i){var li=document.createElement("li");li.textContent=GC[i.value];l.appendChild(li);});var r=document.getElementById("gc-res");r.classList.add("show");r.scrollIntoView({behavior:"smooth",block:"center"});ev("sc_gan_done",{n:c.length});});
// 持病チェック
var jb=document.getElementById("jc-go");if(jb)jb.addEventListener("click",function(){var n=document.querySelectorAll("#jc input:checked").length;var h=document.getElementById("jc-h"),p=document.getElementById("jc-p");if(n){h.textContent="入りやすい保険も、選べます";p.textContent="あてはまるものが"+n+"つありました。持病があっても入りやすい保険があります。ふつうの保険に入れる場合もあるので、まずは試算か、ご相談で確かめてみてください。";}else{h.textContent="ふつうの医療保険から見てみましょう";p.textContent="あてはまるものがなければ、ふつうの医療保険のほうが保険料をおさえられることが多いです。迷ったらご相談ください。";}var r=document.getElementById("jc-res");r.classList.add("show");r.scrollIntoView({behavior:"smooth",block:"center"});ev("sc_jibyo_done",{n:n});});
// 70歳以上
var by=document.getElementById("birth");if(by){var y=new Date().getFullYear();for(var a=70;a<=95;a++){var yr=y-a;var o=document.createElement("option");var sh=yr-1925;o.value=yr+"年（昭和"+sh+"年）";o.textContent=yr+"年（昭和"+sh+"年）ごろ";by.appendChild(o);}}
document.querySelectorAll('input[name="co"]').forEach(function(r){r.addEventListener("change",function(){document.getElementById("co-name").style.display=r.value==="ある"&&r.checked?"block":"none";});});
function vals(n){return [].slice.call(document.querySelectorAll('[data-n="'+n+'"] input:checked')).map(function(i){return i.value;}).join("・");}
function memo(){var co=vals("co");if(co==="ある"){var nm=document.getElementById("co-name").value.trim();co="ある"+(nm?"（"+nm+"）":"");}
return "【70歳以上の方のご相談】\n探している保険："+(vals("kind")||"未選択")+"\n希望の保険会社："+(co||"未選択")+"\n性別："+(vals("sex")||"未選択")+"\nお生まれの年："+(by&&by.value||"未選択")+"\n生年月日（くわしく）：\n知りたいこと："+(vals("want")||"未選択")+"\nご連絡方法："+(vals("how")||"未選択");}
var FORM="__FORM__";
var fg=document.getElementById("f70-go");if(fg)fg.addEventListener("click",function(){var how=vals("how");var map={"LINE":"LINE","電話":"電話","メール":"メール"};var u=FORM+"?usp=pp_url&entry.777293406="+encodeURIComponent("家族のための保障")+"&entry.245163664="+encodeURIComponent(memo())+(map[how]?"&entry.2058551988="+encodeURIComponent(map[how]):"");ev("over70_form",{kind:vals("kind")});window.open(u,"_blank","noopener");});
var fl=document.getElementById("f70-line");if(fl)fl.addEventListener("click",function(e){e.preventDefault();window.open(OA+encodeURIComponent(memo()),"_blank","noopener");});

var OA="https://line.me/R/oaMessage/%40375swnrk/?";
// 案2：広告の動画ごとに最初の画面を変える
var src="";try{src=new URLSearchParams(location.search).get("src")||sessionStorage.getItem("src")||"";}catch(e){}
var H={soba:/soba/,jihyo:/jihyo|lumiere_ninchi|kashimasa_ninchi/};
for(var k in H){if(H[k].test(src)){var el=document.getElementById("hero-"+k);if(el){el.hidden=false;var d=document.getElementById("hero-default");if(d)d.hidden=true;ev("hero_"+k);}}}
// 案1：結果をLINEに保存・家族に送る
function resultText(kind){if(kind==="ninchi"){return "【認知症・介護のセルフチェック結果】\n介護にかかるお金の目安："+(document.getElementById("sc-total").textContent||"")+"\n使えそうなお金の目安："+(document.getElementById("sc-have").textContent||"")+"\n"+(document.getElementById("sc-gap").textContent||"");}
if(kind==="gan"){return "【がん保険チェックの結果】\n確かめたいこと：\n"+[].slice.call(document.querySelectorAll("#gc-list li")).map(function(l){return "・"+l.textContent;}).join("\n");}
if(kind==="jibyo"){return "【持病チェックの結果】\n"+document.getElementById("jc-h").textContent+"\n"+document.getElementById("jc-p").textContent;}return "";}
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("[data-keep],[data-share]");if(!a)return;e.preventDefault();
if(a.hasAttribute("data-keep")){var k=a.getAttribute("data-keep");ev("keep_line_"+k);window.open(OA+encodeURIComponent(resultText(k)+"\n\n（保存用に送ります）"),"_blank","noopener");return;}
var v=a.getAttribute("data-share");var url=location.origin+location.pathname+"#"+v;var msg={ninchi:"認知症の備え、3つの数字とかんたんチェックがあったよ。いっしょに見てみない？",gan:"がんの備え、どの治療に備えるかチェックできるページがあったよ。",jibyo:"持病があっても入りやすい保険のこと、わかりやすいページがあったよ。"}[v]||"保険のこと、わかりやすいページがあったよ。";ev("share_family_"+v);
if(navigator.share){navigator.share({text:msg,url:url}).catch(function(){});}else{window.open("https://line.me/R/share?text="+encodeURIComponent(msg+"\n"+url),"_blank","noopener");}});
// 認知症セルフチェックの結果の下にもボタンを出す
var sr=document.getElementById("sc-res");if(sr){var d2=document.createElement("div");d2.innerHTML='<div class="keep"><a href="#" class="k-line" data-keep="ninchi">📩 この結果を<br>LINEに保存</a><a href="#" class="k-fam" data-share="ninchi">👪 家族に<br>このページを送る</a></div>';sr.appendChild(d2.firstChild);}

// 見積もりメモ（損保）
document.querySelectorAll('#house-type input').forEach(function(r){r.addEventListener("change",function(){document.getElementById("hs-rent").classList.toggle("on",r.value.indexOf("賃貸")===0);document.getElementById("hs-own").classList.toggle("on",r.value.indexOf("持ち家")===0);});});
function hearText(id){var s=document.getElementById(id);var out=["【"+s.getAttribute("data-title")+"】"];
s.querySelectorAll(".hf").forEach(function(h){if(h.closest(".house-sub")&&!h.closest(".house-sub").classList.contains("on"))return;var lab=h.querySelector(".ql").childNodes[0].textContent.replace(/[？?]$/,"");var v=[];
h.querySelectorAll("input:checked").forEach(function(i){v.push(i.value);});h.querySelectorAll("select,input[type=text],textarea").forEach(function(i){if(i.value.trim())v.push(i.value.trim());});out.push(lab+"："+(v.join("・")||"－"));});return out.join("\n");}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("[data-send],[data-sendform]");if(!b)return;var id=b.getAttribute("data-send")||b.getAttribute("data-sendform");var txt=hearText(id);
if(b.hasAttribute("data-send")){ev("hear_line_"+id);window.open(OA+encodeURIComponent(txt),"_blank","noopener");}
else{ev("hear_form_"+id);var cat=document.getElementById(id).getAttribute("data-cat")||"自動車・火災・ケガの保険";var how=document.querySelector("#"+id+" input[name=\"連絡方法\"]:checked");window.open(FORM+"?usp=pp_url&entry.777293406="+encodeURIComponent(cat)+"&entry.245163664="+encodeURIComponent(txt)+(how?"&entry.2058551988="+encodeURIComponent(how.value):""),"_blank","noopener");}});

document.querySelectorAll("[data-sub2]").forEach(function(b){b.addEventListener("click",function(){var s=b.getAttribute("data-sub2");document.querySelectorAll("[data-sub2]").forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false");});document.querySelectorAll(".sub2").forEach(function(d){d.classList.toggle("on",d.id==="s2-"+s);});ev("etc_tab_"+s);});});
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("[data-scroll]");if(!a)return;e.preventDefault();var el=document.getElementById(a.getAttribute("data-scroll"));if(el)el.scrollIntoView({behavior:"smooth"});});
// 損保のサブタブ
var cur="car";document.querySelectorAll(".seg button").forEach(function(b){b.addEventListener("click",function(){cur=b.getAttribute("data-sub");document.querySelectorAll(".seg button").forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false");});["car","fire","etc"].forEach(function(s){document.getElementById("s-"+s).classList.toggle("on",s===cur);});ev("sonpo_tab_"+cur);});});
var sg=document.getElementById("sp-go");if(sg)sg.addEventListener("click",function(){var name={car:"自動車保険",fire:"火災保険",etc:"その他の損害保険"}[cur];var box={car:"cc",fire:"fc",etc:"ec"}[cur];var picks=[].slice.call(document.querySelectorAll("#"+box+" input:checked")).map(function(i){return i.value;}).join("・");var memo="【"+name+"の見積もり・相談】\n気になっていること："+(picks||"未選択")+"\n";var u=FORM+"?usp=pp_url&entry.777293406="+encodeURIComponent(cur==="etc"&&picks.indexOf("会社")>-1?"会社・お店の保険":"自動車・火災・ケガの保険")+"&entry.245163664="+encodeURIComponent(memo);ev("sonpo_form",{kind:cur});window.open(u,"_blank","noopener");});
// 相談テーマ → フォーム（選んだ内容入り）
document.querySelectorAll("[data-topic]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var u=FORM+"?usp=pp_url&entry.777293406="+encodeURIComponent(a.getAttribute("data-topic"))+"&entry.245163664="+encodeURIComponent("相談したいこと："+a.textContent.trim()+"\n");window.open(u,"_blank","noopener");});});
})();
</script>'''.replace('__FORM__', FORM).replace('__LINE__', LINE)

html = ('<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex"><title>認知症・がん・保険のご相談｜ラサール＆パートナーズ</title>'
        '<style>' + head_css + CSS + '</style></head><body><div class="wrap">' + TOP + '<main id="main-content"><a class="tkband" href="#tokuten" data-scroll="tokuten" data-ev="tokuten_band">🎁 <b>無料特典</b>：お金と制度の早わかり表（PDF・ボタン1つでダウンロード）／LINE登録でお孫さんが主役の紙芝居ドラマ <span>受け取る ›</span></a>'
        + V_NINCHI + V_GAN + V_JIBYO + V_70 + V_SONPO + V_SOUZOKU + V_SOUDAN + V_OYA + V_OYANAKI + V_DESK + V_COMP + '</main>' + TOKUTEN_BOX + DESK_BAND + LEGAL + FOOT + '</div>'
        + SC_JS + EV_JS + JS + '<script src="/analytics.js?v=20261116b"></script></body></html>')
import os
os.makedirs('/home/claude/lp/ninchisho/v2', exist_ok=True)
# ---- 2026-11-16 23:3x 小林さん承認：Neoへのボタンはすべて汎用版（ent2）へ。押すと「見方の案内」を先に出す ----
import re as _re
_NEO_POS = {'type=014014': ('6', '認知症保険 toスマイル'),
            'type=014015': ('3', 'がん保険 ネオdeがんちりょう'),
            'type=014002': ('2', 'ネオdeいりょう 健康プロモート（持病がある方の医療保険）')}
def _neo_fix(m):
    a = m.group(0)
    href = _re.search(r'href="([^"]+)"', a).group(1)
    pos, name = '', ''
    for k, v in _NEO_POS.items():
        if k in href: pos, name = v
    a = a.replace('href="%s"' % href, 'href="#neo-guide"', 1).replace(' target="_blank" rel="noopener noreferrer"', '', 1)
    a = a.replace('class="', 'data-guide="1" data-pos="%s" data-prod="%s" class="' % (pos, name), 1)
    a = a.replace('保険料を見てみる', '保障の中身と保険料を見る').replace('保険料を<br>見てみる', '保障と保険料を<br>見てみる')
    if pos:
        a = a.replace('</small></a>', '<span class="neopos">第一ネオのページの上から%s番目「%s」</span></small></a>' % (pos, name.split('（')[0]), 1)
    return a
html = _re.sub(r'<a [^>]*class="[^"]*js-neo[^"]*"[^>]*>.*?</a>', _neo_fix, html, flags=_re.S)
NEO_GUIDE_JS = r"""<script>
(function(){
var ALL="%s",LINE="%s";
var LIST=[["1","医療保険 ネオdeいりょう","入院・手術・三大疾病"],["2","ネオdeいりょう 健康プロモート","持病がある方の医療保険"],["3","がん保険 ネオdeがんちりょう","がんの治療"],["4","ネオde3疾病サポート","がん・心臓・脳の病気"],["5","健康年齢で保険料がきまる保険","8大生活習慣病"],["6","認知症保険 toスマイル","認知症・介護"]];
function ev(n){try{if(window.gtag)gtag("event",n,{transport_type:"beacon",page:"ninchisho"});}catch(e){}}
function close(){var b=document.querySelector(".ng-bg");if(b)b.remove();}
function open(pos,name,orig){
 close();
 var where=pos?('開いたページを下へ進み、<b>上から<span class="pos">'+pos+'番目</span>の「'+name+'」</b>を選び、その横の<b>「インターネットでお申込み」</b>を押します。'):('開いたページに、保険が上から順に並んでいます。<ol class="nglist">'+LIST.map(function(x){return '<li>上から'+x[0]+'番目：<b>'+x[1]+'</b>（'+x[2]+'）</li>';}).join('')+'</ol>入りたい保険を選び、その横の<b>「インターネットでお申込み」</b>を押します。');
 var h='<div class="ng" role="dialog" aria-label="第一ネオ生命のページの見方"><button class="ngx" type="button" aria-label="閉じる">×</button>'
 +'<h3>第一ネオ生命のページは、この順で進んでください</h3>'
 +'<div class="ngkey">保険料が出たら、まず<u>「どんなときに・どんな保障が受けられるか」</u>を確認するのがコツです。</div>'
 +'<ol><li>'+where+'<br><small>※「商品パンフレット」はPDFが開いて戻りにくくなるので、押さなくて大丈夫です。</small></li>'
 +'<li><b>生年月日と性別</b>を入れて、<b>「保険料見積もりスタート」</b>を押します。<br><small>※保険料を見るだけなら、お申込みにはなりません。ご安心ください。</small></li>'
 +'<li>月払の保険料が出ます。<b>右上の青い文字「ⓘ商品詳細」</b>を押してください。<b>どんなときに、どんな保障が受けられるか</b>と、商品の特徴が書いてあります。</li>'
 +'<li><b>「プラン内容を確認・変更する」</b>で、保障の金額を選べます。金額を変えると、保険料も変わります。</li>'
 +'<li>ご納得いただけたら、ほかに入っておきたい保険がないかも一応見てみてください。一番下の<b>「結果を保存」</b>で保存もできます。</li>'
 +'<li>右下のオレンジのボタン<b>「申込み手続きに進む」</b>→確認事項→青いボタン<b>「申込み手続きに進む」</b>の順に進みます。ここから、メールアドレスなどを入れてスマホでお申込みできます。</li></ol>'
 +'<div class="ngkey" style="background:#eaf3ef;border-color:#1f5c4a">途中でわからなくなったら、すぐこのページに戻って、LINEかお電話でご連絡ください。操作をサポートします。</div>'
 +'<a class="nggo js-neo" href="'+ALL+'" target="_blank" rel="noopener noreferrer" data-go="1" data-ev="'+(orig||"neo_guide")+'">第一ネオ生命のページを開く</a>'
 +'<a class="ngline" href="'+LINE+'" target="_blank" rel="noopener noreferrer" data-ev="neo_guide_line">先にLINEで相談する（無料）</a>'
 +'<a class="ngline" href="tel:05036964531" data-ev="neo_guide_tel" style="background:#fff;color:#1f5c4a;border:2px solid #1f5c4a;margin-top:8px">電話で聞く　050-3696-4531</a>'
 +'<p class="note" style="margin:8px 0 0">保険料を見るだけなら、お申込みにはなりません。</p></div>';
 var bg=document.createElement("div");bg.className="ng-bg";bg.innerHTML=h;document.body.appendChild(bg);
 bg.addEventListener("click",function(e){if(e.target===bg||e.target.classList.contains("ngx")){ev("neo_guide_close");close();}});
 bg.querySelector(".nggo").addEventListener("click",function(){setTimeout(close,300);});
 ev("neo_guide_open");
}
window.__openNeoGuide=open;
document.addEventListener("click",function(e){
 var a=e.target.closest&&e.target.closest('a[data-guide="1"]');if(!a)return;
 e.preventDefault();e.stopPropagation();
 open(a.getAttribute("data-pos")||"",a.getAttribute("data-prod")||"",a.getAttribute("data-ev")||"");
},true);
document.addEventListener("click",function(e){
 var w=e.target.closest&&e.target.closest("[data-who]");if(!w)return;
 e.preventDefault();var v=w.getAttribute("data-who");
 var r=document.querySelector('#hear-70 input[name="相談の立場"][value="'+v+'"]');if(r){r.checked=true;r.dispatchEvent(new Event("change",{bubbles:true}));}
 var t=document.getElementById("hear-70");if(t)t.scrollIntoView({behavior:"smooth",block:"start"});
});
})();
</script>""" % (NEO_ALL.replace('&amp;','&'), LINE)
html = html.replace('</body></html>', NEO_GUIDE_JS + '</body></html>')

open('/home/claude/lp/ninchisho/v2/index.html', 'w', encoding='utf8').write(html)
print(len(html))
