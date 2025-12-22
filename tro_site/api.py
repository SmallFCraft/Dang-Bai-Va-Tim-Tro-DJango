"""
REST API module - Consolidated API components
Contains: Serializers, Filters, ViewSets, and URL routing
"""
from django.urls import path, include
from django.db.models import Prefetch
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.routers import DefaultRouter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import MotelRoom, District, Category, Utility, MotelImage, User, Favorite, Review
from .constants import MOTEL_STATUS_APPROVED, MOTEL_STATUS_PENDING
from .utils import increment_views as utils_increment_views


# ============================================================================
# SERIALIZERS
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    """User serializer for API"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'avatar']


class DistrictSerializer(serializers.ModelSerializer):
    """District serializer"""
    
    class Meta:
        model = District
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class UtilitySerializer(serializers.ModelSerializer):
    """Utility serializer"""
    
    class Meta:
        model = Utility
        fields = ['id', 'name', 'icon']


class MotelImageSerializer(serializers.ModelSerializer):
    """Motel image serializer"""
    
    class Meta:
        model = MotelImage
        fields = ['id', 'image', 'thumbnail', 'caption', 'is_primary']


class MotelRoomListSerializer(serializers.ModelSerializer):
    """Motel room list serializer (lightweight)"""
    district = DistrictSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = MotelRoom
        fields = [
            'id', 'title', 'slug', 'price', 'area', 'address',
            'district', 'category', 'owner', 'primary_image',
            'views', 'is_featured', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        # Use prefetched primary_images to avoid N+1 queries
        if hasattr(obj, 'primary_images') and obj.primary_images:
            primary = obj.primary_images[0]
            return primary.thumbnail.url if primary.thumbnail else primary.image.url
        # Fallback: use prefetched images
        if hasattr(obj, '_prefetched_objects_cache') and 'images' in obj._prefetched_objects_cache:
            images = obj._prefetched_objects_cache['images']
            primary = next((img for img in images if img.is_primary), None)
            if primary:
                return primary.thumbnail.url if primary.thumbnail else primary.image.url
            if images:
                return images[0].thumbnail.url if images[0].thumbnail else images[0].image.url
        return None


class MotelRoomDetailSerializer(serializers.ModelSerializer):
    """Motel room detail serializer (full data)"""
    district = DistrictSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    utilities = UtilitySerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    images = MotelImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = MotelRoom
        fields = '__all__'


# ============================================================================
# FILTERS
# ============================================================================

class MotelRoomFilter(django_filters.FilterSet):
    """Advanced filtering for motel rooms"""
    
    title = django_filters.CharFilter(lookup_expr='icontains', label='Tiêu đề')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Giá từ')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Giá đến')
    area_min = django_filters.NumberFilter(field_name='area', lookup_expr='gte', label='Diện tích từ')
    area_max = django_filters.NumberFilter(field_name='area', lookup_expr='lte', label='Diện tích đến')
    district = django_filters.ModelChoiceFilter(queryset=District.objects.all(), label='Quận/Huyện')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Danh mục')
    
    class Meta:
        model = MotelRoom
        fields = ['title', 'district', 'category', 'price_min', 'price_max', 'area_min', 'area_max']


# ============================================================================
# VIEWSETS
# ============================================================================

class MotelRoomViewSet(viewsets.ModelViewSet):
    """API ViewSet for motel rooms"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MotelRoomFilter
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['created_at', 'price', 'area', 'views']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = MotelRoom.objects.filter(status=MOTEL_STATUS_APPROVED).select_related(
            'district', 'category', 'owner'
        )
        # Optimize for list view: prefetch primary images separately
        if self.action == 'list':
            queryset = queryset.prefetch_related(
                Prefetch(
                    'images',
                    queryset=MotelImage.objects.filter(is_primary=True),
                    to_attr='primary_images'
                ),
                'utilities'
            )
        else:
            queryset = queryset.prefetch_related('images', 'utilities')
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MotelRoomListSerializer
        return MotelRoomDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status=MOTEL_STATUS_PENDING)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment view count"""
        room = self.get_object()
        views = utils_increment_views(room)
        return Response({'views': views})


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for districts"""
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UtilityViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for utilities"""
    queryset = Utility.objects.all()
    serializer_class = UtilitySerializer


# ============================================================================
# FAVORITE & REVIEW SERIALIZERS
# ============================================================================

class FavoriteSerializer(serializers.ModelSerializer):
    """Favorite serializer"""
    motel_room = MotelRoomListSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'motel_room', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer"""
    user = UserSerializer(read_only=True)
    motel_room_title = serializers.CharField(source='motel_room.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'motel_room', 'motel_room_title', 'rating', 'comment', 'created_at', 'updated_at']


# ============================================================================
# FAVORITE & REVIEW VIEWSETS
# ============================================================================

class FavoriteViewSet(viewsets.ModelViewSet):
    """API ViewSet for favorites"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FavoriteSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user).select_related(
                'motel_room__district', 'motel_room__category', 'motel_room__owner', 'user'
            ).prefetch_related(
                Prefetch(
                    'motel_room__images',
                    queryset=MotelImage.objects.filter(is_primary=True),
                    to_attr='primary_images'
                )
            )
        return Favorite.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """API ViewSet for reviews"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['motel_room', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Review.objects.select_related('user', 'motel_room')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================================================================
# URL ROUTING
# ============================================================================

router = DefaultRouter()
router.register(r'motel-rooms', MotelRoomViewSet, basename='motelroom')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'utilities', UtilityViewSet, basename='utility')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
