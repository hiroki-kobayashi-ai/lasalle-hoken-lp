// 訪問・ボタンタップの計測（Googleアナリティクス GA4）
// 測定IDが空のあいだは何も送信しません。発行後に下の ID を入れてください（例 "G-XXXXXXXXXX"）。
(function(){
  var GA_ID = "";
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
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a");
    if(!a || a.getAttribute("aria-disabled") === "true") return;
    var href = a.getAttribute("href") || "";
    if(a.classList.contains("js-neo") && href.indexOf("neofirst.co.jp") > -1) send("neo");
    else if(href.indexOf("lin.ee/") > -1) send("line");
    else if(href.indexOf("tel:") === 0) send("tel");
    else if(href.indexOf("docs.google.com/forms") > -1) send("form");
  }, true);
})();
