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


def home(request):
    """Homepage with featured and latest listings"""
    featured_rooms = MotelRoom.objects.featured()[:6]
    latest_rooms = MotelRoom.objects.latest(12)
    districts = District.objects.with_room_count()[:8]
    categories = Category.objects.with_room_count()
    
    # Get favorited room IDs for authenticated users
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


def motel_list(request):
    """List all approved motel rooms with search and filters"""
    form = MotelSearchForm(request.GET)
    rooms = MotelRoom.objects.approved_with_relations()
    
    # Apply filters
    if form.is_valid():
        if q := form.cleaned_data.get('q'):
            rooms = rooms.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(address__icontains=q)
            )
        
        if district := form.cleaned_data.get('district'):
            rooms = rooms.filter(district=district)
        
        if category := form.cleaned_data.get('category'):
            rooms = rooms.filter(category=category)
        
        if price_min := form.cleaned_data.get('price_min'):
            rooms = rooms.filter(price__gte=price_min)
        
        if price_max := form.cleaned_data.get('price_max'):
            rooms = rooms.filter(price__lte=price_max)
        
        if area_min := form.cleaned_data.get('area_min'):
            rooms = rooms.filter(area__gte=area_min)
        
        if area_max := form.cleaned_data.get('area_max'):
            rooms = rooms.filter(area__lte=area_max)
    
    # Pagination
    page_obj = paginate_queryset(rooms, request, per_page=DEFAULT_PAGE_SIZE)
    
    # Get favorited room IDs for authenticated users
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
    """Motel room detail page"""
    room = get_object_or_404(
        MotelRoom.objects.select_related('district', 'category', 'owner')
        .prefetch_related('images', 'utilities'),
        slug=slug,
        status=MOTEL_STATUS_APPROVED
    )
    
    # Increment views
    increment_views(room)
    
    # Check if user favorited
    is_favorited = False
    user_review = None
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, motel_room=room).exists()
        user_review = Review.objects.filter(user=request.user, motel_room=room).first()
    
    # Get reviews with rating stats
    reviews = room.reviews.select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()
    
    # Related rooms
    related_rooms = MotelRoom.objects.filter(
        status=MOTEL_STATUS_APPROVED,
        district=room.district
    ).exclude(id=room.id).select_related('district', 'category')[:4]
    
    # Get favorited room IDs for related rooms
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


@login_required
def motel_create(request):
    """Create new motel listing"""
    if request.method == 'POST':
        form = MotelRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.status = MOTEL_STATUS_PENDING  # Pending approval
            room.save()
            form.save_m2m()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            handle_image_upload(room, images)
            
            messages.success(request, 'Đăng tin thành công! Tin của bạn đang chờ duyệt.')
            return redirect('motel_my_listings')
    else:
        form = MotelRoomForm()
    
    return render(request, 'motel/create.html', {'form': form})


@login_required
def motel_edit(request, slug):
    """Edit existing motel listing"""
    room = get_object_or_404(MotelRoom, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = MotelRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            
            # Handle new image uploads
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
    """Delete motel listing"""
    room = get_object_or_404(MotelRoom, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Đã xóa tin đăng thành công!')
        return redirect('motel_my_listings')
    
    return render(request, 'motel/delete_confirm.html', {'room': room})


@login_required
def motel_my_listings(request):
    """User's own motel listings"""
    rooms = MotelRoom.objects.filter(
        owner=request.user
    ).select_related('district', 'category').prefetch_related('images').order_by('-created_at')
    
    page_obj = paginate_queryset(rooms, request, per_page=DEFAULT_PAGE_SIZE)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'motel/my_listings.html', context)


@login_required
def report_create(request, slug):
    """Report inappropriate listing"""
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    
    # Check if user already reported this room
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


@login_required
def profile_view(request, username):
    """View user profile"""
    user = get_object_or_404(User, username=username)
    rooms = MotelRoom.objects.filter(
        owner=user, status=MOTEL_STATUS_APPROVED
    ).select_related('district', 'category').prefetch_related('images')[:6]
    
    # Get favorited room IDs for authenticated users
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
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('profile_view', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user/profile_edit.html', {'form': form})


# AJAX endpoints
@require_POST
@login_required
def image_delete(request, image_id):
    """Delete motel image via AJAX"""
    image = get_object_or_404(MotelImage, id=image_id, motel_room__owner=request.user)
    image.delete()
    return JsonResponse({'success': True})


@require_POST
@login_required
def image_set_primary(request, image_id):
    """Set image as primary via AJAX"""
    image = get_object_or_404(MotelImage, id=image_id, motel_room__owner=request.user)
    
    # Remove primary from other images
    MotelImage.objects.filter(motel_room=image.motel_room).update(is_primary=False)
    
    # Set this as primary
    image.is_primary = True
    image.save()
    
    return JsonResponse({'success': True})


def district_list(request):
    """List all districts with room counts"""
    districts = District.objects.with_room_count()
    
    return render(request, 'district/list.html', {'districts': districts})


def category_list(request):
    """List all categories with room counts"""
    categories = Category.objects.with_room_count()
    
    return render(request, 'category/list.html', {'categories': categories})


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)


# Test views for error pages (only in development)
def test_404_view(request):
    """Test view to preview 404 page"""
    return render(request, 'errors/404.html', status=404)


def test_500_view(request):
    """Test view to preview 500 page"""
    return render(request, 'errors/500.html', status=500)


# ============================================================================
# FAVORITE VIEWS
# ============================================================================

@login_required
@require_POST
def favorite_toggle(request, slug):
    """Toggle favorite status for a motel room (AJAX)"""
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    favorite, created = Favorite.objects.get_or_create(user=request.user, motel_room=room)
    
    if not created:
        favorite.delete()
        return JsonResponse({'favorited': False, 'message': 'Đã xóa khỏi yêu thích'})
    
    return JsonResponse({'favorited': True, 'message': 'Đã thêm vào yêu thích'})


@login_required
def favorite_list(request):
    """List user's favorite motel rooms"""
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('motel_room__district', 'motel_room__category', 'motel_room__owner').prefetch_related('motel_room__images')
    
    page_obj = paginate_queryset(favorites, request, per_page=DEFAULT_PAGE_SIZE)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'motel/favorites.html', context)


# ============================================================================
# REVIEW VIEWS
# ============================================================================

@login_required
def review_create(request, slug):
    """Create or update review for a motel room"""
    room = get_object_or_404(MotelRoom, slug=slug, status=MOTEL_STATUS_APPROVED)
    
    # Check if user already reviewed
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
    """Delete user's own review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    slug = review.motel_room.slug
    review.delete()
    
    messages.success(request, 'Đã xóa đánh giá!')
    return redirect('motel_detail', slug=slug)
