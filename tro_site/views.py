"""
Views cho ứng dụng Tìm Trọ
Xử lý các request HTTP và trả về response tương ứng
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import (
    MotelRoom, District, Category, Utility, Report, 
    MotelImage, User, Favorite, Review
)
from .forms import (
    MotelRoomForm, MotelSearchForm, ReportForm, 
    UserProfileForm, ReviewForm
)
from .utils import paginate_queryset, handle_image_upload, increment_views, get_favorited_room_ids
from .constants import (
    MOTEL_STATUS_APPROVED, MOTEL_STATUS_PENDING,
    DEFAULT_PAGE_SIZE
)


# =============================================================================
# TRANG CHỦ
# =============================================================================

def home(request):
    """
    Trang chủ - Hiển thị phòng trọ nổi bật và mới nhất
    """
    # Lấy phòng trọ nổi bật (tối đa 6)
    featured_rooms = MotelRoom.objects.featured()[:6]
    
    # Lấy phòng trọ mới nhất (tối đa 12)
    latest_rooms = MotelRoom.objects.latest(12)
    
    # Lấy danh sách quận/huyện có phòng trọ (tối đa 8)
    districts = District.objects.with_room_count()[:8]
    
    # Lấy danh sách danh mục
    categories = Category.objects.with_room_count()
    
    # Lấy danh sách ID phòng đã yêu thích (nếu đã đăng nhập)
    all_room_ids = [room.id for room in list(featured_rooms) + list(latest_rooms)]
    favorited_room_ids = get_favorited_room_ids(request.user, all_room_ids)
    
    context = {
        'featured_rooms': featured_rooms,
        'latest_rooms': latest_rooms,
        'districts': districts,
        'categories': categories,
        'favorited_room_ids': favorited_room_ids,
    }
    return render(request, 'home.html', context)


# =============================================================================
# PHÒNG TRỌ - DANH SÁCH & CHI TIẾT
# =============================================================================

def motel_list(request):
    """
    Danh sách phòng trọ - Hỗ trợ tìm kiếm và lọc nâng cao
    """
    form = MotelSearchForm(request.GET)
    rooms = MotelRoom.objects.approved_with_relations()
    
    # Áp dụng bộ lọc nếu form hợp lệ
    if form.is_valid():
        # Lọc theo từ khóa (tiêu đề, mô tả, địa chỉ)
        if q := form.cleaned_data.get('q'):
            rooms = rooms.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(address__icontains=q)
            )
        
        # Lọc theo quận/huyện
        if district := form.cleaned_data.get('district'):
            rooms = rooms.filter(district=district)
        
        # Lọc theo danh mục
        if category := form.cleaned_data.get('category'):
            rooms = rooms.filter(category=category)
        
        # Lọc theo khoảng giá
        if price_min := form.cleaned_data.get('price_min'):
            rooms = rooms.filter(price__gte=price_min)
        
        if price_max := form.cleaned_data.get('price_max'):
            rooms = rooms.filter(price__lte=price_max)
        
        # Lọc theo diện tích
        if area_min := form.cleaned_data.get('area_min'):
            rooms = rooms.filter(area__gte=area_min)
        
        if area_max := form.cleaned_data.get('area_max'):
            rooms = rooms.filter(area__lte=area_max)
    
    # Phân trang kết quả
    page_obj = paginate_queryset(rooms, request, per_page=DEFAULT_PAGE_SIZE)
    
    # Lấy danh sách ID phòng đã yêu thích
    room_ids = [room.id for room in page_obj.object_list] if page_obj else []
    favorited_room_ids = get_favorited_room_ids(request.user, room_ids)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_count': page_obj.paginator.count if page_obj else 0,
        'favorited_room_ids': favorited_room_ids,
    }
    return render(request, 'motel/list.html', context)


def motel_detail(request, slug):
    """
    Chi tiết phòng trọ - Hiển thị thông tin đầy đủ của một phòng
    """
    # Lấy phòng trọ với các quan hệ liên quan
    room = get_object_or_404(
        MotelRoom.objects.select_related('district', 'category', 'owner')
        .prefetch_related('images', 'utilities'),
        slug=slug,
        status=MOTEL_STATUS_APPROVED
    )
    
    # Tăng lượt xem
    increment_views(room)
    
    # Kiểm tra trạng thái yêu thích và đánh giá của user
    is_favorited = False
    user_review = None
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, motel_room=room).exists()
        user_review = Review.objects.filter(user=request.user, motel_room=room).first()
    
    # Lấy danh sách đánh giá và thống kê
    reviews = room.reviews.select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()
    
    # Lấy phòng trọ liên quan (cùng quận/huyện)
    related_rooms = MotelRoom.objects.filter(
        status=MOTEL_STATUS_APPROVED,
        district=room.district
    ).exclude(id=room.id).select_related('district', 'category')[:4]
    
    # Lấy danh sách ID phòng đã yêu thích
    related_room_ids = [r.id for r in related_rooms]
    favorited_room_ids = get_favorited_room_ids(request.user, related_room_ids)
    
    context = {
        'room': room,
        'related_rooms': related_rooms,
        'is_favorited': is_favorited,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'user_review': user_review,
        'favorited_room_ids': favorited_room_ids,
    }
    return render(request, 'motel/detail.html', context)


# =============================================================================
# PHÒNG TRỌ - QUẢN LÝ TIN ĐĂNG
# =============================================================================

@login_required
def motel_create(request):
    """
    Đăng tin mới - Tạo tin đăng phòng trọ
    Tự động điền thông tin liên hệ từ profile user
    """
    user = request.user
    
    # Điền sẵn thông tin liên hệ từ profile
    initial_data = {
        'contact_name': user.get_full_name() or user.username,
        'contact_phone': user.phone or '',
        'contact_email': user.email or '',
    }
    
    if request.method == 'POST':
        form = MotelRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = user
            room.status = MOTEL_STATUS_PENDING  # Chờ duyệt
            room.save()
            form.save_m2m()  # Lưu quan hệ many-to-many (tiện ích)
            
            # Xử lý upload hình ảnh
            images = request.FILES.getlist('images')
            handle_image_upload(room, images)
            
            messages.success(request, 'Đăng tin thành công! Tin của bạn đang chờ duyệt.')
            return redirect('motel_my_listings')
    else:
        form = MotelRoomForm(initial=initial_data)
    
    return render(request, 'motel/create.html', {'form': form})


@login_required
def motel_edit(request, slug):
    """
    Chỉnh sửa tin đăng - Chỉ chủ sở hữu mới được sửa
    """
    room = get_object_or_404(MotelRoom, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = MotelRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            
            # Xử lý upload hình ảnh mới (không đặt ảnh đầu làm ảnh chính)
            images = request.FILES.getlist('images')
            handle_image_upload(room, images, set_first_primary=False)
            
            messages.success(request, 'Cập nhật tin đăng thành công!')
            return redirect('motel_detail', slug=room.slug)
    else:
        form = MotelRoomForm(instance=room)
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'motel/edit.html', context)


@login_required
def motel_delete(request, slug):
    """
    Xóa tin đăng - Yêu cầu xác nhận trước khi xóa
    """
    room = get_object_or_404(MotelRoom, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Đã xóa tin đăng thành công!')
        return redirect('motel_my_listings')
    
    return render(request, 'motel/delete_confirm.html', {'room': room})


@login_required
def motel_my_listings(request):
    """
    Tin đăng của tôi - Danh sách tin đăng của user hiện tại
    """
    rooms = MotelRoom.objects.filter(
        owner=request.user
    ).select_related('district', 'category').prefetch_related('images').order_by('-created_at')
    
    page_obj = paginate_queryset(rooms, request, per_page=DEFAULT_PAGE_SIZE)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'motel/my_listings.html', context)


# =============================================================================
# BÁO CÁO VI PHẠM
# =============================================================================

@login_required
def report_create(request, slug):
    """
    Báo cáo tin đăng vi phạm
    Mỗi user chỉ được báo cáo 1 lần cho mỗi tin
    """
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    
    # Kiểm tra đã báo cáo chưa
    if Report.objects.filter(motel_room=room, reporter=request.user).exists():
        messages.warning(request, 'Bạn đã báo cáo tin đăng này rồi!')
        return redirect('motel_detail', slug=slug)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.motel_room = room
            report.reporter = request.user
            report.save()
            
            messages.success(request, 'Cảm ơn bạn đã báo cáo. Chúng tôi sẽ xem xét sớm nhất!')
            return redirect('motel_detail', slug=slug)
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'motel/report.html', context)


# =============================================================================
# TRANG CÁ NHÂN
# =============================================================================

@login_required
def profile_view(request, username):
    """
    Xem trang cá nhân - Hiển thị thông tin và tin đăng của user
    """
    user = get_object_or_404(User, username=username)
    
    # Lấy tin đăng đã duyệt của user (tối đa 6)
    rooms = MotelRoom.objects.filter(
        owner=user, status=MOTEL_STATUS_APPROVED
    ).select_related('district', 'category').prefetch_related('images')[:6]
    
    # Lấy danh sách ID phòng đã yêu thích
    room_ids = [room.id for room in rooms]
    favorited_room_ids = get_favorited_room_ids(request.user, room_ids)
    
    context = {
        'profile_user': user,
        'rooms': rooms,
        'favorited_room_ids': favorited_room_ids,
    }
    return render(request, 'user/profile.html', context)


@login_required
def profile_edit(request):
    """
    Chỉnh sửa thông tin cá nhân
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('profile_view', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user/profile_edit.html', {'form': form})


# =============================================================================
# API AJAX - QUẢN LÝ HÌNH ẢNH
# =============================================================================

@require_POST
@login_required
def image_delete(request, image_id):
    """
    Xóa hình ảnh phòng trọ (AJAX)
    Chỉ chủ sở hữu mới được xóa
    """
    image = get_object_or_404(MotelImage, id=image_id, motel_room__owner=request.user)
    image.delete()
    return JsonResponse({'success': True})


@require_POST
@login_required
def image_set_primary(request, image_id):
    """
    Đặt hình ảnh làm ảnh chính (AJAX)
    """
    image = get_object_or_404(MotelImage, id=image_id, motel_room__owner=request.user)
    
    # Bỏ đánh dấu ảnh chính của các ảnh khác
    MotelImage.objects.filter(motel_room=image.motel_room).update(is_primary=False)
    
    # Đặt ảnh này làm ảnh chính
    image.is_primary = True
    image.save()
    
    return JsonResponse({'success': True})


# =============================================================================
# DANH MỤC & KHU VỰC
# =============================================================================

def district_list(request):
    """
    Danh sách quận/huyện - Hiển thị kèm số lượng phòng trọ
    """
    districts = District.objects.with_room_count()
    return render(request, 'district/list.html', {'districts': districts})


def category_list(request):
    """
    Danh sách danh mục - Hiển thị kèm số lượng phòng trọ
    """
    categories = Category.objects.with_room_count()
    return render(request, 'category/list.html', {'categories': categories})


# =============================================================================
# TRANG LỖI TÙY CHỈNH
# =============================================================================

def custom_404(request, exception):
    """Trang lỗi 404 - Không tìm thấy"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Trang lỗi 500 - Lỗi máy chủ"""
    return render(request, 'errors/500.html', status=500)


def test_404_view(request):
    """View test trang 404 (chỉ dùng trong development)"""
    return render(request, 'errors/404.html', status=404)


def test_500_view(request):
    """View test trang 500 (chỉ dùng trong development)"""
    return render(request, 'errors/500.html', status=500)


# =============================================================================
# YÊU THÍCH
# =============================================================================

@login_required
@require_POST
def favorite_toggle(request, slug):
    """
    Thêm/xóa yêu thích (AJAX)
    Nếu đã yêu thích thì xóa, chưa thì thêm
    """
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    favorite, created = Favorite.objects.get_or_create(user=request.user, motel_room=room)
    
    if not created:
        # Đã tồn tại -> xóa
        favorite.delete()
        return JsonResponse({'favorited': False, 'message': 'Đã xóa khỏi yêu thích'})
    
    # Mới tạo -> đã thêm
    return JsonResponse({'favorited': True, 'message': 'Đã thêm vào yêu thích'})


@login_required
def favorite_list(request):
    """
    Danh sách yêu thích - Các phòng trọ user đã lưu
    """
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'motel_room__district', 
        'motel_room__category', 
        'motel_room__owner'
    ).prefetch_related('motel_room__images')
    
    page_obj = paginate_queryset(favorites, request, per_page=DEFAULT_PAGE_SIZE)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'motel/favorites.html', context)


# =============================================================================
# ĐÁNH GIÁ
# =============================================================================

@login_required
def review_create(request, slug):
    """
    Tạo/cập nhật đánh giá
    Mỗi user chỉ được đánh giá 1 lần cho mỗi phòng (có thể sửa)
    """
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    
    # Kiểm tra đánh giá đã tồn tại
    existing_review = Review.objects.filter(user=request.user, motel_room=room).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.motel_room = room
            review.save()
            
            messages.success(request, 'Cảm ơn bạn đã đánh giá!')
            return redirect('motel_detail', slug=slug)
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'room': room,
        'existing_review': existing_review,
    }
    return render(request, 'motel/review.html', context)


@login_required
@require_POST
def review_delete(request, review_id):
    """
    Xóa đánh giá - Chỉ chủ sở hữu mới được xóa
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    slug = review.motel_room.slug
    review.delete()
    
    messages.success(request, 'Đã xóa đánh giá!')
    return redirect('motel_detail', slug=slug)
