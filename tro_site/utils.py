"""
Utility functions cho ứng dụng Tìm Trọ
Các hàm tiện ích dùng chung trong toàn bộ ứng dụng
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from .models import MotelImage, Favorite


def paginate_queryset(queryset, request, per_page=12):
    """
    Phân trang cho queryset
    
    Args:
        queryset: QuerySet cần phân trang
        request: HTTP request (để lấy số trang từ GET params)
        per_page: Số item mỗi trang (mặc định 12)
    
    Returns:
        Page object chứa dữ liệu đã phân trang
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Nếu page không phải số, trả về trang 1
        page_obj = paginator.page(1)
    except EmptyPage:
        # Nếu page vượt quá số trang, trả về trang cuối
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj


def handle_image_upload(motel_room, images, set_first_primary=True):
    """
    Xử lý upload nhiều hình ảnh cho phòng trọ
    
    Args:
        motel_room: Instance của MotelRoom
        images: List các file ảnh từ request.FILES
        set_first_primary: Đặt ảnh đầu tiên làm ảnh chính (mặc định True)
    
    Returns:
        List các MotelImage đã tạo
    """
    created_images = []
    
    for index, image in enumerate(images):
        # Ảnh đầu tiên là ảnh chính (nếu set_first_primary=True)
        is_primary = (index == 0) and set_first_primary
        
        motel_image = MotelImage.objects.create(
            motel_room=motel_room,
            image=image,
            is_primary=is_primary
        )
        created_images.append(motel_image)
    
    return created_images


def increment_views(motel_room):
    """
    Tăng lượt xem cho phòng trọ
    Sử dụng F() expression để tránh race condition
    
    Args:
        motel_room: Instance của MotelRoom
    """
    # Sử dụng update với F() để atomic increment
    from .models import MotelRoom
    MotelRoom.objects.filter(pk=motel_room.pk).update(views=F('views') + 1)


def get_favorited_room_ids(user, room_ids):
    """
    Lấy danh sách ID phòng trọ mà user đã yêu thích
    Dùng để hiển thị trạng thái yêu thích trên danh sách phòng
    
    Args:
        user: User hiện tại (có thể là AnonymousUser)
        room_ids: List các ID phòng trọ cần kiểm tra
    
    Returns:
        Set các ID phòng đã yêu thích (rỗng nếu chưa đăng nhập)
    """
    if not user.is_authenticated:
        return set()
    
    # Query một lần để lấy tất cả favorites
    favorited_ids = Favorite.objects.filter(
        user=user,
        motel_room_id__in=room_ids
    ).values_list('motel_room_id', flat=True)
    
    return set(favorited_ids)


def format_price(price):
    """
    Format giá tiền theo định dạng Việt Nam
    
    Args:
        price: Số tiền (Decimal hoặc int)
    
    Returns:
        String đã format (VD: "2,500,000 VNĐ")
    """
    return f"{price:,.0f} VNĐ"


def format_area(area):
    """
    Format diện tích
    
    Args:
        area: Diện tích (Decimal hoặc float)
    
    Returns:
        String đã format (VD: "25.5 m²")
    """
    return f"{area} m²"
