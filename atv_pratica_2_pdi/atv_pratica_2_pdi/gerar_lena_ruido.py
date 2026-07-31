"""
gerar_lena_ruido.py

Utilitario para gerar 'lena_ruido.bmp' (usada na Questao 2) a partir
de 'lena_gray.bmp', adicionando ruido gaussiano. Nao faz parte do
relatorio original, mas resolve o problema de nao ter mais o arquivo
'lena_ruido.bmp' original.

Requisitos: coloque 'lena_gray.bmp' em 'imagens_entrada/' antes de
rodar este script.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

CAMINHO_ENTRADA = "imagens_entrada/lena_gray.bmp"
CAMINHO_SAIDA = "imagens_entrada/lena_ruido.bmp"


def gerar_ruido(caminho_entrada=CAMINHO_ENTRADA, caminho_saida=CAMINHO_SAIDA,
                 media=0, desvio_padrao=25, mostrar=True):
    img = cv2.imread(caminho_entrada, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(
            f"Nao encontrei '{caminho_entrada}'. Coloque a imagem 'lena_gray.bmp' "
            f"dentro da pasta 'imagens_entrada/' antes de rodar este script."
        )

    # Gera ruido gaussiano com a mesma forma da imagem
    ruido = np.random.normal(media, desvio_padrao, img.shape).astype(np.int16)

    # Soma o ruido a imagem original e garante que o resultado fique em [0, 255]
    img_ruido = np.clip(img.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

    cv2.imwrite(caminho_saida, img_ruido)
    print(f"Imagem com ruido salva em: {caminho_saida}")

    if mostrar:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1), plt.imshow(img, cmap='gray'), plt.title('Imagem Original')
        plt.axis('off')
        plt.subplot(1, 2, 2), plt.imshow(img_ruido, cmap='gray'), plt.title('Imagem com Ruido')
        plt.axis('off')
        plt.show()

    return img_ruido


if __name__ == "__main__":
    gerar_ruido()
