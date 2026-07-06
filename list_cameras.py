"""
Diagnóstico das webcams disponíveis.

Testa os índices de câmera de 0 a MAX_ID e informa quais conseguem abrir e
capturar um frame, usando o backend adequado ao sistema operacional. Use este
script para descobrir os IDs corretos e preenchê-los em CamL_id / CamR_id dos
demais scripts.

Uso:
    python3 list_cameras.py
"""
import sys

import cv2

MAX_ID = 5

# No Windows o backend MSMF costuma falhar ("can't grab frame"); DirectShow
# (CAP_DSHOW) é mais estável com webcams USB.
CAP_BACKEND = cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY


def main():
    print(f"Backend em uso: {'CAP_DSHOW (Windows)' if CAP_BACKEND == cv2.CAP_DSHOW else 'CAP_ANY'}")
    print(f"Testando índices de câmera de 0 a {MAX_ID}...\n")

    disponiveis = []
    for cam_id in range(MAX_ID + 1):
        cap = cv2.VideoCapture(cam_id, CAP_BACKEND)
        if cap.isOpened():
            ok, frame = cap.read()
            if ok and frame is not None:
                h, w = frame.shape[:2]
                print(f"  [ID {cam_id}] OK — frame {w}x{h}")
                disponiveis.append(cam_id)
            else:
                print(f"  [ID {cam_id}] abriu, mas NÃO capturou frame")
        else:
            print(f"  [ID {cam_id}] indisponível")
        cap.release()

    print()
    if len(disponiveis) >= 2:
        print(f"Câmeras utilizáveis: {disponiveis}")
        print(f"Sugestão: CamL_id = {disponiveis[0]}, CamR_id = {disponiveis[1]}")
    elif len(disponiveis) == 1:
        print(f"Apenas 1 câmera detectada (ID {disponiveis[0]}). Verifique se a "
              "segunda webcam está conectada e não está em uso por outro app.")
    else:
        print("Nenhuma câmera capturou frame. Verifique conexões USB, permissões "
              "de câmera do sistema e se nenhum outro programa está usando as webcams.")


if __name__ == '__main__':
    main()
