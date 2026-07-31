"""
Questao 5 - A partir da imagem "quadro.png" resolva o que se pede:

a) Preencher todos os buracos dos objetos pretos
b) Eliminar todos e somente os objetos pretos
c) Preencher os buracos dos objetos de cor: azul, amarelo e verde

Requisitos: colocar 'quadro.png' na pasta 'imagens_entrada/'
(imagem colorida com objetos vermelhos com buraco branco, e um
objeto azul/verde/amarelo com buracos pretos, sobre fundo com
pontos pretos espalhados).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import morfologia as mf
import funcoes_morfologicas as fm

CAMINHO_QUADRO = "imagens_entrada/quadro.png"


def comparar_imagens(imagem_colorida, imagem_binaria):
    # Garantir que a imagem binaria seja binaria (0 ou 255)
    imagem_binaria = cv2.threshold(imagem_binaria, 127, 255, cv2.THRESH_BINARY)[1]

    # Criar uma imagem de saida com a mesma forma da imagem colorida
    imagem_resultante = np.zeros_like(imagem_colorida)

    # Onde a imagem binaria e preta (0), a imagem resultante sera preta
    # Onde a imagem binaria nao e preta, a imagem resultante sera a cor da imagem colorida
    altura, largura = imagem_binaria.shape
    for i in range(altura):
        for j in range(largura):
            if imagem_binaria[i, j] == 0:
                imagem_resultante[i, j] = [0, 0, 0]
            else:
                imagem_resultante[i, j] = imagem_colorida[i, j]

    return imagem_resultante


def eliminar_objs_pretos(imagem_colorida):
    # Criar uma imagem de saida com a mesma forma da imagem colorida
    imagem_resultante = np.zeros_like(imagem_colorida)

    # se aquele ponto da imagem colorida nao for preto, aquele ponto na imagem resultante
    # sera a cor da imagem colorida, se for preto, esse ponto assume a cor branca
    # usando isso eu mantenho as cores originais da imagem colorida
    altura, largura = imagem_colorida.shape[:2]  # pega a altura e a largura da imagem
    for i in range(altura):
        for j in range(largura):
            if not np.array_equal(imagem_colorida[i, j], [0, 0, 0]):
                imagem_resultante[i, j] = imagem_colorida[i, j]
            else:
                imagem_resultante[i, j] = 255

    return imagem_resultante


def questao_5a():
    # carrega a imagem colorida
    imagem_colorida = cv2.imread(CAMINHO_QUADRO)

    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

    # Converter para imagem binaria, o que for 0 e preto, o que for acima de 0 vira branco
    _, imagem_binaria = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY)

    # Inverter a imagem binaria, pq as funcoes de dilatacao e erosao consideram objetos brancos
    # e fundo preto diferente da imagem quadro.png
    imagem_binaria_invertida = cv2.bitwise_not(imagem_binaria)

    # Definir elemento estruturante 5x5 e centro (2, 2)
    elemento_estruturante = np.ones((5, 5), dtype=np.uint8) * 255
    centro = (2, 2)

    # Aplicar fechamento
    imagem_fechamento = mf.fechamento(imagem_binaria_invertida, elemento_estruturante, centro)

    # Inverter novamente a imagem apos fechamento, para que os objetos fiquem pretos e o fundo branco
    imagem_fechamento_invertida = cv2.bitwise_not(imagem_fechamento)

    # mantendo as cores originais e os buracos dos pontos pretos preenchidos
    imagem_colorida_fechamento = comparar_imagens(imagem_colorida, imagem_fechamento_invertida)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.title('Imagem Original')
    plt.imshow(cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Imagem com os pretos fechados')
    plt.imshow(cv2.cvtColor(imagem_colorida_fechamento, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # salva para usar nas proximas etapas ("quadro_erosao.png" no relatorio original)
    cv2.imwrite('quadro_erosao.png', imagem_colorida_fechamento)


def questao_5b():
    # carrega a imagem colorida
    imagem_colorida = cv2.imread(CAMINHO_QUADRO)

    # mantendo as cores originais e eliminando os objetos pretos
    imagem_colorida_sem_pretos = eliminar_objs_pretos(imagem_colorida)

    # salve como png a imagem_colorida_erosao
    cv2.imwrite('quadro_erosao.png', imagem_colorida_sem_pretos)

    # Plotar as imagens
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.title('Imagem Original')
    plt.imshow(cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('imagem sem objetos pretos')
    plt.imshow(cv2.cvtColor(imagem_colorida_sem_pretos, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.show()


def _separar_por_cor(imagem_cinza):
    """
    Separa as 3 formas coloridas (azul, verde, amarelo) da imagem
    "quadro_erosao.png" com base no nivel de intensidade em escala de
    cinza, usando limiares e a funcao diferenca() implementada na
    questao 3.
    """
    # pegando todas as cores binarizadas
    _, imagem_binaria_todas_as_cores = cv2.threshold(imagem_cinza, 230, 255, cv2.THRESH_BINARY)
    # pegando todas as cores binarizadas menos o amarelo
    _, todos_menos_amarelo = cv2.threshold(imagem_cinza, 220, 255, cv2.THRESH_BINARY)
    # invertendo pra funcionar na funcao de diferenca
    inverter_todas_as_cores = cv2.bitwise_not(imagem_binaria_todas_as_cores)
    inverter_todos_menos_amarelo = cv2.bitwise_not(todos_menos_amarelo)
    # pegando a parte amarela
    imagem_binaria_amarelo = fm.diferenca(inverter_todas_as_cores, inverter_todos_menos_amarelo)

    # pegando apenas o azul (limiar 50)
    _, imagem_binaria_azul = cv2.threshold(imagem_cinza, 50, 255, cv2.THRESH_BINARY)

    # pegando apenas o azul e vermelho (limiar 127)
    _, imagem_binaria_vermelho_azul = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)
    inverter_azul_vermelho = cv2.bitwise_not(imagem_binaria_vermelho_azul)

    # pegando a parte verde e amarela
    imagem_binaria_verde_amarela = fm.diferenca(inverter_todas_as_cores, inverter_azul_vermelho)
    imagem_binaria_verde = fm.diferenca(imagem_binaria_verde_amarela, imagem_binaria_amarelo)

    # invertendo pra pegar o resultado de verdade
    imagem_binaria_amarelo = cv2.bitwise_not(imagem_binaria_amarelo)
    imagem_binaria_verde = cv2.bitwise_not(imagem_binaria_verde)

    return imagem_binaria_azul, imagem_binaria_verde, imagem_binaria_amarelo


def questao_5c():
    # imagem erodida/preenchida da questao anterior ("quadro_erosao.png")
    imagem_colorida = cv2.imread('quadro_erosao.png')
    imagem_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

    imagem_binaria_azul, imagem_binaria_verde, imagem_binaria_amarelo = _separar_por_cor(imagem_cinza)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1), plt.imshow(imagem_binaria_azul, cmap='gray'), plt.title('Imagem Binaria - Parte Azul')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(imagem_binaria_verde, cmap='gray'), plt.title('Imagem Binaria - Parte Verde')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(imagem_binaria_amarelo, cmap='gray'), plt.title('Imagem Binaria - Parte amarelo')
    plt.axis('off')
    plt.show()

    # Preenchimento das 3 partes separadamente (fechamento com ES de 1s)
    # Parte azul: ES 40x40, centro (20,20)
    es_azul = np.ones((40, 40), dtype=np.uint8) * 255
    centro_azul = (20, 20)
    imagem_binaria_azul_inv = cv2.bitwise_not(imagem_binaria_azul)
    imagem_binaria_azul_preenchida = mf.fechamento(imagem_binaria_azul_inv, es_azul, centro_azul)
    imagem_binaria_azul_preenchida = cv2.bitwise_not(imagem_binaria_azul_preenchida)
    cv2.imwrite('p_azul.png', imagem_binaria_azul_preenchida)

    # Parte verde: ES 30x30, centro (15,15)
    es_verde = np.ones((30, 30), dtype=np.uint8) * 255
    centro_verde = (15, 15)
    imagem_binaria_verde_inv = cv2.bitwise_not(imagem_binaria_verde)
    imagem_binaria_verde_preenchida = mf.fechamento(imagem_binaria_verde_inv, es_verde, centro_verde)
    imagem_binaria_verde_preenchida = cv2.bitwise_not(imagem_binaria_verde_preenchida)
    cv2.imwrite('p_verde.png', imagem_binaria_verde_preenchida)

    # Parte amarela: ES 10x10, centro (5,5)
    es_amarelo = np.ones((10, 10), dtype=np.uint8) * 255
    centro_amarelo = (5, 5)
    imagem_binaria_amarelo_inv = cv2.bitwise_not(imagem_binaria_amarelo)
    imagem_binaria_amarelo_preenchida = mf.fechamento(imagem_binaria_amarelo_inv, es_amarelo, centro_amarelo)
    imagem_binaria_amarelo_preenchida = cv2.bitwise_not(imagem_binaria_amarelo_preenchida)
    cv2.imwrite('p_amarelo.png', imagem_binaria_amarelo_preenchida)

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 3, 1), plt.imshow(imagem_binaria_azul, cmap='gray'), plt.title('Azul - original')
    plt.axis('off')
    plt.subplot(2, 3, 4), plt.imshow(imagem_binaria_azul_preenchida, cmap='gray'), plt.title('Azul - preenchida')
    plt.axis('off')
    plt.subplot(2, 3, 2), plt.imshow(imagem_binaria_verde, cmap='gray'), plt.title('Verde - original')
    plt.axis('off')
    plt.subplot(2, 3, 5), plt.imshow(imagem_binaria_verde_preenchida, cmap='gray'), plt.title('Verde - preenchida')
    plt.axis('off')
    plt.subplot(2, 3, 3), plt.imshow(imagem_binaria_amarelo, cmap='gray'), plt.title('Amarelo - original')
    plt.axis('off')
    plt.subplot(2, 3, 6), plt.imshow(imagem_binaria_amarelo_preenchida, cmap='gray'), plt.title('Amarelo - preenchida')
    plt.axis('off')
    plt.show()

    # leio as imagens preenchidas
    p_azul = cv2.imread("p_azul.png", cv2.IMREAD_GRAYSCALE)
    p_verde = cv2.imread("p_verde.png", cv2.IMREAD_GRAYSCALE)
    p_amarelo = cv2.imread("p_amarelo.png", cv2.IMREAD_GRAYSCALE)

    # inverto para usar a funcao uniao() (objeto branco e fundo preto)
    p_azul = cv2.bitwise_not(p_azul)
    p_verde = cv2.bitwise_not(p_verde)
    p_amarelo = cv2.bitwise_not(p_amarelo)

    # faco a uniao das imagens
    res_uniao = fm.uniao(p_azul, p_verde)
    res_uniao = fm.uniao(res_uniao, p_amarelo)

    # inverto a imagem para salvar com objeto preto e fundo branco
    res_uniao = cv2.bitwise_not(res_uniao)

    # salvo a imagem final
    cv2.imwrite("resultado_uniao.png", res_uniao)

    plt.figure()
    plt.imshow(res_uniao, cmap='gray')
    plt.title('Uniao das 3 partes (azul, verde e amarelo)')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    questao_5a()
    questao_5b()
    questao_5c()
