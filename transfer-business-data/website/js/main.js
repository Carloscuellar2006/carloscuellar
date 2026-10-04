document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Loader ---------- */
  setTimeout(function () {
    var bspLoader = document.getElementById('bsp-loader');
    if (bspLoader) bspLoader.remove();
    document.querySelectorAll('.bsp-hero .bsp-reveal').forEach(function (el, i) {
      setTimeout(function () { el.classList.add('bsp-is-visible'); }, i * 90);
    });
  }, 1300);

  /* ---------- Nav scroll state ---------- */
  var nav = document.getElementById('nav');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 40) nav.classList.add('bsp-scrolled');
    else nav.classList.remove('bsp-scrolled');
  });

  /* ---------- Mobile menu ---------- */
  var burger = document.getElementById('navBurger');
  var mobileMenu = document.getElementById('mobileMenu');
  burger.addEventListener('click', function () {
    mobileMenu.classList.toggle('bsp-open');
  });
  mobileMenu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { mobileMenu.classList.remove('bsp-open'); });
  });

  /* ---------- Scroll bsp-reveal for section headers ---------- */
  var revealTargets = document.querySelectorAll('.bsp-section-head, .bsp-intro h2, .bsp-intro-body, .bsp-check-row');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('bsp-reveal', 'bsp-is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  revealTargets.forEach(function (el) {
    el.classList.add('bsp-reveal');
    io.observe(el);
  });

  /* ---------- Before / After gallery ---------- */
  var grid = document.getElementById('galleryGrid');
  if (grid && typeof galleryData !== 'undefined') {
    galleryData.forEach(function (job) {
      var card = document.createElement('div');
      if (job.type === 'static') {
        card.className = 'bsp-ba-card bsp-ba-static';
        card.innerHTML =
          '<span class="bsp-ba-label">' + job.label + '</span>' +
          '<div class="bsp-ba-static-pair">' +
          '  <div class="bsp-ba-static-img"><img src="' + job.before + '" alt="' + job.label + ' before"><span class="bsp-ba-before-tag">Before</span></div>' +
          '  <div class="bsp-ba-static-img"><img src="' + job.after + '" alt="' + job.label + ' after"><span class="bsp-ba-after-tag">After</span></div>' +
          '</div>';
        grid.appendChild(card);
      } else {
        card.className = 'bsp-ba-card';
        card.innerHTML =
          '<span class="bsp-ba-label">' + job.label + '</span>' +
          '<div class="bsp-ba-slider" data-job="' + job.id + '">' +
          '  <img class="bsp-ba-img-before" src="' + job.before + '" alt="' + job.label + ' before">' +
          '  <div class="bsp-ba-after-wrap"><img class="bsp-ba-img-after" src="' + job.after + '" alt="' + job.label + ' after"></div>' +
          '  <div class="bsp-ba-divider"></div>' +
          '  <div class="bsp-ba-handle"><svg viewBox="0 0 24 24" fill="none" stroke="#0c0d0f" stroke-width="2"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg></div>' +
          '  <span class="bsp-ba-before-tag">Before</span>' +
          '  <span class="bsp-ba-after-tag">After</span>' +
          '</div>';
        grid.appendChild(card);
        initSlider(card.querySelector('.bsp-ba-slider'));
      }
    });
  }

  function initSlider(slider) {
    var afterWrap = slider.querySelector('.bsp-ba-after-wrap');
    var afterImg = slider.querySelector('.bsp-ba-img-after');
    var divider = slider.querySelector('.bsp-ba-divider');
    var beforeImg = slider.querySelector('.bsp-ba-img-before');

    beforeImg.addEventListener('error', showMissing);
    afterImg.addEventListener('error', showMissing);

    function showMissing() {
      if (slider.querySelector('.bsp-ba-missing')) return;
      beforeImg.style.display = 'none';
      afterWrap.style.display = 'none';
      divider.style.display = 'none';
      slider.querySelector('.bsp-ba-handle').style.display = 'none';
      var note = document.createElement('div');
      note.className = 'bsp-ba-missing';
      slider.appendChild(note);
    }

    function setPosition(percent) {
      percent = Math.max(0, Math.min(100, percent));
      var width = slider.getBoundingClientRect().width;
      afterWrap.style.width = percent + '%';
      afterImg.style.width = width + 'px';
      divider.style.left = percent + '%';
    }

    function resize() {
      var current = parseFloat(afterWrap.style.width) || 50;
      var width = slider.getBoundingClientRect().width;
      afterImg.style.width = width + 'px';
    }
    window.addEventListener('resize', resize);

    setPosition(50);

    var dragging = false;

    function pointerX(e) {
      var rect = slider.getBoundingClientRect();
      var clientX = e.touches ? e.touches[0].clientX : e.clientX;
      return ((clientX - rect.left) / rect.width) * 100;
    }

    slider.addEventListener('mousedown', function (e) { dragging = true; setPosition(pointerX(e)); });
    slider.addEventListener('touchstart', function (e) { dragging = true; setPosition(pointerX(e)); }, { passive: true });
    window.addEventListener('mousemove', function (e) { if (dragging) setPosition(pointerX(e)); });
    window.addEventListener('touchmove', function (e) { if (dragging) setPosition(pointerX(e)); }, { passive: true });
    window.addEventListener('mouseup', function () { dragging = false; });
    window.addEventListener('touchend', function () { dragging = false; });
  }

});
