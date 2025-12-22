from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.cache import cache
from .models import User, MotelRoom, Report, Category, District, Review


# Cache timeout for form querysets (5 minutes)
FORM_QUERYSET_CACHE_TIMEOUT = 300


def get_cached_districts():
    """Get districts queryset with caching"""
    cache_key = 'form_districts_queryset'
    districts = cache.get(cache_key)
    if districts is None:
        districts = list(District.objects.only('id', 'name').order_by('name'))
        cache.set(cache_key, districts, FORM_QUERYSET_CACHE_TIMEOUT)
    return districts


def get_cached_categories():
    """Get categories queryset with caching"""
    cache_key = 'form_categories_queryset'
    categories = cache.get(cache_key)
    if categories is None:
        categories = list(Category.objects.only('id', 'name').order_by('name'))
        cache.set(cache_key, categories, FORM_QUERYSET_CACHE_TIMEOUT)
    return categories


class UserProfileForm(UserChangeForm):
    """User profile edit form"""

    password = None  # Remove password field

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "bio",
            "address",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tên"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Họ"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Số điện thoại"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Giới thiệu về bạn...",
                }
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Địa chỉ"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="form-group col-md-6 mb-3"),
                Column("email", css_class="form-group col-md-6 mb-3"),
            ),
            Row(
                Column("first_name", css_class="form-group col-md-6 mb-3"),
                Column("last_name", css_class="form-group col-md-6 mb-3"),
            ),
            Row(
                Column("phone", css_class="form-group col-md-6 mb-3"),
                Column("avatar", css_class="form-group col-md-6 mb-3"),
            ),
            Field("bio", css_class="form-group mb-3"),
            Field("address", css_class="form-group mb-3"),
            Submit("submit", "Cập nhật", css_class="btn btn-primary"),
        )


class MotelRoomForm(forms.ModelForm):
    """Motel room creation/edit form"""

    class Meta:
        model = MotelRoom
        fields = [
            "title",
            "description",
            "price",
            "area",
            "address",
            "district",
            "latitude",
            "longitude",
            "category",
            "utilities",
            "contact_name",
            "contact_phone",
            "contact_email",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ví dụ: Phòng trọ giá rẻ gần ĐH Bách Khoa",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Mô tả chi tiết về phòng trọ...",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "VNĐ/tháng"}
            ),
            "area": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "m²"}
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Số nhà, tên đường, phường/xã",
                }
            ),
            "district": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "utilities": forms.CheckboxSelectMultiple(),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "contact_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Họ và tên"}
            ),
            "contact_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "0912345678"}
            ),
            "contact_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@example.com"}
            ),
        }


class MotelSearchForm(forms.Form):
    """Advanced search form for motel rooms"""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tìm kiếm theo tiêu đề, địa chỉ...",
                "class": "form-control",
            }
        ),
        label="Từ khóa",
    )
    district = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Tất cả quận/huyện",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Quận/Huyện",
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Tất cả loại phòng",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Loại phòng",
    )
    price_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "Giá tối thiểu", "class": "form-control"}
        ),
        label="Giá từ",
    )
    price_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "Giá tối đa", "class": "form-control"}
        ),
        label="Giá đến",
    )
    area_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "Diện tích tối thiểu", "class": "form-control"}
        ),
        label="Diện tích từ",
    )
    area_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "Diện tích tối đa", "class": "form-control"}
        ),
        label="Diện tích đến",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use cached querysets to avoid repeated DB queries
        self.fields["district"].queryset = District.objects.only('id', 'name').order_by('name')
        self.fields["category"].queryset = Category.objects.only('id', 'name').order_by('name')


class ReviewForm(forms.ModelForm):
    """Form for reviewing/rating motel rooms"""

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} sao") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Chia sẻ trải nghiệm của bạn về phòng trọ này...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Gửi đánh giá", css_class="btn btn-primary")
        )


class ReportForm(forms.ModelForm):
    """Form for reporting inappropriate listings"""

    class Meta:
        model = Report
        fields = ["reason", "description"]
        widgets = {
            "reason": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Vui lòng mô tả chi tiết lý do báo cáo...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Gửi báo cáo", css_class="btn btn-danger")
        )
