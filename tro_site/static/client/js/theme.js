/**
 * Theme Effects (Dark Mode & Glassmorphism)
 * Modern UI/UX Interactions
 */

(function () {
  "use strict";

  // ========================================
  // CLEANUP REGISTRY - Track listeners for cleanup
  // ========================================

  const cleanupRegistry = {
    cardTiltListeners: new Map(),
    scrollListeners: [],
    resizeListeners: [],

    // Cleanup all registered listeners
    cleanup() {
      // Cleanup card tilt listeners
      this.cardTiltListeners.forEach((listeners, card) => {
        card.removeEventListener("mousemove", listeners.move);
        card.removeEventListener("mouseleave", listeners.leave);
      });
      this.cardTiltListeners.clear();

      // Cleanup scroll listeners
      this.scrollListeners.forEach(listener => {
        window.removeEventListener("scroll", listener);
      });
      this.scrollListeners = [];

      // Cleanup resize listeners
      this.resizeListeners.forEach(listener => {
        window.removeEventListener("resize", listener);
      });
      this.resizeListeners = [];
    },
  };

  // Expose cleanup function globally for SPA navigation
  window.themeCleanup = () => cleanupRegistry.cleanup();

  // ========================================
  // DARK MODE - ALWAYS ON (NO TOGGLE)
  // ========================================

  function initDarkMode() {
    // Dark mode is always enabled
    document.documentElement.setAttribute("data-theme", "dark");
  }

  // ========================================
  // GLASS CARD TILT EFFECT
  // ========================================

  function initCardTilt() {
    const cards = document.querySelectorAll(
      ".glass-room-card, .glass-card, .course-item"
    );

    cards.forEach(card => {
      // Skip if already initialized
      if (cleanupRegistry.cardTiltListeners.has(card)) return;

      const moveHandler = handleTilt;
      const leaveHandler = resetTilt;

      card.addEventListener("mousemove", moveHandler);
      card.addEventListener("mouseleave", leaveHandler);

      // Register for cleanup
      cleanupRegistry.cardTiltListeners.set(card, {
        move: moveHandler,
        leave: leaveHandler,
      });
    });
  }

  // Cache for getBoundingClientRect to avoid layout thrashing
  const rectCache = new WeakMap();
  let rafId = null;
  let pendingTilt = null;

  function handleTilt(e) {
    const card = e.currentTarget;

    // Throttle with requestAnimationFrame
    pendingTilt = { card, clientX: e.clientX, clientY: e.clientY };

    if (rafId) return;

    rafId = requestAnimationFrame(() => {
      if (!pendingTilt) {
        rafId = null;
        return;
      }

      const { card, clientX, clientY } = pendingTilt;

      // Use cached rect or compute new one
      let rect = rectCache.get(card);
      if (!rect) {
        rect = card.getBoundingClientRect();
        rectCache.set(card, rect);
        // Invalidate cache after a short delay (handles resize/scroll)
        setTimeout(() => rectCache.delete(card), 100);
      }

      const x = clientX - rect.left;
      const y = clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = (y - centerY) / 20;
      const rotateY = (centerX - x) / 20;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;

      rafId = null;
      pendingTilt = null;
    });
  }

  function resetTilt(e) {
    const card = e.currentTarget;
    card.style.transform =
      "perspective(1000px) rotateX(0) rotateY(0) translateY(0)";
    // Clear cache on mouse leave
    rectCache.delete(card);
  }

  // ========================================
  // SMOOTH SCROLL
  // ========================================

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");
        if (href === "#" || href === "#!") return;

        e.preventDefault();
        const target = document.querySelector(href);

        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });
  }

  // ========================================
  // ANIMATED COUNTER
  // ========================================

  function initCounters() {
    const counters = document.querySelectorAll("[data-count]");

    const observerOptions = {
      threshold: 0.5,
      rootMargin: "0px",
    };

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
  }

  function animateCounter(element) {
    const target = parseInt(element.dataset.count);
    const duration = 2000;
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function for smooth animation
      const easeOutQuad = progress * (2 - progress);
      const current = Math.floor(target * easeOutQuad);

      element.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = target.toLocaleString();
      }
    }

    requestAnimationFrame(updateCounter);
  }

  // ========================================
  // GLASS MORPHISM HOVER EFFECTS
  // ========================================

  function initGlassEffects() {
    const glassElements = document.querySelectorAll(
      ".glass-service-item, .btn-glass"
    );

    glassElements.forEach(element => {
      element.addEventListener("mouseenter", function () {
        this.style.transition = "all 0.3s ease";
      });
    });
  }

  // ========================================
  // NAVBAR SCROLL EFFECT
  // ========================================

  function initNavbarScroll() {
    const navbar = document.querySelector(".navbar");
    if (!navbar) return;

    let lastScroll = 0;

    const scrollHandler = () => {
      const currentScroll = window.pageYOffset;

      if (currentScroll <= 0) {
        navbar.classList.remove("scroll-up");
        return;
      }

      if (
        currentScroll > lastScroll &&
        !navbar.classList.contains("scroll-down")
      ) {
        // Scroll Down
        navbar.classList.remove("scroll-up");
        navbar.classList.add("scroll-down");
      } else if (
        currentScroll < lastScroll &&
        navbar.classList.contains("scroll-down")
      ) {
        // Scroll Up
        navbar.classList.remove("scroll-down");
        navbar.classList.add("scroll-up");
      }

      lastScroll = currentScroll;
    };

    window.addEventListener("scroll", scrollHandler);
    cleanupRegistry.scrollListeners.push(scrollHandler);
  }

  // ========================================
  // SEARCH FORM ENHANCEMENTS
  // ========================================

  function initSearchForm() {
    const searchInputs = document.querySelectorAll(
      ".form-control, .form-select"
    );

    searchInputs.forEach(input => {
      input.addEventListener("focus", function () {
        this.parentElement.classList.add("focused");
      });

      input.addEventListener("blur", function () {
        this.parentElement.classList.remove("focused");
      });
    });
  }

  // ========================================
  // FAVORITE BUTTON ANIMATION
  // ========================================

  function initFavoriteButtons() {
    const favoriteButtons = document.querySelectorAll(
      '[onclick*="toggleFavorite"]'
    );

    favoriteButtons.forEach(button => {
      button.addEventListener("click", function () {
        const icon = this.querySelector("i");
        if (icon) {
          icon.classList.add("animate-pulse");
          setTimeout(() => {
            icon.classList.remove("animate-pulse");
          }, 600);
        }
      });
    });
  }

  // ========================================
  // IMAGE GALLERY LIGHTBOX
  // ========================================

  function initImageGallery() {
    const galleryImages = document.querySelectorAll(".owl-carousel img");

    galleryImages.forEach(img => {
      img.style.cursor = "pointer";
      img.addEventListener("click", function () {
        createLightbox(this.src);
      });
    });
  }

  function createLightbox(imageSrc) {
    const lightbox = document.createElement("div");
    lightbox.className = "lightbox";
    lightbox.innerHTML = `
            <div class="lightbox-content">
                <span class="lightbox-close">&times;</span>
                <img src="${imageSrc}" alt="Lightbox Image">
            </div>
        `;

    document.body.appendChild(lightbox);

    // Add styles
    lightbox.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        `;

    const content = lightbox.querySelector(".lightbox-content");
    content.style.cssText = `
            position: relative;
            max-width: 90%;
            max-height: 90%;
        `;

    const img = lightbox.querySelector("img");
    img.style.cssText = `
            max-width: 100%;
            max-height: 90vh;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        `;

    const closeBtn = lightbox.querySelector(".lightbox-close");
    closeBtn.style.cssText = `
            position: absolute;
            top: -40px;
            right: 0;
            font-size: 40px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        `;

    closeBtn.addEventListener("click", () => {
      lightbox.style.animation = "fadeOut 0.3s ease";
      setTimeout(() => lightbox.remove(), 300);
    });

    lightbox.addEventListener("click", e => {
      if (e.target === lightbox) {
        lightbox.style.animation = "fadeOut 0.3s ease";
        setTimeout(() => lightbox.remove(), 300);
      }
    });
  }

  // ========================================
  // TOAST NOTIFICATIONS
  // ========================================

  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;

    toast.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: rgba(6, 187, 204, 0.9);
            backdrop-filter: blur(10px);
            color: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = "slideOutRight 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Make showToast globally available
  window.showToast = showToast;

  // ========================================
  // INITIALIZE ALL
  // ========================================

  function init() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initAll);
    } else {
      initAll();
    }
  }

  function initAll() {
    initDarkMode();
    initCardTilt();
    initSmoothScroll();
    initCounters();
    initGlassEffects();
    initNavbarScroll();
    initSearchForm();
    initFavoriteButtons();
    initImageGallery();

    console.log("🎨 Theme Effects Initialized");
  }

  // Start initialization
  init();

  // ========================================
  // CSS ANIMATIONS
  // ========================================

  const style = document.createElement("style");
  style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.2);
            }
        }
        
        .animate-pulse {
            animation: pulse 0.6s ease;
        }
        
        .navbar.scroll-down {
            transform: translateY(-100%);
            transition: transform 0.3s ease;
        }
        
        .navbar.scroll-up {
            transform: translateY(0);
            transition: transform 0.3s ease;
        }
        
        .focused {
            transform: scale(1.02);
            transition: transform 0.2s ease;
        }
    `;
  document.head.appendChild(style);
})();
