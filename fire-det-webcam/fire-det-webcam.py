import cv2 

# Busca classificadores do XML treinado
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

# Start da camera
vid = cv2.VideoCapture(0) 

# Teste com vídeo
# vid = cv2.VideoCapture("fire-detection\\fire-cnc-1")

while True:
    # ret será True se a leitura do frame for bem-sucedida
    ret, frame = vid.read() 
    if not ret:
        print("Falha ao capturar o frame. Saindo...")
        break

    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # Detecta fogo no frame
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    # Destaca o fogo detectado no video
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        print("Fogo detectado!")

    # Exibe o frame com os retângulos
    cv2.imshow('Detecção de Fogo', frame)

    # Sai ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha a janela de exibição
vid.release()
cv2.destroyAllWindows()

#python fire-det-webcam.py