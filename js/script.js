(function () {
  // If GSAP fails to load, the page stays fully visible.
  if (!window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: "power3.out" });

  var media = gsap.matchMedia();
  media.add("(prefers-reduced-motion: no-preference)", function () {
    // Never hide content already on screen when motion is enabled again.
    function belowViewport(el) {
      return el.getBoundingClientRect().top >= window.innerHeight;
    }

    gsap.utils.toArray("[data-reveal]").filter(belowViewport).forEach(function (el) {
      gsap.from(el, {
        y: 26,
        // Opacity preserves meaningful content in the accessibility tree.
        opacity: 0,
        duration: 0.85,
        scrollTrigger: { trigger: el, start: "top 90%", once: true }
      });
    });

    var steps = document.querySelector(".steps");
    if (steps && belowViewport(steps)) {
      var stepsVertical = window.matchMedia("(max-width: 700px)").matches;
      gsap.from(".steps__line", {
        scaleX: stepsVertical ? 1 : 0,
        scaleY: stepsVertical ? 0 : 1,
        transformOrigin: stepsVertical ? "center top" : "left center",
        duration: 1.1,
        scrollTrigger: { trigger: steps, start: "top 85%", once: true }
      });

      gsap.from(".step", {
        y: 16,
        opacity: 0,
        duration: 0.6,
        stagger: 0.12,
        scrollTrigger: { trigger: steps, start: "top 85%", once: true }
      });
    }

    var numbers = gsap.utils.toArray(".num").map(function (el) {
      return { el: el, text: el.textContent };
    });
    numbers.forEach(function (number) {
      if (!belowViewport(number.el)) return;
      var target = Number.parseInt(number.text, 10);
      var value = { v: 0 };

      // Create the tween inside the media context so revert cancels it too.
      gsap.to(value, {
        v: target,
        duration: 1.4,
        ease: "power2.out",
        scrollTrigger: { trigger: number.el, start: "top 88%", once: true },
        onUpdate: function () { number.el.textContent = Math.round(value.v); },
        onComplete: function () { number.el.textContent = number.text; }
      });
    });

    var art = document.querySelector(".contact__art");
    if (art && belowViewport(art)) {
      gsap.from(art, {
        scale: 0.9,
        opacity: 0,
        duration: 1.2,
        scrollTrigger: { trigger: ".contact__panel", start: "top 80%", once: true }
      });
    }

    // GSAP restores styles and removes this context's tweens/ScrollTriggers.
    // Text updates are outside CSS, so restore the original numbers explicitly.
    return function () {
      numbers.forEach(function (number) { number.el.textContent = number.text; });
    };
  });

  window.addEventListener("load", function () { ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  }
})();
