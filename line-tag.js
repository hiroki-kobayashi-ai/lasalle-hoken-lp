// LINEボタンに「どのページから来たか」の目印を付ける（2026-11-25 小林さん承認）
// ・ラサール保険研究所（@375swnrk）へのLINEは、認知症・がん・サイバー・コラムなど全ページが同じ窓口なので、
//   どの経路の相談かLINE側で分からなかった。最初の一言の先頭に【◯◯のページより】と src を入れて区別する。
// ・「LINEでお友だち登録する」（特典の登録）は友だち追加のリンクのまま（文面を入れられないため）。
(function(){
  var OA = "https://line.me/R/oaMessage/%40375swnrk/?";
  var p = location.pathname;
  var label =
    /^\/cyber\/shika/.test(p) ? "歯科医院のサイバー保険のページ" :
    /^\/cyber\/school/.test(p) ? "学習塾のサイバー保険のページ" :
    /^\/cyber/.test(p) ? "サイバー保険のページ" :
    /^\/ninchisho/.test(p) ? "認知症保険のページ" :
    /^\/gan/.test(p) ? "がん保険のページ" :
    /^\/column/.test(p) ? "保険コラム" :
    /^\/tokuten/.test(p) ? "特典のページ" :
    "保険のページ";
  var src = "";
  try { src = new URLSearchParams(location.search).get("src") || sessionStorage.getItem("src") || ""; } catch(e) {}
  var tag = "【" + label + "より" + (src ? "・" + src : "") + "】";

  function withTag(text){
    text = text || "";
    if (text.indexOf(tag) === 0) return text; // 付け済み
    return tag + "\n" + text;
  }
  function tagUrl(url){
    if (typeof url === "string" && url.indexOf("lin.ee/5gJWVqG") !== -1) return OA + encodeURIComponent(withTag("保険の相談をしたいです。"));
    if (typeof url !== "string" || url.indexOf(OA) !== 0) return url;
    var rest = url.slice(OA.length), txt = "";
    try { txt = decodeURIComponent(rest); } catch(e) { txt = rest; }
    return OA + encodeURIComponent(withTag(txt));
  }
  function defaultText(a){
    var t = (a.innerText || a.textContent || "");
    if (/証券|写真/.test(t)) return "保険証券の写真を送ります。";
    if (/連絡|事故|手続/.test(t)) return "契約のことで連絡です。";
    return "保険の相談をしたいです。";
  }
  function fix(){
    var links = document.querySelectorAll('a[href*="lin.ee/5gJWVqG"], a[href^="' + OA + '"]');
    for (var i = 0; i < links.length; i++){
      var a = links[i], href = a.getAttribute("href") || "";
      var txt = (a.innerText || a.textContent || "");
      if (href.indexOf("lin.ee/5gJWVqG") !== -1){
        if (/友だち登録|お友だち/.test(txt)) continue; // 特典の友だち登録はそのまま
        a.setAttribute("href", OA + encodeURIComponent(withTag(defaultText(a))));
      } else {
        a.setAttribute("href", tagUrl(href));
      }
    }
  }
  // 画面の中で文面を作って開くボタン（かんたん相談メモ・サイバーの見積依頼）にも付ける
  var open0 = window.open;
  window.open = function(url){
    var args = Array.prototype.slice.call(arguments);
    args[0] = tagUrl(url);
    return open0.apply(window, args);
  };
  // あとから画面の中で行き先が変わるボタンにも、押した瞬間に付ける
  document.addEventListener("click", function(e){
    var a = e.target && e.target.closest ? e.target.closest("a") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "", txt = (a.innerText || a.textContent || "");
    if (href.indexOf("lin.ee/5gJWVqG") !== -1 && !/友だち登録|お友だち/.test(txt)) a.setAttribute("href", OA + encodeURIComponent(withTag(defaultText(a))));
    else if (href.indexOf(OA) === 0) a.setAttribute("href", tagUrl(href));
  }, true);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fix); else fix();
})();
