(function ($) {
  "use strict";

  // ========================================
  // UTILITY FUNCTIONS
  // ========================================

  /**
   * Get cookie value by name
   */
  window.getCookie = function (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  /**
   * Toggle favorite room
   * @param {string} slug - Room slug
   * @param {HTMLElement} button - Button element (optional)
   * @param {Function} onSuccess - Callback function after success (optional)
   */
  window.toggleFavorite = function (slug, button, onSuccess) {
    const csrftoken = getCookie("csrftoken");

    fetch(`/phong-tro/${slug}/yeu-thich/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
    })
      .then(response => response.json())
      .then(data => {
        if (button) {
          const icon = button.querySelector("i");
          const text =
            button.querySelector("#favoriteText") ||
            button.querySelector("span");
          const isFavorited = data.favorited;

          if (icon) {
            // Preserve existing classes like 'me-2' and update icon type
            const baseClasses = icon.className
              .replace(/fa[rs] fa-heart/g, "")
              .trim();
            icon.className =
              (isFavorited ? "fas" : "far") +
              " fa-heart" +
              (baseClasses ? " " + baseClasses : "");
          }

          // Update text if exists
          if (text && text.id === "favoriteText") {
            text.textContent = isFavorited ? "Đã yêu thích" : "Yêu thích";
          }

          // Update button styles for glassmorphism
          if (button.id === "favoriteBtn") {
            // Detail page button
            button.style.background = isFavorited
              ? "rgba(239, 68, 68, 0.9)"
              : "rgba(255, 255, 255, 0.1)";
            button.style.borderColor = isFavorited
              ? "rgba(239, 68, 68, 0.5)"
              : "rgba(255, 255, 255, 0.2)";
            button.style.color = "white";
          } else if (button.classList.contains("favorite-btn-card")) {
            // Room card button
            button.style.background = isFavorited
              ? "rgba(239, 68, 68, 0.9)"
              : "rgba(255, 255, 255, 0.2)";
            button.style.borderColor = isFavorited
              ? "rgba(239, 68, 68, 0.5)"
              : "rgba(255, 255, 255, 0.3)";
          }
        }

        // Show notification
        if (data.message) {
          const notification = document.createElement("div");
          notification.className =
            "alert alert-" +
            (data.favorited ? "success" : "info") +
            " alert-dismissible fade show position-fixed";
          notification.style.cssText =
            "top: 80px; right: 20px; z-index: 9999; min-width: 300px; backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);";
          notification.innerHTML = `
                    ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
          document.body.appendChild(notification);
          setTimeout(() => notification.remove(), 3000);
        }

        // Call custom callback if provided
        if (onSuccess && typeof onSuccess === "function") {
          onSuccess(data, button);
        }
      })
      .catch(error => {
        console.error("Error:", error);
        alert("Có lỗi xảy ra. Vui lòng thử lại.");
      });
  };

  /**
   * Toggle favorite card (wrapper for room cards)
   */
  window.toggleFavoriteCard = function (slug, button) {
    toggleFavorite(slug, button);
  };

  // ========================================
  // INITIALIZATION
  // ========================================

  // Spinner
  var spinner = function () {
    setTimeout(function () {
      if ($("#spinner").length > 0) {
        $("#spinner").removeClass("show");
      }
    }, 1);
  };
  spinner();

  // Initiate the wowjs
  new WOW().init();

  // Sticky Navbar
  $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
      $(".sticky-top").css("top", "0px");
    } else {
      $(".sticky-top").css("top", "-100px");
    }
  });

  // Dropdown on mouse hover
  const $dropdown = $(".dropdown");
  const $dropdownToggle = $(".dropdown-toggle");
  const $dropdownMenu = $(".dropdown-menu");
  const showClass = "show";

  $(window).on("load resize", function () {
    if (this.matchMedia("(min-width: 992px)").matches) {
      $dropdown.hover(
        function () {
          const $this = $(this);
          $this.addClass(showClass);
          $this.find($dropdownToggle).attr("aria-expanded", "true");
          $this.find($dropdownMenu).addClass(showClass);
        },
        function () {
          const $this = $(this);
          $this.removeClass(showClass);
          $this.find($dropdownToggle).attr("aria-expanded", "false");
          $this.find($dropdownMenu).removeClass(showClass);
        }
      );
    } else {
      $dropdown.off("mouseenter mouseleave");
    }
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });
  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
    return false;
  });

  // Header carousel
  $(".header-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1500,
    items: 1,
    dots: false,
    loop: true,
    nav: true,
    navText: [
      '<i class="bi bi-chevron-left"></i>',
      '<i class="bi bi-chevron-right"></i>',
    ],
  });
})(jQuery);
