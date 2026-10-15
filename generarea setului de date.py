import math
import random

X_MIN, X_MAX = -300, 300
Y_MIN, Y_MAX = -300, 300

NR_PUNCTE = 3000
FISIER = "puncte.txt"

ZONE = [
    {"mx": -150, "my":  120, "sx": 30, "sy": 40},  
    {"mx":  160, "my":  100, "sx": 50, "sy": 25},  
    {"mx":    0, "my": -170, "sx": 40, "sy": 35}, 
]


def gauss(x, m, sigma):
    return math.exp(-((m - x) ** 2) / (2 * sigma ** 2))


def genereaza_coordonata(m, sigma, vmin, vmax):
    while True:
        x = random.uniform(vmin, vmax)      
        g = gauss(x, m, sigma)              
        prag = random.uniform(0, 1)         
        if g > prag:                         
            return x


def main():
    puncte = []
    for _ in range(NR_PUNCTE):
        zona = random.randrange(len(ZONE))   
        z = ZONE[zona]
        x = genereaza_coordonata(z["mx"], z["sx"], X_MIN, X_MAX)
        y = genereaza_coordonata(z["my"], z["sy"], Y_MIN, Y_MAX)
        puncte.append((x, y, zona))

    with open(FISIER, "w") as f:
        for x, y, zona in puncte:
            f.write(f"{x:.2f} {y:.2f} {zona}\n")

    print(f"{'Nr.':>5} | {'x':>9} | {'y':>9} | {'Zona':>4}")
    print("-" * 37)
    for i, (x, y, zona) in enumerate(puncte, start=1):
        print(f"{i:>5} | {x:>9.2f} | {y:>9.2f} | {zona:>4}")
    print("-" * 37)

    print("\nRezumat pe zone:")
    for k, z in enumerate(ZONE):
        pz = [(x, y) for x, y, zn in puncte if zn == k]
        mx = sum(p[0] for p in pz) / len(pz)
        my = sum(p[1] for p in pz) / len(pz)
        print(f"  Zona {k}: {len(pz):4d} puncte | centru setat ({z['mx']}, {z['my']})"
              f" | media obtinuta ({mx:.1f}, {my:.1f})")
    print(f"\nTotal: {len(puncte)} puncte scrise in '{FISIER}'")

    deseneaza(puncte)


def deseneaza(puncte):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib nu este instalat -> desenez cu tkinter."
              "\n(Pentru graficul matplotlib: pip install matplotlib)")
        deseneaza_tkinter(puncte)
        return

    culori = ["tab:red", "tab:blue", "tab:green"]
    plt.figure(figsize=(7, 7))
    for k in range(len(ZONE)):
        xs = [x for x, y, zn in puncte if zn == k]
        ys = [y for x, y, zn in puncte if zn == k]
        plt.scatter(xs, ys, s=4, c=culori[k], label=f"Zona {k}")
    plt.axhline(0, color="gray", lw=0.8)
    plt.axvline(0, color="gray", lw=0.8)
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)
    plt.gca().set_aspect("equal")
    plt.title("3000 de puncte generate cu functia lui Gauss")
    plt.legend()
    plt.savefig("puncte.png", dpi=120)
    print("\nGrafic salvat in 'puncte.png'. Se deschide fereastra...")
    plt.show()


def deseneaza_tkinter(puncte):
    import tkinter as tk

    latime = X_MAX - X_MIN
    inaltime = Y_MAX - Y_MIN
    culori = ["red", "blue", "green"]

    def ecran(x, y):
        return x + latime / 2, inaltime / 2 - y

    fereastra = tk.Tk()
    fereastra.title("3000 de puncte generate cu functia lui Gauss")
    c = tk.Canvas(fereastra, width=latime, height=inaltime, bg="white")
    c.pack()

    c.create_line(0, inaltime / 2, latime, inaltime / 2, fill="gray")
    c.create_line(latime / 2, 0, latime / 2, inaltime, fill="gray")

    for x, y, zona in puncte:
        ex, ey = ecran(x, y)
        c.create_oval(ex - 1.5, ey - 1.5, ex + 1.5, ey + 1.5,
                      fill=culori[zona], outline=culori[zona])

    for k in range(len(ZONE)):
        c.create_text(latime - 60, 15 + 18 * k, text=f"Zona {k}",
                      fill=culori[k], anchor="w")

    fereastra.mainloop()


if __name__ == "__main__":
    main()