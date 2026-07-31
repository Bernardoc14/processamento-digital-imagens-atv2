"""
binarizar_imagem.py

Utilitario para "limpar" imagens obtidas por print/screenshot do PDF
do relatorio, forcando cada pixel a ficar exatamente 0 (preto) ou 255
(branco). Isso e necessario porque as funcoes de fm.py e morfologia.py
comparam pixels com '== 255' e '== 0', e um print costuma introduzir
tons intermediarios de cinza nas bordas (anti-aliasing).

Uso:
    python binarizar_imagem.py imagens_entrada/imagem1.png
"""

import sys
import cv2


def binarizar(caminho, limiar=127, sobrescrever=True):
    img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Nao encontrei o arquivo: {caminho}")

    _, img_binaria = cv2.threshold(img, limiar, 255, cv2.THRESH_BINARY)

    destino = caminho if sobrescrever else caminho.replace(".png", "_binaria.png")
    cv2.imwrite(destino, img_binaria)
    print(f"Imagem binarizada salva em: {destino}")
    return img_binaria


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python binarizar_imagem.py <caminho_da_imagem> [limiar]")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    limiar_escolhido = int(sys.argv[2]) if len(sys.argv) > 2 else 127
    binarizar(caminho_arquivo, limiar_escolhido)
