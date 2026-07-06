"""
Utilitários compartilhados para abrir as webcams da câmera estéreo.

Centraliza a escolha do backend do OpenCV e as configurações de captura, para
que todos os scripts (captura, calibração ao vivo e gravação) abram as câmeras
da mesma forma.

Ajuste as constantes abaixo se necessário:

- CAP_BACKEND: no Windows usamos DirectShow (CAP_DSHOW), que é mais estável que
  o MSMF padrão (evita o erro "can't grab frame"). Em Linux/Mac usamos CAP_ANY.
- USE_MJPG: força o formato MJPG. Deixe False por padrão — forçar MJPG em algumas
  webcams faz o driver DirectShow devolver imagem PRETA. Ligue (True) apenas se
  precisar reduzir a banda USB (duas webcams no mesmo controlador).
- FRAME_W / FRAME_H: resolução desejada. Deixe None para usar o padrão da câmera
  (foi o modo que funcionou no teste com uma câmera só). Defina, por exemplo,
  640 x 480 se quiser reduzir a banda USB.
- WARMUP_FRAMES: frames descartados no início para a câmera estabilizar
  exposição/foco (evita os primeiros frames pretos).
"""
import sys

import cv2

CAP_BACKEND = cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY

USE_MJPG = False
FRAME_W = None
FRAME_H = None
WARMUP_FRAMES = 15


def abrir_camera(cam_id):
    """Abre uma webcam com o backend/configuração adequados e a 'aquece'."""
    cap = cv2.VideoCapture(cam_id, CAP_BACKEND)
    if not cap.isOpened():
        return cap

    if USE_MJPG:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    if FRAME_W:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    if FRAME_H:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    # Descarta os primeiros frames (podem vir pretos enquanto a câmera estabiliza).
    for _ in range(WARMUP_FRAMES):
        cap.read()
    return cap
