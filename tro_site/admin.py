from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, District, Category, Utility, MotelRoom, MotelImage, Report
from .constants import (
    MOTEL_STATUS_APPROVED, MOTEL_STATUS_REJECTED,
    REPORT_STATUS_PROCESSING, REPORT_STATUS_RESOLVED
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin"""
    list_display = ['username', 'email', 'role', 'phone', 'created_at', 'is_active']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('role', 'phone', 'avatar', 'bio', 'address')
        }),
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """District admin"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    list_display = ['name', 'slug', 'icon', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    """Utility admin"""
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name']


class MotelImageInline(admin.TabularInline):
    """Inline for motel images"""
    model = MotelImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']


@admin.register(MotelRoom)
class MotelRoomAdmin(admin.ModelAdmin):
    """Enhanced MotelRoom admin with approval actions"""
    list_display = [
        'title', 
        'owner', 
        'district', 
        'price_display', 
        'area',
        'status_badge',
        'views',
        'created_at'
    ]
    list_filter = ['status', 'district', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'address', 'owner__username']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at', 'approved_at']
    filter_horizontal = ['utilities']
    inlines = [MotelImageInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Giá & Diện tích', {
            'fields': ('price', 'area')
        }),
        ('Vị trí', {
            'fields': ('address', 'district', 'latitude', 'longitude')
        }),
        ('Tiện ích', {
            'fields': ('utilities',)
        }),
        ('Liên hệ', {
            'fields': ('contact_name', 'contact_phone', 'contact_email')
        }),
        ('Trạng thái', {
            'fields': ('status', 'owner', 'is_featured', 'views')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_listings', 'reject_listings', 'mark_featured']
    
    def price_display(self, obj):
        return f"{obj.price:,.0f} VNĐ"
    price_display.short_description = 'Giá'
    
    def status_badge(self, obj):
        colors = {0: 'warning', 1: 'success', 2: 'danger'}
        labels = {0: 'Chờ duyệt', 1: 'Đã duyệt', 2: 'Từ chối'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            {'warning': '#ffc107', 'success': '#28a745', 'danger': '#dc3545'}[colors[obj.status]],
            labels[obj.status]
        )
    status_badge.short_description = 'Trạng thái'
    
    def approve_listings(self, request, queryset):
        updated = queryset.update(status=MOTEL_STATUS_APPROVED, approved_at=timezone.now())
        self.message_user(request, f'Đã duyệt {updated} tin đăng.')
    approve_listings.short_description = 'Duyệt tin đăng đã chọn'
    
    def reject_listings(self, request, queryset):
        updated = queryset.update(status=MOTEL_STATUS_REJECTED)
        self.message_user(request, f'Đã từ chối {updated} tin đăng.')
    reject_listings.short_description = 'Từ chối tin đăng đã chọn'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'Đã đánh dấu {updated} tin nổi bật.')
    mark_featured.short_description = 'Đánh dấu tin nổi bật'


@admin.register(MotelImage)
class MotelImageAdmin(admin.ModelAdmin):
    """Motel Image admin"""
    list_display = ['motel_room', 'image_preview', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['motel_room__title', 'caption']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report admin"""
    list_display = [
        'motel_room',
        'reporter',
        'reason',
        'status_badge',
        'created_at'
    ]
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['motel_room__title', 'reporter__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin báo cáo', {
            'fields': ('motel_room', 'reporter', 'reason', 'description')
        }),
        ('Xử lý', {
            'fields': ('status', 'admin_note')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_processing', 'mark_resolved']
    
    def status_badge(self, obj):
        colors = {0: 'warning', 1: 'info', 2: 'success'}
        labels = {0: 'Chưa xử lý', 1: 'Đang xử lý', 2: 'Đã xử lý'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            {'warning': '#ffc107', 'info': '#17a2b8', 'success': '#28a745'}[colors[obj.status]],
            labels[obj.status]
        )
    status_badge.short_description = 'Trạng thái'
    
    def mark_processing(self, request, queryset):
        updated = queryset.update(status=REPORT_STATUS_PROCESSING)
        self.message_user(request, f'Đã đánh dấu {updated} báo cáo đang xử lý.')
    mark_processing.short_description = 'Đánh dấu đang xử lý'
    
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status=REPORT_STATUS_RESOLVED)
        self.message_user(request, f'Đã đánh dấu {updated} báo cáo đã xử lý.')
    mark_resolved.short_description = 'Đánh dấu đã xử lý'
