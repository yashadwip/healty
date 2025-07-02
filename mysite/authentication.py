from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout

def login_view(request):
    template_name = "login.html"
    pesan = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            pesan = "Username dan password wajib diisi"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                pesan = "Username atau password salah"
    context = {
        'pesan': pesan
    }
    return render(request, template_name, context)

def registrasi(request):
    template_name = "registrasi.html"
    pesan = ''
    if request.method == "POST":
        username = request.POST.get('username')
        nama_depan = request.POST.get('first_name')
        nama_belakang = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not nama_depan or not nama_belakang or not password1 or not password2:
            pesan = "Semua data wajib diisi yah"
        elif password1 != password2:
            pesan = "Password 1 dan 2 tidak sama"
        elif User.objects.filter(username=username).exists():
            pesan = "Username sudah digunakan"
        else:
            # Buat dan simpan user baru
            User.objects.create_user(
                username=username,
                first_name=nama_depan,
                last_name=nama_belakang,
                password=password1
            )
            return redirect("/auth-login")

    context = {
        'pesan': pesan
    }
    return render(request, template_name, context)

def logout(request):
    auth_logout(request)
    return redirect('/')
