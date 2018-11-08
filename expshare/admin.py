from django.contrib import admin
from expshare import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name','createuser','createdate','updateuser','updatedate',)
    list_per_page = 20
    # list_editable = ('name',)

@admin.register(models.ExpModel)
class ExpModelAdmin(admin.ModelAdmin):
    list_display = ('problem','reason','resolve','category','state',)
    list_per_page = 20

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('share','type','reason','is_resolved','state','resolve_note','createuser','createdate','updateuser','updatedate',)
    list_per_page = 20

class UserInline(admin.StackedInline):
    model = models.UserExtends
    can_delete = False
    verbose_name_plural = '用户信息拓展'

class UserAdmin(UserAdmin):
    inlines = (UserInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)