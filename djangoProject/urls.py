from django.contrib import admin
from django.urls import path, re_path
from . import views, social, update, invite, manage, json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.runoob),
    path('social/', invite.get_form),
    path('social/list/', social.get_school),
    path('social/info/', social.get_info),
    path('social/update/', update.get_form),
    path('social/update/school/', update.update_school),
    path('social/update/result/', update.update_info),
    path('social/update/model/', update.get_model),
    path('social/invite/', invite.get_form),
    path('social/verify/', invite.verify),
    path('social/exit/', invite.exit),
    path('social/manage/', manage.manage_list),
    path('social/user/list/', manage.manage_list),
    path('social/user/add/', manage.add_user),
    path('social/user/delete/', manage.del_user),
    path('social/user/edit/', manage.edit_user),
    path('social/json/info/', json.get_info)
]
