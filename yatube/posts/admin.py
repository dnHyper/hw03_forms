from django.contrib import admin

from yatube.settings import EMPTY_VALUE

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = ('pk',
                    'text',
                    'pub_date',
                    'author',
                    'group'
                    )
    list_display_links = ('text',)
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'description',
                    'slug',
                    )
    list_editable = ('slug',
                     )
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('pk',)
    empty_value_display = EMPTY_VALUE


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
