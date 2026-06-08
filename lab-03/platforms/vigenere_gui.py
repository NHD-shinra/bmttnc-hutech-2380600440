# vigenere_gui.py
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont

class VigenereCipherUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vigenère Cipher - vigenere.ui")
        self.resize(650, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 20, 40, 30)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("VIGENÈRE CIPHER NGUYỄN HỮU ĐẠT-2380600440")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Form Layout
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(15)
        label_font = QFont("Arial", 11)
        
        # Plain Text
        lbl_plain = QLabel("Plain Text:")
        lbl_plain.setFont(label_font)
        self.txt_plain = QTextEdit()
        self.txt_plain.setMaximumHeight(100)
        grid_layout.addWidget(lbl_plain, 0, 0, Qt.AlignTop)
        grid_layout.addWidget(self.txt_plain, 0, 1)
        
        # Key
        lbl_key = QLabel("Key (Chuỗi):")
        lbl_key.setFont(label_font)
        self.txt_key = QLineEdit()
        grid_layout.addWidget(lbl_key, 1, 0)
        grid_layout.addWidget(self.txt_key, 1, 1)
        
        # Cipher Text
        lbl_cipher = QLabel("CipherText:")
        lbl_cipher.setFont(label_font)
        self.txt_cipher = QTextEdit()
        self.txt_cipher.setMaximumHeight(100)
        grid_layout.addWidget(lbl_cipher, 2, 0, Qt.AlignTop)
        grid_layout.addWidget(self.txt_cipher, 2, 1)
        
        main_layout.addLayout(grid_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_encrypt = QPushButton("Encrypt")
        self.btn_encrypt.setMinimumSize(100, 30)
        self.btn_decrypt = QPushButton("Decrypt")
        self.btn_decrypt.setMinimumSize(100, 30)
        
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        btn_layout.addWidget(self.btn_encrypt)
        btn_layout.addItem(QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        btn_layout.addWidget(self.btn_decrypt)
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        main_layout.addLayout(btn_layout)

        self.btn_encrypt.clicked.connect(self.process_encrypt)
        self.btn_decrypt.clicked.connect(self.process_decrypt)

    def get_key(self):
        key = self.txt_key.text().strip().upper()
        if not key or not all('A' <= c <= 'Z' for c in key):
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Key) phải là một chuỗi chữ cái tiếng Anh (A-Z)!")
            return None
        return key

    def process_encrypt(self):
        key = self.get_key()
        if not key: return
            
        plain_text = self.txt_plain.toPlainText()
        n = len(plain_text)
        if n == 0: return
        
        repeated_key = (key * (n // len(key) + 1))[:n]
        
        cipher_text = ""
        for i in range(n):
            char = plain_text[i]
            if 'A' <= char <= 'Z':
                k = ord(repeated_key[i]) - 65
                cipher_text += chr((ord(char) - 65 + k) % 26 + 65)
            elif 'a' <= char <= 'z':
                k = ord(repeated_key[i]) - 65
                cipher_text += chr((ord(char) - 97 + k) % 26 + 97)
            else:
                cipher_text += char
                
        self.txt_cipher.setPlainText(cipher_text)

    def process_decrypt(self):
        key = self.get_key()
        if not key: return
            
        cipher_text = self.txt_cipher.toPlainText()
        n = len(cipher_text)
        if n == 0: return
        
        repeated_key = (key * (n // len(key) + 1))[:n]
        
        plain_text = ""
        for i in range(n):
            char = cipher_text[i]
            if 'A' <= char <= 'Z':
                k = ord(repeated_key[i]) - 65
                plain_text += chr((ord(char) - 65 - k + 26) % 26 + 65)
            elif 'a' <= char <= 'z':
                k = ord(repeated_key[i]) - 65
                plain_text += chr((ord(char) - 97 - k + 26) % 26 + 97)
            else:
                plain_text += char
                
        self.txt_plain.setPlainText(plain_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereCipherUI()
    window.show()
    sys.exit(app.exec_())