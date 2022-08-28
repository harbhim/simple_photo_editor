import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QStatusBar,
                             QFileDialog, QMessageBox, QVBoxLayout, QWidget,
                             QDialog, QToolBar, QDockWidget, QPushButton)
from PyQt6.QtGui import QPixmap, QAction, QPainter, QTransform, QIcon
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

class PhotoEditor(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui()
        self.show()

    def ui(self):

        self.setMinimumSize(1366, 768)
        self.setWindowTitle('Photo Editor')

        self.createActions()
        self.setUpMainWindow()
        self.createToolbar()
        self.createDockWidget()
        self.addingMenu()

    def setUpMainWindow(self):

        self.img_lab = QLabel()
        self.img_pix = QPixmap()
        self.img_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.img_lab)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        self.menu_bar = self.menuBar()

    def createActions(self):

        self.open_act = QAction('&Open')
        self.open_act.setIcon(QIcon('images/open_file.png'))
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.setStatusTip('Open an Image File')
        self.open_act.triggered.connect(self.openFile)

        self.save_act = QAction('&Save')
        self.save_act.setIcon(QIcon('images/save_file.png'))
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.setStatusTip('Save an Image File')
        self.save_act.triggered.connect(self.saveFile)

        self.print_act = QAction('&Print')
        self.print_act.setIcon(QIcon('images/print.png'))
        self.print_act.setShortcut('Ctrl+P')
        self.print_act.setStatusTip('Print an Image File')
        self.print_act.triggered.connect(self.printFile)
        self.print_act.setEnabled(False)

        self.quit_act = QAction('&Quit')
        self.quit_act.setIcon(QIcon('images/exit.png'))
        self.quit_act.setShortcut('Ctrl+Q')
        self.quit_act.setStatusTip('Quit an Image File')
        self.quit_act.triggered.connect(self.close)

        self.rotate_90 = QAction('&Rotate 90')
        self.rotate_90.setStatusTip('Rotate Image by 90 clockwise')
        self.rotate_90.triggered.connect(self.rotate90cw)

        self.rotate_180 = QAction('&Rotate 180')
        self.rotate_180.setStatusTip('Rotate Image by 180 clockwise')
        self.rotate_180.triggered.connect(self.rotate180cw)

        self.flip_h = QAction('&Flip Horizontal')
        self.flip_h.setStatusTip('Flip image horizontally')
        self.flip_h.triggered.connect(self.flipH)

        self.flip_v = QAction('&Flip Vertical')
        self.flip_v.setStatusTip('Flip image vertically')
        self.flip_v.triggered.connect(self.flipV)

        self.resize_half = QAction('&Resize Half')
        self.resize_half.setStatusTip(
            'Resize image to half of current resolution')
        self.resize_half.triggered.connect(self.resizeHalf)

        self.clear_img = QAction('&Clear Image')
        self.clear_img.setIcon(QIcon('images/clear.png'))
        self.clear_img.setStatusTip('Clear image from screen')
        self.clear_img.triggered.connect(self.clearImg)

        self.about_act = QAction('&About')
        self.about_act.setStatusTip('Show about info')
        self.about_act.triggered.connect(self.aboutMB)

    def createToolbar(self):

        self.tool_bar = QToolBar('Photo Editor Toolbar')
        self.tool_bar.setFloatable(False)
        self.tool_bar.setIconSize(QSize(20,20))
        self.addToolBar(self.tool_bar)

        self.tool_bar.addAction(self.open_act)
        self.tool_bar.addAction(self.save_act)
        self.tool_bar.addAction(self.print_act)
        self.tool_bar.addAction(self.clear_img)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.quit_act)

    def createDockWidget(self):

        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('Edit Image Tools')
        dock_widget.setMinimumWidth(200)
        dock_widget.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea)

        rotate_90 = QPushButton('Rotate 90')
        rotate_90.setStatusTip('Rotate image by 90 in clockwise')
        rotate_90.clicked.connect(self.rotate90cw)

        rotate_180 = QPushButton('Rotate 180')
        rotate_180.setStatusTip('Rotate image by 180 in clockwise')
        rotate_180.clicked.connect(self.rotate180cw)

        flip_h = QPushButton('Flip Horizontal')
        flip_h.setStatusTip('Flip image horizontally')
        flip_h.clicked.connect(self.flipH)

        flip_v = QPushButton('Flip Vertical')
        flip_v.setStatusTip('Flip image vertically')
        flip_v.clicked.connect(self.flipV)

        resize_half = QPushButton('Resize Half')
        resize_half.setStatusTip(
            'Resize image with half pixels both the sides')
        resize_half.clicked.connect(self.resizeHalf)

        container = QWidget()
        v_box_dock = QVBoxLayout()

        v_box_dock.setContentsMargins(40,20,40,20)

        v_box_dock.addWidget(rotate_90)
        v_box_dock.addStretch(5)
        v_box_dock.addWidget(rotate_180)
        v_box_dock.addStretch(20)
        v_box_dock.addWidget(flip_h)
        v_box_dock.addStretch(5)
        v_box_dock.addWidget(flip_v)
        v_box_dock.addStretch(20)
        v_box_dock.addWidget(resize_half)
        v_box_dock.addStretch(200)

        container.setLayout(v_box_dock)

        dock_widget.setWidget(container)

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock_widget)

        self.toggle_edit_dock = dock_widget.toggleViewAction()

    def addingMenu(self):

        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction(self.open_act)
        self.file_menu.addAction(self.save_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.print_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_act)

        self.edit_menu = self.menu_bar.addMenu('&Edit')
        self.edit_menu.addAction(self.rotate_90)
        self.edit_menu.addAction(self.rotate_180)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.flip_h)
        self.edit_menu.addAction(self.flip_v)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.resize_half)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.clear_img)

        self.view_menu = self.menu_bar.addMenu('&View')
        self.view_menu.addAction(self.toggle_edit_dock)

        self.help_menu = self.menu_bar.addMenu('&Help')
        self.help_menu.addAction(self.about_act)
    def openFile(self):

        fd = QFileDialog.getOpenFileName(
            self,
            'Open an image file', '/home/study/',
            'Image Files (*.jpg *.jpeg *.png *.gif *.bmp)')

        if fd[0]:

            self.img_pix = QPixmap(fd[0])
            self.img_lab.setPixmap(
                self.img_pix.scaled(
                    self.img_lab.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation))

            self.print_act.setEnabled(True)

        else:

            QMessageBox.information(
                self,
                'No Image',
                'No image selected',
                QMessageBox.StandardButton.Ok)

    def saveFile(self):

        fds = QFileDialog.getSaveFileName(
            self,
            'Chose Location and Name of file to save with extension',
            '/home/study/',
            'JPG Files (*.jpg *.jpeg);; PNG file (*.png);;\
            GIF File (*.gif);; BMP File (*.bmp)')

        if fds[0] and self.img_pix.isNull() == False:
            self.img_pix.save(fds[0])

        else:
            QMessageBox.information(
                self,
                'Not Saved',
                'File Not Saved',
                QMessageBox.StandardButton.Ok)

    def printFile(self):

        printer = QPrinter()
        print_dialog = QPrintDialog(printer)

        if print_dialog.exec() == QDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)
            rect = QRect(painter.viewport())
            size = QSize(self.img_lab.pixmap().size())
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(0, 0, size.width(), size.height())
            painter.setWindow(self.img_lab.pixmap().rect())
            painter.drawPixmap(0, 0, self.img_lab.pixmap())
            painter.end()

    def rotate90cw(self):

        if not self.img<F4>_pix.isNull():
            trans = QTransform()
            trans1 = trans.rotate(90, Qt.Axis.ZAxis)
            pixmap = QPixmap(self.img_pix)
            rotated_pix = pixmap.transformed(
                trans1,
                Qt.TransformationMode.SmoothTransformation)
            rotated_pix1 = rotated_pix.scaled(
                self.img_lab.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self.img_lab.setPixmap(rotated_pix1)
            self.img_pix = QPixmap(rotated_pix)
            self.img_lab.repaint()

    def rotate180cw(self):

        if not self.img_pix.isNull():
            transform180 = QTransform().rotate(180, Qt.Axis.ZAxis)
            pixmap = QPixmap(self.img_pix)
            mode = Qt.TransformationMode.SmoothTransformation
            rotated = pixmap.transformed(transform180, mode)
            self.img_lab.setPixmap(
                rotated.scaled(
                    self.img_lab.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,mode))
            self.img_pix = QPixmap(rotated)
            self.img_lab.repaint()

    def flipH(self):

        if not self.img_pix.isNull():
            trans = QTransform()
            trans1 = trans.scale(-1,1)
            pixmap = QPixmap(self.img_pix)
            flipped = pixmap.transformed(
                trans1,
                Qt.TransformationMode.SmoothTransformation)
            self.img_lab.setPixmap(
                flipped.scaled(
                self.img_lab.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
            self.img_pix = QPixmap(flipped)

    def flipV(self):

        if not self.img_pix.isNull():
            trans = QTransform()
            trans1 = trans.scale(1,-1)
            pixmap = QPixmap(self.img_pix)
            flipped = pixmap.transformed(
                trans1,
                Qt.TransformationMode.SmoothTransformation)
            self.img_lab.setPixmap(
                flipped.scaled(
                self.img_lab.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
            self.img_pix = QPixmap(flipped)

    def resizeHalf(self):

        if not self.img_pix.isNull():
            trans = QTransform()
            resized = trans.scale(0.5,0.5)
            pixmap = QPixmap(self.img_pix)
            resized1 = pixmap.transformed(resized)
            self.img_lab.setPixmap(
                resized1.scaled(
                    self.img_lab.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation))
            self.img_pix = QPixmap(resized1)

    def clearImg(self):

        self.img_lab.clear()
        self.img_pix = QPixmap()
        self.print_act.setEnabled(False)

    def aboutMB(self):

        mb = QMessageBox.about(
            self,
            'About Creator',
            'Created by Hardik Bhimani')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoEditor()
    sys.exit(app.exec())
