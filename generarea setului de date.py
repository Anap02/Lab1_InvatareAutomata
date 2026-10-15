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

    try:
        import matplotlib.pyplot as plt
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
        plt.show()
    except ImportError:
        pass


if __name__ == "__main__":
    main()