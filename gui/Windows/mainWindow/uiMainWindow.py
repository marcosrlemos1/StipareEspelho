from library import *
from gui.Widgest.pushButton import PyPushButton
from gui.pages.uiPages import Ui_StackedWidget

#IMPORT CUSTOM WIDGETS
class UI_MainWindow(object):
    def setupUi(self,parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        #SET INITIAL PARAMETERS
        parent.resize(480,360)
        
        #CREATE CENTRAL WIDGET
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("background-color: #313338")
        parent.setCentralWidget(self.centralWidget)
        
        #CREATE MAIN_LAYOUT
        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        
        #CREATE LEFT MENU
        self.leftMenu = QFrame()
        self.leftMenu.setStyleSheet("background-color:#1E1F22; border: 0.50px black solid")
        self.leftMenu.setMaximumWidth(50)
        self.leftMenu.setMinimumWidth(50)
        self.mainLayout.addWidget(self.leftMenu)

        #LEFT MENU LAYOUT
        self.leftMenuLayout =QVBoxLayout(self.leftMenu)
        self.leftMenuLayout.setContentsMargins(0,0,0,0)
        self.leftMenuLayout.setSpacing(0)

        #FRAME TO LEFT MENU
        self.leftMenuTopFrame = QFrame()
        self.leftMenuTopFrame.setStyleSheet("border-radius: 25px;")
        self.leftMenuTopFrame.setMinimumHeight(50)
        self.leftMenuLayout.addWidget(self.leftMenuTopFrame)

        #LAYOUT TO TOP FRAME
        self.leftMenuTopFrameLayout = QVBoxLayout(self.leftMenuTopFrame)
        self.leftMenuTopFrameLayout.setContentsMargins(0,0,0,0)
        self.leftMenuTopFrameLayout.setSpacing(0)

        #BUTTON TO TOP_FRAME
        self.toggle = PyPushButton(
            text="",
            btnColor= "#1E1F22", 
            heigh=50,
            borderRadius=25,
            btnPressed="red",
            )
        self.pixmap = QPixmap(r"GUI\Imagens\icons\icon_camera.png")
        self.toggle.setIcon(self.pixmap)
        self.toggle.setIconSize(self.pixmap.rect().size()/3)
        self.leftMenuTopFrameLayout.addWidget(self.toggle)
        
        #LEFT MENU SPACING
        self.leftMenuSpacing =QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.leftMenuLayout.addItem(self.leftMenuSpacing)

        #FRAME TO LEFT MENU
        self.leftMenuBottomFrame = QFrame()
        self.leftMenuBottomFrame.setMinimumHeight(50)
        self.leftMenuLayout.addWidget(self.leftMenuBottomFrame)

        #FRAME TO BOTTOM FRAME
        self.leftmenuBottomFrameLayout = QVBoxLayout(self.leftMenuBottomFrame)
        self.leftmenuBottomFrameLayout.setContentsMargins(0,0,0,0)
        self.leftmenuBottomFrameLayout.setSpacing(0)

        #CREATE CONTENT
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #313338")
        self.mainLayout.addWidget(self.content)

        #CREATE CONTENT_LAYOUT
        self.contentLayout =QVBoxLayout(self.content)
        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentLayout.setSpacing(0)

        #CREATE TOOLBAR
        self.toolbar = QFrame()
        self.toolbar.setMaximumHeight(30)
        self.toolbar.setMinimumHeight(30)
        self.toolbar.setStyleSheet("background-color:#2B2D31; border: 0.50px solid black; color:white")
        self.contentLayout.addWidget(self.toolbar)

        #CREATE LAYOUT TO TOOLBAR
        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setContentsMargins(0,0,0,0)
        self.toolbarLayout.setSpacing(0)

        #CREATE BUTTON FILE
        self.file = PyPushButton("Arquivos", heigh=25, width=55, borderRadius=4)
        self.toolbarLayout.addWidget(self.file)
        
        #CREATE BUTTON EDIT
        self.edit = PyPushButton("Editar", heigh=25, width=45, borderRadius=4)
        self.toolbarLayout.addWidget(self.edit)

        #CREATE SPACE TO TOOLBAR
        self.toolSpace =QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toolbarLayout.addItem(self.toolSpace)

        self.menuOne = QMenu(parent)
        self.menuOne.setStyleSheet("""
            QMenu {
                background-color: #1E1F22; /* Cor de fundo */
                color: #FFF; /* Cor do texto */
                border: 1px solid #555; /* Borda */
                border-radius: 4px; /* Raio da borda */
            }


            QMenu::item {
                padding: 5px 15px; /* Espaçamento interno */
            }

            QMenu::item:selected {
                background-color: #04395E; /* Cor de fundo do item selecionado */
            }
        """)

        self.menuTwo = QMenu(parent)
        self.menuTwo.setStyleSheet("""
            QMenu {
                background-color: #1E1F22; /* Cor de fundo */
                color: #FFF; /* Cor do texto */
                border: 1px solid #555; /* Borda */
                border-radius: 4px; /* Raio da borda */
            }


            QMenu::item {
                padding: 5px 15px; /* Espaçamento interno */
            }

            QMenu::item:selected {
                background-color: #04395E; /* Cor de fundo do item selecionado */
            }
        """)

        self.actionSaveImage = QAction("Salvar Imagem")
        self.actionSaveLog = QAction("Salvar Log")
        self.actionSaveSettings = QAction("Salvar Configurações")
        self.actionLoadSettings = QAction("Carregar Configurações")
        self.actionExit = QAction("Sair")

        self.menuOne.addAction(self.actionSaveImage)
        self.menuOne.addAction(self.actionSaveLog)
        self.menuOne.addAction(self.actionSaveSettings)
        self.menuOne.addAction(self.actionLoadSettings)
        self.menuOne.addAction(self.actionExit)

        self.actionResetSettings = QAction('Resetar Configurações')
        self.actionFrame = QAction('Selecionar Região')
        self.actionResetFrame = QAction('Restaurar Frame')
        
        self.menuTwo.addAction(self.actionResetSettings)
        self.menuTwo.addAction(self.actionFrame)
        self.menuTwo.addAction(self.actionResetFrame)

        self.file.setMenu(self.menuOne)
        self.file.setStyleSheet('''
            QPushButton {
                background-color: #2B2D31;
                color: #FFF;
                border: None; 
                border-radius: 4px; 
                padding: 10px 20px; 
                width: 120px; 
            }
            QPushButton::menu-indicator {
                image: none; 
                width: 0px; 
            }
            QPushButton:hover {
                background-color: #3E4145;
            }
            QPushButton:pressed {
                background-color: #1E2022; 
            }
        ''')

        self.edit.setMenu(self.menuTwo)
        self.edit.setStyleSheet('''
            QPushButton {
                background-color: #2B2D31;
                color: #FFF;
                border: None; 
                border-radius: 4px; 
                padding: 10px 20px; 
                width: 120px; 
            }
            QPushButton::menu-indicator {
                image: none; 
                width: 0px; 
            }
            QPushButton:hover {
                background-color: #3E4145;
            }
            QPushButton:pressed {
                background-color: #1E2022; 
            }
        ''')

        #CREATE APPLICATION PAGES
        self.page = QFrame()
        self.page.setStyleSheet("background-color:#313338")
        self.contentLayout.addWidget(self.page)

        #CREATE LAYOUT TO PAGES
        self.pageLayout = QHBoxLayout(self.page)
        self.pageLayout.setContentsMargins(0,0,0,0)

        #CREATE SIDE MENU
        self.side = QFrame()
        self.side.setStyleSheet("background-color:#2B2D31; border: 0.50px solid black; color:white")
        self.side.setMaximumWidth(204)
        self.side.setMinimumWidth(204)
        self.pageLayout.addWidget(self.side)

        #CREATE LAYOUT TO SIDE MENU
        self.sideLayout = QVBoxLayout(self.side)

        self.pages = QStackedWidget()
        self.pages.setStyleSheet("border: none")
        self.uiPages = Ui_StackedWidget()
        self.uiPages.setupUi(self.pages)
        self.sideLayout.addWidget(self.pages)

        #CREATE EXHIBITION AREA
        self.exhibition = QFrame()
        self.exhibition.setStyleSheet("background-color:#313338")
        self.pageLayout.addWidget(self.exhibition)

        #CREATE LAYOUT TO EXHIBITION AREA
        self.exhibitionLayout = QVBoxLayout(self.exhibition)
        self.exhibitionLayout.setContentsMargins(30,30,30,5)
        self.exhibitionLayout.setSpacing(20)

        #CREATE FRAMES TO EXHBITION AREA
        self.frameCamera = QFrame()
        self.frameCamera.setStyleSheet("background-color:black")
        self.exhibitionLayout.addWidget(self.frameCamera)

        self.frameCameraLayout = QHBoxLayout(self.frameCamera)
        self.frameCameraLayout.setContentsMargins(0,0,0,0)
        self.frameCameraLayout.setSpacing(0)

        self.frameCameraLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        self.labelCamera = QLabel()
        self.labelCamera.setStyleSheet('background-color: Red')
        self.labelCamera.setMinimumWidth(100)
        self.frameCameraLayout.addWidget(self.labelCamera)

        self.frameCameraLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        #CREATE PROMPT FOR EXHIBITION AREA
        self.prompt = QFrame()
        self.prompt.setMinimumHeight(150)
        self.prompt.setMaximumHeight(150)
        self.prompt.setStyleSheet("background-color: #181818")
        self.exhibitionLayout.addWidget(self.prompt)

        #LAYOUT PROMPT
        self.promptLayout = QVBoxLayout(self.prompt)
        self.promptLayout.setContentsMargins(15,0,15,15)
        self.promptLayout.setSpacing(10)

        #LABEL PROMPT
        self.labelPrompt = QLabel("TERMINAL")
        self.labelPrompt.setMinimumHeight(20)
        self.labelPrompt.setStyleSheet("color:white; border-bottom: 2px solid white;")
        self.promptLayout.addWidget(self.labelPrompt)

        self.textEdit = QTextEdit()
        self.promptLayout.addWidget(self.textEdit)
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet("font-family: Courier; color: white; border: None")

        #CREATE STATUSBAR
        self.statusBar = QFrame()
        self.statusBar.setMaximumHeight(20)
        self.statusBar.setMinimumHeight(20)
        self.statusBar.setStyleSheet("background-color:#2B2D31; border: 1px solid black; color:white")
        self.contentLayout.addWidget(self.statusBar)

        #CREATE LAYOUT TO STATUSBAR
        self.statusBarLayout = QHBoxLayout(self.statusBar)
        self.statusBarLayout.setContentsMargins(0,0,0,0)
        self.statusBarLayout.setSpacing(0)  

        #CREATE LABEL TO STATUS BAR
        self.labelStatus = QLabel("xx/xx/xxxx as xx:xx")
        self.labelStatus.setStyleSheet("border: none;")

        #CREATE SPACE TO STATUSBAR
        self.statusSpace =QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toolbarLayout.addItem(self.statusSpace)

        #ADD STATUS_SPACE AND label_status
        self.statusBarLayout.addItem(self.statusSpace)
        self.statusBarLayout.addWidget(self.labelStatus)