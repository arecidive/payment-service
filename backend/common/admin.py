from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = "Административная панель сервиса платежей"
admin.site.site_title = "Административная панель сервиса платежей"

admin.site.unregister(Group)
