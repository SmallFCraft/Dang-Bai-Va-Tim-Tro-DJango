from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Motel listings
    path('phong-tro/', views.motel_list, name='motel_list'),
    path('phong-tro/<slug:slug>/', views.motel_detail, name='motel_detail'),
    path('dang-tin/', views.motel_create, name='motel_create'),
    path('phong-tro/<slug:slug>/sua/', views.motel_edit, name='motel_edit'),
    path('phong-tro/<slug:slug>/xoa/', views.motel_delete, name='motel_delete'),
    path('tin-cua-toi/', views.motel_my_listings, name='motel_my_listings'),
    
    # Favorites
    path('yeu-thich/', views.favorite_list, name='favorite_list'),
    path('phong-tro/<slug:slug>/yeu-thich/', views.favorite_toggle, name='favorite_toggle'),
    
    # Reviews
    path('phong-tro/<slug:slug>/danh-gia/', views.review_create, name='review_create'),
    path('danh-gia/<int:review_id>/xoa/', views.review_delete, name='review_delete'),
    
    # Reports
    path('phong-tro/<slug:slug>/bao-cao/', views.report_create, name='report_create'),
    
    # User profiles
    path('nguoi-dung/<str:username>/', views.profile_view, name='profile_view'),
    path('tai-khoan/chinh-sua/', views.profile_edit, name='profile_edit'),
    
    # AJAX endpoints
    path('api/image/<int:image_id>/delete/', views.image_delete, name='image_delete'),
    path('api/image/<int:image_id>/set-primary/', views.image_set_primary, name='image_set_primary'),
    
    # Browse by location/category
    path('quan-huyen/', views.district_list, name='district_list'),
    path('danh-muc/', views.category_list, name='category_list'),
]

# Test error pages in development
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path('test-404/', views.test_404_view, name='test_404'),
        path('test-500/', views.test_500_view, name='test_500'),
    ]
