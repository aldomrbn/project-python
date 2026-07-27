import math
import random
import time
import turtle
import winsound  # <--- [BARU] Import modul suara bawaan Windows

# 1. Pengaturan Layar Utama
layar = turtle.Screen()
layar.title("Game Ular Sederhana")
layar.bgcolor("black")
layar.setup(width=600, height=600)
layar.tracer(0)

# 2. Kepala Ular
kepala = turtle.Turtle()
kepala.speed(0)
kepala.shape("square")
kepala.color("green")
kepala.penup()
kepala.goto(0, 0)
kepala.arah = "stop"

# 3. Makanan Ular
makanan = turtle.Turtle()
makanan.speed(0)
makanan.shape("circle")
makanan.color("red")
makanan.penup()
makanan.goto(0, 100)

badan_ular = []
skor = 0
skor_tertinggi = 0

# Papan Skor
papan_skor = turtle.Turtle()
papan_skor.speed(0)
papan_skor.color("white")
papan_skor.penup()
papan_skor.hideturtle()
papan_skor.goto(0, 260)
papan_skor.write(
    "Skor: 0  Skor Tertinggi: 0", align="center", font=("Courier", 16, "normal")
)

# [BARU] Penyu Khusus Teks Game Over
pen_game_over = turtle.Turtle()
pen_game_over.speed(0)
pen_game_over.color("red")
pen_game_over.penup()
pen_game_over.hideturtle()


# [BARU] Fungsi Tampilan Game Over & Suara Kalah
def tampilkan_game_over():
    # Suara Game Over (Frekuensi Rendah / Nada Turun)
    winsound.Beep(400, 200)
    winsound.Beep(200, 400)

    # Cetak Teks Game Over di Tengah Layar
    pen_game_over.goto(0, 0)
    pen_game_over.write("GAME OVER", align="center", font=("Courier", 32, "bold"))
    pen_game_over.goto(0, -40)
    pen_game_over.write(
        "Tekan Arah Panah untuk Mulai Lagi",
        align="center",
        font=("Courier", 14, "normal"),
    )


def sembunyikan_game_over():
    pen_game_over.clear()


# Kontrol Arah
def ke_atas():
    if kepala.arah != "down":
        sembunyikan_game_over()
        kepala.arah = "up"


def ke_bawah():
    if kepala.arah != "up":
        sembunyikan_game_over()
        kepala.arah = "down"


def ke_kiri():
    if kepala.arah != "right":
        sembunyikan_game_over()
        kepala.arah = "left"


def ke_kanan():
    if kepala.arah != "left":
        sembunyikan_game_over()
        kepala.arah = "right"


def jalan():
    if kepala.arah == "up":
        kepala.sety(kepala.ycor() + 20)
    if kepala.arah == "down":
        kepala.sety(kepala.ycor() - 20)
    if kepala.arah == "left":
        kepala.setx(kepala.xcor() - 20)
    if kepala.arah == "right":
        kepala.setx(kepala.xcor() + 20)


layar.listen()
layar.onkeypress(ke_atas, "Up")
layar.onkeypress(ke_bawah, "Down")
layar.onkeypress(ke_kiri, "Left")
layar.onkeypress(ke_kanan, "Right")

# Loop Utama Game
while True:
    layar.update()

    # Cek Tabrakan Dinding
    if (
        kepala.xcor() > 290
        or kepala.xcor() < -290
        or kepala.ycor() > 290
        or kepala.ycor() < -290
    ):
        tampilkan_game_over()  # <--- [BARU] Panggil fungsi Game Over
        time.sleep(1)
        kepala.goto(0, 0)
        kepala.arah = "stop"

        for bagian in badan_ular:
            bagian.goto(1000, 1000)
        badan_ular.clear()

        skor = 0
        papan_skor.clear()
        papan_skor.write(
            f"Skor: {skor}  Skor Tertinggi: {skor_tertinggi}",
            align="center",
            font=("Courier", 16, "normal"),
        )

    # Cek Makan Makanan
    if kepala.distance(makanan) < 20:
        # [BARU] Suara Makan (Beep Frekuensi Tinggi)
        winsound.Beep(1000, 80)

        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        makanan.goto(x, y)

        badan_baru = turtle.Turtle()
        badan_baru.speed(0)
        badan_baru.shape("square")
        badan_baru.color("lightgreen")
        badan_baru.penup()
        badan_ular.append(badan_baru)

        skor += 10
        if skor > skor_tertinggi:
            skor_tertinggi = skor

        papan_skor.clear()
        papan_skor.write(
            f"Skor: {skor}  Skor Tertinggi: {skor_tertinggi}",
            align="center",
            font=("Courier", 16, "normal"),
        )

    # Pergerakan Badan
    for index in range(len(badan_ular) - 1, 0, -1):
        x = badan_ular[index - 1].xcor()
        y = badan_ular[index - 1].ycor()
        badan_ular[index].goto(x, y)

    if len(badan_ular) > 0:
        x = kepala.xcor()
        y = kepala.ycor()
        badan_ular[0].goto(x, y)

    jalan()

    # Cek Tabrakan Badan
    for bagian in badan_ular:
        if bagian.distance(kepala) < 20:
            tampilkan_game_over()  # <--- [BARU] Panggil fungsi Game Over
            time.sleep(1)
            kepala.goto(0, 0)
            kepala.arah = "stop"

            for b in badan_ular:
                b.goto(1000, 1000)
            badan_ular.clear()

            skor = 0
            papan_skor.clear()
            papan_skor.write(
                f"Skor: {skor}  Skor Tertinggi: {skor_tertinggi}",
                align="center",
                font=("Courier", 16, "normal"),
            )

    time.sleep(0.1)

layar.mainloop()