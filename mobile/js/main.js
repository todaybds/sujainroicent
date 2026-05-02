  // 서브페이지 헤더 마킹: index가 아니면 header에 .is-sub 추가 (로고 상시 컬러 유지)
  (function () {
    var fileName = (location.pathname || '').split('/').pop().toLowerCase();
    var isMain = !fileName || fileName === 'index.html' || fileName === 'index.htm';
    if (!isMain) {
      document.addEventListener('DOMContentLoaded', function () {
        var h = document.querySelector('header');
        if (h) h.classList.add('is-sub');
      });
    }
  })();

  document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.querySelector(".menu_btn");
    const nav = document.querySelector("header nav");

    menuBtn.addEventListener("click", function () {
      menuBtn.classList.toggle("active");
      nav.classList.toggle("on");

      // 메뉴 오픈 시 헤더 배경/로고를 원본 상태로 되돌리기 위한 플래그
      var headerEl = document.querySelector("header");
      if (headerEl) headerEl.classList.toggle("menu-open", nav.classList.contains("on"));

      if (nav.classList.contains("on")) {
        // 자연스럽게 왼쪽에서 들어오게 설정
        nav.style.transition = "left 0.4s ease";
        nav.style.left = "0";
      } else {
        nav.style.transition = "left 0.4s ease";
        nav.style.left = "-100vw";
      }
    });


    // hea_drop 
$(document).ready(function () {
  $(".drop_smenu").click(function () {
    $(".drop_smenu, .smenu_wrap ul").toggleClass("active");
    $(".hea_drop").removeClass("active"); // hea_menu 비활성화
    $(".hea_menu").removeClass("active"); // hea_menu 비활성화
  });

  $(".hea_menu").click(function () {
    $(".hea_drop").toggleClass("active");
    $(".hea_menu").toggleClass("active");
    $(".drop_smenu, .smenu_wrap ul").removeClass("active"); // drop_smenu 비활성화
  });
});

// scroll magic

  //scrollmagic
  const spyEls = document.querySelectorAll(".scroll-spy");
  // console.log(spyEls)
  // const spyEls = $('section.scroll-spy') 제이쿼리
  spyEls.forEach(function (spyEl) {
    new ScrollMagic.Scene({
      triggerElement: spyEl,
      triggerHook: 0.8, //triggerhook은 trigger되는 시점을 말한다.
    })
      .setClassToggle(spyEl, "show") //요소가 화면에 보이면 show클래스 추가
      .addTo(new ScrollMagic.Controller()); //컨트롤러에 장면을 할당
  });

  $(window).scroll(function (event) {
    let st = $(this).scrollTop();
    if (st > 30) {
      $('header').addClass('scrolled');
    } else {
      $('header').removeClass('scrolled');
    }
  });
});


window.addEventListener('DOMContentLoaded', () => {
  const images = document.querySelectorAll('.sequential-img');
  images.forEach((img, index) => {
    setTimeout(() => {
      img.classList.add('visible');
    }, index * 400); // 각 이미지마다 ms 간격으로 등장
  });

    
  });


  