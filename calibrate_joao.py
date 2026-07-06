"""
Calibração da câmera estéreo construída com duas webcams USB.

Baseado no exemplo "Making A Low-Cost Stereo Camera Using OpenCV" (LearnOpenCV),
adaptado para os experimentos do Laboratório 5.

O programa:
  1. Lê os pares de imagens do tabuleiro capturados por capture_images_joao.py;
  2. Detecta e refina os cantos do tabuleiro;
  3. Calibra cada câmera individualmente (intrínsecos e distorção);
  4. Executa a calibração estéreo (rotação, translação, matriz essencial e
     fundamental entre as duas câmeras);
  5. Retifica o par estéreo e gera os mapas de remapeamento;
  6. Salva os parâmetros no arquivo XML data/params_joao.xml.

Uso:
    python3 calibrate_joao.py
"""
import numpy as np
import cv2

try:
    from tqdm import tqdm
except ImportError:  # tqdm é opcional; usa identidade se não estiver instalado
    def tqdm(x):
        return x

# =====================================================================
# PARÂMETROS QUE DEVEM SER AJUSTADOS PARA A NOSSA CÂMERA ESTÉREO
# =====================================================================
pathL = "./data/stereoL/"
pathR = "./data/stereoR/"

# Dimensões INTERNAS do tabuleiro (colunas, linhas) — igual ao script de captura.
CHESSBOARD = (9, 6)

# Quantidade de pares de imagens capturados (ajuste conforme o experimento).
NUM_IMAGENS = 15

# Nome de um integrante da equipe — usado no arquivo de parâmetros gravado.
NOME_EQUIPE = "joao"
PARAMS_FILE = f"data/params_{NOME_EQUIPE}.xml"

print("Extraindo as coordenadas dos cantos do padrão 3D ....\n")

# Critério de parada para o refinamento dos cantos detectados.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Pontos 3D do tabuleiro no referencial do próprio padrão (Z = 0).
objp = np.zeros((CHESSBOARD[0] * CHESSBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)

img_ptsL = []
img_ptsR = []
obj_pts = []

imgL_gray = None
imgR_gray = None

for i in tqdm(range(1, NUM_IMAGENS + 1)):
    imgL = cv2.imread(pathL + "img%d.png" % i)
    imgR = cv2.imread(pathR + "img%d.png" % i)
    if imgL is None or imgR is None:
        continue

    imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    outputL = imgL.copy()
    outputR = imgR.copy()

    retR, cornersR = cv2.findChessboardCorners(outputR, CHESSBOARD, None)
    retL, cornersL = cv2.findChessboardCorners(outputL, CHESSBOARD, None)

    if retR and retL:
        obj_pts.append(objp)
        cv2.cornerSubPix(imgR_gray, cornersR, (11, 11), (-1, -1), criteria)
        cv2.cornerSubPix(imgL_gray, cornersL, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(outputR, CHESSBOARD, cornersR, retR)
        cv2.drawChessboardCorners(outputL, CHESSBOARD, cornersL, retL)
        cv2.imshow('cornersR', outputR)
        cv2.imshow('cornersL', outputL)
        cv2.waitKey(0)

        img_ptsL.append(cornersL)
        img_ptsR.append(cornersR)

cv2.destroyAllWindows()

if len(obj_pts) == 0 or imgL_gray is None:
    raise RuntimeError(
        "Nenhum par válido de tabuleiro foi encontrado. Verifique as imagens em "
        f"{pathL} e {pathR} e as dimensões CHESSBOARD={CHESSBOARD}."
    )

print("Calculando os parâmetros da câmera esquerda ... ")
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(
    obj_pts, img_ptsL, imgL_gray.shape[::-1], None, None)
hL, wL = imgL_gray.shape[:2]
new_mtxL, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distL, (wL, hL), 1, (wL, hL))

print("Calculando os parâmetros da câmera direita ... ")
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(
    obj_pts, img_ptsR, imgR_gray.shape[::-1], None, None)
hR, wR = imgR_gray.shape[:2]
new_mtxR, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distR, (wR, hR), 1, (wR, hR))

print("Calibração estéreo .....")
# Fixamos os intrínsecos para que apenas Rot, Trns, Emat e Fmat sejam calculados.
flags = cv2.CALIB_FIX_INTRINSIC
criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(
    obj_pts, img_ptsL, img_ptsR,
    new_mtxL, distL, new_mtxR, distR,
    imgL_gray.shape[::-1], criteria_stereo, flags)

# Retificação estéreo.
rectify_scale = 1  # 0 => imagem cortada, 1 => imagem não cortada
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR = cv2.stereoRectify(
    new_mtxL, distL, new_mtxR, distR,
    imgL_gray.shape[::-1], Rot, Trns,
    rectify_scale, (0, 0))

# Mapas de remapeamento (undistort + rectify) para as câmeras esquerda e direita.
Left_Stereo_Map = cv2.initUndistortRectifyMap(
    new_mtxL, distL, rect_l, proj_mat_l, imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map = cv2.initUndistortRectifyMap(
    new_mtxR, distR, rect_r, proj_mat_r, imgR_gray.shape[::-1], cv2.CV_16SC2)

# Exibe no terminal as matrizes e vetores obtidos (para o relatório).
np.set_printoptions(precision=4, suppress=True)
print("\n===== PARÂMETROS OBTIDOS =====")
print("Matriz intrínseca esquerda (mtxL):\n", new_mtxL)
print("Distorção esquerda (distL):\n", distL.ravel())
print("Matriz intrínseca direita (mtxR):\n", new_mtxR)
print("Distorção direita (distR):\n", distR.ravel())
print("Rotação entre câmeras (Rot):\n", Rot)
print("Translação entre câmeras (Trns):\n", Trns.ravel())
print("Matriz essencial (Emat):\n", Emat)
print("Matriz fundamental (Fmat):\n", Fmat)
print("Matriz de reprojeção (Q):\n", Q)

print(f"\nSalvando parâmetros em {PARAMS_FILE} ......")
cv_file = cv2.FileStorage(PARAMS_FILE, cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x", Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y", Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x", Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y", Right_Stereo_Map[1])
cv_file.release()
print("Concluído.")
