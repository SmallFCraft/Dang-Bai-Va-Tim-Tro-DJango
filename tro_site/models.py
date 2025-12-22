"""
Models cho ứng dụng Tìm Trọ
Định nghĩa cấu trúc dữ liệu và quan hệ giữa các bảng
"""

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from slugify import slugify as unicode_slugify

from .constants import (
    USER_ROLES, MOTEL_STATUS_CHOICES, MOTEL_STATUS_APPROVED,
    REPORT_STATUS_CHOICES, REPORT_REASONS
)


# =============================================================================
# MODEL NGƯỜI DÙNG
# =============================================================================

class User(AbstractUser):
    """
    Model người dùng mở rộng từ AbstractUser
    Thêm các trường: vai trò, số điện thoại, avatar, bio, địa chỉ
    """
    role = models.IntegerField(
        choices=USER_ROLES, 
        default=0, 
        verbose_name='Vai trò'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name='Số điện thoại'
    )
    avatar = ProcessedImageField(
        upload_to="avatars/",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 90},
        blank=True,
        null=True,
        verbose_name="Ảnh đại diện",
    )
    bio = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Giới thiệu"
    )
    address = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Địa chỉ"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Kiểm tra user có phải admin không (role = 1)"""
        return self.role == 1


# =============================================================================
# QUERYSET TÙY CHỈNH CHO QUẬN/HUYỆN VÀ DANH MỤC
# =============================================================================

class LocationQuerySet(models.QuerySet):
    """QuerySet tùy chỉnh cho District và Category"""
    
    def with_room_count(self):
        """Đếm số phòng trọ đã duyệt trong mỗi quận/danh mục"""
        return self.annotate(
            room_count=models.Count(
                'motel_rooms', 
                filter=models.Q(motel_rooms__status=MOTEL_STATUS_APPROVED)
            )
        ).filter(room_count__gt=0)


# =============================================================================
# MODEL QUẬN/HUYỆN
# =============================================================================

class District(models.Model):
    """
    Model quận/huyện - Dùng để lọc phòng trọ theo vị trí
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Tên quận/huyện'
    )
    slug = models.SlugField(
        max_length=120, 
        unique=True, 
        blank=True, 
        verbose_name='Slug'
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Mô tả'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Ngày tạo'
    )

    objects = LocationQuerySet.as_manager()

    class Meta:
        verbose_name = "Quận/Huyện"
        verbose_name_plural = "Quận/Huyện"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """Tự động tạo slug từ tên nếu chưa có"""
        if not self.slug:
            self.slug = unicode_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =============================================================================
# MODEL DANH MỤC
# =============================================================================

class Category(models.Model):
    """
    Model danh mục phòng trọ
    Ví dụ: Phòng trọ, Chung cư mini, Nhà nguyên căn, v.v.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Tên loại'
    )
    slug = models.SlugField(
        max_length=120, 
        unique=True, 
        blank=True, 
        verbose_name='Slug'
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Mô tả'
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name='Icon class'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Ngày tạo'
    )

    objects = LocationQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """Tự động tạo slug từ tên nếu chưa có"""
        if not self.slug:
            self.slug = unicode_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =============================================================================
# MODEL TIỆN ÍCH
# =============================================================================

