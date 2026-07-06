# Passo a passo — Lab 5 (Câmera Estéreo) depois de montar a caixa

> **Resumo rápido:** o Jupyter **sozinho não roda tudo**. A captura das imagens, a
> visualização 3D ao vivo e a gravação do vídeo **precisam dos scripts `.py`**
> (eles abrem as webcams e janelas — coisa que o notebook não faz bem). A
> calibração pode rodar tanto pelo script quanto pela célula do notebook. O
> notebook é onde você **junta tudo** (texto + imagens + vídeo) para entregar.

Ordem recomendada: **0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8**.

---

## 0. Ajustar os parâmetros nos scripts (uma vez)

Abra os 4 scripts e confira o cabeçalho de cada um. Os valores a checar são os mesmos:

| Variável | Onde | O que é | O que fazer |
|---|---|---|---|
| `CamL_id`, `CamR_id` | todos os scripts | ID das webcams (esquerda/direita) | testar (ver passo 1). Normalmente 0, 1 ou 2 |
| `CHESSBOARD` | `capture_images_joao.py`, `calibrate_joao.py` | cantos **internos** do tabuleiro `(colunas, linhas)` | ajustar ao tabuleiro usado (o exemplo usa `(9, 6)`) |
| `NUM_IMAGENS` | `calibrate_joao.py` | quantos pares capturou | igualar ao nº de pares (10–15) |
| `NOME_EQUIPE` | `capture/calibrate/movie3d...` | sufixo/nome do arquivo | trocar `"joao"` pelo nome do integrante, se quiser |

> ⚠️ Se você trocar `NOME_EQUIPE`, o arquivo de parâmetros muda de
> `data/params_joao.xml` para `data/params_<nome>.xml` — e aí atualize também o
> nome nos scripts `movie3d_*` e na célula da Seção 3.3 do notebook.

---

## 0.1 Descobrir os IDs das webcams (recomendado)

```bash
python3 list_cameras.py
```
Ele testa os índices 0..5 e diz quais funcionam, sugerindo valores para
`CamL_id`/`CamR_id`. Ajuste esses valores no topo dos scripts.

---

## 1. Descobrir qual webcam é a esquerda e qual é a direita

```bash
python3 capture_images_joao.py
```
Ele mostra as duas janelas (`imgL` e `imgR`). Se a esquerda/direita estiverem
trocadas, pressione **n** (inverte os IDs); se estiverem corretas, pressione **y**.
Anote os IDs corretos e, se necessário, ajuste `CamL_id`/`CamR_id` nos outros scripts.

---

## 2. Capturar as imagens de calibração (tabuleiro) — 10 a 15 pares

Ainda dentro do `capture_images_joao.py` (mesmo comando do passo 1):

- Segure o **tabuleiro de xadrez** na frente das duas câmeras, variando posição e ângulo.
- Ele salva um par automaticamente **só quando detecta o tabuleiro nas duas câmeras**.
- Os arquivos são gravados como:
  - `data/stereoL/img1.png`, `img2.png`, … (esquerda)
  - `data/stereoR/img1.png`, `img2.png`, … (direita)
- Pare com **ESC** quando tiver de 10 a 15 pares.

> **Não precisa renomear nada** — os arquivos já saem como `img1..imgN.png`,
> que é exatamente o que o `calibrate_joao.py` espera. Só garanta que a numeração
> seja contínua (img1, img2, … sem buracos) e que a pasta L e R tenham o mesmo nº.

**(Opcional) Um par de teste para o anaglifo estático do notebook:** salve um par
qualquer (uma cena com objetos a distâncias diferentes) como
`imagens/teste_L.png` e `imagens/teste_R.png` — a Seção 3.4 do notebook gera o
anaglifo a partir deles.

---

## 3. Calibrar a câmera estéreo

```bash
python3 calibrate_joao.py
```
- Mostra os cantos detectados em cada par (pressione uma tecla para avançar).
- No fim, **imprime no terminal** as matrizes/vetores: `K_L`, `K_R`, distorções,
  `R`, `t`, `E`, `F`, `Q`. **Copie essa saída** — você vai colar na Seção 4.3 do notebook.
- Salva os mapas de retificação em **`data/params_joao.xml`**.

---

## 4. Ver a imagem 3D ao vivo (anaglifo)

```bash
python3 movie3d_joao.py
```
- Coloque o **óculos anaglifo** (lente vermelha no olho esquerdo, ciano no direito).
- Tire um **print da janela "3D movie"** e salve como `imagens/anaglifo_aovivo.png`.
- **ESC** para sair.

---

## 5. Gravar o vídeo 3D (10–20 s) e converter para MP4

