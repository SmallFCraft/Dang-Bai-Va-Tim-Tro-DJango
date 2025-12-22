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


class User(AbstractUser):
    """Extended User model with additional fields"""
    role = models.IntegerField(choices=USER_ROLES, default=0, verbose_name='Vai trò')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Số điện thoại')
    avatar = ProcessedImageField(
        upload_to="avatars/",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 90},
        blank=True,
        null=True,
        verbose_name="Ảnh đại diện",
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Giới thiệu")
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Địa chỉ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 1


class LocationQuerySet(models.QuerySet):
    """Custom QuerySet for District and Category models"""
    
    def with_room_count(self):
        """Annotate with approved room count"""
        return self.annotate(
            room_count=models.Count('motel_rooms', filter=models.Q(motel_rooms__status=MOTEL_STATUS_APPROVED))
        ).filter(room_count__gt=0)


class District(models.Model):
    """Districts/Areas for location filtering"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên quận/huyện')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    objects = LocationQuerySet.as_manager()

    class Meta:
        verbose_name = "Quận/Huyện"
        verbose_name_plural = "Quận/Huyện"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unicode_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Room categories (Phòng trọ, Chung cư mini, Nhà nguyên căn, etc.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên loại')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Icon class')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    objects = LocationQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unicode_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Utility(models.Model):
    """Utilities/Amenities (Wifi, Điều hòa, Máy giặt, etc.)"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Tên tiện ích")
    icon = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Icon class"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Tiện ích"
        verbose_name_plural = "Tiện ích"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MotelRoomQuerySet(models.QuerySet):
    """Custom QuerySet for MotelRoom model"""
    
    def approved(self):
        """Get all approved rooms"""
        return self.filter(status=MOTEL_STATUS_APPROVED)
    
    def with_relations(self):
        """Prefetch common relations"""
        return self.select_related(
            'district', 'category', 'owner'
        ).prefetch_related('images', 'utilities')
    
    def approved_with_relations(self):
        """Common queryset for approved rooms with relations"""
        return self.approved().with_relations()
    
    def featured(self):
        """Get featured approved rooms"""
        return self.approved().filter(is_featured=True).with_relations()


class MotelRoomManager(models.Manager):
    """Custom Manager for MotelRoom model"""
    
    def get_queryset(self):
        return MotelRoomQuerySet(self.model, using=self._db)
    
    def approved(self):
        return self.get_queryset().approved()
    
    def with_relations(self):
        return self.get_queryset().with_relations()
    
    def approved_with_relations(self):
        return self.get_queryset().approved_with_relations()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def latest(self, limit=12):
        return self.approved_with_relations()[:limit]


class MotelRoom(models.Model):
    """Main motel room listing model"""
    
    # Basic Information
    title = models.CharField(max_length=255, verbose_name='Tiêu đề')
    slug = models.SlugField(max_length=300, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Mô tả chi tiết')

    # Pricing & Area
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

    # Location
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="motel_rooms",
        verbose_name="Quận/Huyện",
    )
    latitude = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True, verbose_name="Vĩ độ"
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, blank=True, null=True, verbose_name="Kinh độ"
    )

    # Category & Utilities
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="motel_rooms",
        verbose_name="Danh mục",
    )
    utilities = models.ManyToManyField(
        Utility, blank=True, related_name="motel_rooms", verbose_name="Tiện ích"
    )

    # Contact Information
    contact_name = models.CharField(max_length=100, verbose_name="Tên liên hệ")
    contact_phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email")

    # Status & Ownership
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

    # Metadata
    views = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")
    is_featured = models.BooleanField(default=False, verbose_name="Tin nổi bật")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày duyệt")
    
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
        if not self.slug:
            self.slug = unicode_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_approved(self):
        return self.status == MOTEL_STATUS_APPROVED
    
    @property
    def status_badge(self):
        badges = {
            0: '<span class="badge bg-warning">Chờ duyệt</span>',
            1: '<span class="badge bg-success">Đã duyệt</span>',
            2: '<span class="badge bg-danger">Từ chối</span>',
        }
        return badges.get(self.status, '')


class MotelImage(models.Model):
    """Images for motel rooms"""

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
        max_length=255, blank=True, null=True, verbose_name="Chú thích"
    )
    is_primary = models.BooleanField(default=False, verbose_name="Ảnh chính")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")

    class Meta:
        verbose_name = "Hình ảnh phòng trọ"
        verbose_name_plural = "Hình ảnh phòng trọ"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Image for {self.motel_room.title}"


class Favorite(models.Model):
    """User favorites/bookmarks for motel rooms"""

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")

    class Meta:
        verbose_name = "Yêu thích"
        verbose_name_plural = "Yêu thích"
        ordering = ["-created_at"]
        unique_together = ["user", "motel_room"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} favorites {self.motel_room.title}"


class Review(models.Model):
    """User reviews/ratings for motel rooms"""

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
    comment = models.TextField(verbose_name="Nhận xét")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đánh giá")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-created_at"]
        unique_together = ["user", "motel_room"]
        indexes = [
            models.Index(fields=["motel_room", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.rating}★ on {self.motel_room.title}"


class Report(models.Model):
    """User reports for inappropriate listings"""
    
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
    description = models.TextField(verbose_name="Mô tả chi tiết")
    status = models.IntegerField(
        choices=REPORT_STATUS_CHOICES,
        default=0,
        verbose_name="Trạng thái",
    )
    admin_note = models.TextField(blank=True, null=True, verbose_name="Ghi chú admin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày báo cáo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Báo cáo"
        verbose_name_plural = "Báo cáo"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report by {self.reporter.username} on {self.motel_room.title}"
