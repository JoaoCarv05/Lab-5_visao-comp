"""
Diagnóstico das webcams disponíveis.

Testa os índices de câmera de 0 a MAX_ID e informa, para cada um, se abre, se
captura frame e o **brilho médio** do frame (para detectar imagem preta). Usa o
mesmo backend/configuração dos demais scripts (ver stereo_utils.py).

Use este script para:
  - descobrir os IDs corretos das webcams (CamL_id / CamR_id);
  - identificar se alguma câmera está retornando imagem PRETA (brilho ~0).

Uso:
    python3 list_cameras.py
"""
import cv2

from stereo_utils import CAP_BACKEND, abrir_camera

MAX_ID = 5


def main():
    backend_nome = "CAP_DSHOW (Windows)" if CAP_BACKEND == cv2.CAP_DSHOW else "CAP_ANY"
    print(f"Backend em uso: {backend_nome}")
    print(f"Testando índices de câmera de 0 a {MAX_ID}...\n")

    utilizaveis = []
    for cam_id in range(MAX_ID + 1):
        cap = abrir_camera(cam_id)
        if not cap.isOpened():
            print(f"  [ID {cam_id}] indisponível")
            cap.release()
            continue

        ok, frame = cap.read()
        if ok and frame is not None:
            h, w = frame.shape[:2]
            brilho = float(frame.mean())
            if brilho < 5.0:
                print(f"  [ID {cam_id}] abriu e captura, mas frame PRETO "
                      f"(brilho médio={brilho:.1f}) — {w}x{h}")
            else:
                print(f"  [ID {cam_id}] OK — frame {w}x{h}, brilho médio={brilho:.1f}")
                utilizaveis.append(cam_id)
        else:
            print(f"  [ID {cam_id}] abriu, mas NÃO capturou frame")
        cap.release()

    print()
    if len(utilizaveis) >= 2:
        print(f"Câmeras com imagem válida: {utilizaveis}")
        print(f"Sugestão: CamL_id = {utilizaveis[0]}, CamR_id = {utilizaveis[1]}")
    elif len(utilizaveis) == 1:
        print(f"Apenas 1 câmera com imagem válida (ID {utilizaveis[0]}).")
        print("Se a outra abriu mas ficou preta, veja as dicas em PASSO_A_PASSO.md")
        print("(porta USB, formato MJPG, app usando a câmera).")
    else:
        print("Nenhuma câmera retornou imagem válida. Se abriram mas ficaram pretas,")
        print("tente ligar as webcams em portas USB de controladores diferentes e")
        print("feche apps que usem a câmera. Veja PASSO_A_PASSO.md.")


if __name__ == '__main__':
    main()
