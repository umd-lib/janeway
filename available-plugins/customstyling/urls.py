from django.urls import re_path

from plugins.customstyling import views


urlpatterns = [
    re_path(r'^manager/$', views.manager, name='customstyling_manager'),
    re_path(r'^manager/settings/$', views.settings, name='customstyling_settings'),
    re_path(r'^manager/press/$', views.manage_press_css, name='customstyling_manage_press_css'),
    re_path(r'^manager/journal/(?P<journal_id>\d+)$', views.manage_css, name='customstyling_manage_css_journal'),
    re_path(r'^manager/repository/(?P<repository_id>\d+)$', views.manage_css, name='customstyling_manage_css_repository'),

    re_path(r'^manager/cjs/new/$', views.manage_cross_journal_stylesheets, name='customstyling_new_lcjsc'),
    re_path(r'^manager/cjs/(?P<stylesheet_id>\d+)/$', views.manage_cross_journal_stylesheets, name='customstyling_edit_lcjsc'),
]
