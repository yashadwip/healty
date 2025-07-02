from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    tanggal = models.DateTimeField(auto_now_add=True)
    gambar = models.ImageField(upload_to='artikel_images/', blank=True, null=True)

    def __str__(self):
        return self.judul
