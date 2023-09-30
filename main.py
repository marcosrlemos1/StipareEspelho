# IMPORT MODULES
import sys
import os
import configparser

# IMPORT QT_CORE
from qt_core import *

# import opencv
import cv2

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import UI_MainWindow

# class  MAIN WINDOW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.setWindowTitle("Tellescom")

        # SHOW APPLICATION
        self.show()
        self.ui.toggle.setCheckable(False)
        self.ui.toggle.clicked.connect(self.handle_toggle)

        # INITIAL PARAMETERS
        self.cam_width = 800
        self.cam_height = 600
        self.brilho = 49
        self.contraste = 49
        self.selected_option = 0
        self.index = 0
        self.frame_tratado = None
        self.capture = None
        self.restore_control = False
        self.camera_ativa = False
        self.switch_value = False
        self.switch_value2 = False
        self.switch_value3 = False
        self.switch_value4 = False

        # Configurações padrões
        self.default_settings = {
            'brilho': 49,
            'contraste': 49,
            'index': 0,
            'switch_value': False,
        }

        sys.stdout = self
        self.log_messages = []
        self.settings = configparser.ConfigParser()

        self.ui.ui_pages.slider.setEnabled(False)
        self.ui.ui_pages.slider2.setEnabled(False)
        self.ui.ui_pages.combobox.setEnabled(False)
        self.ui.ui_pages.switch.setEnabled(False)
        self.ui.ui_pages.switch2.setEnabled(False)
        self.ui.ui_pages.switch3.setEnabled(False)
        self.ui.ui_pages.switch4.setEnabled(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.video_frame)
        self.timer.timeout.connect(self.update_label)
        self.timer.timeout.connect(self.tratamento_frame)
        self.timer.start(30)  # Atualiza o frame a cada 30 milissegundos

        self.ui.ui_pages.combobox.currentIndexChanged.connect(self.combobox_selection_changed)  # Conectar o sinal ao método
        self.ui.ui_pages.slider.valueChanged.connect(self.slider_value_changed)
        self.ui.ui_pages.slider2.valueChanged.connect(self.slider_value_changed2)
        self.ui.ui_pages.switch.clicked.connect(self.switch_changed)
        self.ui.ui_pages.switch2.clicked.connect(self.switch_changed2)
        self.ui.ui_pages.switch3.clicked.connect(self.switch_changed3)
        self.ui.ui_pages.switch4.clicked.connect(self.switch_changed4)
        self.ui.ui_pages.restore_button.clicked.connect(self.restore_defaults)
        self.ui.edit.clicked.connect(self.restore_defaults)

        self.data_hora2 = self.update_label()

        self.ui.toggle2.clicked.connect(self.show_page_2)
        self.ui.toggle.clicked.connect(self.show_page_1)

        self.ui.action1.triggered.connect(self.save_image)
        self.ui.action2.triggered.connect(self.save_log)
        self.ui.action3.triggered.connect(self.saveSettings)
        self.ui.action4.triggered.connect(self.loadSettings)
        self.ui.action5.triggered.connect(self.exit_application)

    def show_page_1(self):
        self.ui.paginas.setCurrentWidget(self.ui.ui_pages.page1)

    def show_page_2(self):
        self.ui.paginas.setCurrentWidget(self.ui.ui_pages.page2)

    def update_label(self):
        atual = QDateTime.currentDateTime()
        formatted_datetime = atual.toString("dd/MM/yyyy - hh:mm:ss")
        self.ui.label_status.setText("STATUS: " + formatted_datetime)

    # função responsavel para ativar e desativar a camera e botão
    def handle_toggle(self):
        # camera desativada e botão desativado
        if self.ui.toggle.isChecked() and self.camera_ativa == True:
            self.ui.toggle.setStyleSheet(
                "QPushButton:hover {"
                "background-color: #3E4145;"
                "}"
            )

            self.capture.release()  # Libera a câmera
            self.capture = None
            self.camera_ativa = False
            self.report(f"{self.data_hora()} / Câmera desativada")

        # camera ativada e botão ativado
        else:
            self.ui.toggle.setCheckable(True)
            self.camera_ativa = True
            self.ui.toggle.setStyleSheet("background-color: red")
            self.capture = cv2.VideoCapture(0)
            self.report(f"{self.data_hora()} / Câmera ativada")

    def capturar_frame(self):
        if self.capture is not None:
            ret, self.frame = self.capture.read()  # Captura um frame da câmera
            if ret:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
                return self.frame
            else:
                QMessageBox.warning(None, "Sem frame","A câmera não está retornando frame.")
                self.capture = None
                self.ui.toggle.setCheckable(True)

    def video_frame(self):
        self.frame = self.capturar_frame()
        if self.frame_tratado is not None:
            self.ui.ui_pages.slider.setEnabled(True)
            self.ui.ui_pages.slider2.setEnabled(True)
            self.ui.ui_pages.combobox.setEnabled(True)
            self.ui.ui_pages.switch.setEnabled(True)
            self.ui.ui_pages.switch2.setEnabled(True)
            self.ui.ui_pages.switch3.setEnabled(True)
            self.ui.ui_pages.switch4.setEnabled(True)

            # Define as dimensões desejadas para exibição
            target_width, target_height = self.cam_width, self.cam_height

            # Redimensiona o quadro para as dimensões desejadas
            resized_frame = cv2.resize(
                self.frame_tratado, (target_width, target_height))

            # Converte o quadro redimensionado em uma imagem QImage
            image = QImage(resized_frame.data, target_width,
                           target_height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # Redimensiona a pixmap para a exibição sem cortar
            pixmap = pixmap.scaled(
                target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.label_camera.setPixmap(pixmap)
            self.ui.label_camera.setFixedSize(target_width, target_height)
        else:
            self.ui.ui_pages.slider.setEnabled(False)
            self.ui.ui_pages.slider2.setEnabled(False)
            self.ui.ui_pages.combobox.setEnabled(False)
            self.ui.ui_pages.switch.setEnabled(False)
            self.ui.ui_pages.switch2.setEnabled(False)
            self.ui.ui_pages.switch3.setEnabled(False)
            self.ui.ui_pages.switch4.setEnabled(False)

            # Define as dimensões desejadas para exibição
            target_width, target_height = 480, 360

            # Cria uma imagem preta com as dimensões desejadas
            dark_frame = QImage(target_width, target_height,
                                QImage.Format_RGB888)
            dark_frame.fill(Qt.black)

            # Exibe o quadro escuro
            pixmap = QPixmap.fromImage(dark_frame)

            # Redimensiona a pixmap para a exibição sem cortar
            pixmap = pixmap.scaled(
                target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.label_camera.setPixmap(pixmap)
            self.ui.label_camera.setFixedSize(target_width, target_height)

    def brilho_contraste(self, imagem, brilho, contraste):
        brilho = (((brilho + 1)-50)/50)*127
        contraste = ((contraste + 1)*2)/100
        # Aplicar a transformação linear de ajuste de brilho e contraste
        imagem_ajustada = cv2.convertScaleAbs(
            imagem, alpha=contraste, beta=brilho)

        return imagem_ajustada

    # Aplicando super-resolução - ESPCN
    def super_resolucao(self, imagem, path, index):
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(path)
        sr.setModel("espcn", index+1)
        result_sr = sr.upsample(imagem)

        return result_sr

    # Aplicação de equalização por histograma
    def histogram_equalization(self, imagem):
        canal_azul, canal_verde, canal_vermelho = cv2.split(imagem)
        # Aplicar a equalização de histograma a cada canal
        canal_azul_equalizado = cv2.equalizeHist(canal_azul)
        canal_verde_equalizado = cv2.equalizeHist(canal_verde)
        canal_vermelho_equalizado = cv2.equalizeHist(canal_vermelho)
        # Mesclar os canais equalizados para obter a imagem colorida final
        imagem_equalizada = cv2.merge(
            (canal_azul_equalizado, canal_verde_equalizado, canal_vermelho_equalizado))

        return imagem_equalizada

    # Aplicação de filtro passa baixa
    def passa_baixa(self, imagem):
        kernel_size = (5, 5)  # Tamanho do kernel
        filtro_passa_baixa = np.ones(
            kernel_size, dtype=np.float32) / (kernel_size[0] * kernel_size[1])

        # Aplicar o filtro passa-baixa
        imagem_suavizada = cv2.filter2D(imagem, -1, filtro_passa_baixa)

        return imagem_suavizada

    def filtro_mediana(self, imagem):
        # Aplicar o filtro de mediana separadamente a cada canal de cor
        canal_azul = cv2.medianBlur(imagem[:, :, 0], 5)
        canal_verde = cv2.medianBlur(imagem[:, :, 1], 5)
        canal_vermelho = cv2.medianBlur(imagem[:, :, 2], 5)

        # Mesclar os canais para obter a imagem suavizada
        imagem_suavizada_m = cv2.merge(
            (canal_azul, canal_verde, canal_vermelho))

        return imagem_suavizada_m

    def nitidez(self, imagem):
        # Crie um kernel de nitidez
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])

        # Aplique o filtro de nitidez à imagem
        imagem_nitida = cv2.filter2D(imagem, -1, kernel)

        return imagem_nitida

    # Função pra retornar o indice do Combobox
    def combobox_selection_changed(self, index):
        self.index = index
        if self.index == 0 and self.restore_control is False:
            self.report(f"{self.data_hora()} / Escala de super resolução desativada")
        if self.index != 0 and self.restore_control is False:
            self.selected_option = 'ESPCN/' + self.ui.ui_pages.combobox.currentText()  # Obter a opção selecionada
            self.report(f"{self.data_hora()} / Escala de super resolução mudou para {self.ui.ui_pages.combobox.currentText()}")

    # Função para retornar o valor do brilho
    def slider_value_changed(self, value):
        self.brilho = value
        self.ui.ui_pages.label.setText(f"Brilho : {(value+1)-50}")

    # Função para retornar o valor do contraste
    def slider_value_changed2(self, value2):
        self.contraste = value2
        self.ui.ui_pages.label2.setText(f"Contraste : {(value2+1)-50}")

    # Função para retornar o valor do botão EH
    def switch_changed(self, switch_value):
        self.switch_value = switch_value
        if switch_value is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Equilização por histograma ativado")
        if switch_value is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Equilização por histograma desativado")

    # Função para retornar o valor do botão FPB
    def switch_changed2(self, switch_value2):
        self.switch_value2 = switch_value2

        if switch_value2 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro passa-baixa ativado")
        if switch_value2 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro passa-baixa desativado")

    # Função para retornar o valor do botão FM
    def switch_changed3(self, switch_value3):
        self.switch_value3 = switch_value3

        if switch_value3 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro por mediana ativado")
        if switch_value3 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro por mediana desativado")

    # Função para retornar o valor do botão FM
    def switch_changed4(self, switch_value4):
        self.switch_value4 = switch_value4

        if switch_value4 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Nitidez ativada")
        if switch_value4 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Nitidez desativada")

    # Função de tratamento de frame com correção de iluminação e super resolução
    def tratamento_frame(self):
        self.frame_tratado = self.brilho_contraste(self.frame, self.brilho, self.contraste)
        if self.index != 0 and self.frame is not None:
            self.frame_tratado = self.super_resolucao(self.frame_tratado, self.selected_option, self.index)
        if self.switch_value is True and self.frame is not None:
            self.frame_tratado = self.histogram_equalization(self.frame_tratado)
        if self.switch_value2 is True and self.frame is not None:
            self.frame_tratado = self.passa_baixa(self.frame_tratado)
        if self.switch_value3 is True and self.frame is not None:
            self.frame_tratado = self.filtro_mediana(self.frame_tratado)
        if self.switch_value4 is True and self.frame is not None:
            self.frame_tratado = self.nitidez(self.frame_tratado)

    # Função de mensagem para o console
    def report(self, message):
        # Adiciona uma mensagem de reportagem ao console
        self.write(message + '\n')

    # Funcão para salvar dados do terminal
    def save_log(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.HideNameFilterDetails

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Salvar Log", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)", options=options)

        if file_name:
            with open(file_name, 'w') as log_file:
                # Escreve todas as mensagens armazenadas no arquivo
                log_file.write('\n'.join(self.log_messages))

    # Substitua a função write para redirecionar a saída para o QTextEdit
    def write(self, text):
        self.ui.text_edit.moveCursor(QTextCursor.End)
        self.ui.text_edit.insertPlainText(text)
        self.ui.text_edit.moveCursor(QTextCursor.End)

        # Adicione a mensagem à lista de mensagens de log
        self.log_messages.append(text.strip())

    # Função para retornar a data e a hora atual
    def data_hora(self):
        atual = datetime.now()

        return atual.strftime("%d/%m/%Y - %H:%M")

    def exit_application(self):
        # Perguntar ao usuário se ele deseja salvar as configurações
        reply = QMessageBox.question(self, "Salvar Configurações", "Deseja salvar as configurações antes de sair?",
                                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            self.saveSettings()
            QApplication.quit()
        elif reply == QMessageBox.No:
            QApplication.quit()
        else:
            pass  # O usuário cancelou, não faz nada
  
    # Função para salvar um frame da imagem
    def save_image(self):
        if self.camera_ativa == True:
            self.frame_rgb = cv2.cvtColor(self.frame_tratado, cv2.COLOR_BGR2RGB)
            # Solicitar ao usuário um local e nome de arquivo para salvar a imagem
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)")

            # Salvar a imagem capturada como arquivo PNG usando o OpenCV
            if file_path:
                cv2.imwrite(file_path, self.frame_rgb)

        else:
            QMessageBox.warning(None, "sem frame", "A câmera não está ativa.")
    
    def restore_defaults(self):
        # Restaura as configurações padrões
        self.restore_control = True
        self.ui.ui_pages.slider.setValue(self.default_settings['brilho'])
        self.ui.ui_pages.slider2.setValue(self.default_settings['contraste'])
        self.ui.ui_pages.combobox.setCurrentIndex(self.default_settings['index'])
        self.ui.ui_pages.switch.setChecked(self.default_settings['switch_value'])
        self.switch_value = self.default_settings['switch_value']
        self.ui.ui_pages.switch2.setChecked(self.default_settings['switch_value'])
        self.switch_value2 = self.default_settings['switch_value']
        self.ui.ui_pages.switch3.setChecked(self.default_settings['switch_value'])
        self.switch_value3 = self.default_settings['switch_value']
        self.ui.ui_pages.switch4.setChecked(self.default_settings['switch_value'])
        self.switch_value4 = self.default_settings['switch_value']
        

        QMessageBox.information(None, "Restaurar configuração", "Restaurado com sucesso")
        self.report(f"{self.data_hora()} / Configurações restauradas")
        self.restore_control = False
    
    def saveSettings(self):
        str_brilho = str(self.brilho)
        str_contraste = str(self.contraste)
        str_index = str(self.index)
        str_switch_value = str(self.switch_value)
        str_switch_value2 = str(self.switch_value2)
        str_switch_value3 = str(self.switch_value3)
        str_switch_value4 = str(self.switch_value4)

        # Configurações personalizadas
        self.settings['Configuracoes'] = {
            'brilho': str_brilho,
            'contraste': str_contraste,
            'index': str_index,
            'switch_value': str_switch_value,
            'switch_value2': str_switch_value2,
            'switch_value3': str_switch_value3,
            'switch_value4': str_switch_value4,
        }

        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Configurações", "", "Arquivos de Configuração (*.ini);;Todos os Arquivos (*)")

        if file_name:
            # Salvar as configurações em um arquivo
            with open(file_name, 'w') as configfile:
                self.settings.write(configfile)
            QMessageBox.information(None, "Informação", "Configurações salvas com sucesso.")
    
    def loadSettings(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Carregar Configurações", "", "Arquivos de Configuração (*.ini);;Todos os Arquivos (*)")

        if file_name:
            # Carregar configurações de um arquivo
            try:
                self.settings.read(file_name)
                self.ui.ui_pages.slider.setValue(self.settings.getint('Configuracoes', 'brilho'))
                self.ui.ui_pages.slider2.setValue(self.settings.getint('Configuracoes', 'contraste'))
                self.ui.ui_pages.combobox.setCurrentIndex(self.settings.getint('Configuracoes', 'index'))
                self.ui.ui_pages.switch.setChecked(self.settings.getboolean('Configuracoes', 'switch_value'))
                self.switch_value = self.settings.getboolean('Configuracoes', 'switch_value')
                self.ui.ui_pages.switch2.setChecked(self.settings.getboolean('Configuracoes', 'switch_value2'))
                self.switch_value2 = self.settings.getboolean('Configuracoes', 'switch_value2')
                self.ui.ui_pages.switch3.setChecked(self.settings.getboolean('Configuracoes', 'switch_value3'))
                self.switch_value3 = self.settings.getboolean('Configuracoes', 'switch_value3')
                self.ui.ui_pages.switch4.setChecked(self.settings.getboolean('Configuracoes', 'switch_value4'))
                self.switch_value4 = self.settings.getboolean('Configuracoes', 'switch_value4')
            except FileNotFoundError:
                QMessageBox.warning(None, "Aviso", "O arquivo de configuração não foi encontrado.")
        
# Inicilização da IDE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())