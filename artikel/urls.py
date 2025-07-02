from django.urls import path
from . import views
from .views import berita_kesehatan

urlpatterns = [
    # Dashboard utama
    path('', views.dashboard, name='dashboard'),

    # CRUD Artikel (untuk admin/operator)
    path('artikel/', views.artikel_list, name='artikel_list'),
    path('artikel/tambah/', views.artikel_tambah, name='artikel_tambah'),
    path('artikel/edit/<int:id>/', views.artikel_edit, name='artikel_edit'),
    path('artikel/delete/<int:id>/', views.artikel_delete, name='artikel_delete'),

    # Detail Artikel
    path('artikel/<int:id>/', views.detail_artikel, name='detail_artikel'),

    # Pencarian Makanan Sehat
    path('makanan/cari/', views.cari_makanan, name='cari_makanan'),

    # Halaman Tips Diet Sehat
    path('healthy/', views.healthy_page, name='healthy_page'),

    # Halaman Berita Kesehatan Terkini (baru ditambahkan)
    path('berita-kesehatan/', views.berita_kesehatan, name='berita_kesehatan'),
]
