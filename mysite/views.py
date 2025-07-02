import requests
from django.shortcuts import render, redirect
from artikel.models import Kategori, Artikel

def welcome(request):
    template_name = "landingpage/index.html"
    kategori_list = Kategori.objects.all()
    artikel_list = Artikel.objects.all()
    print(request.user)
    
    context = {
        "title": "Selamat datang",
        "kategori": kategori_list,
        "artikel": artikel_list,
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = "landingpage/detail.html"
    try:
        artkel = Artikel.objects.get(id=id)
    except Artikel.DoesNotExist:
        return redirect("not_found_artikel")
    
    artikel_lainnya = Artikel.objects.all().exclude(id=id)
    
    context = {
        "title": "Detail Artikel",
        "artikel": artkel,
        "artikel_lainnya" : artikel_lainnya,
    }
    return render(request, template_name, context)

def not_found_artikel(request):
    template_name = "healty.html"
    return render(request, template_name)

def healty(request):
    template_name = "healty.html"
    context = {
        "title": "Halaman"
    }
    return render(request, template_name, context)

def kontak(request):
    template_name = "cv.html"
    context = {
        "title": "Halaman Kontak"
    }
    return render(request, template_name, context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/auth-login')
    template_name = "dashboard/index.html"
    context = {
        "title": "Halaman Kontak"
    }
    return render(request, template_name, context)


def artikel_list(request):
    template_name = "dashboard/artikel_list.html."
    context = {
        "title": "Halaman Kontak"
    }
    return render(request, template_name, context)

def dashboard(request):
  return render(request, 'dashboard/index.html', {'nama': 'Yasha'})

