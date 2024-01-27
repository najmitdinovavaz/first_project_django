from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import Blog, Category, Comment, Teg, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('custom_image', 'username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_("Personal info"), {'fields': ('first_name', 'last_name', 'email', 'image')}),
        (
            _("Permissions"),
            {'fields': ('is_active',
                        'is_staff',
                        'is_superuser',
                        'groups', 'user_permissions'),
             },
        ),
        (_("Important dates"), {'fields': ('last_login', 'date_joined')}),
    )

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.image.url))

    custom_image.short_description = 'Image'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Teg)
class TegAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
