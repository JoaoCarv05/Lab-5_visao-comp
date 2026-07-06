"""
Gravação de um vídeo 3D anaglifo (vermelho/ciano) com a câmera estéreo construída
com duas webcams USB.

Baseado no exemplo "Making A Low-Cost Stereo Camera Using OpenCV" (LearnOpenCV),
adaptado para o Laboratório 5. Além de exibir a imagem 3D ao vivo, esta versão
grava aproximadamente 10 a 20 segundos de vídeo anaglifo em disco.

O vídeo é gravado em videos/video3d_joao.avi. Para converter para MP4 (conforme
pedido no enunciado), use, por exemplo:

    ffmpeg -i videos/video3d_joao.avi videos/video3d_joao.mp4

Uso:
    python3 movie3d_joao_gravacao.py

Controles:
    ESC — encerrar antes do tempo
"""
import sys
import time

import cv2

# No Windows o backend MSMF costuma falhar ("can't grab frame"); DirectShow
# (CAP_DSHOW) é mais estável com webcams USB.
CAP_BACKEND = cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY


def abrir_camera(cam_id):
    cap = cv2.VideoCapture(cam_id, CAP_BACKEND)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

# =====================================================================
# PARÂMETROS QUE DEVEM SER AJUSTADOS PARA A NOSSA CÂMERA ESTÉREO
# =====================================================================
CamL_id = 0          # webcam da esquerda
CamR_id = 1          # webcam da direita

NOME_EQUIPE = "joao"
PARAMS_FILE = f"data/params_{NOME_EQUIPE}.xml"

# Duração da gravação em segundos (o enunciado pede de 10 a 20 s).
DURACAO_S = 15

# Dimensões e taxa de quadros do vídeo de saída.
OUT_SIZE = (700, 700)
FPS = 20.0
OUTPUT_FILE = f"videos/video3d_{NOME_EQUIPE}.avi"


def main():
    CamL = abrir_camera(CamL_id)
    CamR = abrir_camera(CamR_id)

    if not CamL.isOpened() or not CamR.isOpened():
        print(f"Erro: não foi possível abrir as webcams (IDs {CamL_id} e {CamR_id}).")
        print("Rode 'python3 list_cameras.py' e ajuste CamL_id / CamR_id.")
        return

    print("Lendo parâmetros de calibração ......")
    cv_file = cv2.FileStorage(PARAMS_FILE, cv2.FILE_STORAGE_READ)
    Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
    Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
    Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
    Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
    cv_file.release()

    if Left_Stereo_Map_x is None:
        raise RuntimeError(
            f"Não foi possível ler {PARAMS_FILE}. Execute calibrate_joao.py antes."
        )

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, OUT_SIZE)

    print(f"Gravando {DURACAO_S}s de vídeo 3D em {OUTPUT_FILE}. ESC para parar.")
    start = time.time()

    while True:
        retL, imgL = CamL.read()
        retR, imgR = CamR.read()

        if not (retL and retR):
            print("Erro ao capturar frame das webcams.")
            break

        Left_nice = cv2.remap(imgL, Left_Stereo_Map_x, Left_Stereo_Map_y,
                              cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        Right_nice = cv2.remap(imgR, Right_Stereo_Map_x, Right_Stereo_Map_y,
                               cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

        # Composição anaglifo: canais B e G da direita, canal R da esquerda.
        output = Right_nice.copy()
        output[:, :, 0] = Right_nice[:, :, 0]
        output[:, :, 1] = Right_nice[:, :, 1]
        output[:, :, 2] = Left_nice[:, :, 2]

        output = cv2.resize(output, OUT_SIZE)
        writer.write(output)

        cv2.namedWindow("3D movie (gravando)", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("3D movie (gravando)", OUT_SIZE[0], OUT_SIZE[1])
        cv2.imshow("3D movie (gravando)", output)

        if (time.time() - start) >= DURACAO_S:
            print("Tempo de gravação atingido.")
            break
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    writer.release()
    CamL.release()
    CamR.release()
    cv2.destroyAllWindows()
    print(f"Vídeo salvo em {OUTPUT_FILE}.")
    print("Converta para MP4 com: "
          f"ffmpeg -i {OUTPUT_FILE} videos/video3d_{NOME_EQUIPE}.mp4")


if __name__ == '__main__':
    main()
