// 訪問・ボタンタップの計測（Googleアナリティクス GA4）
// 測定IDが空のあいだは何も送信しません。発行後に下の ID を入れてください（例 "G-XXXXXXXXXX"）。
(function(){
  var GA_ID = "G-ERPXVZ39RD";
  if(!GA_ID) return;

  // 流入元（?src=ig / ?src=yt など）を覚えておく
  var src = "";
  try{
    src = new URLSearchParams(location.search).get("src") || "";
    if(src){ sessionStorage.setItem("src", src); } else { src = sessionStorage.getItem("src") || ""; }
  }catch(e){}

  var s = document.createElement("script");
  s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  var cfg = {};
  if(src){ cfg.src = src; cfg.campaign_source = src; cfg.campaign_medium = "social"; }
  gtag("config", GA_ID, cfg);

  // Metaピクセル（2026-11-11追加・小林さん承認。データセット「保険LP hoken.lasalle2023.com」）
  // 広告の最適化用。送るのはページ表示・滞在10秒・ボタン押下の種類と src だけ（質問の答えなど個人の情報は送らない）。
  // 社内確認（src に check / maki / test を含む）は送らない。
  var META_PIXEL_ID = "3842260025928077";
  var fbOn = META_PIXEL_ID && !/check|maki|test/i.test(src);
  if(fbOn){
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq("init", META_PIXEL_ID);
    fbq("track", "PageView");
  }
  // GA4のイベント名 → Metaの標準イベント（Lead＝自分で申込へ進む、Contact＝相談・問い合わせ）
  var FB_MAP = { neo: "Lead", line: "Contact", line_msg: "Contact", tel: "Contact", shoken_check: "Contact", form: "Contact" };
  function fb(name){
    if(!fbOn || !window.fbq) return;
    var p = src ? { src: src } : {};
    if(FB_MAP[name]) fbq("track", FB_MAP[name], p);
    else if(name === "stay_10s") fbq("trackCustom", "Stay10s", p);
  }

  function send(name){ gtag("event", name, src ? { src: src } : {}); fb(name); }

  // 滞在・スクロールの計測（2026-11-09追加）
  // Instagramのアプリ内ブラウザでは滞在時間が0秒と記録されやすいため、
  // 画面が表示されている時間を自前で数え、3秒・10秒の到達をイベントで送る。
  // stay_3s / stay_10s が来ているのに滞在0秒のセッションは「測れていないだけ」と判断できる。
  function sendNow(name, extra){
    var p = { transport_type: "beacon" };
    if(src) p.src = src;
    if(extra) for(var k in extra) p[k] = extra[k];
    gtag("event", name, p);
    fb(name);
  }
  var visibleMs = 0, lastTick = Date.now(), sentStay = {};
  function tick(){
    var now = Date.now();
    if(document.visibilityState === "visible") visibleMs += now - lastTick;
    lastTick = now;
    [3, 10, 30].forEach(function(sec){
      if(!sentStay[sec] && visibleMs >= sec * 1000){ sentStay[sec] = true; sendNow("stay_" + sec + "s"); }
    });
  }
  setInterval(tick, 500);
  document.addEventListener("visibilitychange", function(){ lastTick = Date.now(); });

  var sentScroll = {};
  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if(h <= 0) return;
    var pct = (window.scrollY || document.documentElement.scrollTop) / h * 100;
    [25, 50, 75, 90].forEach(function(t){
      if(!sentScroll[t] && pct >= t){ sentScroll[t] = true; sendNow("scroll_" + t, { percent_scrolled: t }); }
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a");
    if(!a || a.getAttribute("aria-disabled") === "true") return;
    var href = a.getAttribute("href") || "";
    if(a.classList.contains("js-neo") && href.indexOf("neofirst.co.jp") > -1) send("neo");
    else if(a.classList.contains("js-shoken")) send("shoken_check");
    else if(a.classList.contains("js-line-msg")) send("line_msg");
    else if(a.classList.contains("js-tokuten-pdf")) send("tokuten_pdf");
    else if(a.classList.contains("js-howto")) return;
    else if(href.indexOf("lin.ee/") > -1 || href.indexOf("line.me/") > -1) send("line");
    else if(href.indexOf("tel:") === 0) send("tel");
    else if(href.indexOf("docs.google.com/forms") > -1) send("form");
  }, true);

  // 「迷ったらLINE」（2026-11-13追加・小林さん承認）
  // 第一ネオ生命の画面へ移ったあと、このページに戻ってきた人に一度だけ、LINEで聞ける案内を下から出す。
  // ねらい：Neoのボタンは押されているのに申込0件のため、途中で迷った人を相談（LINE）で拾う。
  // 計測：表示＝neo_return、LINEを押した＝neo_return_line（＋共通の line）、閉じた＝neo_return_close
  var LINE_URL = "https://lin.ee/5gJWVqG";
  var leftForNeo = false, returnShown = false;
  try{ returnShown = sessionStorage.getItem("neo_return_shown") === "1"; }catch(e){}
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a.js-neo");
    if(a && (a.getAttribute("href") || "").indexOf("neofirst.co.jp") > -1){
      leftForNeo = true;
      try{ sessionStorage.setItem("neo_left", "1"); }catch(_){}
    }
  }, true);
  function showReturn(){
    if(returnShown) return;
    returnShown = true;
    try{ sessionStorage.setItem("neo_return_shown", "1"); }catch(_){}
    var st = document.createElement("style");
    st.textContent = ".neo-return{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#fff;border-top:3px solid #9a5a12;box-shadow:0 -6px 24px #18221f33;padding:16px 16px 20px;font:18px/1.6 'BIZ UDPGothic','Hiragino Sans','Yu Gothic','Meiryo',sans-serif;color:#18221f}"
      + ".neo-return .in{max-width:760px;margin:auto}.neo-return p{margin:0 0 4px;font-size:21px;font-weight:700;line-height:1.45;padding-right:40px}"
      + ".neo-return small{display:block;font-size:17px;color:#4f5c57;margin-bottom:12px}"
      + ".neo-return a{display:flex;justify-content:center;align-items:center;min-height:58px;border-radius:12px;background:#06c755;color:#fff;font-size:21px;font-weight:700;text-decoration:none}"
      + ".neo-return button{position:absolute;top:8px;right:10px;width:44px;height:44px;border:0;background:none;font-size:28px;color:#4f5c57;cursor:pointer}";
    document.head.appendChild(st);
    var box = document.createElement("div");
    box.className = "neo-return";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", "迷ったらLINEで聞けます");
    box.innerHTML = '<div class="in"><button type="button" aria-label="閉じる">×</button>'
      + '<p>申込みの画面で迷いましたか？</p>'
      + '<small>どの保険がいいか、ご家族の分など、LINEでそのまま聞けます。無料です。聞いても申し込まなくて大丈夫です。</small>'
      + '<a href="' + LINE_URL + '" target="_blank" rel="noopener noreferrer" data-ev="neo_return_line">LINEで聞いてみる</a></div>';
    document.body.appendChild(box);
    sendNow("neo_return");
    box.querySelector("a").addEventListener("click", function(){
      // /ninchisho/ はページ側の data-ev 計測が送るので二重に送らない
      if(!/\/ninchisho\//.test(location.pathname)) sendNow("neo_return_line");
      box.remove();
    });
    box.querySelector("button").addEventListener("click", function(){ sendNow("neo_return_close"); box.remove(); });
  }
  // 別タブのNeoから戻った（このタブが再び表示された・前面に戻った）
  function backFromNeo(){
    if(leftForNeo && document.visibilityState === "visible") setTimeout(showReturn, 600);
  }
  document.addEventListener("visibilitychange", backFromNeo);
  window.addEventListener("focus", function(){ if(leftForNeo) setTimeout(showReturn, 600); });
  // 同じタブでNeoへ行き「戻る」で帰ってきた（パソコン・アプリ内ブラウザで多い。
  // 戻ったページがそのまま復元される場合も、読み直される場合も出す）
  window.addEventListener("pageshow", function(){
    var left = false;
    try{ left = sessionStorage.getItem("neo_left") === "1"; }catch(_){}
    if(left){ leftForNeo = true; setTimeout(showReturn, 600); }
  });
})();
