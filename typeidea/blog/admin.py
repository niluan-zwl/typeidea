from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):  # 可选择继承来自admin.StackedInline以获取不同样式
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]  # 在分类编辑页面，多了一个新增或删除温文章的组件
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')  # 列表时，定制显示的列
    fields = ('name', 'status')  # 详细页面时，控制展示哪些元素，组合显示，或横排竖排

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 导入自定义Form
    list_display = ('title', 'category', 'status',
                    'created_time', 'owner', 'operator')
    list_display_links = ['title']  # 列表时，定制列可以点击跳转

    list_filter = [CategoryOwnerFilter, ]  # 列表时，定制右侧快速筛选
    search_fields = ['title', 'category__time']  # 列表时，模糊搜索的功能

    actions_on_top = True  # Action选项都是在页面上方显示
    actions_on_bottom = True  # Action选项都是在页面下方显示

    save_on_top = True  # 详细页面，在页面上方是否也显示保存删除等按钮

    exclude = ('owner',)
    """
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )
    """

    fieldsets = (
        ('基础配置', {
            'description': '基本配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
           'fields': (
               'desc',
               'content'
           ),
        }),
        ('额外信息', {
            'classes': ('wide', ),
            'fields': ('tag', ),
        }),
    )
    # filter_horizontal = ('tags', )
    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.show_description = '操作'

    # 自动设置owner为当前用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 当前登录用户
        return super(PostAdmin, self).save_model(request, obj, form, change)

    """当前用户只能查看自己的文章"""
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

#    @admin.register(LogEntry, site=custom_site)
#    class LogEntryAdmin(BaseOwnerAdmin):
#        list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

    """  
    class Media:
        cs = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js", )
    """



