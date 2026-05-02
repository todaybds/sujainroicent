$(function () {
  let fileName = window.location.pathname.split("/").pop().split(".")[0].trim();

  // fileName이 비어있지 않고, 영문/숫자/언더스코어만 허용
  if (/^[a-zA-Z0-9_]+$/.test(fileName)) {
    $("." + fileName).addClass("tab_on");
    $(".it_" + fileName).addClass("it_on");
    $(".sm_" + fileName).addClass("smtab_on").parents(".papa").addClass("smtab_on");

    $('.tabwrap a[href]').each(function () {
      const href = $(this).attr('href').split('?')[0].split('#')[0];
      let hrefFileName = href.split("/").pop().split(".")[0].trim();

      if (hrefFileName === fileName) {
        $(this).addClass("on");
      }
    });
  }
});