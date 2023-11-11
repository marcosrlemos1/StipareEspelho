# IMPORT MODULES
import sys
import os
import configparser
import copy

# IMPORT QT_CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import UI_MainWindow

#GLOBAL VAR
control_cam =  False
x1_cam = None
y1_cam = None
x2_cam = None
y2_cam = None
frame_tratado = None

# class  MAIN WINDOW
class Frame_Cam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecione a região da câmera")
        icon = QIcon("./gui/imagens/icons/tellescom_logo.png")
        self.setWindowIcon(icon)

        self.selection_start = None
        self.selection_end = None
        self.geometry = True
        self.capture_frame = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.label.mousePressEvent = self.mouse_press_event
        self.label.mouseReleaseEvent = self.mouse_release_event
        self.label.mouseMoveEvent = self.mouse_move_event

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.mostrar_frame_camera)
        self.timer.start(30)  # Atualização do feed da câmera a cada 30 milissegundos

        if control_cam is True:
            self.capture_frame = cv2.VideoCapture(cv2.CAP_DSHOW)
        
    def mostrar_frame_camera(self):
        if control_cam is True and self.capture_frame is not None:
            ret, frame = self.capture_frame.read()

            if ret:
                # Desenhe o retângulo na área de visualização da câmera, se houver uma seleção
                if self.selection_start and self.selection_end:
                    x1, y1 = self.selection_start.x(), self.selection_start.y()
                    x2, y2 = self.selection_end.x(), self.selection_end.y()
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Desenhe o retângulo vermelho

                # Converta o quadro do OpenCV para um formato exibível pelo PySide6
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.height_cam, self.width_cam, channel = frame.shape

                if self.geometry is True:
                    self.setGeometry(100, 100, self.width_cam, self.height_cam)
                    self.geometry = False

                qt_image = QImage(frame.data, self.width_cam, self.height_cam, QImage.Format_RGB888)

                # Exiba o quadro na janela
                pixmap = QPixmap.fromImage(qt_image)
                self.label.setPixmap(pixmap)
                self.label.adjustSize()

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_start = event.pos()
            self.selection_end = None
            self.update()

    def mouse_release_event(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

            # Calcule a área em relação à resolução da câmera
            if self.selection_start and self.selection_end:
                x1, y1 = self.selection_start.x(), self.selection_start.y()
                x2, y2 = self.selection_end.x(), self.selection_end.y()

                width = abs(x2 - x1)
                height = abs(y2 - y1)

                # Mostre um diálogo de mensagem perguntando ao usuário o que fazer
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Seleção Concluída")
                msg_box.setText(f"Área selecionada: X:{x1}, Y:{y1}, Width:{width}, Height:{height}")
                msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Retry)
                msg_box.setDefaultButton(QMessageBox.Save)
                choice = msg_box.exec()

                if choice == QMessageBox.Save:
                    self.save_selection(x1, y1, x2, y2)
                elif choice == QMessageBox.Retry:
                    self.reset_selection()

    def mouse_move_event(self, event):
        # Atualize a seleção em tempo real enquanto o mouse se move
        if event.buttons() == Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

    def save_selection(self, x1, y1, x2, y2):
        global control_cam
        control_cam = False

        global x1_cam
        global y1_cam
        global x2_cam
        global y2_cam

        x1_cam = x1
        y1_cam = y1
        x2_cam = x2
        y2_cam = y2

        self.capture_frame.release()
        self.close()

    def reset_selection(self):
        # Reinicie a seleção
        self.selection_start = None
        self.selection_end = None
        self.update()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.setWindowTitle("Tellescom")
        icon = QIcon("./gui/imagens/icons/tellescom_logo.png")
        self.setWindowIcon(icon)

        # SHOW APPLICATION
        self.show()
        self.ui.toggle.setCheckable(False)
        self.ui.toggle.clicked.connect(self.handle_toggle)

        #YOLO PARAMETERS
        model_weights = './data/Yolo/yolov4_2000_final_caixa_aberta.weights'
        model_config = './data/Yolo/yolov4_custom.cfg'

        net_caixa_aberta = cv2.dnn.readNet(model_weights, model_config)
        self.model_caixa_aberta = cv2.dnn_DetectionModel(net_caixa_aberta)
        self.model_caixa_aberta.setInputParams(size=(249,249), scale=1/255)

        # INITIAL PARAMETERS
        self.brilho = 49
        self.contraste = 49
        self.selected_option = 0
        self.index = 0
        self.index_modo = 0
        self.capture = None
        self.restore_control = False
        self.control_save = False
        self.camera_ativa = False
        self.switch_value = False
        self.switch_value2 = False
        self.switch_value3 = False
        self.switch_value4 = False
        self.box = []
        self.box2 = []
        self.box3 = []
        self.label = None
        self.label2 = None
        self.label3 = None
        self.create_control = True
        self.frame_cache = {}
        self.control_detection = True

        sys.stdout = self
        self.log_messages = []
        self.settings = configparser.ConfigParser()
        self.default_settings = configparser.ConfigParser()
        self.current_settings = configparser.ConfigParser()

        # Configurações padrões
        self.default_settings['Configuracoes'] = {
            'brilho': '49',
            'contraste': '49',
            'index': '0',
            'switch_value': 'False',
            'switch_value2': 'False',
            'switch_value3': 'False',
            'switch_value4': 'False',
        }

        self.current_settings = copy.deepcopy(self.default_settings)
        self.settings = copy.deepcopy(self.default_settings)

        self.ui.ui_pages.slider.setEnabled(False)
        self.ui.ui_pages.slider2.setEnabled(False)
        self.ui.ui_pages.combobox.setEnabled(False)
        self.ui.ui_pages.switch.setEnabled(False)
        self.ui.ui_pages.switch2.setEnabled(False)
        self.ui.ui_pages.switch3.setEnabled(False)
        self.ui.ui_pages.switch4.setEnabled(False)

        self.timer, self.timer2 = QTimer(), QTimer()
        self.timer.timeout.connect(self.video_frame)
        self.timer.timeout.connect(self.update_label)
        self.timer.timeout.connect(self.tratamento_frame)
        self.timer2.timeout.connect(self.yolo)
        self.timer.start(10)  # Atualiza o frame a cada 30 milissegundos
        self.timer2.start(3000)

        self.ui.ui_pages.combobox.currentIndexChanged.connect(self.combobox_selection_changed)  # Conectar o sinal ao método
        self.ui.ui_pages.combobox_modo.currentIndexChanged.connect(self.combobox_modo_selection_changed)
        self.ui.ui_pages.slider.valueChanged.connect(self.slider_value_changed)
        self.ui.ui_pages.slider2.valueChanged.connect(self.slider_value_changed2)
        self.ui.ui_pages.switch.clicked.connect(self.switch_changed)
        self.ui.ui_pages.switch2.clicked.connect(self.switch_changed2)
        self.ui.ui_pages.switch3.clicked.connect(self.switch_changed3)
        self.ui.ui_pages.switch4.clicked.connect(self.switch_changed4)

        self.data_hora2 = self.update_label()

        self.ui.action1.triggered.connect(self.save_image)
        self.ui.action2.triggered.connect(self.save_log)
        self.ui.action3.triggered.connect(self.saveSettings)
        self.ui.action4.triggered.connect(self.loadSettings)
        self.ui.action5.triggered.connect(self.exit_application)

        self.ui.action2_1.triggered.connect(self.restore_defaults)
        self.ui.action2_2.triggered.connect(self.frame_cam)
        self.ui.action2_3.triggered.connect(self.frame_cam_restore)

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

        # camera ativada e botão ativado
        else:
            self.ui.toggle.setCheckable(True)
            self.camera_ativa = True
            self.ui.toggle.setStyleSheet("background-color: red")
            self.capture = cv2.VideoCapture(cv2.CAP_DSHOW)

    def capturar_frame(self):
        if self.capture is not None:
            ret, self.frame = self.capture.read()  # Captura um frame da câmera
            if ret:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
                if x1_cam is not None:
                    self.frame = self.frame[y1_cam:y2_cam, x1_cam:x2_cam]
                return self.frame
            else:
                QMessageBox.warning(None, "Sem frame","A câmera não está retornando frame.")
                self.capture = None
                self.ui.toggle.setCheckable(True)

    def video_frame(self): 
        self.frame = self.capturar_frame()
        global frame_tratado
        if frame_tratado is not None:
            self.ui.ui_pages.slider.setEnabled(True)
            self.ui.ui_pages.slider2.setEnabled(True)
            self.ui.ui_pages.combobox.setEnabled(True)
            self.ui.ui_pages.switch.setEnabled(True)
            self.ui.ui_pages.switch2.setEnabled(True)
            self.ui.ui_pages.switch3.setEnabled(True)
            self.ui.ui_pages.switch4.setEnabled(True)

            width, height = 800,600

            if self.index_modo == 0 :
                pass
            else:
                if len(self.box) > 0:
                    cv2.rectangle(frame_tratado, self.box, (0, 255, 0), 2)
                    cv2.putText(frame_tratado, self.label, (self.box[0], self.box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            resized_frame = cv2.resize(frame_tratado, (width, height))
             
            # Converte o quadro redimensionado em uma imagem QImage
            image = QImage(resized_frame.data,width, height,QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # Redimensiona a pixmap para a exibição sem cortar
            pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
            
            self.ui.label_camera.setFixedSize(width, height)
            self.ui.label_camera.setPixmap(pixmap)
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

    # Ajuste de brilho e contraste
    def brilho_contraste(self, imagem, brilho, contraste):
        brilho = (((brilho + 1)-50)/50)*127
        contraste = ((contraste + 1)*2)/100
        # Aplicar a transformação linear de ajuste de brilho e contraste
        imagem_ajustada = cv2.convertScaleAbs(imagem, alpha=contraste, beta=brilho)

        return imagem_ajustada

    # Aplicando super-resolução - ESPCN
    def super_resolucao(self, imagem, path, index):  
        if self.create_control is True:
            self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
            self.sr.readModel(path)
            self.sr.setModel("espcn", index+1)
            self.create_control = False
        
        if imagem.tobytes() in self.frame_cache:
            result = self.frame_cache[imagem.tobytes()]
        else:
            result = self.sr.upsample(imagem)
            self.frame_cache[imagem.tobytes()] = result

        return result

    # Aplicação de equalização por histograma
    def histogram_equalization(self, imagem):
        canal_vermelho, canal_verde, canal_azul= cv2.split(imagem)
        # Aplicar a equalização de histograma a cada canal
        canal_azul_equalizado = cv2.equalizeHist(canal_azul)
        canal_verde_equalizado = cv2.equalizeHist(canal_verde)
        canal_vermelho_equalizado = cv2.equalizeHist(canal_vermelho)
        # Mesclar os canais equalizados para obter a imagem colorida final
        imagem_equalizada = cv2.merge(
            (canal_vermelho_equalizado, canal_verde_equalizado, canal_azul_equalizado))

        return imagem_equalizada

    # Aplicação de filtro passa baixa
    def passa_baixa(self, imagem):
        kernel_size = (5, 5)  # Tamanho do kernel
        filtro_passa_baixa = np.ones(
            kernel_size, dtype=np.float32) / (kernel_size[0] * kernel_size[1])

        # Aplicar o filtro passa-baixa
        imagem_suavizada = cv2.filter2D(imagem, -1, filtro_passa_baixa)

        return imagem_suavizada

    # Aplicação de filtro mediana
    def filtro_mediana(self, imagem):
        # Aplicar o filtro de mediana separadamente a cada canal de cor
        canal_azul = cv2.medianBlur(imagem[:, :, 0], 5)
        canal_verde = cv2.medianBlur(imagem[:, :, 1], 5)
        canal_vermelho = cv2.medianBlur(imagem[:, :, 2], 5)

        # Mesclar os canais para obter a imagem suavizada
        imagem_suavizada_m = cv2.merge(
            (canal_azul, canal_verde, canal_vermelho))

        return imagem_suavizada_m

    #Aplicação de nitidez
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
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
        if self.index != 0 and self.restore_control is False:
            self.create_control = True
            self.selected_option = 'ESPCN/' + self.ui.ui_pages.combobox.currentText()  # Obter a opção selecionada
            self.report(f"{self.data_hora()} / Escala de super resolução mudou para {self.ui.ui_pages.combobox.currentText()}")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
    
    def combobox_modo_selection_changed(self, index):
        self.index_modo = index
        if self.index_modo == 0:
            self.report(f"{self.data_hora()} / Modo de detecção desativada")
        else:
            self.report(f"{self.data_hora()} / Modo de detecção de caixa aberta")

    # Função para retornar o valor do brilho
    def slider_value_changed(self, value):
        self.brilho = value
        self.ui.ui_pages.label.setText(f"Brilho : {(value+1)-50}")
        self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função para retornar o valor do contraste
    def slider_value_changed2(self, value2):
        self.contraste = value2
        self.ui.ui_pages.label2.setText(f"Contraste : {(value2+1)-50}")
        self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função para retornar o valor do botão EH
    def switch_changed(self, switch_value):
        self.switch_value = switch_value
        if switch_value is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Equilização por histograma ativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
        if switch_value is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Equilização por histograma desativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função para retornar o valor do botão FPB
    def switch_changed2(self, switch_value2):
        self.switch_value2 = switch_value2

        if switch_value2 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro passa-baixa ativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
        if switch_value2 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro passa-baixa desativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função para retornar o valor do botão FM
    def switch_changed3(self, switch_value3):
        self.switch_value3 = switch_value3

        if switch_value3 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro por mediana ativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
        if switch_value3 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Filtro por mediana desativado")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função para retornar o valor do botão FM
    def switch_changed4(self, switch_value4):
        self.switch_value4 = switch_value4

        if switch_value4 is True and self.restore_control is False:
            self.report(f"{self.data_hora()} / Nitidez ativada")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)
        if switch_value4 is False and self.restore_control is False:
            self.report(f"{self.data_hora()} / Nitidez desativada")
            self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                self.switch_value2,self.switch_value3,self.switch_value4)

    # Função de tratamento de frame com correção de iluminação e super resolução
    def tratamento_frame(self):
        global frame_tratado
        frame_tratado = self.brilho_contraste(self.frame, self.brilho, self.contraste)
        if self.index != 0 and self.frame is not None:
            frame_tratado = self.super_resolucao(frame_tratado, self.selected_option, self.index)
        if self.switch_value is True and self.frame is not None:
            frame_tratado = self.histogram_equalization(frame_tratado)
        if self.switch_value2 is True and self.frame is not None:
            frame_tratado = self.passa_baixa(frame_tratado)
        if self.switch_value3 is True and self.frame is not None:
            frame_tratado = self.filtro_mediana(frame_tratado)
        if self.switch_value4 is True and self.frame is not None:
            frame_tratado = self.nitidez(frame_tratado)

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

    def exit_application(self, event):
        if self.current_settings != self.settings:
            # Perguntar ao usuário se ele deseja salvar as configurações
            reply = QMessageBox.question(self, "Salvar Configurações", "Deseja salvar as configurações antes de sair?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.saveSettings()
                if self.control_save is True:
                    QApplication.quit()
            elif reply == QMessageBox.No:
                QApplication.quit()
            else:
                pass  # O usuário cancelou, não faz nada
        else:
            QApplication.quit()
    
    def closeEvent(self, event):
        if self.current_settings != self.settings:
            # Perguntar ao usuário se ele deseja salvar as configurações
            reply = QMessageBox.question(self, "Salvar Configurações", "Deseja salvar as configurações antes de sair?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.saveSettings()
                event.ignore()
                if self.control_save is True:
                   event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()  # O usuário cancelou, não faz nada
        else:
            event.accept()
  
    # Função para salvar um frame da imagem
    def save_image(self):
        if self.camera_ativa == True:
            cv2.rectangle(frame_tratado, self.box, (0, 255, 0), 2)
            cv2.putText(frame_tratado, self.label, (self.box[0], self.box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            self.frame_rgb = cv2.cvtColor(frame_tratado, cv2.COLOR_BGR2RGB)
            # Solicitar ao usuário um local e nome de arquivo para salvar a imagem
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)")

            # Salvar a imagem capturada como arquivo PNG usando o OpenCV
            if file_path:
                cv2.imwrite(file_path, self.frame_rgb)

        else:
            QMessageBox.warning(None, "sem frame", "A câmera não está ativa.")
    
    # Restaura as configurações padrões
    def restore_defaults(self):
        self.restore_control = True

        self.ui.ui_pages.slider.setValue(self.default_settings.getint('Configuracoes', 'brilho'))
        self.ui.ui_pages.slider2.setValue(self.default_settings.getint('Configuracoes', 'contraste'))
        self.ui.ui_pages.combobox.setCurrentIndex(self.default_settings.getint('Configuracoes', 'index'))
        self.ui.ui_pages.switch.setChecked(self.default_settings.getboolean('Configuracoes', 'switch_value'))
        self.switch_value = self.default_settings.getboolean('Configuracoes', 'switch_value')
        self.ui.ui_pages.switch2.setChecked(self.default_settings.getboolean('Configuracoes', 'switch_value2'))
        self.switch_value2 = self.default_settings.getboolean('Configuracoes', 'switch_value2')
        self.ui.ui_pages.switch3.setChecked(self.default_settings.getboolean('Configuracoes', 'switch_value3'))
        self.switch_value3 = self.default_settings.getboolean('Configuracoes', 'switch_value3')
        self.ui.ui_pages.switch4.setChecked(self.default_settings.getboolean('Configuracoes', 'switch_value4'))
        self.switch_value4 = self.default_settings.getboolean('Configuracoes', 'switch_value4')
        
        QMessageBox.information(None, "Restaurar configuração", "Restaurado com sucesso")
        self.report(f"{self.data_hora()} / Configurações restauradas")
        self.restore_control = False
    
    #Salva as configurações
    def saveSettings(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Configurações", "", "Arquivos de Configuração (*.ini);;Todos os Arquivos (*)")

        if file_name:
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
            # Salvar as configurações em um arquivo
            with open(file_name, 'w') as configfile:
                self.settings.write(configfile)
            #QMessageBox.information(None, "Informação", "Configurações salvas com sucesso.")
            self.control_save = True
            self.report(f"{self.data_hora()} / Configurações Salvas")

    #Carrega as configurações        
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

                self.updateSettings(self.brilho,self.contraste,self.index, self.switch_value, 
                                    self.switch_value2,self.switch_value3,self.switch_value4)
                self.report(f"{self.data_hora()} / Configurações carregadas")

            except FileNotFoundError:
                QMessageBox.warning(None, "Aviso", "O arquivo de configuração não foi encontrado.")
    
    #Atualiza a mudança de configurações
    def updateSettings(self, brilho, contraste, index, switch_value, 
                       switch_value2, switch_value3, switch_value4):
        str_brilho = str(brilho)
        str_contraste = str(contraste)
        str_index = str(index)
        str_switch_value = str(switch_value)
        str_switch_value2 = str(switch_value2)
        str_switch_value3 = str(switch_value3)
        str_switch_value4 = str(switch_value4)

        # Configurações personalizadas
        self.current_settings['Configuracoes'] = {
            'brilho': str_brilho,
            'contraste': str_contraste,
            'index': str_index,
            'switch_value': str_switch_value,
            'switch_value2': str_switch_value2,
            'switch_value3': str_switch_value3,
            'switch_value4': str_switch_value4,
        }

    #Abrir nova janela para selecionar região da câmera
    def frame_cam(self):
        if self.frame is None:
            global control_cam
            control_cam = True
            nova_janela = Frame_Cam()
            nova_janela.show()
        else:
            QMessageBox.warning(None, "Desative a Câmera", "Desative a câmera primeiro.")
    
    #Restaura a região do frame para tamanho original
    def frame_cam_restore(self):
        global x1_cam
        x1_cam = None

    #Detecção usando YoloV4
    def yolo(self):
        global frame_tratado
        if frame_tratado is not None:
            if self.index_modo == 0:
               pass

            if self.index_modo == 1:
                classes, scores, boxes = self.model_caixa_aberta.detect(frame_tratado, 0.1, 0.2)
                if len(boxes) > 0:  # Verifica se há caixas detectadas
                    for (classid, score, box) in zip(classes, scores, boxes):
                        self.label = f"Caixa aberta: {score:.2f}"
                        self.box = box
                        if self.control_detection is True:
                            self.report(f"{self.data_hora()} / Caixa aberta detectada")
                            self.control_detection = False
                else:
                    # Se nenhuma caixa foi detectada, defina self.box como vazio
                    self.box = []
                    self.control_detection = True

# Inicilização da IDE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())