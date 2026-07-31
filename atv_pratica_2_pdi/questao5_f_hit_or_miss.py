"""
Questao 5f - A partir do resultado do item (c), utilizar a
transformada hit-or-miss para localizar cada um dos objetos vermelhos
na imagem.

O processo consiste na intersecao de todos os "hits" de uma imagem A
erodida com uma mascara D (o objeto a ser localizado), com o
complemento de A erodido por (W - D), onde W e um objeto que contem D
e nao contem outros objetos ou partes deles.

Nota: para esse script a funcao de erosao foi adaptada para tambem
retornar as coordenadas dos pixels que sobrevivem a erosao (usadas
depois na intersecao), diferente da erosao "padrao" de morfologia.py
usada nas outras questoes.

Requisitos:
- rodar 'questao5_a_b_c_quadro.py' antes, para gerar 'quadro_erosao.png'
  e 'resultado_uniao.png';
- ter as mascaras D e W de cada objeto vermelho (D_vermelho1.png /
  W_vermelho1.png, D_vermelho2.png / W_vermelho2.png, etc.), feitas
  manualmente (no Paint, por exemplo) a partir da imagem resultante.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import funcoes_morfologicas as fm


def erosao(imagem, elemento_estruturante, centro):
    """
    Versao da erosao adaptada para o hit-or-miss: alem da imagem
    erodida, tambem retorna a lista de coordenadas (i, j) dos pixels
    que sobreviveram a erosao.
    """
    altura_img, largura_img = imagem.shape
    altura_ee, largura_ee = elemento_estruturante.shape
    coord = []
    imagem_erodida = np.zeros_like(imagem)

    centro_x, centro_y = centro

    for i in range(altura_img):
        for j in range(largura_img):
            is_eroded = True
            for m in range(altura_ee):
                for n in range(largura_ee):
                    if elemento_estruturante[m, n] == 255:
                        x = i + (m - centro_x)
                        y = j + (n - centro_y)
                        if not (0 <= x < altura_img and 0 <= y < largura_img and imagem[x, y] == 255):
                            is_eroded = False
                            break
                if not is_eroded:
                    break
            if is_eroded:
                imagem_erodida[i, j] = 255
                coord.append((i, j))

    return imagem_erodida, coord


def hit_or_miss(A, D, W):
    # Erosao com o elemento estruturante D
    centro_D = D.shape[0] // 2, D.shape[1] // 2
    A_erodido, coord1 = erosao(A, D, centro_D)

    # Erosao com o elemento estruturante W - D
    WD = fm.diferenca(W, D)
    centro_WD = WD.shape[0] // 2, WD.shape[1] // 2
    complemento_A = cv2.bitwise_not(A)
    compA_erodido, coord2 = erosao(complemento_A, WD, centro_WD)

    # Fazendo a intersecao das duas listas de coordenadas
    coord = list(set(coord1).intersection(coord2))

    return coord


def gerar_resultado_final():
    """
    Une os objetos vermelhos (presentes em 'quadro_erosao.png', a
    imagem sem os pretos e com os buracos preenchidos) com o
    resultado da uniao azul + verde + amarelo (item c).
    """
    resultado = cv2.imread("resultado_uniao.png", cv2.IMREAD_GRAYSCALE)
    quadro = cv2.imread("quadro_erosao.png", cv2.IMREAD_GRAYSCALE)

    # converter quadro para binario
    _, quadro = cv2.threshold(quadro, 127, 255, cv2.THRESH_BINARY)

    # inverto para usar a funcao uniao() (objeto branco e fundo preto)
    quadro = cv2.bitwise_not(quadro)
    resultado = cv2.bitwise_not(resultado)

    # faco a uniao das imagens
    res_uniao = fm.uniao(quadro, resultado)

    # inverto a imagem para salvar com objeto preto e fundo branco
    res_uniao = cv2.bitwise_not(res_uniao)

    # salvo a imagem final
    cv2.imwrite("resultado_final.png", res_uniao)

    plt.imshow(res_uniao, cmap="gray")
    plt.title("resultado_final.png")
    plt.axis("off")
    plt.show()


def localizar_objeto_vermelho(indice):
    # Leitura da imagem
    A = cv2.imread("resultado_final.png", cv2.IMREAD_GRAYSCALE)
    # Leitura dos elementos estruturantes (mascaras feitas manualmente
    # para cada objeto vermelho)
    D = cv2.imread(f"D_vermelho{indice}.png", cv2.IMREAD_GRAYSCALE)
    W = cv2.imread(f"W_vermelho{indice}.png", cv2.IMREAD_GRAYSCALE)

    # inverte as imagens para funcionarem nas funcoes feitas na questao 3 e 4
    A = cv2.bitwise_not(A)
    D = cv2.bitwise_not(D)
    W = cv2.bitwise_not(W)

    # Executa a operacao hit-or-miss
    print(f"executando (objeto vermelho {indice})")
    coord = hit_or_miss(A, D, W)
    print("Coordenada(s):")
    print(coord)
    return coord


if __name__ == "__main__":
    gerar_resultado_final()

    # Repita para cada objeto vermelho identificado manualmente
    # (o relatorio original trabalhou com 3 objetos vermelhos)
    for indice in (1, 2, 3):
        localizar_objeto_vermelho(indice)
