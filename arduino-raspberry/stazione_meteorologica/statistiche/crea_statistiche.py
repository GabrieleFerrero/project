import matplotlib.pyplot as plt
import numpy as np

def main():
    file = "./dati_stazione_0.csv"
    
    pioggia = np.genfromtxt(fname=file, skip_header=1, usecols=3, delimiter=",", missing_values="9999.9", usemask=True)
    uv = np.genfromtxt(fname=file, skip_header=1, usecols=4, delimiter=",", missing_values="9999.9", usemask=True)
    luce = np.genfromtxt(fname=file, skip_header=1, usecols=5, delimiter=",", missing_values="9999.9", usemask=True)
    pressione = np.genfromtxt(fname=file, skip_header=1, usecols=6, delimiter=",", missing_values="9999.9", usemask=True)
    umidita = np.genfromtxt(fname=file, skip_header=1, usecols=7, delimiter=",", missing_values="9999.9", usemask=True)
    temperatura = np.genfromtxt(fname=file, skip_header=1, usecols=8, delimiter=",", missing_values="9999.9", usemask=True)
    temperatura_interna = np.genfromtxt(fname=file, skip_header=1, usecols=9, delimiter=",", missing_values="9999.9", usemask=True)

    fig, ax0 = plt.subplots(figsize=(30,10))
    ax0.plot(pioggia, "o")
    plt.title("PIOGGIA")
    resolution_value = 250
    plt.savefig("pioggia.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax1 = plt.subplots(figsize=(30,10))
    ax1.plot(uv, "o")
    plt.title("UV")
    plt.savefig("uv.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax2 = plt.subplots(figsize=(30,10))
    ax2.plot(luce, "o")
    plt.title("LUCE")
    plt.savefig("luce.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax3 = plt.subplots(figsize=(30,10))
    ax3.plot(pressione, "o")
    plt.title("PRESSIONE")
    plt.savefig("pressione.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax4 = plt.subplots(figsize=(30,10))
    ax4.plot(umidita, "o")
    plt.title("UMIDITA")
    plt.savefig("umidita.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax5 = plt.subplots(figsize=(30,10))
    ax5.plot(temperatura, "o")
    plt.title("TEMPERATURA")
    plt.savefig("temperatura.png", format="png", dpi=resolution_value)
    plt.close()

    fig, ax6 = plt.subplots(figsize=(30,10))
    ax6.plot(temperatura_interna, "o")
    plt.title("TEMPERATURA INTERNA")
    plt.savefig("temperatura_interna.png", format="png", dpi=resolution_value)
    plt.close()
    
    plt.show()
            


if __name__ == "__main__":
    main()