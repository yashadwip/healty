from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import view publik
from mysite.views import (
    welcome,
    detail_artikel,
    not_found_artikel,
    healty,
    kontak,
)

# Import view untuk autentikasi
from mysite.authentication import login_view, logout, registrasi

# Import view berita dari app artikel


urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Halaman publik
    path('', welcome, name="welcome"),
    path('artikel/<int:id>/', detail_artikel, name="detail_artikel"),
    path('artikel-not-found/', not_found_artikel, name="not_found_artikel"),
    path('healty/', healty, name="healty"),
    path('kontak/', kontak, name="kontak"),

    # Dashboard (kelola artikel)
    path('dashboard/', include("artikel.urls")),

    # Autentikasi pengguna
    path('auth-login/', login_view, name="auth-login"),
    path('auth-logout/', logout, name="logout"),
    path('auth-registrasi/', registrasi, name="registrasi"),

    # CKEditor 5 untuk upload gambar/artikel
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Konfigurasi file static dan media saat development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
