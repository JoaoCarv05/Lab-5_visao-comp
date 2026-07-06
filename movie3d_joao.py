"""
Exibição ao vivo da imagem 3D anaglifo (vermelho/ciano) da câmera estéreo
construída com duas webcams USB.

Baseado no exemplo "Making A Low-Cost Stereo Camera Using OpenCV" (LearnOpenCV),
adaptado para os experimentos do Laboratório 5. Diferentemente do exemplo
original (que lê arquivos de vídeo .mp4), esta versão lê as duas webcams ao vivo.

Requer óculos 3D anaglifo com lente vermelha (olho esquerdo) e ciano (olho
direito).

Uso:
    python3 movie3d_joao.py

Controles:
    ESC — encerrar
"""
import cv2

from stereo_utils import abrir_camera

# =====================================================================
# PARÂMETROS QUE DEVEM SER AJUSTADOS PARA A NOSSA CÂMERA ESTÉREO
# =====================================================================
CamL_id = 0          # webcam da esquerda
CamR_id = 1          # webcam da direita

NOME_EQUIPE = "joao"
PARAMS_FILE = f"data/params_{NOME_EQUIPE}.xml"


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

    print("Pressione ESC para encerrar.")

    while True:
        retL, imgL = CamL.read()
        retR, imgR = CamR.read()

        if not (retL and retR):
            print("Erro ao capturar frame das webcams.")
            break

        # Retifica e corrige a distorção de cada câmera.
        Left_nice = cv2.remap(imgL, Left_Stereo_Map_x, Left_Stereo_Map_y,
                              cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        Right_nice = cv2.remap(imgR, Right_Stereo_Map_x, Right_Stereo_Map_y,
                               cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

        # Composição anaglifo: canais B e G da direita, canal R da esquerda.
        output = Right_nice.copy()
        output[:, :, 0] = Right_nice[:, :, 0]
        output[:, :, 1] = Right_nice[:, :, 1]
        output[:, :, 2] = Left_nice[:, :, 2]

        output = cv2.resize(output, (700, 700))
        cv2.namedWindow("3D movie", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("3D movie", 700, 700)
        cv2.imshow("3D movie", output)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    CamL.release()
    CamR.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
