import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil
from git import Repo

class CloneRepoThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, repo_url, target_folder, file_extensions):
        super().__init__()
        self.repo_url = repo_url
        self.target_folder = target_folder
        self.file_extensions = file_extensions

    def run(self):
        temp_clone_folder = 'temp_repo'
        if os.path.exists(temp_clone_folder):
            shutil.rmtree(temp_clone_folder)
        Repo.clone_from(self.repo_url, temp_clone_folder)

        for root, dirs, files in os.walk(temp_clone_folder):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    shutil.copy(file_path, self.target_folder)

        shutil.rmtree(temp_clone_folder)
        self.finished.emit("Clone and file extraction complete!")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.urlInput = QLineEdit(self)
        self.urlInput.setPlaceholderText("Repository URL")
        layout.addWidget(self.urlInput)

        self.targetFolderInput = QLineEdit(self)
        self.targetFolderInput.setPlaceholderText("Target Folder")
        layout.addWidget(self.targetFolderInput)

        self.browseButton = QPushButton('Browse', self)
        self.browseButton.clicked.connect(self.browseFolder)
        layout.addWidget(self.browseButton)

        self.languageCombo = QComboBox(self)
        self.languageCombo.addItems(["Python (.py)", "C++ (.cpp)"])
        layout.addWidget(self.languageCombo)

        self.cloneButton = QPushButton('Clone and Extract', self)
        self.cloneButton.clicked.connect(self.startClone)
        layout.addWidget(self.cloneButton)

        self.setLayout(layout)
        self.setWindowTitle('Repo Clone and Extract')
        self.setGeometry(300, 300, 300, 150)
        self.show()

    def browseFolder(self):
        target_folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.targetFolderInput.setText(target_folder)

    def startClone(self):
        repo_url = self.urlInput.text()
        target_folder = self.targetFolderInput.text()
        language = self.languageCombo.currentText()
        file_extensions = ['.py'] if 'Python' in language else ['.cpp']

        if not repo_url or not target_folder:
            QMessageBox.warning(self, "Missing Information", "Please specify both the repository URL and the target folder.")
            return

        self.cloneThread = CloneRepoThread(repo_url, target_folder, file_extensions)
        self.cloneThread.finished.connect(self.onFinished)
        self.cloneThread.start()

    def onFinished(self, message):
        QMessageBox.information(self, "Done", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
