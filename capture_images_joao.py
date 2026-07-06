"""
Captura das imagens do padrão de calibração (tabuleiro de xadrez) com a câmera
estéreo construída com duas webcams USB.

Baseado no exemplo "Making A Low-Cost Stereo Camera Using OpenCV" (LearnOpenCV),
adaptado para os experimentos do Laboratório 5.

Uso:
    python3 capture_images_joao.py

Controles:
    y / n  — confirmar ou inverter os IDs das câmeras (esquerda / direita)
    ESC    — encerrar a captura

O programa salva pares sincronizados de imagens (esquerda e direita) somente
quando o tabuleiro é detectado simultaneamente nas duas câmeras. As imagens são
gravadas em data/stereoL/ e data/stereoR/. Obtenha entre 10 e 15 pares.
"""
import time

import cv2

# =====================================================================
# PARÂMETROS QUE DEVEM SER AJUSTADOS PARA A NOSSA CÂMERA ESTÉREO
# =====================================================================
# IDs das webcams USB do laboratório (podem variar de máquina para máquina).
CamL_id = 0          # webcam da esquerda
CamR_id = 2          # webcam da direita

# Dimensões INTERNAS do tabuleiro de xadrez (cantos internos): (colunas, linhas)
CHESSBOARD = (9, 6)

# Número máximo de pares de imagens a capturar (o enunciado pede de 10 a 15).
MAX_PAIRS = 15

# Intervalo (em segundos) entre capturas automáticas.
T = 5

# Prefixo dos arquivos salvos — use o nome de um integrante da equipe.
NOME_EQUIPE = "joao"

output_path = "./data/"


def main():
    print("Verificando os IDs das câmeras esquerda e direita:")
    print("Pressione (y) se os IDs estiverem corretos e (n) para invertê-los")
    print("Pressione ENTER para iniciar >> ")
    input()

    camL_id, camR_id = CamL_id, CamR_id
    CamL = cv2.VideoCapture(camL_id)
    CamR = cv2.VideoCapture(camR_id)

    # Estabiliza a exposição das câmeras descartando os primeiros frames.
    for _ in range(30):
        CamL.read()
        CamR.read()

    retL, frameL = CamL.read()
    retR, frameR = CamR.read()
    if retL and retR:
        cv2.imshow('imgL', frameL)
        cv2.imshow('imgR', frameR)

    key = cv2.waitKey(0) & 0xFF
    if key in (ord('n'), ord('N')):
        camL_id, camR_id = CamR_id, CamL_id
        print("IDs das câmeras invertidos")
    else:
        print("IDs das câmeras mantidos")

    CamR.release()
    CamL.release()

    CamL = cv2.VideoCapture(camL_id)
    CamR = cv2.VideoCapture(camR_id)

    start = time.time()
    count = 0

    print("Capturando pares de imagens do tabuleiro. Pressione ESC para sair.")

    while True:
        timer = T - int(time.time() - start)
        retR, frameR = CamR.read()
        retL, frameL = CamL.read()

        if not (retR and retL):
            print("Erro ao capturar frame das webcams.")
            break

        img_temp = frameL.copy()
        cv2.putText(img_temp, "%r" % timer, (50, 50), 1, 5, (55, 0, 0), 5)
        cv2.imshow('imgR', frameR)
        cv2.imshow('imgL', img_temp)

        grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
        grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

        # Procura os cantos do tabuleiro nas duas imagens.
        foundR, _ = cv2.findChessboardCorners(grayR, CHESSBOARD, None)
        foundL, _ = cv2.findChessboardCorners(grayL, CHESSBOARD, None)

        # Salva o par apenas quando o tabuleiro é visto nas duas câmeras.
        if foundR and foundL and timer <= 0:
            count += 1
            cv2.imwrite(output_path + 'stereoR/img%d.png' % count, frameR)
            cv2.imwrite(output_path + 'stereoL/img%d.png' % count, frameL)
            print(f"Par {count} salvo ({NOME_EQUIPE}).")

        if timer <= 0:
            start = time.time()

        if count >= MAX_PAIRS:
            print(f"{MAX_PAIRS} pares capturados. Encerrando.")
            break

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            print("Encerrando a captura!")
            break

    CamR.release()
    CamL.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
