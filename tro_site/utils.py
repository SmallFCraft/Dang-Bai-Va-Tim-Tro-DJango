"""Utility functions for common operations"""
from django.core.paginator import Paginator
from .constants import DEFAULT_PAGE_SIZE


def paginate_queryset(queryset, request, per_page=DEFAULT_PAGE_SIZE):
    """
    Paginate a queryset.
    
    Args:
        queryset: Django QuerySet to paginate
        request: HttpRequest object
        per_page: Number of items per page (default: 12)
    
    Returns:
        Page object from Paginator
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def handle_image_upload(motel_room, files, set_first_primary=True):
    """
    Handle multiple image uploads for a motel room.
    
    Args:
        motel_room: MotelRoom instance
        files: List of uploaded image files
        set_first_primary: Set first image as primary (default: True)
    
    Returns:
        List of created MotelImage instances
    """
    from .models import MotelImage
    
    images = []
    for idx, image_file in enumerate(files):
        is_primary = (idx == 0) if set_first_primary else False
        image = MotelImage.objects.create(
            motel_room=motel_room,
            image=image_file,
            is_primary=is_primary
        )
        images.append(image)
    return images


def increment_views(motel_room):
    """
    Increment view count for a motel room atomically.
    
    Args:
        motel_room: MotelRoom instance
    
    Returns:
        Updated view count
    """
    from django.db.models import F
    from .models import MotelRoom
    
    MotelRoom.objects.filter(pk=motel_room.pk).update(views=F('views') + 1)
    motel_room.refresh_from_db(fields=['views'])
    return motel_room.views


def get_favorited_room_ids(user, room_ids):
    """
    Get favorited room IDs for a user.
    
    Args:
        user: User instance (có thể là AnonymousUser)
        room_ids: List/QuerySet of room IDs to check
    
    Returns:
        Set of favorited room IDs
    """
    from .models import Favorite
    
    if not user.is_authenticated or not room_ids:
        return set()
    
    if not isinstance(room_ids, (list, tuple, set)):
        room_ids = list(room_ids)
    
    if not room_ids:
        return set()
    
    return set(
        Favorite.objects.filter(user=user, motel_room_id__in=room_ids)
        .values_list('motel_room_id', flat=True)
    )
