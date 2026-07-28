/* Imagify — interactions
   - counter-scrolling ticker columns (scroll-linked, wheel-extended, infinite wrap)
   - grid/list view toggle with persisted choice
   - list-row hover image reveal
   All content is server-rendered in the HTML; this file only animates it. */

(function () {
  "use strict";

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- hero parallax ---------- */
  var wordmark = document.querySelector("[data-hero-wordmark]");
  if (wordmark && !prefersReduced) {
    window.addEventListener("scroll", function () {
      var y = window.scrollY;
      wordmark.style.transform = "translateY(" + y * -0.18 + "px)";
    }, { passive: true });
  }

  /* ---------- ticker belts (project browser + team) ---------- */
  function initBelts(section, opts) {
    var belts = Array.prototype.slice.call(section.querySelectorAll(".belt"));
    if (!belts.length) return null;

    var state = belts.map(function (belt, i) {
      return {
        el: belt,
        copyH: 0,
        dir: i % 2 === 0 ? 1 : -1,
        offset: opts.offsets[i % opts.offsets.length] || 0
      };
    });

    var extra = 0;          // wheel-accumulated distance past scroll end
    var raf = null;

    function measure() {
      state.forEach(function (s) {
        var copy = s.el.querySelector(".copy");
        s.copyH = copy ? copy.offsetHeight : 0;
      });
    }

    function mod(n, m) { return ((n % m) + m) % m; }

    function render() {
      raf = null;
      if (!state[0].copyH) measure();          // self-heal if measured too early
      var travel = (window.scrollY + extra) * opts.speed;
      state.forEach(function (s) {
        if (s.copyH <= 1) return;
        var t = mod(s.offset + s.dir * travel, s.copyH);
        // keep belt shifted up by one copy so wrapping is invisible both directions
        s.el.style.transform = "translateY(" + (-s.copyH + t) + "px)";
      });
    }
    function schedule() { if (!raf) raf = requestAnimationFrame(render); }

    measure();
    window.addEventListener("load", function () { measure(); schedule(); });
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", function () { measure(); schedule(); });

    if (opts.endless) {
      window.addEventListener("wheel", function (e) {
        if (section.dataset.mode === "list") return;
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var atEnd = window.scrollY >= max - 2;
        if (atEnd && e.deltaY > 0) {
          extra += e.deltaY;
          e.preventDefault();
          schedule();
        } else if (atEnd && e.deltaY < 0 && extra > 0) {
          extra = Math.max(0, extra + e.deltaY);
          e.preventDefault();
          schedule();
        }
      }, { passive: false });
    }

    schedule();
    return { schedule: schedule };
  }

  var browser = document.querySelector("[data-browser]");
  if (browser && !prefersReduced) {
    initBelts(browser, {
      speed: 0.55,
      endless: browser.dataset.endless === "true",
      offsets: [-140, -560, -60, -660]
    });
  }
  var teamSection = document.querySelector("[data-team-belts]");
  if (teamSection && !prefersReduced) {
    initBelts(teamSection, {
      speed: 0.35,
      endless: false,
      offsets: [-120, -480, -40, -600]
    });
  }

  /* ---------- grid / list toggle ---------- */
  var toggle = document.querySelector("[data-view-toggle]");
  if (toggle && browser) {
    var KEY = "imagify-view";
    function setMode(mode, persist) {
      browser.dataset.mode = mode;
      toggle.dataset.mode = mode;
      if (persist) try { sessionStorage.setItem(KEY, mode); } catch (e) {}
    }
    var saved = null;
    try { saved = sessionStorage.getItem(KEY); } catch (e) {}
    if (saved === "list" || saved === "grid") setMode(saved, false);
    toggle.addEventListener("click", function () {
      setMode(browser.dataset.mode === "grid" ? "list" : "grid", true);
    });
  }

  /* ---------- list-row hover image reveal ---------- */
  var table = document.querySelector("[data-list-table]");
  if (table) {
    var imgs = {};
    Array.prototype.forEach.call(table.querySelectorAll(".row-img"), function (im) {
      imgs[im.dataset.for] = im;
    });
    var current = null;
    table.addEventListener("mouseover", function (e) {
      var row = e.target.closest("[data-slug]");
      if (!row) return;
      var img = imgs[row.dataset.slug];
      if (img === current) return;
      if (current) current.classList.remove("show");
      current = img || null;
      if (img) {
        var r = row.getBoundingClientRect();
        var top = Math.min(Math.max(r.top - 120, 70), window.innerHeight - 420);
        img.style.top = top + "px";
        img.classList.add("show");
      }
    });
    table.addEventListener("mouseleave", function () {
      if (current) current.classList.remove("show");
      current = null;
    });
  }

  /* ---------- close pill menu when a link is chosen ---------- */
  var navBox = document.getElementById("nav-open");
  if (navBox) {
    document.querySelectorAll(".pill-nav .menu a").forEach(function (a) {
      a.addEventListener("click", function () { navBox.checked = false; });
    });
  }

  window.IMAGIFY = { ready: true, hasToggle: !!toggle, hasBrowser: !!browser };
})();
