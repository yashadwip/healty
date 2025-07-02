from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from .models import Artikel
from .forms import ArtikelForm
import requests
import random

# Artikel dari luar (sumber eksternal)
ARTIKEL_LUAR = [
    {
        'judul': 'Jenis-Jenis Makanan Sehat - Alodokter',
        'url': 'https://www.alodokter.com/jenis-jenis-makanan-sehat',
        'gambar': 'https://img.alodokter.com/site/uploads/jenis-makanan-sehat.jpg'
    },
    {
        'judul': 'Panduan Gizi Seimbang - HelloSehat',
        'url': 'https://hellosehat.com/nutrisi/fakta-gizi/pedoman-gizi-seimbang/',
        'gambar': 'https://hellosehat.com/wp-content/uploads/2021/05/gizi-seimbang.jpg'
    },
    {
        'judul': '10 Makanan Sehat yang Baik untuk Tubuh - SehatQ',
        'url': 'https://www.sehatq.com/artikel/10-jenis-makanan-sehat-yang-baik-untuk-tubuh',
        'gambar': 'https://cdn.sehatq.com/articles/2021/01/10-makanan-sehat_300.jpeg'
    },
    {
        'judul': 'Makanan Bergizi dan Kandungan Gizi - DokterSehat',
        'url': 'https://doktersehat.com/nutrisi/gizi-dan-vitamin/makanan-bergizi/',
        'gambar': 'https://cdn.doktersehat.com/wp-content/uploads/2020/02/makanan-bergizi.jpg'
    },
    {
        'judul': 'Tips Pola Makan Sehat Sehari-hari - KlikDokter',
        'url': 'https://www.klikdokter.com/info-sehat/read/3639474/7-cara-untuk-mulai-pola-makan-sehat',
        'gambar': 'https://www.klikdokter.com/health-tools/images/thumb/health-info-tips-pola-makan.jpg'
    },
    {
        'judul': 'Pentingnya Serat Dalam Makanan - Alodokter',
        'url': 'https://www.alodokter.com/pentingnya-serat-dalam-makanan',
        'gambar': 'https://img.alodokter.com/site/uploads/pentingnya-serat-dalam-makanan.jpg'
    },
    {
        'judul': 'Mengenal Karbohidrat Kompleks dan Manfaatnya - HelloSehat',
        'url': 'https://hellosehat.com/nutrisi/fakta-gizi/karbohidrat-kompleks/',
        'gambar': 'https://hellosehat.com/wp-content/uploads/2022/01/karbo-kompleks.jpg'
    },
    {
        'judul': 'Superfood: Makanan Padat Nutrisi - KlikDokter',
        'url': 'https://www.klikdokter.com/info-sehat/read/3645621/apa-itu-superfood-dan-manfaatnya',
        'gambar': 'https://www.klikdokter.com/health-tools/images/thumb/superfood.jpg'
    },
    {
        'judul': 'Manfaat Sayuran Hijau untuk Kesehatan - SehatQ',
        'url': 'https://www.sehatq.com/artikel/manfaat-sayuran-hijau-untuk-kesehatan',
        'gambar': 'https://cdn.sehatq.com/images/sayuran-hijau.jpg'
    },
    {
        'judul': 'Camilan Sehat untuk Diet - Alodokter',
        'url': 'https://www.alodokter.com/camilan-sehat-untuk-diet',
        'gambar': 'https://img.alodokter.com/site/uploads/camilan-sehat.jpg'
    },
    {
        'judul': 'Fakta Gizi dalam Buah-buahan - HelloSehat',
        'url': 'https://hellosehat.com/nutrisi/fakta-gizi/nutrisi-dalam-buah/',
        'gambar': 'https://hellosehat.com/wp-content/uploads/2021/04/nutrisi-buah.jpg'
    },
    {
        'judul': 'Pola Makan Sehat Anak Sekolah - Kemkes RI',
        'url': 'https://www.gizi.depkes.go.id/artikel/pola-makan-anak-sekolah/',
        'gambar': 'https://www.gizi.depkes.go.id/uploads/images/makan-anak.jpg'
    }
]

# ====================
# DASHBOARD
# ====================
def dashboard(request):
    return render(request, 'dashboard/index.html', {'nama': 'Yasha'})

# ====================
# CRUD ARTIKEL
# ====================
def artikel_list(request):
    artikel_list = Artikel.objects.all().order_by('-tanggal')
    return render(request, 'dashboard/artikel_list.html', {'artikel_list': artikel_list})

def artikel_tambah(request):
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artikel_list')
    else:
        form = ArtikelForm()
    return render(request, 'dashboard/admin/artikel_form.html', {'form': form})

