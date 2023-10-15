import os, sys, sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import deskpy_pdf
os.system('cls')

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_ui()
        self.page()
        self.bbdd()
        self.show()

    def start_ui(self):
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)))
        self.setWindowTitle('DeskPy')
        self.setMinimumWidth(900)
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        tb_help = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)), 'Ayuda', self)
        tb_info = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)), 'Información general', self)
        tb_save = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)), 'Guardar configuración', self)
        tb_proc = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)), 'Abrir carpeta de procesados', self)
        tb_help.triggered.connect(self.show_help)
        tb_info.triggered.connect(self.show_info)
        tb_proc.triggered.connect(self.go_to_folder)
        tb_save.triggered.connect(self.update_bbdd)
        toolbar.addAction(tb_help)
        toolbar.addSeparator()
        toolbar.addAction(tb_info)
        toolbar.addSeparator()
        toolbar.addAction(tb_save)
        toolbar.addSeparator()
        toolbar.addAction(tb_proc)
        tb_help.setShortcuts(['Ctrl+H','F1'])
        tb_info.setShortcuts(['Ctrl+I','F2'])
        tb_save.setShortcuts(['Ctrl+S','F3'])
        tb_proc.setShortcuts(['Ctrl+A','F4'])
        status = QStatusBar()
        self.setStatusBar(status)
        self.processing_type = QLabel('Generar solo identificación y CIC')
        self.processing_type.setStyleSheet('padding: 3px 5px; color: #DDE;')
        self.processing_type.setFixedWidth(230)
        self.processing_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.addWidget(self.processing_type)
        status.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        status.setMinimumWidth(900)
        status.setStyleSheet("QStatusBar::item {border: none;}")

    def page(self):
        self.widget = QWidget()
        wlayout = QVBoxLayout()
        self.widget.setLayout(wlayout)
        self.setCentralWidget(self.widget)
        h1 = QLabel('DeskPy')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('padding: 15px; margin-bottom: 10px; background: #303040; color: #FFF; border: 3px ridge #222; border-radius: 5px; font-size: 16px; font-weight: 600;')
        h1.setMaximumHeight(100)
        wlayout.addWidget(h1)
        self.cpu_mode = QCheckBox('Generar todos los documentos')
        self.are_scan = QCheckBox('Documentos escaneados')
        self.cpu_mode.setCursor(Qt.CursorShape.PointingHandCursor)
        self.are_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cpu_mode.setStyleSheet('color: #777;')
        self.cpu_mode.setMaximumWidth(185)
        self.cpu_mode.clicked.connect(self.cpu_mode_2)
        self.are_scan.setDisabled(True)
        cpu_hbox = QVBoxLayout()
        cpu_hbox.addWidget(self.cpu_mode)
        cpu_hbox.addWidget(self.are_scan)
        cpu_hbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        wlayout.addLayout(cpu_hbox)
        wlayout.setContentsMargins(20,20,20,20)
        path_1_label = QLabel('Buscar los documentos en:')
        path_1_label.setStyleSheet('color: #888; margin-top: 15px;')
        self.path_1 = QLabel('N/A')
        self.path_1.setStyleSheet('background: #FFF; padding: 0px 10px; border: 4px groove #DDD; border-radius: 5px;')
        self.switch_p1 = QPushButton('Cambiar')
        self.switch_p1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_p1.setShortcut('Ctrl+B')
        self.switch_p1.setMaximumWidth(100)
        self.switch_p1.setStyleSheet('padding: 10px 0px;')
        wrap_p1 = QHBoxLayout()
        wrap_p1.addWidget(self.path_1)
        wrap_p1.addWidget(self.switch_p1)
        path_2_label = QLabel('Guardar los documentos en:')
        path_2_label.setStyleSheet('color: #888; margin-top: 10px;')
        self.path_2 = QLabel('N/A')
        self.path_2.setStyleSheet('background: #FFF; padding: 0px 10px; border: 4px groove #DDD; border-radius: 5px;')
        self.switch_p2 = QPushButton('Cambiar')
        self.switch_p2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_p2.setShortcut('Shift+B')
        self.switch_p2.setMaximumWidth(100)
        self.switch_p2.setStyleSheet('padding: 10px 0px;')
        wrap_p2 = QHBoxLayout()
        wrap_p2.addWidget(self.path_2)
        wrap_p2.addWidget(self.switch_p2)
        self.l_ident = QLineEdit()
        self.l_fname = QLineEdit()
        self.l_kycdt = QLineEdit()
        self.l_ident.setMaximumWidth(170)
        self.l_kycdt.setMaximumWidth(170)
        self.l_ident.setPlaceholderText('Identificación')
        self.l_fname.setPlaceholderText('Apellidos y nombre')
        self.l_kycdt.setPlaceholderText('Fechado KYC')
        self.l_ident.setDisabled(True)
        self.l_fname.setDisabled(True)
        self.l_kycdt.setDisabled(True)
        self.l_ident_act = QCheckBox()
        self.l_fname_act = QCheckBox()
        self.l_kycdt_act = QCheckBox()
        self.l_ident_act.setCursor(Qt.CursorShape.PointingHandCursor)
        self.l_fname_act.setCursor(Qt.CursorShape.PointingHandCursor)
        self.l_kycdt_act.setCursor(Qt.CursorShape.PointingHandCursor)
        self.l_fname_act.setStyleSheet('padding-left: 20px;')
        self.l_kycdt_act.setStyleSheet('padding-left: 20px;')
        self.l_ident_act.clicked.connect(self.enablefield_ident)
        self.l_fname_act.clicked.connect(self.enablefield_fname)
        self.l_kycdt_act.clicked.connect(self.enablefield_kycdt)
        customer_info = QHBoxLayout()
        customer_info.addWidget(self.l_ident_act)
        customer_info.addWidget(self.l_ident)
        customer_info.addWidget(self.l_fname_act)
        customer_info.addWidget(self.l_fname)
        customer_info.addWidget(self.l_kycdt_act)
        customer_info.addWidget(self.l_kycdt)
        onlyread = QPushButton('Leer')
        onlyread.setCursor(Qt.CursorShape.PointingHandCursor)
        onlyread.setStyleSheet('padding: 15px; font-size: 15px;')
        onlyread.clicked.connect(self.pre_run_app)
        onlyread.setShortcut('Ctrl+Space')
        launch = QPushButton('Procesar')
        launch.setCursor(Qt.CursorShape.PointingHandCursor)
        launch.setStyleSheet('padding: 15px; font-size: 15px;')
        # launch.clicked.connect(self.run_app)
        launch.clicked.connect(self.testing)

        launch.setShortcut('Ctrl+Return')
        triggerswrapper = QHBoxLayout()
        triggerswrapper.addWidget(onlyread)
        triggerswrapper.addWidget(launch)
        self.page_wrapper = QVBoxLayout()
        self.page_wrapper.addWidget(path_1_label)
        self.page_wrapper.addLayout(wrap_p1)
        self.page_wrapper.addWidget(path_2_label)
        self.page_wrapper.addLayout(wrap_p2)
        wrap_p2.setContentsMargins(0,0,0,15)
        l = QLabel('Renombrar los documentos con los datos del cliente:')
        l.setStyleSheet('color: #888;')
        self.page_wrapper.addWidget(l)
        self.page_wrapper.addLayout(customer_info)
        self.page_wrapper.addLayout(triggerswrapper)
        wlayout.addLayout(self.page_wrapper)
        self.page_wrapper.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.switch_p1.clicked.connect(self._load)
        self.switch_p2.clicked.connect(self._save)
        self.page_wrapper.addStretch()

    def go_to_folder(self):
        try: os.startfile(self.path_2.text())
        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)

    def cpu_mode_2(self):
        if self.cpu_mode.isChecked():
            self.cpu_mode.setStyleSheet('color: #000;')
            self.processing_type.setText('Generar todos los documentos')
        else:
            self.cpu_mode.setStyleSheet('color: #777;')
            self.processing_type.setText('Generar solo identificación y CIC')

    def _filedialog(self):
        self.filedialog = QFileDialog.getExistingDirectory()
        self.filedialog += '/'
        if self.filedialog == '/': self.filedialog = 'N/A'

    def _load(self):
        self._filedialog()
        self.path_1.setText(self.filedialog.replace('\\','/'))

    def _save(self):
        self._filedialog()
        self.path_2.setText(self.filedialog.replace('\\','/'))

    def enablefield_ident(self):
        if self.l_ident_act.isChecked(): self.l_ident.setDisabled(False)
        else: self.l_ident.setDisabled(True)

    def enablefield_fname(self):
        if self.l_fname_act.isChecked(): self.l_fname.setDisabled(False)
        else: self.l_fname.setDisabled(True)

    def enablefield_kycdt(self):
        if self.l_kycdt_act.isChecked(): self.l_kycdt.setDisabled(False)
        else: self.l_kycdt.setDisabled(True)

    def pre_run_app(self):
        deskpy_pdf.PDF.constructor(self, self.path_1, self.path_2, [0], self.cpu_mode, self.l_ident_act, self.l_fname_act, self.l_kycdt_act)
        try:
            deskpy_pdf.PDF.pdf_text(self)
            if self.is_doc_kyc[0]:
                self.l_ident.setText(self.is_doc_kyc[2][0])
                self.l_fname.setText(self.is_doc_kyc[2][1])
                self.l_kycdt.setText(self.is_doc_kyc[2][2])
                self.deploy_msg()
            elif self.is_doc_cic[0]:
                self.l_ident.setText(self.is_doc_cic[2][0])
                self.l_fname.setText(self.is_doc_cic[2][1])
                self.deploy_msg()
        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)

    def run_app(self):
        deskpy_pdf.PDF.constructor(self, self.path_1, self.path_2, [0], self.cpu_mode, self.l_ident_act, self.l_fname_act, self.l_kycdt_act)
        try:
            if self.is_doc_kyc[0] or self.is_doc_cic[0]:
                try:
                    deskpy_pdf.PDF.pdf_from_img(self)
                    try:
                        deskpy_pdf.PDF.pdf_merge(self)
                        try:
                            deskpy_pdf.PDF.run_wizzard(self)
                            self.deploy_msg()
                        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
                    except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
                except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)

    def deploy_msg(self):
        try: self.msg.deleteLater()
        except: pass
        self.msg = QLabel()
        self.msg.setStyleSheet('margin: 10px 0; padding: 15px; color: #556; background: #DDE; border: 3px groove #AAB; border-radius: 5px; font-size: 14px;')
        self.page_wrapper.addWidget(self.msg)
        if self.sender().text() == 'Leer':
            self.msg.setText('Listo para procesar.')
        elif self.sender().text() == 'Procesar':
            self.msg.setText(f'Expediente "{self.l_ident.text()} {self.l_fname.text()}" procesado correctamente.')
            self.l_ident.setText('')
            self.l_fname.setText('')
            self.l_kycdt.setText('')

    def show_help(self):
        dlg = QDialog(self)
        dlg.setMaximumWidth(1080)
        dlg.setWindowTitle('PyDesk - Ayuda')
        self.dlg_layout = QVBoxLayout()
        dlg.setLayout(self.dlg_layout)
        h1 = QLabel('DeskPy - Ayuda')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('padding: 15px; margin-bottom: 10px; background: #303040; color: #FFF; border: 3px ridge #222; border-radius: 5px; font-size: 16px; font-weight: 600;')
        self.dlg_layout.addWidget(h1)
        self.entry('h1','1] Barra de herramientas')
        self.entry('h2','1.1] Guardar configuración actual')
        self.entry('p','Esta función permite a los usuarios guardar las configuraciones de la aplicación para poder iniciarla posteriormente con las mismas preferencias.')
        self.entry('h2','1.2] Abrir carpeta de "procesados"')
        self.entry('p','Inicia automáticamente el explorador de archivos en la carpeta de trabajo especificada para guardar los documentos procesados.')
        self.entry('h1','2] Casilla "Generar todos los documentos"')
        self.entry('p','De forma predeterminada, la aplicación solo genera la autorización CIC y procesa la identificación (ID). Sin embargo, al seleccionar esta casilla, la aplicación\ngenerará automáticamente otros documentos presentes en el documento de origen, incluyendo CIC, CICAC, KYC, declaración jurada y el consentimiento informado.')
        self.entry('h1','3] Sección: Configuración de rutas')
        self.entry('p','Para habilitar el funcionamiento adecuado de la aplicación, requiere establecer las rutas de entrada y salida de documentos. Estas rutas determinan las ubicaciones\nde los archivos de origen que se procesarán y dónde se guardarán los documentos resultantes.')
        self.entry('h1','4] Sección "Renombrar los documentos con los datos del cliente"')
        self.entry('p','La aplicación realiza la lectura de los documentos de origen y efectúa una recopilación de datos para obtener de manera automática los campos correspondientes.\nEl usuario tiene la opción de habilitar o deshabilitar estos campos según su preferencia, lo que le permite el control sobre el proceso de renombramiento de los\ndocumentos generados.')
        self.entry('h1','5] Botones de acción')
        self.entry('p','Con todas las configuraciones debidamente seleccionadas, el usuario debe activar la función "Leer" para el proceso de validación de datos en la interfaz, en caso\nde que requiera modificar o corregir algún dato, luego, para iniciar la ejecución del programa y proceder con el procesamiento de los documentos, debe\nseleccionar la opción "Procesar".')
        dlg.exec()

    def show_info(self):
        dlg = QDialog(self)
        dlg.setMaximumWidth(1080)
        dlg.setWindowTitle('PyDesk - Información')
        self.dlg_layout = QVBoxLayout()
        dlg.setLayout(self.dlg_layout)
        h1 = QLabel('DeskPy - Información general')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('padding: 15px; margin-bottom: 10px; background: #303040; color: #FFF; border: 3px ridge #222; border-radius: 5px; font-size: 16px; font-weight: 600;')
        self.dlg_layout.addWidget(h1)
        self.entry('h1','1] Carga de documentos')
        self.entry('h2','1.1] Generar solo la autorización CIC y el ID')
        self.entry('p','- El documento de origen debe estar renombrado como "affidavit", no afecta el uso de mayúsculas o minúsculas.\n- El programa acepta uno o dos documentos del ID, si es un solo documento o imagen, debe renombrarse específicamente como "id", si son dos documentos deben renombrarse como "id1" y "id2".\n- El ID puede estar en los siguientes formatos de origen: .pdf, .png, .jpg, .jpeg, .jfif.\n- El uso de mayúsculas o minúsculas no afecta el funcionamiento de la aplicación.')
        self.entry('h2','1.2] Generar todos los documentos incluidos en el origen')
        self.entry('p','- Debe estar marcada la casilla "Generar todos los documentos".\n- La aplicación va a generar únicamente los documentos que contenga el origen (affidavit).\n- Los formatos de carga no varían, el origen como "affidavit" y el ID como "id" si es un documento o como "id1" y "id2" si son dos documentos.')
        self.entry('h1','2] Accesos directos por teclado')
        self.entry('p','F1 / Ctrl+H\tVentana de ayuda\nF2 / Ctrl+I\tVentana de información\nF3 / Ctrl+S\tGuardar la configuración de trabajo actual\nF4 / Ctrl+A\tAbrir carpeta de expedientes procesados\nCtrl+B\t\tCambiar la ruta "Buscar los documentos en"\nShift+B\t\tCambiar la ruta "Guardar los documentos en"\nCtrl+Space\tBotón de "Leer"\nCtrl+Enter\tBotón de "Procesar"')
        dlg.exec()

    def entry(self, wtype, text):
        e = QLabel(text)
        if wtype == 'h1': e.setStyleSheet('padding: 5px; color: #556; background: #FFF; border: 3px groove #BBC; border-radius: 5px; font-size: 14px; font-weight: 600;')
        elif wtype == 'h2': e.setStyleSheet('padding: 3px; font-size: 13px; font-weight: 600;')
        elif wtype == 'p': e.setStyleSheet('padding: 3px; margin-bottom: 10px;')
        self.dlg_layout.addWidget(e)

    def bbdd(self):
        self.con = sqlite3.connect('settings.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute('''
                CREATE TABLE user_settings(
                    WORKFLOW BOOLEAN,
                    DIR_PATH_1 VARCHAR(999),
                    DIR_PATH_2 VARCHAR(999),
                    ENTRY_ID BOOLEAN,
                    ENTRY_FNAME BOOLEAN,
                    ENTRY_KYCDATED BOOLEAN)''')
            self.record = f'INSERT INTO user_settings VALUES (0, "N/A", "N/A", 0, 0, 0)'
            self.cur.execute(self.record)
        except sqlite3.OperationalError:
            self.req = self.cur.execute('SELECT * FROM user_settings')
            self.res = self.req.fetchone()
            cache = list(self.res)
            if cache[0] == 1:
                self.cpu_mode.setChecked(True)
                self.cpu_mode.setStyleSheet('color: #000;')
                self.processing_type.setText('Generar todos los documentos')
            else:
                self.cpu_mode.setChecked(False)
                self.cpu_mode.setStyleSheet('color: #777;')
                self.processing_type.setText('Generar solo identificación y CIC')
            self.path_1.setText(cache[1])
            self.path_2.setText(cache[2])
            if cache[3] == 1:
                self.l_ident_act.setChecked(True)
                self.l_ident.setDisabled(False)
            else:
                self.l_ident_act.setChecked(False)
                self.l_ident.setDisabled(True)
            if cache[4] == 1:
                self.l_fname_act.setChecked(True)
                self.l_fname.setDisabled(False)
            else:
                self.l_fname_act.setChecked(False)
                self.l_fname.setDisabled(True)
            if cache[5] == 1:
                self.l_kycdt_act.setChecked(True)
                self.l_kycdt.setDisabled(False)
            else:
                self.l_kycdt_act.setChecked(False)
                self.l_kycdt.setDisabled(True)
        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
        finally:
            self.con.commit()
            self.con.close()

    def update_bbdd(self):
        self.con = sqlite3.connect('settings.db')
        self.cur = self.con.cursor()
        self.req = self.cur.execute('SELECT * FROM user_settings')
        self.res = self.req.fetchone()
        if self.cpu_mode.isChecked(): write = 'UPDATE user_settings SET WORKFLOW = 1'
        else: write = 'UPDATE user_settings SET WORKFLOW = 0'
        self.cur.execute(write)
        write = f'UPDATE user_settings SET DIR_PATH_1 = "{self.path_1.text()}"'
        self.cur.execute(write)
        write = f'UPDATE user_settings SET DIR_PATH_2 = "{self.path_2.text()}"'
        self.cur.execute(write)
        if self.l_ident_act.isChecked(): write = 'UPDATE user_settings SET ENTRY_ID = 1'
        else: write = 'UPDATE user_settings SET ENTRY_ID = 0'
        self.cur.execute(write)
        if self.l_fname_act.isChecked(): write = 'UPDATE user_settings SET ENTRY_FNAME = 1'
        else: write = 'UPDATE user_settings SET ENTRY_FNAME = 0'
        self.cur.execute(write)
        if self.l_kycdt_act.isChecked(): write = 'UPDATE user_settings SET ENTRY_KYCDATED = 1'
        else: write = 'UPDATE user_settings SET ENTRY_KYCDATED = 0'
        self.cur.execute(write)
        self.con.commit()
        self.con.close()

    def testing(self):
        deskpy_pdf.PDF.TestingTool(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget{font-family Segoe UI sans-serif; font-size: 13px; border: 1px solid red;}
        QToolBar{padding: 10px; background: #556; color: #DDF;}
        QToolBar::separator{width: 10px; height: 1px; border: none;}
        QLabel{font-size: 12px;}
        QPushButton{color: #556; font-weight: 600;}
        QLineEdit{padding: 6px 3px; margin: 0 0 15px 0; font-size: 16px;}
        QPushButton:hover{color: #DDF; background: #556; border-radius: 5px;}
        QComboBox{color: #556;}
        QStatusBar{background: #303040;}
        *{font-family: Segoe UI;}
        """)
    win = Main()
    sys.exit(app.exec())