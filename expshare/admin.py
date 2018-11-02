from django.contrib import admin
from expshare import models
from django.contrib.auth.models import User

@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name','createuser','createdate','updateuser','updatedate',)
    list_per_page = 20
    # list_editable = ('name',)

@admin.register(models.ExpModel)
class ExpModelAdmin(admin.ModelAdmin):
    list_display = ('problem','reason','resolve','category','state')
    list_per_page = 20