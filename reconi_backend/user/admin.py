from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ReconiUser
from .forms import ReconiUserCreationForm, ReconiUserChangeForm


class UserAdmin(BaseUserAdmin):
    form = ReconiUserChangeForm
    add_form = ReconiUserCreationForm

    model = ReconiUser
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("nickname", "gender", "age", "favorite_scent")},
        ),
        (
            "Taste Info",
            {
                "fields": (
                    "sweetness",
                    "body_feel",
                    "acidity",
                    "roasting_characteristics",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "nickname", "gender", "age", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "gender")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    # USERNAME_FIELD를 id로 설정
    def get_fieldsets(self, request, obj=None):
        if not obj:  # Adding new User
            return [(None, {"fields": ("email", "password")})]
        return super().get_fieldsets(request, obj)


# 커스텀 UserAdmin으로 User 모델을 등록합니다.
admin.site.register(ReconiUser, UserAdmin)
