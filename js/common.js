$(document).ready(function () {
  $(window).scroll(function () {
    if ($(this).scrollTop() > 10) {
      $(".header").addClass("active");
    } else {
      $(".header").removeClass("active");
    }
  });
});