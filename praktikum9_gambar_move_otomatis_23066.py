import pygame
import sys
import random

pygame.init()

# ============================
# SETUP LAYAR
# ============================
LEBAR = 800
TINGGI = 600
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Game Pesawat Tembak - Level & Nyawa")

font = pygame.font.Font(None, 40)
font_big = pygame.font.Font(None, 80)
clock = pygame.time.Clock()

# ============================
# LOAD GAMBAR
# ============================
def load_img(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        print(f"Gagal memuat {path}")
        sys.exit()

# Background luar angkasa
try:
    bg = pygame.image.load("space_bg.webp").convert()
    bg = pygame.transform.scale(bg, (LEBAR, TINGGI))
except:
    print("Gagal memuat space_bg.webp")
    sys.exit()

pesawat = load_img("pesawat.webp", (80, 80))
peluru_img = load_img("peluru.webp", (15, 30))
musuh_img = load_img("musuh.webp", (60, 60))

# ============================
# POSISI PLAYER
# ============================
player_x = LEBAR // 2
player_y = TINGGI - 120
kecepatan = 6

peluru_list = []
musuh_list = []

skor = 0
level = 1
spawn_rate = 50
frame_count = 0

nyawa = 3
game_over = False

# ============================
# GAME LOOP
# ============================
while True:
    # Jika game over, tampilkan layar game over
    if game_over:
        layar.blit(bg, (0, 0))

        teks_over = font_big.render("GAME OVER", True, (255, 0, 0))
        layar.blit(teks_over, (LEBAR//2 - 160, TINGGI//2 - 100))

        teks_score = font.render(f"Skor Akhir: {skor}", True, (255, 255, 255))
        layar.blit(teks_score, (LEBAR//2 - 90, TINGGI//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        continue

    # ====================================
    # EVENT
    # ====================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Tembak peluru
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                peluru_list.append([player_x + 32, player_y])

    tombol = pygame.key.get_pressed()
    if tombol[pygame.K_LEFT]:
        player_x -= kecepatan
    if tombol[pygame.K_RIGHT]:
        player_x += kecepatan

    player_x = max(0, min(player_x, LEBAR - 80))

    # ====================================
    # SPAWN MUSUH
    # ====================================
    frame_count += 1
    if frame_count % spawn_rate == 0:
        mx = random.randint(0, LEBAR - 60)
        musuh_list.append([mx, -50])

    # ====================================
    # UPDATE PELURU
    # ====================================
    for p in peluru_list:
        p[1] -= 10
    peluru_list = [p for p in peluru_list if p[1] > -40]

    # ====================================
    # UPDATE MUSUH
    # ====================================
    for m in musuh_list:
        kecepatan_musuh = 2 + (level * 0.7)
        m[1] += kecepatan_musuh

    # CEK MUSUH YANG LOLOS (TIDAK KENA TEMBAK)
    for m in musuh_list:
        if m[1] > TINGGI:
            nyawa -= 1
            musuh_list.remove(m)

            if nyawa <= 0:
                game_over = True

    # ====================================
    # TABRAKAN PELURU vs MUSUH
    # ====================================
    for p in peluru_list:
        p_rect = pygame.Rect(p[0], p[1], 15, 30)
        for m in musuh_list:
            m_rect = pygame.Rect(m[0], m[1], 60, 60)
            if p_rect.colliderect(m_rect):
                skor += 10
                musuh_list.remove(m)
                peluru_list.remove(p)
                break

    # ====================================
    # LEVEL UP
    # ====================================
    if skor >= level * 100:
        level += 1
        spawn_rate = max(10, spawn_rate - 5)

    # ====================================
    # GAMBAR LAYAR
    # ====================================
    layar.blit(bg, (0, 0))

    # Musuh
    for m in musuh_list:
        layar.blit(musuh_img, (m[0], m[1]))

    # Peluru
    for p in peluru_list:
        layar.blit(peluru_img, (p[0], p[1]))

    # Player
    layar.blit(pesawat, (player_x, player_y))

    # UI
    layar.blit(font.render(f"Skor: {skor}", True, (255, 255, 255)), (20, 20))
    layar.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (20, 60))
    layar.blit(font.render(f"Nyawa: {nyawa}", True, (255, 100, 100)), (20, 100))

    pygame.display.flip()
    clock.tick(60)
