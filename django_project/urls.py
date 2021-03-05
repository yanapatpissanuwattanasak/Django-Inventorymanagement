"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.stock),
    path('login',views.login),
    path('login/<slug:validation>',views.login),
    path('go_login',views.go_login),
    path('update/<int:id>',views.update),
    path('delete/<int:id>',views.delete),
    path('insert',views.insert),
    path('register',views.register_employee),
    path('create_account',views.create_account),
    path('logout',views.logout),
    path('history',views.open_history),
    path('history_import',views.history_import),
    path('Transmission_history',views.Transmission_history),
    path('user_list',views.user_list),
    path('detail/<slug:product_id>',views.detail),
    path('import_product',views.import_product),
    path('detail_user/<slug:user_id>',views.detail_user),
    path('shipping',views.shipping),
    path('status_request_send',views.status_request_send),
    path('status_send',views.status_send),
    path('checkstock',views.checkstock),
    path('edit_item',views.edit_item),
    path('input',views.input),
    path('submit_product',views.submit_product),
     path('lost_item',views.lost_item),
    path('check_detail',views.check_detail),
    path('contact',views.contact),
    path('sumarize',views.sumarize),
    path('checkemployee',views.checkemployee),
    path('submit_user/<slug:user_id>',views.submit_user),
    path('sale_output_owner',views.sale_output_owner),
    path('output',views.output_product),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),


]
