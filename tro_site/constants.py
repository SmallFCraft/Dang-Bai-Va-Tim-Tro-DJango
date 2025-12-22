"""Constants for the tro_site application"""

# User roles
USER_ROLE_TENANT = 0
USER_ROLE_ADMIN = 1

USER_ROLES = [
    (USER_ROLE_TENANT, 'Người dùng'),
    (USER_ROLE_ADMIN, 'Quản trị viên'),
]

# Motel room status
MOTEL_STATUS_PENDING = 0
MOTEL_STATUS_APPROVED = 1
MOTEL_STATUS_REJECTED = 2

MOTEL_STATUS_CHOICES = [
    (MOTEL_STATUS_PENDING, 'Chờ duyệt'),
    (MOTEL_STATUS_APPROVED, 'Đã duyệt'),
    (MOTEL_STATUS_REJECTED, 'Từ chối'),
]

# Report status
REPORT_STATUS_PENDING = 0
REPORT_STATUS_PROCESSING = 1
REPORT_STATUS_RESOLVED = 2

REPORT_STATUS_CHOICES = [
    (REPORT_STATUS_PENDING, 'Chưa xử lý'),
    (REPORT_STATUS_PROCESSING, 'Đang xử lý'),
    (REPORT_STATUS_RESOLVED, 'Đã xử lý'),
]

# Report reasons
REPORT_REASONS = [
    ('spam', 'Spam/Lừa đảo'),
    ('inappropriate', 'Nội dung không phù hợp'),
    ('duplicate', 'Tin trùng lặp'),
    ('wrong_info', 'Thông tin sai lệch'),
    ('other', 'Khác'),
]

# Pagination defaults
DEFAULT_PAGE_SIZE = 12
ADMIN_PAGE_SIZE = 20
