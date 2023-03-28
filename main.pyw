from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os
import ui_pdf_merger
from crop_image import get_cropped_images
from img_to_pdf import merge_pdf
from convert import pdf_to_images
import shutil 

class MergeThread(QThread):
    finished = pyqtSignal()

    def __init__(self, file_path, page_size, parent_obj):
        super().__init__()
        self.file_path = file_path
        self.page_size = page_size
        self.parent_obj = parent_obj

    def run(self):
        
        if self.file_path is None:
            self.parent_obj.edit_status.append('[ERROR] please upload a file first')
            return
        
        pdf_to_images(self.file_path, 'temp', self.parent_obj)
        get_cropped_images(self.parent_obj)
        merge_pdf(self.page_size, self.parent_obj)
        
        self.finished.emit()

class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
        # check if both "temp" and "output" directories exist
        os.path.exists('temp') or os.mkdir('temp')
        os.path.exists('output') or os.mkdir('output')
        
        # Load the Ui File 
        self.ui = ui_pdf_merger.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Set the window title
        self.setWindowTitle('PDF Merger')
        self.setWindowIcon(QIcon('merge.ico'))
        
        # Set class variables
        self.file_path = None
        self.page_size = None
        
        # connect buttons
        self.ui.btn_upload_file.clicked.connect(self.upload_file)
        self.ui.btn_merge_file.clicked.connect(self.merge_file)
        self.ui.btn_download_file.clicked.connect(self.open_download_file)
        self.ui.edit_status.setText("[WARNING] Before merging, please make sure that the 'OUTPUT' file is not opened by any PDF Reader. If so, then close it and then run Merge PDF. Else you might get ERROR or CRASH\n")
        
    def upload_file(self):
        
        if os.path.exists('temp'):
            shutil.rmtree('temp')
            os.mkdir('temp')
            
        self.ui.edit_status.clear()
        self.file_path = QFileDialog.getOpenFileName(self, 'Open File', '', 'PDF Files (*.pdf)')
        
        # extract the file name from the file path
        file_name = self.file_path[0].split('/')[-1]
        self.ui.lbl_file_name.setText(file_name)
        self.ui.edit_status.append(f'[FILE] {file_name} uploaded successfully\n')
        
    def merge_file(self):
        
        if self.file_path is None:
            self.ui.edit_status.append('[ERROR] please upload a file first')
            return 
        
        self.ui.edit_status.clear()
        
        self.ui.btn_download_file.setEnabled(False)
        self.page_size = self.ui.cmb_page_size.currentText()

        self.ui.edit_status.append('[PAGE SIZE] {}\n'.format(self.page_size))
        self.ui.edit_status.append("[MERGING] merging is in progress.......\n")

        self.ui.edit_status.repaint()

        # separate thread for merging helps to avoid blocking the UI
        self.merge_thread = MergeThread(self.file_path[0], self.page_size, self.ui)
        self.merge_thread.finished.connect(self.on_merge_finished)
        self.merge_thread.start()

    def on_merge_finished(self):
        self.ui.edit_status.append("\n[DONE] click the 'Download' button to get the merged file.......\n")
        self.ui.edit_status.append("\n[WARNING] After you finished working with 'merged.pdf' file Please 'CLOSE' it. Else you might get ERROR or CRASH\n")
        self.ui.btn_download_file.setEnabled(True)

    def open_download_file(self):
        os.startfile('output')
        
        
if __name__ == '__main__':
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
    
