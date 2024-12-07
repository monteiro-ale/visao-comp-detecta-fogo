import cv2
import numpy as np

# Inicialize variáveis globais
prev_frame = None  # Para armazenar o quadro anterior

def processa_frame(img):
    """
    Processa o quadro e retorna a máscara de movimento para a cor branca.
    """
    global prev_frame

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Cria uma máscara onde a cor branca (255) é isolada
    _, white_mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)  # Detecta áreas brancas

    # Se tivermos um quadro anterior, calcule a diferença entre eles
    if prev_frame is not None:
        frame_diff = cv2.absdiff(white_mask, prev_frame)
        _, motion_mask = cv2.threshold(frame_diff, 45, 255, cv2.THRESH_BINARY)
    else:
        motion_mask = np.zeros_like(white_mask)  # Inicializa com zero se for o primeiro quadro

    # Atualiza o quadro anterior
    prev_frame = white_mask.copy()

    return motion_mask, white_mask

def analisa_movimento(img, motion_mask):
    """
    Analisa o movimento da cor branca baseado na máscara de movimento.
    """
    # Encontra os contornos das áreas de movimento
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    qt_movimento = 0
    for contour in contours:
        # Ignora pequenos contornos (áreas pequenas)
        if cv2.contourArea(contour) > 500:  # Ajuste o limite conforme necessário
            qt_movimento += 1

            # Desenha o contorno da área de movimento na imagem
            cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)

    return qt_movimento

def exibe_status(img, qt_movimento):
    """
    Exibe o status da detecção de movimento.
    """
    cv2.rectangle(img, (90, 0), (415, 60), (0, 0, 0), -1)
    cv2.putText(img, 'FIRE!: {}'.format(qt_movimento), (180, 45), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 5)

def main():
    video_path = 'C:/Users/usuario/Desktop/Inteligencia Artificial/visao-comp-detecta-fogo/fire-detection/videoplayback2.mp4'
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    paused = False  # Variável para controlar o estado de pausa

    while True:
        if not paused:
            check, img = video.read()
            if not check:
                break

            # Processa o frame para detectar o movimento da cor branca
            motion_mask, white_mask = processa_frame(img)

            # Analisa o movimento
            qt_movimento = analisa_movimento(img, motion_mask)

            # Exibe o status do movimento detectado
            exibe_status(img, qt_movimento)

            # Exibe o vídeo original
            cv2.imshow('Video', img)
            
            # Exibe a máscara de movimento
            cv2.namedWindow('Passo', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Passo', 180, 320)
            cv2.imshow('Passo', motion_mask)

            # Exibe a área branca isolada
            cv2.namedWindow('Area Branca', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Area Branca', 178, 292)
            cv2.imshow('Area Branca', white_mask)

        # Captura a tecla pressionada
        key = cv2.waitKey(90)

        if key == ord('q'):  # Pressione 'q' para sair
            break
        elif key == ord('p'):  # Pressione 'p' para pausar/despausar
            paused = not paused

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
