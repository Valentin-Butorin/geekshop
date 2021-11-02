from django.contrib import admin
from users.models import User

from baskets.admin import BasketsAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketsAdmin,)
