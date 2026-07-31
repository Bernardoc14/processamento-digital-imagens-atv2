# Atividade Prática 02 — Processamento Digital de Imagens

Universidade Federal do Piauí (UFPI) — Departamento de Computação
Docente: Kelson Romulo Teixeira Aires · Discente: Bernardo de Carvalho Cavalcante

> ⚠️ **Sobre esta reconstrução:** o código-fonte original deste trabalho foi
> perdido; este projeto foi **reconstruído a partir dos prints de código e das
> explicações presentes no relatório em PDF** entregue na disciplina. A lógica,
> os nomes de funções, as máscaras e os parâmetros seguem fielmente o que está
> documentado no relatório. Pequenos ajustes de organização (separação em
> módulos/arquivos) foram feitos para facilitar a leitura, mas os algoritmos são
> os mesmos.

## Bibliotecas utilizadas

- `numpy`
- `opencv-python` (cv2)
- `matplotlib`

Instale com:
```bash
pip install -r requirements.txt
```

## Estrutura do projeto

```
.
├── filtros.py                          # convolução, laplaciano, gaussiana, prewitt, sobel, mediana
├── funcoes_morfologicas.py             # (fm) união, interseção, diferença
├── morfologia.py                       # (mf) dilatação, erosão, abertura, fechamento
├── gerar_lena_ruido.py                 # utilitário: gera lena_ruido.bmp a partir de lena_gray.bmp
├── binarizar_imagem.py                 # utilitário: binariza imagens obtidas por print/screenshot
├── questao1_laplaciano_unsharp_bordas.py
├── questao2_filtro_mediana.py
├── questao3_operacoes_logicas.py
├── questao4_operacoes_morfologicas.py
├── questao5_a_b_c_quadro.py
├── questao5_d_fecho_convexo.py
├── questao5_e_esqueleto.py
├── questao5_f_hit_or_miss.py
├── imagens_entrada/                    # <- coloque aqui as imagens de entrada
└── requirements.txt
```

## Imagens necessárias (não incluídas)

As imagens usadas no relatório original não estão neste repositório. Duas
categorias:

**Essenciais** (o exercício foi desenhado em cima delas — sem elas a
comparação com o relatório não faz sentido):

| Questão | Arquivo esperado | Descrição |
|---|---|---|
| 1 e 2 | `lena_gray.bmp` | Imagem clássica de teste, em tons de cinza |
| 2 | `lena_ruido.bmp` | Mesma imagem com ruído adicionado (**gerada com `gerar_lena_ruido.py`**, veja abaixo) |
| 5 | `quadro.png` | Imagem colorida com objetos vermelhos (com buraco), e formas azul/verde/amarela (com buracos pretos), sobre fundo com ruído de pontos pretos |

**Livres** (qualquer imagem binária — objeto branco em fundo preto — serve
pra testar a lógica; não precisa ser igual à do relatório original):

| Questão | Arquivo esperado | Descrição |
|---|---|---|
| 3 | `imagem1.png`, `imagem2.png` | Duas formas brancas em fundo preto, mesmo tamanho |
| 4 | `carro.png` | Qualquer desenho binário (objeto branco em fundo preto) |
| 5f | `D_vermelho{1,2,3}.png`, `W_vermelho{1,2,3}.png` | Máscaras D e W feitas manualmente a partir dos objetos vermelhos do seu `quadro.png` |

### Passo a passo para preencher `imagens_entrada/`

1. **`lena_gray.bmp`** → já baixada, é só colocar em `imagens_entrada/`.
2. **`lena_ruido.bmp`** → não precisa printar nada. Depois do passo 1, rode:
   ```bash
   python gerar_lena_ruido.py
   ```
   Isso lê `imagens_entrada/lena_gray.bmp` e gera `imagens_entrada/lena_ruido.bmp`
   automaticamente com ruído gaussiano.
3. **`quadro.png`** (Questão 5) → print da imagem colorida (objetos vermelhos,
   azul, verde, amarelo) do relatório, salve em `imagens_entrada/`.
4. **`imagem1.png` e `imagem2.png`** (Questão 3) → duas formas quaisquer,
   pode desenhar no Paint/GIMP ou usar as do relatório (opcional).
5. **`carro.png`** (Questão 4) → qualquer desenho binário 80x80 (ou outro
   tamanho — o código não depende de dimensão fixa).
6. **`D_vermelho1.png`, `W_vermelho1.png`, `D_vermelho2.png`, ...**
   (Questão 5f) → recorte/desenhe as máscaras D e W a partir dos objetos
   vermelhos do seu `quadro.png`, salve em `imagens_entrada/`.
7. **Binarize as imagens dos passos 4 a 6** (são todas preto/branco puro; um
   print introduz tons de cinza intermediários nas bordas que quebram a
   lógica das funções). Rode, para cada uma:
   ```bash
   python binarizar_imagem.py imagens_entrada/imagem1.png
   python binarizar_imagem.py imagens_entrada/imagem2.png
   python binarizar_imagem.py imagens_entrada/carro.png
   python binarizar_imagem.py imagens_entrada/D_vermelho1.png
   python binarizar_imagem.py imagens_entrada/W_vermelho1.png
   # ... repita para os demais D_vermelho{2,3} e W_vermelho{2,3}
   ```
   > `quadro.png` **não** deve ser binarizada — ela é colorida e precisa
   > continuar assim (o próprio script `questao5_a_b_c_quadro.py` já faz a
   > conversão para escala de cinza/binário internamente quando precisa).

Depois disso, é só seguir a seção "Como rodar" abaixo.

## Como rodar

Cada questão é um script independente (rode a partir da raiz do projeto):

```bash
python questao1_laplaciano_unsharp_bordas.py
python questao2_filtro_mediana.py
python questao3_operacoes_logicas.py
python questao4_operacoes_morfologicas.py
python questao5_a_b_c_quadro.py   # gera quadro_erosao.png, resultado_uniao.png, p_azul/verde/amarelo.png
python questao5_d_fecho_convexo.py
python questao5_e_esqueleto.py
python questao5_f_hit_or_miss.py   # depende dos arquivos gerados pela 5a-c
```

## Resumo do que cada questão faz

1. **Laplaciano, Unsharp Masking, Highboost e detecção de bordas** (Prewitt e
   Sobel) sobre `lena_gray.bmp`, com convolução implementada manualmente.
2. **Filtro da mediana** comparado a 4 máscaras de suavização diferentes, sobre
   `lena_ruido.bmp`.
3. **Operações lógicas** (união, interseção, diferença) entre duas imagens
   binárias.
4. **Operações morfológicas** (dilatação, erosão, abertura, fechamento) com
   elemento estruturante e centro configuráveis.
5. A partir de `quadro.png`:
   - (a) preenche os buracos dos objetos pretos via fechamento morfológico;
   - (b) remove todos os objetos pretos da imagem;
   - (c) separa e preenche os buracos dos objetos azul, verde e amarelo;
   - (d) calcula o fecho convexo de cada um desses objetos (algoritmo do
     livro *Processamento Digital de Imagens*, Gonzalez & Woods);
   - (e) calcula o esqueleto morfológico de cada objeto;
   - (f) localiza cada objeto vermelho na imagem usando a transformada
     hit-or-miss.
