"""
Questao 5e - A partir do resultado do item (c), encontrar o esqueleto
dos objetos de cor: azul, amarelo e verde.

Baseado no algoritmo de esqueletonizacao morfologica descrito no livro
"Processamento Digital de Imagens" (3a edicao, Gonzalez e Woods):
S(A) = uniao_k [ (A erodido k vezes) - (abertura da k-esima erosao) ]

Requisitos: rodar 'questao5_a_b_c_quadro.py' antes, para gerar os
arquivos 'p_azul.png', 'p_verde.png' e 'p_amarelo.png'.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import morfologia as mf
import funcoes_morfologicas as fm

# Elemento estruturante usado: vetor de 1s (255) 30x30, centro (15, 15)
es = np.ones((30, 30), dtype=np.uint8) * 255
centro = (15, 15)


def esqueleto(imagem, es, centro):
    erosoes = []
    aberturas = []
    k = 0
    while True:
        img_erosao = imagem.copy()
        for i in range(0, k):
            img_erosao = mf.erosao(img_erosao, es, centro)

        if np.all(img_erosao == 0):
            break

        erosoes.append(img_erosao.copy())
        aberturas.append(mf.abertura(img_erosao, es, centro))

        k += 1

    esqueleto_final = np.zeros_like(imagem)
    for i in range(k):
        diferenca = fm.diferenca(erosoes[i], aberturas[i])
        esqueleto_final = fm.uniao(esqueleto_final, diferenca)

    return esqueleto_final


def processar(caminho_imagem, nome_cor):
    objeto = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

    # converte pra binaria
    _, objeto = cv2.threshold(objeto, 127, 255, cv2.THRESH_BINARY)

    # invertendo as cores pra bater com a funcao (objeto branco e fundo preto)
    objeto = cv2.bitwise_not(objeto)

    esq = esqueleto(objeto, es, centro)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(objeto, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title(f"Esqueleto ({nome_cor})")
    plt.imshow(esq, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return esq


if __name__ == "__main__":
    processar("p_amarelo.png", "amarelo")
    processar("p_verde.png", "verde")
    processar("p_azul.png", "azul")
