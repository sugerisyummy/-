import sys
import threading
import pytesseract
from PIL import ImageGrab, Image
from PyQt5 import QtWidgets, QtGui, QtCore
import time
import keyboard
from googletrans import Translator
import os

# ✅ 設定 tesseract 執行路徑（支援打包與開發環境）
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
pytesseract.pytesseract.tesseract_cmd = os.path.join(base_path, 'Tesseract-OCR', 'tesseract.exe')

# ✅ 初始化 Google 翻譯器
translator = Translator()

def translate_with_google(text, target_lang='zh-TW'):
    if not text.strip():
        return "未偵測到可翻譯內容"
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"翻譯失敗: {e}"

# ✅ 浮動視窗
class FloatingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(400, 200)

        self.bg = QtWidgets.QLabel(self)
        self.bg.setGeometry(0, 0, 400, 200)
        self.bg.setStyleSheet("background-color: rgba(30, 30, 30, 200); border-radius: 15px;")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(20, 20, 360, 160)
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.label.setWordWrap(True)

        self.show()

    def update_text(self, text):
        self.label.setText(text)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

# ✅ OCR + 翻譯邏輯
def capture_and_translate(window, last_text):
    try:
        screenshot = ImageGrab.grab()
        img = screenshot.convert("RGB")
        text = pytesseract.image_to_string(img, lang='eng+jpn').strip()
        if not text or text == last_text:
            return last_text
        translated = translate_with_google(text)
        window.update_text(translated)
        return text
    except Exception as e:
        window.update_text(f"錯誤: {e}")
        return last_text

# ✅ 定時執行翻譯
def realtime_monitor(window, interval=2):
    last_text = ""
    while True:
        last_text = capture_and_translate(window, last_text)
        time.sleep(interval)

# ✅ ESC 退出
def esc_exit_monitor():
    keyboard.wait('esc')
    sys.exit(0)

# ✅ 主程式
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FloatingWindow()
    threading.Thread(target=realtime_monitor, args=(window,), daemon=True).start()
    threading.Thread(target=esc_exit_monitor, daemon=True).start()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
