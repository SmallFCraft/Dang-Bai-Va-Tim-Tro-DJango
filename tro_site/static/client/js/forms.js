/**
 * Forms JavaScript - Ứng dụng Tìm Trọ
 * Xử lý preview hình ảnh, validation form và các tương tác
 */

(function () {
  "use strict";

  let initialized = false;

  // Khởi tạo khi DOM đã sẵn sàng
  document.addEventListener("DOMContentLoaded", function () {
    if (initialized) return;
    initialized = true;

    initImagePreview();
    initFormValidation();
    initRealTimeValidation();
  });

  // ==========================================================================
  // HỆ THỐNG TOAST THÔNG BÁO
  // ==========================================================================

  const Toast = {
    container: null,

    /**
     * Khởi tạo container cho toast
     */
    init() {
      if (this.container) return;
      this.container = document.createElement("div");
      this.container.className =
        "toast-container position-fixed top-0 end-0 p-3";
      this.container.style.zIndex = "9999";
      document.body.appendChild(this.container);
    },

    /**
     * Hiển thị toast thông báo
     * @param {string} message - Nội dung thông báo
     * @param {string} type - Loại thông báo: error, success, warning, info
     */
    show(message, type = "error") {
      this.init();

      // Icon tương ứng với loại thông báo
      const icons = {
        error: "fa-exclamation-circle",
        success: "fa-check-circle",
        warning: "fa-exclamation-triangle",
        info: "fa-info-circle",
      };

      // Màu nền tương ứng
      const bgColors = {
        error: "bg-danger",
        success: "bg-success",
        warning: "bg-warning",
        info: "bg-info",
      };

      // Tạo element toast
      const toast = document.createElement("div");
      toast.className = `toast align-items-center text-white ${bgColors[type]} border-0 show`;
      toast.setAttribute("role", "alert");
      toast.innerHTML = `
        <div class="d-flex">
          <div class="toast-body">
            <i class="fa ${icons[type]} me-2"></i>${message}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      `;

      this.container.appendChild(toast);

      // Tự động ẩn sau 5 giây
      setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
      }, 5000);

      // Xử lý nút đóng
      toast.querySelector(".btn-close").addEventListener("click", () => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
      });
    },

    // Các phương thức tiện ích
    error(message) {
      this.show(message, "error");
    },
    success(message) {
      this.show(message, "success");
    },
    warning(message) {
      this.show(message, "warning");
    },
    info(message) {
      this.show(message, "info");
    },
  };

  // Expose Toast ra global scope
  window.Toast = Toast;

  // ==========================================================================
  // QUY TẮC VALIDATION
  // ==========================================================================

  const ValidationRules = {
    title: {
      required: true,
      minLength: 10,
      maxLength: 255,
      message: {
        required: "Vui lòng nhập tiêu đề",
        minLength: "Tiêu đề phải có ít nhất 10 ký tự",
        maxLength: "Tiêu đề không được quá 255 ký tự",
      },
    },
    description: {
      required: true,
      minLength: 50,
      message: {
        required: "Vui lòng nhập mô tả",
        minLength: "Mô tả phải có ít nhất 50 ký tự",
      },
    },
    price: {
      required: true,
      min: 100000,
      max: 100000000,
      message: {
        required: "Vui lòng nhập giá thuê",
        min: "Giá thuê tối thiểu 100,000 VNĐ",
        max: "Giá thuê tối đa 100,000,000 VNĐ",
      },
    },
    area: {
      required: true,
      min: 5,
      max: 1000,
      message: {
        required: "Vui lòng nhập diện tích",
        min: "Diện tích tối thiểu 5 m²",
        max: "Diện tích tối đa 1000 m²",
      },
    },
    district: {
      required: true,
      message: {
        required: "Vui lòng chọn quận/huyện",
      },
    },
    category: {
      required: true,
      message: {
        required: "Vui lòng chọn loại phòng",
      },
    },
    address: {
      required: true,
      minLength: 10,
      message: {
        required: "Vui lòng nhập địa chỉ",
        minLength: "Địa chỉ phải có ít nhất 10 ký tự",
      },
    },
    contact_name: {
      required: true,
      minLength: 2,
      message: {
        required: "Vui lòng nhập tên liên hệ",
        minLength: "Tên liên hệ phải có ít nhất 2 ký tự",
      },
    },
    contact_phone: {
      required: true,
      pattern: /^(0|\+84)[0-9]{9,10}$/,
      message: {
        required: "Vui lòng nhập số điện thoại",
        pattern: "Số điện thoại không hợp lệ (VD: 0912345678)",
      },
    },
    contact_email: {
      required: false,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: {
        pattern: "Email không hợp lệ",
      },
    },
    images: {
      required: true,
      minCount: 3,
      maxCount: 10,
      maxSize: 5 * 1024 * 1024, // 5MB
      message: {
        required: "Vui lòng chọn hình ảnh",
        minCount: "Vui lòng chọn ít nhất 3 hình ảnh",
        maxCount: "Chỉ được chọn tối đa 10 hình ảnh",
        maxSize: "Kích thước ảnh không được vượt quá 5MB",
      },
    },
  };

  // ==========================================================================
  // HÀM VALIDATION
  // ==========================================================================

  /**
   * Validate một field
   * @param {string} fieldName - Tên field
   * @param {string} value - Giá trị của field
   * @param {FileList} files - Danh sách file (cho input file)
   * @returns {Object} - { valid: boolean, message: string }
   */
  function validateField(fieldName, value, files = null) {
    const rules = ValidationRules[fieldName];
    if (!rules) return { valid: true };

    // Xử lý input file (hình ảnh)
    if (fieldName === "images" && files) {
      if (rules.required && files.length === 0) {
        return { valid: false, message: rules.message.required };
      }
      if (files.length > 0 && files.length < rules.minCount) {
        return { valid: false, message: rules.message.minCount };
      }
      if (files.length > rules.maxCount) {
        return { valid: false, message: rules.message.maxCount };
      }
      // Kiểm tra kích thước từng file
      for (let file of files) {
        if (file.size > rules.maxSize) {
          return {
            valid: false,
            message: `Ảnh "${file.name}" vượt quá 5MB`,
          };
        }
      }
      return { valid: true };
    }

    // Kiểm tra bắt buộc
    if (rules.required && (!value || value.toString().trim() === "")) {
      return { valid: false, message: rules.message.required };
    }

    // Bỏ qua các validation khác nếu field rỗng và không bắt buộc
    if (!value || value.toString().trim() === "") {
      return { valid: true };
    }

    // Kiểm tra độ dài tối thiểu
    if (rules.minLength && value.length < rules.minLength) {
      return { valid: false, message: rules.message.minLength };
    }

    // Kiểm tra độ dài tối đa
    if (rules.maxLength && value.length > rules.maxLength) {
      return { valid: false, message: rules.message.maxLength };
    }

    // Kiểm tra giá trị tối thiểu
    if (rules.min !== undefined && parseFloat(value) < rules.min) {
      return { valid: false, message: rules.message.min };
    }

    // Kiểm tra giá trị tối đa
    if (rules.max !== undefined && parseFloat(value) > rules.max) {
      return { valid: false, message: rules.message.max };
    }

    // Kiểm tra pattern (regex)
    if (rules.pattern && !rules.pattern.test(value)) {
      return { valid: false, message: rules.message.pattern };
    }

    return { valid: true };
  }

  /**
   * Hiển thị lỗi cho field
   */
  function showFieldError(field, message) {
    field.classList.add("is-invalid");
    field.classList.remove("is-valid");

    let feedback = field.parentElement.querySelector(".invalid-feedback");
    if (!feedback) {
      feedback = document.createElement("div");
      feedback.className = "invalid-feedback";
      field.parentElement.appendChild(feedback);
    }
    feedback.textContent = message;
    feedback.style.display = "block";
  }

  /**
   * Xóa lỗi của field
   */
  function clearFieldError(field) {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");

    const feedback = field.parentElement.querySelector(".invalid-feedback");
    if (feedback) {
      feedback.style.display = "none";
    }
  }

  // ==========================================================================
  // VALIDATION THỜI GIAN THỰC
  // ==========================================================================

  /**
   * Khởi tạo validation thời gian thực cho các field
   */
  function initRealTimeValidation() {
    const form = document.getElementById("motelForm");
    if (!form) return;

    // Danh sách field cần validate
    const fieldsToValidate = [
      "title",
      "description",
      "price",
      "area",
      "district",
      "category",
      "address",
      "contact_name",
      "contact_phone",
      "contact_email",
    ];

    fieldsToValidate.forEach(fieldName => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (!field) return;

      // Validate khi blur (rời khỏi field)
      field.addEventListener("blur", function () {
        const result = validateField(fieldName, this.value);
        if (!result.valid) {
          showFieldError(this, result.message);
        } else {
          clearFieldError(this);
        }
      });

      // Xóa lỗi khi đang nhập
      field.addEventListener("input", function () {
        if (this.classList.contains("is-invalid")) {
          const result = validateField(fieldName, this.value);
          if (result.valid) {
            clearFieldError(this);
          }
        }
      });
    });

    // Validation cho input hình ảnh
    const imageInput = document.getElementById("imageInput");
    if (imageInput) {
      imageInput.addEventListener("change", function () {
        const result = validateField("images", null, this.files);
        if (!result.valid) {
          showFieldError(this, result.message);
          Toast.error(result.message);
        } else {
          clearFieldError(this);
        }
      });
    }
  }

  // ==========================================================================
  // PREVIEW HÌNH ẢNH
  // ==========================================================================

  /**
   * Khởi tạo chức năng preview hình ảnh
   */
  function initImagePreview() {
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementById("imagePreview");

    if (!imageInput || !imagePreview) return;

    // Xử lý khi chọn file
    imageInput.addEventListener("change", function () {
      handleImageSelection(this.files);
    });

    // Xử lý khi click nút xóa ảnh
    imagePreview.addEventListener("click", function (e) {
      const removeBtn = e.target.closest(".remove-image");
      if (removeBtn) {
        handleImageRemoval(removeBtn);
      }
    });
  }

  /**
   * Xử lý khi chọn hình ảnh
   */
  function handleImageSelection(files) {
    const preview = document.getElementById("imagePreview");
    preview.innerHTML = "";

    if (files.length === 0) {
      preview.classList.remove("active");
      return;
    }

    preview.classList.add("active");

    Array.from(files).forEach((file, index) => {
      // Kiểm tra định dạng file
      if (!file.type.startsWith("image/")) {
        Toast.warning(`File "${file.name}" không phải là hình ảnh`);
        return;
      }

      // Kiểm tra kích thước file (5MB)
      const maxSize = 5 * 1024 * 1024;
      if (file.size > maxSize) {
        Toast.error(`Ảnh "${file.name}" vượt quá kích thước cho phép (5MB)`);
        return;
      }

      // Đọc và hiển thị preview
      const reader = new FileReader();
      reader.onload = function (e) {
        const col = createPreviewElement(e.target.result, index, file.name);
        preview.appendChild(col);
      };
      reader.readAsDataURL(file);
    });

    // Hiển thị thông báo số ảnh đã chọn
    if (files.length > 0) {
      Toast.info(`Đã chọn ${files.length} hình ảnh`);
    }
  }

  /**
   * Tạo element preview cho một hình ảnh
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
        ${index === 0 ? '<span class="primary-badge">Ảnh chính</span>' : ""}
      </div>
    `;

    return col;
  }

  /**
   * Xử lý xóa hình ảnh khỏi preview
   */
  function handleImageRemoval(removeBtn) {
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");
    const index = parseInt(removeBtn.dataset.index);

    // Tạo FileList mới không chứa file bị xóa
    const dt = new DataTransfer();
    const files = Array.from(input.files);

    files.forEach((file, i) => {
      if (i !== index) {
        dt.items.add(file);
      }
    });

    // Cập nhật input files
    input.files = dt.files;

    // Xóa element preview
    const previewItem = removeBtn.closest(".col-6");
    if (previewItem) {
      previewItem.remove();
    }

    // Ẩn container nếu không còn ảnh
    if (input.files.length === 0) {
      preview.classList.remove("active");
    }

    // Đánh lại index cho các preview còn lại
    reindexPreviews();
    Toast.info(`Còn lại ${input.files.length} hình ảnh`);

    // Validate lại
    const result = validateField("images", null, input.files);
    if (!result.valid) {
      showFieldError(input, result.message);
    } else {
      clearFieldError(input);
    }
  }

  /**
   * Đánh lại index cho các preview sau khi xóa
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

      // Cập nhật badge ảnh chính
      const badge = item.querySelector(".primary-badge");
      if (newIndex === 0 && !badge) {
        const previewItem = item.querySelector(".preview-item");
        const badgeEl = document.createElement("span");
        badgeEl.className = "primary-badge";
        badgeEl.textContent = "Ảnh chính";
        previewItem.appendChild(badgeEl);
      } else if (newIndex !== 0 && badge) {
        badge.remove();
      }
    });
  }

  // ==========================================================================
  // VALIDATION KHI SUBMIT FORM
  // ==========================================================================

  /**
   * Khởi tạo validation khi submit form
   */
  function initFormValidation() {
    const form = document.getElementById("motelForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      const validationResult = validateAllFields();

      if (!validationResult.valid) {
        e.preventDefault();

        // Hiển thị tất cả lỗi dưới dạng toast
        validationResult.errors.forEach((error, index) => {
          setTimeout(() => Toast.error(error), index * 200);
        });

        // Focus vào field lỗi đầu tiên
        const firstInvalid = form.querySelector(".is-invalid");
        if (firstInvalid) {
          firstInvalid.focus();
          firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
        }

        return false;
      }

      // Hiển thị trạng thái loading
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML =
          '<i class="fa fa-spinner fa-spin me-2"></i>Đang xử lý...';
        submitBtn.disabled = true;
      }

      Toast.info("Đang gửi tin đăng...");
    });
  }

  /**
   * Validate tất cả các field trong form
   */
  function validateAllFields() {
    const form = document.getElementById("motelForm");
    const errors = [];
    let isValid = true;

    // Danh sách field cần validate
    const fieldsToValidate = [
      { name: "title", label: "Tiêu đề" },
      { name: "description", label: "Mô tả" },
      { name: "price", label: "Giá thuê" },
      { name: "area", label: "Diện tích" },
      { name: "district", label: "Quận/Huyện" },
      { name: "category", label: "Loại phòng" },
      { name: "address", label: "Địa chỉ" },
      { name: "contact_name", label: "Tên liên hệ" },
      { name: "contact_phone", label: "Số điện thoại" },
      { name: "contact_email", label: "Email" },
    ];

    // Validate từng field
    fieldsToValidate.forEach(({ name }) => {
      const field = form.querySelector(`[name="${name}"]`);
      if (!field) return;

      const result = validateField(name, field.value);
      if (!result.valid) {
        isValid = false;
        errors.push(result.message);
        showFieldError(field, result.message);
      } else {
        clearFieldError(field);
      }
    });

    // Validate hình ảnh
    const imageInput = document.getElementById("imageInput");
    if (imageInput) {
      const result = validateField("images", null, imageInput.files);
      if (!result.valid) {
        isValid = false;
        errors.push(result.message);
        showFieldError(imageInput, result.message);
      } else {
        clearFieldError(imageInput);
      }
    }

    return { valid: isValid, errors };
  }
})();
