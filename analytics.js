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

  function send(name){ gtag("event", name, src ? { src: src } : {}); }

  // 滞在・スクロールの計測（2026-11-09追加）
  // Instagramのアプリ内ブラウザでは滞在時間が0秒と記録されやすいため、
  // 画面が表示されている時間を自前で数え、3秒・10秒の到達をイベントで送る。
  // stay_3s / stay_10s が来ているのに滞在0秒のセッションは「測れていないだけ」と判断できる。
  function sendNow(name, extra){
    var p = { transport_type: "beacon" };
    if(src) p.src = src;
    if(extra) for(var k in extra) p[k] = extra[k];
    gtag("event", name, p);
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
