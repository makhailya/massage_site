(function () {
  // If GSAP fails to load or motion is reduced, the page stays fully visible.
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: "power3.out" });

  var intro = gsap.timeline({ defaults: { duration: 0.9 } });
  intro
    .from(".top__inner > *", { y: -10, autoAlpha: 0, duration: 0.6, stagger: 0.07 })
    .from(".hero__copy > *", { y: 26, autoAlpha: 0, stagger: 0.1 }, "-=.3")
    .from(".portrait", { y: 24, scale: 0.95, autoAlpha: 0, duration: 1.1 }, "-=.7")
    .from(".portrait [data-shape]", { scale: 0.6, autoAlpha: 0, duration: 1, stagger: 0.08 }, "-=.9")
    .from(".portrait__badge", { y: 10, autoAlpha: 0, duration: 0.6 }, "-=.6");

  gsap.utils.toArray("[data-reveal]").forEach(function (el) {
    gsap.from(el, {
      y: 26,
      autoAlpha: 0,
      duration: 0.85,
      scrollTrigger: { trigger: el, start: "top 90%", once: true }
    });
  });

  var stepsVertical = window.matchMedia("(max-width: 700px)").matches;
  gsap.from(".steps__line", {
    scaleX: stepsVertical ? 1 : 0,
    scaleY: stepsVertical ? 0 : 1,
    transformOrigin: stepsVertical ? "center top" : "left center",
    duration: 1.1,
    scrollTrigger: { trigger: ".steps", start: "top 85%", once: true }
  });

  // Steps animate as one staggered group; they deliberately have no
  // data-reveal attribute, otherwise two tweens would fight over opacity.
  gsap.from(".step", {
    y: 16,
    autoAlpha: 0,
    duration: 0.6,
    stagger: 0.12,
    scrollTrigger: { trigger: ".steps", start: "top 85%", once: true }
  });

  gsap.utils.toArray(".num").forEach(function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var value = { v: 0 };

    ScrollTrigger.create({
      trigger: el,
      start: "top 88%",
      once: true,
      onEnter: function () {
        el.textContent = "0";
        gsap.to(value, {
          v: target,
          duration: 1.4,
          ease: "power2.out",
          onUpdate: function () { el.textContent = Math.round(value.v); },
          onComplete: function () { el.textContent = target; }
        });
      }
    });
  });

  gsap.from(".contact__art", {
    scale: 0.9,
    autoAlpha: 0,
    duration: 1.2,
    scrollTrigger: { trigger: ".contact__panel", start: "top 80%", once: true }
  });

  window.addEventListener("load", function () { ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  }
})();
