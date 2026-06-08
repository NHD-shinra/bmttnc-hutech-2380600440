# playfair_gui.py
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont

class PlayfairCipherUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playfair Cipher - playfair.ui")
        self.resize(650, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 20, 40, 30)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("PLAYFAIR CIPHER NGUYỄN HỮU ĐẠT-2380600440")
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

    def _generate_matrix(self, key):
        key = "".join([c for c in key.upper() if 'A' <= c <= 'Z']).replace('J', 'I')
        matrix = []
        seen = set()
        for char in key:
            if char not in seen:
                seen.add(char)
                matrix.append(char)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in seen:
                seen.add(char)
                matrix.append(char)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def _find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return 0, 0

    def process_encrypt(self):
        key = self.txt_key.text().strip()
        if not key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập từ khóa (Key)!")
            return
            
        matrix = self._generate_matrix(key)
        plain_text = self.txt_plain.toPlainText().upper()
        raw_text = "".join([c for c in plain_text if 'A' <= c <= 'Z']).replace('J', 'I')
        if not raw_text:
            return
        
        prepared_text = ""
        i = 0
        while i < len(raw_text):
            char1 = raw_text[i]
            if i + 1 < len(raw_text):
                char2 = raw_text[i+1]
                if char1 == char2:
                    filler = 'Q' if char1 == 'X' else 'X'
                    prepared_text += char1 + filler
                    i += 1
                else:
                    prepared_text += char1 + char2
                    i += 2
            else:
                filler = 'Q' if char1 == 'X' else 'X'
                prepared_text += char1 + filler
                i += 1
            
        ciphertext = ""
        for i in range(0, len(prepared_text), 2):
            r1, c1 = self._find_position(matrix, prepared_text[i])
            r2, c2 = self._find_position(matrix, prepared_text[i+1])
            if r1 == r2:
                ciphertext += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                ciphertext += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else:
                ciphertext += matrix[r1][c2] + matrix[r2][c1]
                
        self.txt_cipher.setPlainText(ciphertext)

    def process_decrypt(self):
        key = self.txt_key.text().strip()
        if not key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập từ khóa (Key)!")
            return
            
        matrix = self._generate_matrix(key)
        cipher_text = self.txt_cipher.toPlainText().upper()
        text = "".join([c for c in cipher_text if 'A' <= c <= 'Z']).replace('J', 'I')
        if not text:
            return
        if len(text) % 2 != 0:
            QMessageBox.warning(self, "Lỗi", "Độ dài bản mã Playfair hợp lệ phải là số chẵn!")
            return
            
        plaintext = ""
        for i in range(0, len(text), 2):
            r1, c1 = self._find_position(matrix, text[i])
            r2, c2 = self._find_position(matrix, text[i+1])
            if r1 == r2:
                plaintext += matrix[r1][(c1 - 1 + 5) % 5] + matrix[r2][(c2 - 1 + 5) % 5]
            elif c1 == c2:
                plaintext += matrix[(r1 - 1 + 5) % 5][c1] + matrix[(r2 - 1 + 5) % 5][c2]
            else:
                plaintext += matrix[r1][c2] + matrix[r2][c1]
                
        self.txt_plain.setPlainText(plaintext)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairCipherUI()
    window.show()
    sys.exit(app.exec_())