def artikel_edit(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if form.is_valid():
            form.save()
            return redirect('artikel_list')
    else:
        form = ArtikelForm(instance=artikel)
    return render(request, 'dashboard/admin/artikel_form.html', {'form': form, 'edit': True})

def artikel_delete(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    artikel.delete()
    return redirect('artikel_list')

def detail_artikel(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    rekomendasi = Artikel.objects.exclude(id=artikel.id).order_by('-tanggal')[:3]
    return render(request, 'detail_artikel.html', {'artikel': artikel, 'rekomendasi': rekomendasi})

# ====================
# FITUR CARI MAKANAN
# ====================
def cari_makanan(request):
    query = request.GET.get("q", "")
    hasil = []

    # Daftar nama makanan sehat sebagai keyword untuk rekomendasi
    rekomendasi_keyword = ["broccoli", "oatmeal", "boiled egg", "banana", "spinach", "almond"]
    rekomendasi = []

    # Ambil data dari API untuk masing-masing keyword
    for keyword in rekomendasi_keyword:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms=banana&search_simple=1&action=process&json=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            if products:
                produk = products[0]  # Ambil produk pertama
                nutriments = produk.get("nutriments", {})
                rekomendasi.append({
                    "name": produk.get("product_name", keyword.title()),
                    "kalori": round(nutriments.get("energy-kcal", 0), 2),
                    "protein": round(nutriments.get("proteins", 0), 2),
                    "lemak": round(nutriments.get("fat", 0), 2),
                    "karbo": round(nutriments.get("carbohydrates", 0), 2),
                })

    # Proses pencarian jika ada query dari user
    if query:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("products", [])[:6]:
                nutriments = item.get("nutriments", {})
                hasil.append({
                    "name": item.get("product_name", "Tidak diketahui"),
                    "calories": round(nutriments.get("energy-kcal", 0), 2),
                    "protein_g": round(nutriments.get("proteins", 0), 2),
                    "fat_total_g": round(nutriments.get("fat", 0), 2),
                    "carbohydrates_total_g": round(nutriments.get("carbohydrates", 0), 2),
                })

    artikel_list = Artikel.objects.all()[:6]
    artikel_luar = ARTIKEL_LUAR[:3]  # ambil dari data di atas

    context = {
        "query": query,
        "hasil": hasil,
        "rekomendasi": rekomendasi,
        "artikel_list": artikel_list,
        "artikel_luar": artikel_luar,
    }
    return render(request, "dashboard/cari_makanan.html", context)

# ====================
# HALAMAN TIPS SEHAT
# ====================
def healthy_page(request):
    return render(request, 'healty.html')

from django.shortcuts import render
import random

def berita_kesehatan(request):
    # Data dummy manual
    data_kesehatan = [
        {"title": "Makanan Sehat untuk Mahasiswa", "deskripsi": "Tips memilih makanan bergizi yang hemat dan sehat untuk anak kos.", "link": "#"},
        {"title": "Pentingnya Olahraga Rutin", "deskripsi": "Aktivitas fisik ringan seperti jalan kaki dapat menjaga tubuh tetap bugar.", "link": "#"},
        {"title": "Manfaat Minum Air Putih", "deskripsi": "Air putih membantu metabolisme dan konsentrasi saat belajar.", "link": "#"},
    ]

    data_teknologi = [
        {"title": "AI dalam Dunia Kesehatan", "deskripsi": "Kecerdasan buatan makin banyak digunakan untuk diagnosa penyakit.", "link": "#"},
        {"title": "Teknologi Wearable", "deskripsi": "Smartwatch kini bisa memantau detak jantung dan pola tidur kamu.", "link": "#"},
        {"title": "Inovasi Aplikasi Gaya Hidup Sehat", "deskripsi": "Banyak aplikasi yang bisa bantu atur pola makan dan olahraga.", "link": "#"},
    ]

    data_nasional = [
        {"title": "Program Gizi Nasional", "deskripsi": "Pemerintah luncurkan kampanye makan sehat untuk pelajar.", "link": "#"},
        {"title": "Gerakan Indonesia Sehat", "deskripsi": "Kampanye hidup sehat semakin digaungkan di berbagai kota.", "link": "#"},
        {"title": "Kesehatan Remaja di Indonesia", "deskripsi": "Masih banyak remaja yang belum sadar pentingnya gaya hidup sehat.", "link": "#"},
    ]

    semua_berita = data_kesehatan + data_teknologi + data_nasional
    random.shuffle(semua_berita)  # Supaya tampilannya berubah-ubah saat di-reload

    rekomendasi = [
        {
            "title": "Cara Makan Sehat ala Mahasiswa",
            "deskripsi": "Tips sederhana menjalani pola makan sehat dan hemat sebagai mahasiswa aktif.",
            "link": "#"
        },
        {
            "title": "Tips Tidur Berkualitas",
            "deskripsi": "Bagaimana menjaga kualitas tidur agar tubuh tetap segar dan fokus saat kuliah.",
            "link": "#"
        },
        {
            "title": "Manfaat Puasa bagi Tubuh",
            "deskripsi": "Puasa tidak hanya spiritual, tetapi juga memberikan dampak positif bagi kesehatan.",
            "link": "#"
        },
    ]

    return render(request, "berita_kesehatan.html", {
        "semua_berita": semua_berita,
        "rekomendasi": rekomendasi
    })
