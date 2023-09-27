#IMPORT QT_CORE

from qt_core import *

#IMPORT CUSTOM WIDGETS
from gui.widgest.py_push_button import PyPushButton
from gui.widgest.py_Slider import PySlider
from gui.pages.ui_pages import Ui_StackedWidget


class UI_MainWindow(object):
    def setup_ui(self,parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")


        #SET INITIAL PARAMETERS
        parent.resize(480,360)
        
        #CREATE CENTRAL WIDGET
        self.central_widget = QFrame()
        self.central_widget.setStyleSheet("background-color: #313338")
        parent.setCentralWidget(self.central_widget)
        

        #CREATE MAIN_LAYOUT
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
        #CREATE LEFT MENU
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color:#1E1F22; border: 0.50px black solid")
        self.left_menu.setMaximumWidth(50)
        self.left_menu.setMinimumWidth(50)
        self.main_layout.addWidget(self.left_menu)

        #LEFT MENU LAYOUT
        self.left_menu_layout =QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0,0,0,0)
        self.left_menu_layout.setSpacing(0)


        #FRAME TO LEFT MENU
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setStyleSheet("border-radius: 25px;")
        self.left_menu_top_frame.setMinimumHeight(50)
        self.left_menu_layout.addWidget(self.left_menu_top_frame)

        #LAYOUT TO TOP FRAME
        self.left_menu_top_frame_layout =QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_frame_layout.setContentsMargins(0,0,0,0)
        self.left_menu_top_frame_layout.setSpacing(0)

        #BUTTON TO TOP_FRAME
        self.toggle = PyPushButton(
            text="",
            btn_color= "#1E1F22", 
            heigh=50,
            border_radius=25,
            btn_pressed="red",
            )
        self.pixmap = QPixmap(r"gui\imagens\icons\icon_camera.png")
        self.toggle.setIcon(self.pixmap)
        self.toggle.setIconSize(self.pixmap.rect().size()/3)
        self.left_menu_top_frame_layout.addWidget(self.toggle)
        

        #LEFT MENU SPACING
        self.left_menu_spacing =QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.left_menu_layout.addItem(self.left_menu_spacing)


        #FRAME TO LEFT MENU
        self.left_menu_bottom_frame = QFrame()
        self.left_menu_bottom_frame.setMinimumHeight(50)
        self.left_menu_layout.addWidget(self.left_menu_bottom_frame)

        #FRAME TO BOTTOM FRAME
        self.left_menu_bottom_frame_layout = QVBoxLayout(self.left_menu_bottom_frame)
        self.left_menu_bottom_frame_layout.setContentsMargins(0,0,0,0)
        self.left_menu_bottom_frame_layout.setSpacing(0)

        #CREATE BUTTOM TO BOTTOM FRAME
        self.toggle2 =PyPushButton("",
                                   btn_color="#1E1F22",
                                   heigh=50,
                                   border_radius=25)
        self.pixmap2 = QPixmap(r"gui\imagens\icons\icon_gear.png")
        self.toggle2.setIcon(self.pixmap2)
        self.toggle2.setIconSize(self.pixmap2.rect().size()/3)
        self.left_menu_bottom_frame_layout.addWidget(self.toggle2)


        #CREATE CONTENT
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #313338")
        self.main_layout.addWidget(self.content)

        #CREATE CONTENT_LAYOUT
        self.content_layout =QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)


        #CREATE TOOLBAR
        self.toolbar = QFrame()
        self.toolbar.setMaximumHeight(30)
        self.toolbar.setMinimumHeight(30)
        self.toolbar.setStyleSheet("background-color:#2B2D31; border: 0.50px solid black; color:white")
        self.content_layout.addWidget(self.toolbar)

        #CREATE LAYOUT TO TOOLBAR
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(0,0,0,0)
        self.toolbar_layout.setSpacing(0)


        #CREATE BUTTON FILE
        self.file = PyPushButton("FILES", heigh=25, width=55, border_radius=4)
        self.toolbar_layout.addWidget(self.file)
        

        #CREATE BUTTON EDIT
        self.edit = PyPushButton("EDIT", heigh=25, width=45, border_radius=4)
        self.toolbar_layout.addWidget(self.edit)

        #CREATE BUTTON HELP
        self.help = PyPushButton("HELP", heigh=25, width=45, border_radius=4)
        self.toolbar_layout.addWidget(self.help)


        #CREATE SPACE TO TOOLBAR
        self.tool_space =QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toolbar_layout.addItem(self.tool_space)




        self.menu1 = QMenu(parent)
        self.menu1.setStyleSheet("""
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


        self.action1 = QAction("Save image")
        self.action2 = QAction("Exit")

        self.menu1.addAction(self.action1)
        self.menu1.addAction(self.action2)


        self.file.setMenu(self.menu1)
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





        #CREATE APPLICATION PAGES
        self.page = QFrame()
        self.page.setStyleSheet("background-color:#313338")
        self.content_layout.addWidget(self.page)

        #CREATE LAYOUT TO PAGES
        self.page_layout = QHBoxLayout(self.page)
        self.page_layout.setContentsMargins(0,0,0,0)

        #CREATE SIDE MENU
        self.side = QFrame()
        self.side.setStyleSheet("background-color:#2B2D31; border: 0.50px solid black; color:white")
        self.side.setMaximumWidth(180)
        self.side.setMinimumWidth(180)
        self.page_layout.addWidget(self.side)

        #CREATE LAYOUT TO SIDE MENU
        self.side_layout = QVBoxLayout(self.side)


        self.paginas = QStackedWidget()
        self.paginas.setStyleSheet("border: none")
        self.ui_pages = Ui_StackedWidget()
        self.ui_pages.setupUi(self.paginas)

        #
        self.side_layout.addWidget(self.paginas)



        #CREATE EXHIBITION AREA

        self.exhibition = QFrame()
        self.exhibition.setStyleSheet("background-color:#313338")
        self.page_layout.addWidget(self.exhibition)

        #CREATE LAYOUT TO EXHIBITION AREA
        self.exhibition_layout = QVBoxLayout(self.exhibition)
        self.exhibition_layout.setContentsMargins(30,30,30,5)
        self.exhibition_layout.setSpacing(20)

        #CREATE FRAMES TO EXHBITION AREA

        self.frame_camera = QFrame()
        self.frame_camera.setStyleSheet("background-color:black")
        self.exhibition_layout.addWidget(self.frame_camera)

        self.frame_camera_layout = QHBoxLayout(self.frame_camera)
        self.frame_camera_layout.setContentsMargins(0,0,0,0)
        self.frame_camera_layout.setSpacing(0)

        self.frame_camera_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        self.label_camera = QLabel()
        self.label_camera.setStyleSheet('background-color: Red')
        self.label_camera.setMinimumWidth(100)
        self.frame_camera_layout.addWidget(self.label_camera)

        self.frame_camera_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        #CREATE PROMPT FOR EXHIBITION AREA

        self.prompt = QFrame()
        self.prompt.setMinimumHeight(150)
        self.prompt.setMaximumHeight(150)
        self.prompt.setStyleSheet("background-color: #181818")
        self.exhibition_layout.addWidget(self.prompt)

        #LAYOUT PROMPT

        self.prompt_layout = QVBoxLayout(self.prompt)
        self.prompt_layout.setContentsMargins(15,0,15,15)
        self.prompt_layout.setSpacing(10)

        #Label

        self.label_prompt = QLabel("TERMINAL")
        self.label_prompt.setMinimumHeight(20)
        self.label_prompt.setStyleSheet("color:white; border-bottom: 2px solid white;")
        self.prompt_layout.addWidget(self.label_prompt)


        self.text_edit = QTextEdit()
        self.prompt_layout.addWidget(self.text_edit)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("font-family: Courier; color: white; border: None")

        #CREATE STATUSBAR
        self.statusbar = QFrame()
        self.statusbar.setMaximumHeight(20)
        self.statusbar.setMinimumHeight(20)
        self.statusbar.setStyleSheet("background-color:#2B2D31; border: 1px solid black; color:white")
        self.content_layout.addWidget(self.statusbar)

        #CREATE LAYOUT TO STATUSBAR

        self.statusbar_layout = QHBoxLayout(self.statusbar)
        self.statusbar_layout.setContentsMargins(0,0,0,0)
        self.statusbar_layout.setSpacing(0)  

        #CREATE LABEL TO STATUS BAR

        self.label_status = QLabel("xx/xx/xxxx as xx:xx")
        self.label_status.setStyleSheet("border: none;")


        #CREATE SPACE TO STATUSBAR
        self.status_space =QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toolbar_layout.addItem(self.status_space)

        #ADD STATUS_SPACE AND label_status

        self.statusbar_layout.addItem(self.status_space)
        self.statusbar_layout.addWidget(self.label_status)
