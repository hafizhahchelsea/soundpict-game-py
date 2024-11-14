import pygame
import random
import sys 

pygame.init()

# konfigurasi layar 
lebar_layar = 800
tinggi_layar = 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Tebak Hewan")

# warna yang digunakan 
putih = (255,255,255)
hitam = (0,0,0)

# inisialisasi font
font = pygame.font.Font(None, 36)

# inisialisasi suara untuk setiap hewan dan list suara dan nama hewan 
suara_singa = pygame.mixer.Sound("singa.wav")
suara_gajah = pygame.mixer.Sound("gajah.wav")
suara_kuda = pygame.mixer.Sound("kuda.wav")
suara_kucing = pygame.mixer.Sound("kucing.wav")
suara_monyet = pygame.mixer.Sound("monyet.wav")

suara_hewan = [suara_singa, suara_gajah, suara_kuda, suara_kucing, suara_monyet]
hewan = ["Singa", "Gajah", "Kuda", "Kucing", "Monyet"]

# Gambar hewan
gambar_hewan = {
    "Singa": pygame.transform.scale(pygame.image.load("singa.jpg"), (200, 200)),
    "Gajah": pygame.transform.scale(pygame.image.load("gajah.jpg"), (200, 200)),
    "Kuda": pygame.transform.scale(pygame.image.load("kuda.jpg"), (200, 200)),
    "Kucing": pygame.transform.scale(pygame.image.load("kucing.jpg"), (200, 200)),
    "Monyet": pygame.transform.scale(pygame.image.load("monyet.jpg"), (200, 200)),
}

# Fungsi untuk menampilkan teks di layar
def tampilkan_teks(teks, warna, x, y):
    teks_layar = font.render(teks, True, warna)
    teks_kotak = teks_layar.get_rect(center=(x, y))
    layar.blit(teks_layar, teks_kotak)

# Fungsi untuk menampilkan gambar dengan batas hitam
def tampilkan_gambar_dengan_batas(gambar, x, y):
    kotak_gambar = gambar.get_rect(center=(x, y))
    pygame.draw.rect(layar, hitam, kotak_gambar, 2)
    layar.blit(gambar, kotak_gambar)

# Fungsi untuk menampilkan menu utama
def tampilkan_menu():
    layar.fill(putih)
    tampilkan_teks("Tebak Hewan", hitam, lebar_layar // 2, 100)

    tombol_main = pygame.Rect(lebar_layar // 2 - 75, tinggi_layar // 2 - 25, 150, 50)
    pygame.draw.rect(layar, hitam, tombol_main, 2)
    tampilkan_teks("Main", hitam, lebar_layar // 2, tinggi_layar // 2)

    tombol_keluar = pygame.Rect(lebar_layar // 2 - 75, tinggi_layar // 2 + 50, 150, 50)
    pygame.draw.rect(layar, hitam, tombol_keluar, 2)
    tampilkan_teks("Keluar", hitam, lebar_layar // 2, tinggi_layar // 2 + 75)

    pygame.display.update()
    return tombol_main, tombol_keluar

# Fungsi untuk menampilkan layar akhir permainan
def tampilkan_layar_akhir(skor):
    layar.fill(putih)
    tampilkan_teks(f"Anda benar {skor} dari 3.", hitam, lebar_layar // 2, tinggi_layar // 2)

    tombol_retry = pygame.Rect(lebar_layar // 2 - 75, tinggi_layar // 2 + 50, 150, 50)
    pygame.draw.rect(layar, hitam, tombol_retry, 2)
    tampilkan_teks("Main lagi", hitam, lebar_layar // 2, tinggi_layar // 2 + 75)

    pygame.display.update()
    return tombol_retry

# Variabel permainan
berjalan = True
dalam_menu = True
pertanyaan_tersisa = 3
skor = 0
sedang_memainkan_suara = False
tombol_main, tombol_keluar, tombol_retry = None, None, None
hewan_acak = []

while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
        elif dalam_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tombol_main and tombol_main.collidepoint(event.pos):
                    dalam_menu = False
                elif tombol_keluar and tombol_keluar.collidepoint(event.pos):
                    berjalan = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not sedang_memainkan_suara and pertanyaan_tersisa > 0:
                indeks_hewan_acak = random.sample(range(len(hewan)), 3)
                suara_hewan_sekarang = suara_hewan[indeks_hewan_acak[0]]
                hewan_sekarang = hewan[indeks_hewan_acak[0]]
                suara_hewan_sekarang.play()
                sedang_memainkan_suara = True
                hewan_acak = [hewan[indeks_hewan_acak[0]], hewan[indeks_hewan_acak[1]], hewan[indeks_hewan_acak[2]]]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sedang_memainkan_suara and pertanyaan_tersisa > 0:
                tebakan_benar = False
                for i in range(3):
                    if (
                        (i + 1) * lebar_layar // 4 - 100 <= event.pos[0] <= (i + 1) * lebar_layar // 4 + 100
                        and tinggi_layar // 2 - 100 <= event.pos[1] <= tinggi_layar // 2 + 100
                        and hewan_sekarang == hewan_acak[i]
                    ):
                        tebakan_benar = True
                        break

                pertanyaan_tersisa -= 1
                sedang_memainkan_suara = False

                if tebakan_benar:
                    skor += 1 

    if dalam_menu:
        tombol_main, tombol_keluar = tampilkan_menu()
    else:
        layar.fill(putih)

        if pertanyaan_tersisa > 0:
            if sedang_memainkan_suara:
                tampilkan_teks("Suara Hewan Apakah itu?", hitam, lebar_layar// 2,100)
                for i in range(3):
                    tampilkan_gambar_dengan_batas(gambar_hewan[hewan_acak[i]], (i + 1) * lebar_layar // 4, tinggi_layar // 2)
            else:
                tampilkan_teks("Tekan spasi untuk memainkan suara.", hitam, lebar_layar // 2, 100)
        else:
            tombol_retry = tampilkan_layar_akhir(skor)
            if tombol_retry and event.type == pygame.MOUSEBUTTONDOWN and tombol_retry.collidepoint(event.pos):
                pertanyaan_tersisa = 3
                skor = 0
                dalam_menu = True

        pygame.display.update()

pygame.quit()
sys.exit()