```bash
python3 movie3d_joao_gravacao.py
ffmpeg -i videos/video3d_joao.avi videos/video3d_joao.mp4
```
- Grava ~15 s em `videos/video3d_joao.avi` e converte para `videos/video3d_joao.mp4`.
- (Ajuste `DURACAO_S` no script se quiser outra duração.)

---

## 6. Tirar uma foto da câmera (a caixa montada)

Fotografe a sua câmera estéreo (caixa + 2 webcams) e salve como
`imagens/camera_estereo.jpg`.

---

## 7. Arquivos que devem existir no fim (checklist de mídia)

```
data/stereoL/img1.png ... imgN.png      (10–15 pares)
data/stereoR/img1.png ... imgN.png
data/params_joao.xml                     (gerado pela calibração)
imagens/camera_estereo.jpg               (foto da caixa)
imagens/anaglifo_aovivo.png              (print do 3D ao vivo)
imagens/teste_L.png / teste_R.png        (opcional, par de teste)
videos/video3d_joao.mp4                  (vídeo 3D convertido)
```

---

## 8. Preencher o notebook e rodar tudo

No `Lab5_Estereo.ipynb`, preencha os campos marcados como `[preencher]` /
`[ESPAÇO RESERVADO ...]`:

- **Capa:** datas de realização e de publicação.
- **Seção 3.1:** distância inter-pupilar medida (baseline) e nome da câmera.
- **Seção 3.3:** `NUM_IMAGENS` = nº de pares capturados; a tabela de valores
  modificados (IDs das câmeras, dimensões do tabuleiro).
- **Seção 4.3:** cole os valores numéricos das matrizes impressas no passo 3.
- **Seção 4.4:** a percepção 3D de **cada integrante** (ao vivo × gravado).

Depois rode o notebook do início ao fim:
```bash
jupyter notebook Lab5_Estereo.ipynb    # Cell > Run All
```
As células com `os.path.exists(...)` vão **exibir automaticamente** as imagens,
o anaglifo e o vídeo assim que os arquivos estiverem nas pastas.

---

## 9. Subir para o GitHub

```bash
git add -A
git commit -m "feat: mídias e dados do experimento Lab 5 (câmera estéreo)"
git push
```
Isso atualiza o PR #1 automaticamente.

> **Sobre apagar os arquivos no laboratório:** o enunciado pede para apagar do
> **computador do laboratório** os arquivos baixados do exemplo. Isso **não**
> afeta o seu repositório — depois do `git push`, tudo fica salvo no GitHub.

---

## Solução de problemas — webcams no Windows

Se aparecer algo como:

```
CvCapture_MSMF::grabFrame videoio(MSMF): can't grab frame. Error: -2147483638
```

isso é o backend padrão do OpenCV no Windows (MSMF) falhando ao capturar. As
causas mais comuns e as correções (já aplicadas nos scripts):

1. **Backend MSMF instável** → os scripts agora abrem a câmera com
   `cv2.VideoCapture(id, cv2.CAP_DSHOW)` (DirectShow) automaticamente no Windows.
2. **ID de câmera errado** → o padrão foi mudado para `CamL_id = 0`, `CamR_id = 1`
   (o valor antigo `2` normalmente não existe). Rode `python3 list_cameras.py`
   para confirmar os IDs válidos.
3. **Câmera em uso por outro app** → feche Teams/Zoom/Câmera do Windows/OBS etc.
4. **Permissão de câmera** → Windows: *Configurações → Privacidade → Câmera* →
   permitir apps de desktop acessarem a câmera.

### Câmeras abrem mas a imagem fica PRETA

As webcams abrem/capturam, mas a janela mostra tela preta. A configuração de
abertura fica em **`stereo_utils.py`**:

- **Formato MJPG forçado** era a causa mais comum: em alguns drivers DirectShow,
  forçar MJPG devolve tela preta. Por isso `USE_MJPG = False` por padrão (usa o
  formato nativo da câmera, que é o modo que funciona no teste com uma câmera só).
- **Frames de aquecimento**: `WARMUP_FRAMES = 15` descarta os primeiros frames
  (que costumam vir pretos enquanto a câmera ajusta exposição).
- Rode `python3 list_cameras.py` — ele mostra o **brilho médio** de cada câmera,
  então dá para ver qual está preta (brilho ~0).
- **Banda USB** (duas webcams no mesmo controlador podem não transmitir juntas):
  ligue cada webcam em **portas USB de controladores diferentes** (evite hubs).
  Se precisar reduzir a banda, em `stereo_utils.py` defina `USE_MJPG = True` e/ou
  `FRAME_W = 640`, `FRAME_H = 480`.
