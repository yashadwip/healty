from django.contrib import admin
from .models import Artikel, Kategori

@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kategori', 'tanggal']
    list_filter = ['kategori', 'tanggal']
    search_fields = ['judul', 'isi']
    fields = ['judul', 'isi', 'kategori', 'gambar']
    
@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama']
