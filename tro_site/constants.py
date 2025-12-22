"""
Constants cho ứng dụng Tìm Trọ
Định nghĩa các hằng số và choices dùng trong toàn bộ ứng dụng
"""

# =============================================================================
# VAI TRÒ NGƯỜI DÙNG
# =============================================================================

USER_ROLE_TENANT = 0      # Người dùng thường
USER_ROLE_ADMIN = 1       # Quản trị viên

USER_ROLES = [
    (USER_ROLE_TENANT, 'Người dùng'),
    (USER_ROLE_ADMIN, 'Quản trị viên'),
]


# =============================================================================
# TRẠNG THÁI TIN ĐĂNG PHÒNG TRỌ
# =============================================================================

MOTEL_STATUS_PENDING = 0   # Chờ duyệt
MOTEL_STATUS_APPROVED = 1  # Đã duyệt
MOTEL_STATUS_REJECTED = 2  # Từ chối

MOTEL_STATUS_CHOICES = [
    (MOTEL_STATUS_PENDING, 'Chờ duyệt'),
    (MOTEL_STATUS_APPROVED, 'Đã duyệt'),
    (MOTEL_STATUS_REJECTED, 'Từ chối'),
]


# =============================================================================
# TRẠNG THÁI BÁO CÁO VI PHẠM
# =============================================================================

REPORT_STATUS_PENDING = 0     # Chưa xử lý
REPORT_STATUS_PROCESSING = 1  # Đang xử lý
REPORT_STATUS_RESOLVED = 2    # Đã xử lý

REPORT_STATUS_CHOICES = [
    (REPORT_STATUS_PENDING, 'Chưa xử lý'),
    (REPORT_STATUS_PROCESSING, 'Đang xử lý'),
    (REPORT_STATUS_RESOLVED, 'Đã xử lý'),
]


# =============================================================================
# LÝ DO BÁO CÁO
# =============================================================================

REPORT_REASONS = [
    ('spam', 'Spam/Lừa đảo'),
    ('inappropriate', 'Nội dung không phù hợp'),
    ('duplicate', 'Tin trùng lặp'),
    ('wrong_info', 'Thông tin sai lệch'),
    ('other', 'Khác'),
]


# =============================================================================
# CẤU HÌNH PHÂN TRANG
# =============================================================================

DEFAULT_PAGE_SIZE = 12    # Số item mỗi trang (trang người dùng)
ADMIN_PAGE_SIZE = 20      # Số item mỗi trang (trang admin)
