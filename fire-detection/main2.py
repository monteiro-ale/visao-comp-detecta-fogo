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
    Analisa o movimento da cor branca baseado na máscara de movimento e desenha
    um único retângulo envolvendo todas as áreas de movimento.
    """
    # Encontra os contornos das áreas de movimento
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    qt_movimento = 0
    
    # Inicializa as variáveis para calcular a caixa delimitadora total
    x_min, y_min, x_max, y_max = float('inf'), float('inf'), -float('inf'), -float('inf')

    for contour in contours:
        # Ignora pequenos contornos (áreas pequenas)
        if cv2.contourArea(contour) > 600:  # Ajuste o limite conforme necessário
            qt_movimento += 1

            # Obtém as coordenadas do retângulo que envolve o contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Atualiza as coordenadas mínima e máxima
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

    # Desenha o único retângulo que envolve todas as áreas de movimento
    if qt_movimento > 0:
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Cor verde e espessura 2

    return qt_movimento


def exibe_status(img, qt_movimento, new_height):
    """
    Exibe o status da detecção de movimento, redimensionado proporcionalmente à altura do vídeo.
    """
    # Calcula a posição e o tamanho da caixa de status de acordo com a altura do vídeo redimensionado
    box_height = int(new_height * 0.1)  # Tamanho da caixa de status em 10% da altura do vídeo
    box_width = int(img.shape[1] * 0.5)  # Largura da caixa em 50% da largura do vídeo

    # Define as coordenadas da caixa de status
    top_left = (int(img.shape[1] * 0.1), 0)  # Posição horizontal proporcional
    bottom_right = (top_left[0] + box_width, box_height)  # Posição da parte inferior da caixa

    # Desenha a caixa de status
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), -1)

    # Exibe o texto dentro da caixa
    cv2.putText(img, f'FIRE: {qt_movimento}', (top_left[0] + 10, top_left[1] + box_height - 10),
                cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 5)


def main():
    namevideo = 'fire-cnc.mp4'
    #namevideo = 'fire-cnc-1.mp4'
    #namevideo = 'fire-cnc-2.mp4'
    video_path = f'C:/Users/usuario/Desktop/Inteligencia Artificial/visao-comp-detecta-fogo/fire-detection/{namevideo}'
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    # Obtém a resolução original do vídeo
    original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define a altura desejada para o vídeo redimensionado
    new_height = 500

    # Calcula a nova largura mantendo a proporção do vídeo original
    aspect_ratio = original_width / original_height
    new_width = int(new_height * aspect_ratio)

    paused = False  # Variável para controlar o estado de pausa

    while True:
        if not paused:
            check, img = video.read()
            if not check:
                break

            # Redimensiona o frame
            resized_frame = cv2.resize(img, (new_width, new_height))

            # Processa o frame para detectar o movimento da cor branca
            motion_mask, white_mask = processa_frame(resized_frame)

            # Analisa o movimento
            qt_movimento = analisa_movimento(resized_frame, motion_mask)

            # Exibe o status do movimento detectado
            exibe_status(resized_frame, qt_movimento, new_height)

            # Exibe o vídeo redimensionado
            cv2.imshow('Video', resized_frame)
            
            # Exibe a máscara de movimento
            cv2.namedWindow('Passo', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Passo', 180, 320)
            cv2.imshow('Passo', motion_mask)

            # Exibe a área branca isolada
            cv2.namedWindow('Area Branca', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Area Branca', 178, 292)
            cv2.imshow('Area Branca', white_mask)

        # Delay no vídeo
        key = cv2.waitKey(50)

        if key == ord('q'):  # Pressione 'q' para sair
            break
        elif key == ord('p'):  # Pressione 'p' para pausar/despausar
            paused = not paused

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
