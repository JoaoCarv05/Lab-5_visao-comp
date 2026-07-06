# Laboratório 5 – Câmera Estéreo

**Visão Computacional 2026.2**

## Descrição

Este repositório contém o relatório e os códigos do Laboratório 5 da disciplina de Visão Computacional, focado em **estereoscopia**, **geometria epipolar** e na construção e calibração de uma **câmera estéreo** de baixo custo com duas webcams USB, culminando na geração de uma **imagem 3D anaglifo** (vermelho/ciano).

## Conteúdo

- `Lab5_Estereo.ipynb` — Relatório completo em formato Jupyter Notebook
- `capture_images_joao.py` — Captura dos pares de imagens do tabuleiro de calibração (10–15 pares)
- `calibrate_joao.py` — Calibração estéreo e geração do arquivo de parâmetros `data/params_joao.xml`
- `movie3d_joao.py` — Apresentação da imagem 3D anaglifo **ao vivo** com as duas webcams
- `movie3d_joao_gravacao.py` — Gravação de um vídeo 3D anaglifo (~10–20 s)
- `data/` — Imagens de calibração (`stereoL/`, `stereoR/`) e arquivo de parâmetros XML
- `imagens/` — Fotos da câmera construída e capturas de tela dos resultados
- `videos/` — Vídeo 3D gravado

> **Nota:** as pastas `data/stereoL`, `data/stereoR`, `imagens/` e `videos/` contêm apenas placeholders (`.gitkeep`). As mídias (imagens de calibração, fotos, capturas de tela e vídeo) são produzidas durante o experimento no laboratório e devem ser adicionadas nos espaços reservados indicados no notebook.

## Requisitos

```bash
pip install opencv-python opencv-contrib-python numpy matplotlib tqdm jupyter
```

Para converter o vídeo gravado para MP4 é necessário o `ffmpeg`.

## Execução

### Relatório (notebook)
```bash
jupyter notebook Lab5_Estereo.ipynb
```

### Fluxo completo do experimento (requer duas webcams USB)
```bash
# 1. Capturar 10-15 pares de imagens do tabuleiro de xadrez (9x6)
python3 capture_images_joao.py

# 2. Calibrar a câmera estéreo (gera data/params_joao.xml)
python3 calibrate_joao.py

# 3. Visualizar a imagem 3D anaglifo ao vivo (requer óculos vermelho/ciano)
python3 movie3d_joao.py

# 4. Gravar um vídeo 3D anaglifo (~10-20 s) e converter para MP4
python3 movie3d_joao_gravacao.py
ffmpeg -i videos/video3d_joao.avi videos/video3d_joao.mp4
```

Ajuste os IDs das webcams (`CamL_id`, `CamR_id`) e as dimensões do tabuleiro (`CHESSBOARD`) no início de cada script conforme o setup do laboratório.

## Nota sobre uso de IA Generativa

Conforme a Portaria CNPq 2664/2026, declara-se o uso da ferramenta de IA Generativa Devin (Cognition AI) no auxílio à estruturação e redação do relatório e dos códigos-base (adaptados dos exemplos do LearnOpenCV). Todo o conteúdo final, experimentos e análises foram revisados e validados pelos autores.
