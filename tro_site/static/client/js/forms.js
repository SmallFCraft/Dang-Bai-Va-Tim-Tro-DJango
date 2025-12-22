/**
 * Global Forms JavaScript
 * Handles image preview, validation, and form interactions for all forms
 */

(function () {
  "use strict";

  // Prevent multiple initializations
  let initialized = false;

  // Wait for DOM to be ready
  document.addEventListener("DOMContentLoaded", function () {
    if (initialized) return;
    initialized = true;

    initImagePreview();
    initFormValidation();
  });

  /**
   * Initialize image preview functionality
   */
  function initImagePreview() {
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementById("imagePreview");

    if (!imageInput || !imagePreview) return;

    // Handle file selection
    imageInput.addEventListener("change", function (e) {
      handleImageSelection(this.files);
    });

    // Handle image removal
    imagePreview.addEventListener("click", function (e) {
      const removeBtn = e.target.closest(".remove-image");
      if (removeBtn) {
        handleImageRemoval(removeBtn);
      }
    });
  }

  /**
   * Handle image file selection and preview
   */
  function handleImageSelection(files) {
    const preview = document.getElementById("imagePreview");
    preview.innerHTML = "";

    if (files.length === 0) {
      preview.classList.remove("active");
      return;
    }

    preview.classList.add("active");

    // Convert FileList to Array and process each file
    Array.from(files).forEach((file, index) => {
      if (!file.type.startsWith("image/")) {
        console.warn(`File ${file.name} is not an image`);
        return;
      }

      // Check file size (5MB limit)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) {
        alert(`Ảnh "${file.name}" vượt quá kích thước cho phép (5MB)`);
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = function (e) {
        const col = createPreviewElement(e.target.result, index, file.name);
        preview.appendChild(col);
      };
      reader.onerror = function () {
        console.error(`Error reading file ${file.name}`);
      };
      reader.readAsDataURL(file);
    });
  }

  /**
   * Create preview element for an image
   */
  function createPreviewElement(src, index, filename) {
    const col = document.createElement("div");
    col.className = "col-6 col-md-4 col-lg-3";
    col.setAttribute("data-index", index);

    col.innerHTML = `
            <div class="preview-item">
                <img src="${src}" alt="${filename}" loading="lazy">
                <button type="button" class="remove-image" data-index="${index}" title="Xóa ảnh">
                    <i class="fa fa-times"></i>
                </button>
            </div>
        `;

    return col;
  }

  /**
   * Handle image removal from preview
   */
  function handleImageRemoval(removeBtn) {
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");
    const index = parseInt(removeBtn.dataset.index);

    // Create new FileList without the removed file
    const dt = new DataTransfer();
    const files = Array.from(input.files);

    files.forEach((file, i) => {
      if (i !== index) {
        dt.items.add(file);
      }
    });

    // Update input files
    input.files = dt.files;

    // Remove preview element
    const previewItem = removeBtn.closest(".col-6");
    if (previewItem) {
      previewItem.remove();
    }

    // Hide preview container if no images left
    if (input.files.length === 0) {
      preview.classList.remove("active");
    }

    // Re-index remaining previews
    reindexPreviews();
  }

  /**
   * Re-index preview items after removal
   */
  function reindexPreviews() {
    const preview = document.getElementById("imagePreview");
    const items = preview.querySelectorAll("[data-index]");

    items.forEach((item, newIndex) => {
      item.setAttribute("data-index", newIndex);
      const removeBtn = item.querySelector(".remove-image");
      if (removeBtn) {
        removeBtn.setAttribute("data-index", newIndex);
      }
    });
  }

  /**
   * Initialize form validation
   */
  function initFormValidation() {
    const form = document.getElementById("motelForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      if (!validateForm()) {
        e.preventDefault();
        return false;
      }

      // Add loading state to submit button
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.classList.add("loading");
        submitBtn.disabled = true;
      }
    });
  }

  /**
   * Validate form before submission
   */
  function validateForm() {
    let isValid = true;
    const errors = [];

    // Validate image count
    const imageInput = document.getElementById("imageInput");
    if (imageInput && imageInput.files.length < 3) {
      errors.push("Vui lòng chọn ít nhất 3 hình ảnh!");
      isValid = false;
      imageInput.classList.add("is-invalid");
    } else if (imageInput) {
      imageInput.classList.remove("is-invalid");
    }

    // Validate image count max
    if (imageInput && imageInput.files.length > 10) {
      errors.push("Chỉ được chọn tối đa 10 hình ảnh!");
      isValid = false;
      imageInput.classList.add("is-invalid");
    }

    // Show errors if any
    if (!isValid) {
      alert(errors.join("\n"));

      // Focus on first invalid field
      const firstInvalid = document.querySelector(".is-invalid");
      if (firstInvalid) {
        firstInvalid.focus();
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }

    return isValid;
  }

})();