class Utility(models.Model):
    """
    Model tiện ích phòng trọ
    Ví dụ: Wifi, Điều hòa, Máy giặt, Tủ lạnh, v.v.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Tên tiện ích"
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Icon class"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày tạo"
    )

    class Meta:
        verbose_name = "Tiện ích"
        verbose_name_plural = "Tiện ích"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =============================================================================
# QUERYSET VÀ MANAGER CHO PHÒNG TRỌ
# =============================================================================

class MotelRoomQuerySet(models.QuerySet):
    """QuerySet tùy chỉnh cho MotelRoom với các phương thức tiện ích"""
    
    def approved(self):
        """Lấy tất cả phòng trọ đã duyệt"""
        return self.filter(status=MOTEL_STATUS_APPROVED)
    
    def with_relations(self):
        """Prefetch các quan hệ thường dùng để tối ưu query"""
        return self.select_related(
            'district', 'category', 'owner'
        ).prefetch_related('images', 'utilities')
    
    def approved_with_relations(self):
        """Kết hợp: phòng đã duyệt + prefetch quan hệ"""
        return self.approved().with_relations()
    
    def featured(self):
        """Lấy phòng trọ nổi bật đã duyệt"""
        return self.approved().filter(is_featured=True).with_relations()


class MotelRoomManager(models.Manager):
    """Manager tùy chỉnh cho MotelRoom"""
    
    def get_queryset(self):
        return MotelRoomQuerySet(self.model, using=self._db)
    
    def approved(self):
        """Lấy phòng đã duyệt"""
        return self.get_queryset().approved()
    
    def with_relations(self):
        """Lấy phòng kèm quan hệ"""
        return self.get_queryset().with_relations()
    
    def approved_with_relations(self):
        """Lấy phòng đã duyệt kèm quan hệ"""
        return self.get_queryset().approved_with_relations()
    
    def featured(self):
        """Lấy phòng nổi bật"""
        return self.get_queryset().featured()
    
    def latest(self, limit=12):
        """Lấy phòng mới nhất (mặc định 12 phòng)"""
        return self.approved_with_relations()[:limit]


# =============================================================================
# MODEL PHÒNG TRỌ
# =============================================================================

class MotelRoom(models.Model):
    """
    Model phòng trọ - Bảng chính lưu thông tin tin đăng
    Bao gồm: thông tin cơ bản, giá, vị trí, tiện ích, liên hệ, trạng thái
    """
    
    # --- Thông tin cơ bản ---
    title = models.CharField(
        max_length=255, 
        verbose_name='Tiêu đề'
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True, 
        verbose_name='Slug'
    )
    description = models.TextField(
        verbose_name='Mô tả chi tiết'
    )

    # --- Giá và diện tích ---
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="Giá thuê (VNĐ/tháng)",
    )
    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Diện tích (m²)",
    )

    # --- Vị trí ---
    address = models.CharField(
        max_length=255, 
        verbose_name="Địa chỉ"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="motel_rooms",
        verbose_name="Quận/Huyện",
    )
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        blank=True, 
        null=True, 
        verbose_name="Vĩ độ"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        blank=True, 
        null=True, 
        verbose_name="Kinh độ"
    )

    # --- Danh mục và tiện ích ---
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="motel_rooms",
        verbose_name="Danh mục",
    )
    utilities = models.ManyToManyField(
        Utility, 
        blank=True, 
        related_name="motel_rooms", 
        verbose_name="Tiện ích"
    )

    # --- Thông tin liên hệ ---
    contact_name = models.CharField(
        max_length=100, 
        verbose_name="Tên liên hệ"
    )
    contact_phone = models.CharField(
        max_length=15, 
        verbose_name="Số điện thoại"
    )
    contact_email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="Email"
    )

    # --- Trạng thái và chủ sở hữu ---
    status = models.IntegerField(
        choices=MOTEL_STATUS_CHOICES, 
        default=0,
        verbose_name="Trạng thái",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="motel_rooms",
        verbose_name="Người đăng",
    )

    # --- Metadata ---
    views = models.PositiveIntegerField(
        default=0, 
        verbose_name="Lượt xem"
    )
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Tin nổi bật"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày đăng"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )
    approved_at = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Ngày duyệt"
    )
    
    objects = MotelRoomManager()

    class Meta:
        verbose_name = "Phòng trọ"
        verbose_name_plural = "Phòng trọ"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["district", "status"]),
            models.Index(fields=["category", "status"]),
        ]

    def save(self, *args, **kwargs):
        """Tự động tạo slug từ tiêu đề nếu chưa có"""
        if not self.slug:
            self.slug = unicode_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_approved(self):
        """Kiểm tra tin đã được duyệt chưa"""
        return self.status == MOTEL_STATUS_APPROVED
    
    @property
    def status_badge(self):
        """Trả về HTML badge hiển thị trạng thái"""
        badges = {
            0: '<span class="badge bg-warning">Chờ duyệt</span>',
            1: '<span class="badge bg-success">Đã duyệt</span>',
            2: '<span class="badge bg-danger">Từ chối</span>',
        }
        return badges.get(self.status, '')


# =============================================================================
# MODEL HÌNH ẢNH PHÒNG TRỌ
# =============================================================================

class MotelImage(models.Model):
    """
    Model hình ảnh phòng trọ
    Tự động resize ảnh: 1200x800 (chính), 400x300 (thumbnail)
    """
    motel_room = models.ForeignKey(
        MotelRoom,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Phòng trọ",
    )
    image = ProcessedImageField(
        upload_to="motel_rooms/",
        processors=[ResizeToFill(1200, 800)],
        format="JPEG",
        options={"quality": 85},
        verbose_name="Hình ảnh",
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(400, 300)],
        format="JPEG",
        options={"quality": 80},
    )
    caption = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Chú thích"
    )
    is_primary = models.BooleanField(
        default=False, 
        verbose_name="Ảnh chính"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày tải lên"
    )

    class Meta:
        verbose_name = "Hình ảnh phòng trọ"
        verbose_name_plural = "Hình ảnh phòng trọ"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Ảnh của {self.motel_room.title}"


# =============================================================================
# MODEL YÊU THÍCH
# =============================================================================

class Favorite(models.Model):
    """
    Model yêu thích - Lưu danh sách phòng trọ user đã lưu
    Mỗi user chỉ được yêu thích 1 phòng 1 lần (unique_together)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Người dùng",
    )
    motel_room = models.ForeignKey(
        MotelRoom,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Phòng trọ",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày thêm"
    )

    class Meta:
        verbose_name = "Yêu thích"
        verbose_name_plural = "Yêu thích"
        ordering = ["-created_at"]
        unique_together = ["user", "motel_room"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} yêu thích {self.motel_room.title}"


# =============================================================================
# MODEL ĐÁNH GIÁ
# =============================================================================

class Review(models.Model):
    """
    Model đánh giá phòng trọ
    Mỗi user chỉ được đánh giá 1 phòng 1 lần (có thể cập nhật)
    """
    motel_room = models.ForeignKey(
        MotelRoom,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Phòng trọ",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Người đánh giá",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Đánh giá (1-5 sao)",
    )
    comment = models.TextField(
        verbose_name="Nhận xét"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày đánh giá"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-created_at"]
        unique_together = ["user", "motel_room"]
        indexes = [
            models.Index(fields=["motel_room", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.rating}★ cho {self.motel_room.title}"


# =============================================================================
# MODEL BÁO CÁO VI PHẠM
# =============================================================================

class Report(models.Model):
    """
    Model báo cáo vi phạm
    Cho phép user báo cáo tin đăng không phù hợp
    """
    motel_room = models.ForeignKey(
        MotelRoom,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Phòng trọ",
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Người báo cáo",
    )
    reason = models.CharField(
        max_length=20,
        choices=REPORT_REASONS,
        verbose_name='Lý do'
    )
    description = models.TextField(
        verbose_name="Mô tả chi tiết"
    )
    status = models.IntegerField(
        choices=REPORT_STATUS_CHOICES,
        default=0,
        verbose_name="Trạng thái",
    )
    admin_note = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Ghi chú admin"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày báo cáo"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Báo cáo"
        verbose_name_plural = "Báo cáo"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Báo cáo của {self.reporter.username} về {self.motel_room.title}"
