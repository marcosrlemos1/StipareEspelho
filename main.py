#IMPORT MODULES
import sys
import os

#IMPORT QT_CORE
from qt_core import *

#import opencv
import cv2

#IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import UI_MainWindow

#class  MAIN WINDOW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)


        #SHOW APPLICATION
        self.show()
        self.ui.toggle.setCheckable(False)
        self.ui.toggle.clicked.connect(self.handle_toggle)

        #INITIAL PARAMETERS
        self.brilho = 49
        self.constraste = 49
        self.selected_option = None
        self.control = False
        self.frame_tratado = None
        self.capture = None
        self.camera_ativa = False
        self.ui.ui_pages.slider.setEnabled(False)
        self.ui.ui_pages.slider2.setEnabled(False)
        self.ui.ui_pages.combobox.setEnabled(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.video_frame)
        self.timer.timeout.connect(self.update_label)
        self.timer.timeout.connect(self.tratamento_frame)
        self.timer.start(30) # Atualiza o frame a cada 30 milissegundos

        self.ui.ui_pages.combobox.currentIndexChanged.connect(self.combobox_selection_changed)  # Conectar o sinal ao método
        self.ui.ui_pages.slider.valueChanged.connect(self.slider_value_changed)
        self.ui.ui_pages.slider2.valueChanged.connect(self.slider_value_changed2)

        self.data_hora2 =self.update_label()

        self.ui.toggle2.clicked.connect(self.show_page_2)
        self.ui.toggle.clicked.connect(self.show_page_1)

        self.ui.action1.triggered.connect(self.capture_and_save_image)
        self.ui.action2.triggered.connect(self.exit_application)

    def show_page_1(self):
        self.ui.paginas.setCurrentWidget(self.ui.ui_pages.page1)

    def show_page_2(self):
        self.ui.paginas.setCurrentWidget(self.ui.ui_pages.page2)


    def update_label(self):
        atual = QDateTime.currentDateTime()
        formatted_datetime = atual.toString("dd/MM/yyyy - hh:mm:ss")
        self.ui.label_status.setText("STATUS: " + formatted_datetime)


    #função responsavel para ativar e desativar a camera e botão
    def handle_toggle(self):
        #camera desativada e botão desativado
        if self.ui.toggle.isChecked() and self.camera_ativa == True:
            self.ui.toggle.setStyleSheet(
                "QPushButton:hover {"
                "background-color: #3E4145;" 
                "}"
                )
            
            self.capture.release()  # Libera a câmera
            self.capture = None
            self.camera_ativa = False
        
        #camera ativada e botão ativado
        else:
            self.ui.toggle.setCheckable(True)
            self.camera_ativa = True
            self.ui.toggle.setStyleSheet("background-color: red")
            self.capture = cv2.VideoCapture(0)



    def capturar_frame(self):
        if self.capture is not None:
            ret, self.frame = self.capture.read()  # Captura um frame da câmera
            if ret:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
                return cv2.resize(self.frame, (480, 360))
            else:
                QMessageBox.warning(None, "Sem frame", "A câmera não está retornando frame.")
                self.capture = None
                self.ui.toggle.setCheckable(True)

    def video_frame(self):
        self.frame = self.capturar_frame()
        if self.frame_tratado is not None:
            self.ui.ui_pages.slider.setEnabled(True)
            self.ui.ui_pages.slider2.setEnabled(True)
            self.ui.ui_pages.combobox.setEnabled(True)
            # Define as dimensões desejadas para exibição
            target_width, target_height = 480, 360

            # Redimensiona o quadro para as dimensões desejadas
            resized_frame = cv2.resize(self.frame_tratado, (target_width, target_height))

            # Converte o quadro redimensionado em uma imagem QImage
            image = QImage(resized_frame.data, target_width, target_height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # Redimensiona a pixmap para a exibição sem cortar
            pixmap = pixmap.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.label_camera.setPixmap(pixmap)
            self.ui.label_camera.setFixedSize(target_width, target_height)
        else:
            self.ui.ui_pages.slider.setEnabled(False)
            self.ui.ui_pages.slider2.setEnabled(False)
            self.ui.ui_pages.combobox.setEnabled(False)
            # Define as dimensões desejadas para exibição
            target_width, target_height = 480, 360

            # Cria uma imagem preta com as dimensões desejadas
            dark_frame = QImage(target_width, target_height, QImage.Format_RGB888)
            dark_frame.fill(Qt.black)

            # Exibe o quadro escuro
            pixmap = QPixmap.fromImage(dark_frame)

            # Redimensiona a pixmap para a exibição sem cortar
            pixmap = pixmap.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.label_camera.setPixmap(pixmap)
            self.ui.label_camera.setFixedSize(target_width, target_height)

    def brilho_contraste(self, imagem, brilho, contraste):
        brilho = (((brilho + 1)-50)/50)*127
        contraste = ((contraste + 1)*2)/100
        # Aplicar a transformação linear de ajuste de brilho e contraste
        imagem_ajustada = cv2.convertScaleAbs(imagem, alpha=contraste, beta=brilho)

        return imagem_ajustada

    # Aplicando super-resolução - ESPCN 
    def super_resolucao(self, imagem, path, index):
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(path)
        sr.setModel("espcn", index+1)
        result_sr = sr.upsample(imagem)

        return result_sr
    
    #Função pra retornar o indice do Combobox
    def combobox_selection_changed(self, index):
        self.index = index
        self.selected_option = 'ESPCN_SR/'+self.ui.ui_pages.combobox.currentText()  # Obter a opção selecionada
        self.control = True
        self.report(f"{self.data_hora()} / Escala de super resolução mudou para {self.ui.ui_pages.combobox.currentText()}")

    #Função para retornar o valor do brilho
    def slider_value_changed(self, value):
        self.brilho = value
        self.ui.ui_pages.label.setText(f"BRILHO : {(value+1)-50}")
    
    #Função para retornar o valor do contraste
    def slider_value_changed2(self, value2):
        self.constraste = value2
        self.ui.ui_pages.label2.setText(f"CONTRASTE : {(value2+1)-50}")

    #Função de tratamento de frame com correção de iluminação e super resolução
    def tratamento_frame(self):
        self.frame_tratado = self.brilho_contraste(self.frame, self.brilho, self.constraste)
        if self.control is True:
            self.frame_tratado = self.super_resolucao(self.frame_tratado, self.selected_option, self.index)
            self.control = False
        
    #Função de mensagem para o console 
    def report(self, message):
        # Adiciona uma mensagem de reportagem ao console
        self.ui.text_edit.append(message)
    
    #Função para retornar a data e a hora atual
    def data_hora(self):
        atual = datetime.now()
        return atual.strftime("%d/%m/%Y - %H:%M")
    
    def exit_application(self):
        # Exibir um diálogo de confirmação antes de sair
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def capture_and_save_image(self):

        if self.camera_ativa == True:
            # Capturar a tela inteira usando o OpenCV
            screenshot = cv2.VideoCapture(0)
            ret, frame = screenshot.read()

            # Solicitar ao usuário um local e nome de arquivo para salvar a imagem
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")

            # Salvar a imagem capturada como arquivo PNG usando o OpenCV
            if file_path:
                cv2.imwrite(file_path, frame)

        else:
            QMessageBox.warning(None,"sem frame", "A câmera não está ativa.")
            
#Inicilização da IDE
if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    sys.exit(app.exec())