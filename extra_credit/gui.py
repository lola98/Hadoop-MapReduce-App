from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys, glob
from os.path import isfile
from upload_files import Upload_Files

class Ui_Form(object):
    files = []
    _translate = QtCore.QCoreApplication.translate

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 600)

        # define font size
        custom_font = QFont()
        custom_font.setPointSize(20)
        QApplication.setFont(custom_font, "QLabel")

        # create header
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 20, 500, 180))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # create file upload button
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 150, 200, 100))
        self.pushButton.setStyleSheet("background-color:white;\n"
                                      "color: black;\n"
                                      "border-style: outset;\n"
                                      "border-width:2px;\n"
                                      "border-radius:10px;\n"
                                      "border-color:black;\n"
                                      "font:bold 16px;\n"
                                      "padding :10px;\n"
                                      "min-width:10px;\n"
                                      "\n"
                                      "\n"
                                      "")
        self.pushButton.setObjectName("pushButton")

        # create empty block to print input file names
        self.label_filenames = QtWidgets.QPlainTextEdit(Form) 
        self.label_filenames.setGeometry(QtCore.QRect(150, 275, 300, 100))
        self.label_filenames.setReadOnly(True)
        self.label_filenames.setBackgroundVisible(False)
        self.label_filenames.setObjectName("label_filenames")

        # # create confirmation button
        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(150, 400, 300, 100))
        self.pushButton2.setStyleSheet("background-color:white;\n"
                                      "color: black;\n"
                                      "border-style: outset;\n"
                                      "border-width:2px;\n"
                                      "border-radius:10px;\n"
                                      "border-color:black;\n"
                                      "font:bold 16px;\n"
                                      "padding :10px;\n"
                                      "min-width:10px;\n"
                                      "\n"
                                      "\n"
                                      "")
        self.pushButton2.setObjectName("pushButton2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        Form.setWindowTitle(self._translate("Form", "Upload Folder / Files"))
        self.label.setText(self._translate("Form", "Upload Files to GCP Bucket"))
        self.pushButton.setText(self._translate("Form", "Choose Folder / Files"))
        self.pushButton2.setText(self._translate("Form", "Upload Folder / Files"))

        # set on-click events
        self.pushButton.clicked.connect(self.pushButton_handler)
        self.pushButton2.clicked.connect(self.pushButton2_handler)


    def pushButton_handler(self):
        self.files = str(QFileDialog.getExistingDirectory(None, "Select Directory"))

        for f in glob.iglob(self.files + '**/**', recursive=True):
            base_folder = self.files.replace(self.files.split('/')[-1], '')
            if isfile(f) and not f.startswith('.'):
                self.label_filenames.appendPlainText(self._translate("Form", f.replace(base_folder, '')))

        self.pushButton2.setText(self._translate("Form", "Upload Files"))

    # upload selected files to GCP bucket
    def pushButton2_handler(self):
        Upload_Files.upload_to_bucket(self.files, "dataproc-staging-us-central1-105135044036-jlvf54fr", 'temperature')
        self.update_page()

    def update_page(self):
        # update header
        if (len(self.files) ==0):
            self.label.setText(self._translate("Form", "Please Select Files First"))
        else:
            self.label.setText(self._translate("Form", "Files have been successfully loaded \n " \
            +"Please check the GCP bucket"))

            self.label_filenames.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())