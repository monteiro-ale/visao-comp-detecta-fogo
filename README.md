# Projeto de Visão Computacional
Protótipo de projeto para detectar fogo em máquinas de corte a laser.

Este projeto utiliza técnicas de visão computacional para detectar áreas brancas em movimento, como possíveis indícios de fogo, em vídeos de máquinas de corte a laser. O código é escrito em Python e depende de bibliotecas como OpenCV e NumPy.

---

## 🛠 Configuração do Ambiente

### Pré-requisitos
   **Python instalado**:
     Certifique-se de ter o Python 3.10+ instalado em sua máquina.
     Verifique com:
     ```bash
     python --version
     ```

   **Ambiente virtual**:
     É recomendável usar um ambiente virtual para isolar as dependências do projeto.

---

### Passos para configurar:

  #### 1. Criar o ambiente virtual
  No terminal ou prompt de comando, execute:
	```bash
	python -m venv env-visao
	```

  #### 2. Ativar o ambiente virtual:
  No macOS e Linux:
	```bash
	source ./env-visao/bin/activate
	```
  No Windows:
	```bash
	.\env-visao\Scripts\activate
	```

## 📦 Instalação de Dependências

  #### Depois de ativar o ambiente virtual, instale as dependências listadas no arquivo requirements.txt:
	```bash
	pip install -r requirements.txt
	```

## 🚀 Execução do Projeto

  #### Para executar o reconhecimento de fogo no vídeo:

	```bash
	python main.py
	```

## 🎥 Funcionalidades Específicas

  **Pausa e Continuação do Vídeo**
  Enquanto o vídeo está sendo exibido e analisado, é possível pausá-lo e retomá-lo com as seguintes teclas:

  **Tecla P: Pausar/continuar o vídeo.**
  **Tecla Q: Encerrar a execução do programa.**
  Máscaras e Visualizações
  Janela Principal: Exibe o vídeo original com a detecção de movimento.
  Máscara de Movimento: Realça áreas brancas em movimento.
  Área Branca: Destaca as áreas brancas identificadas no quadro atual.

## 📁 Estrutura do Projeto

  #### A estrutura do projeto é organizada como segue:
	```bash
	C:.
	│   .gitignore
	│   README.md
	│   requirements.txt
	│
	└───fire-detection
					main.py
					README.md
					roi.py
					videoplayback.webm
					videoplayback2.mp4
	```

## 📝 Notas Importantes

  **Certifique-se de que o caminho do vídeo esteja corretamente configurado no script.**

  No código, altere a linha:
	```python
	video_path = 'caminho/para/seu/video.mp4'
	```
  **O limite de detecção para áreas brancas pode ser ajustado no código:**

	```python
	_, white_mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
	```
Ajuste o valor 240 para modificar a sensibilidade à cor branca.
Pequenos contornos são ignorados por padrão (áreas menores que 500 pixels). Caso necessário, modifique o valor no trecho:

	```python
	if cv2.contourArea(contour) > 500:
		```
A velocidade de reprodução do vídeo pode ser ajustada modificando o valor de cv2.waitKey() no laço principal do código.