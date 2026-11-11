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
})();
