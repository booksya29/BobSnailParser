import ctypes
import json
import os
import time
import winsound
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QLabel,
    QMessageBox,
)

BASE_DIR = Path(__file__).resolve().parent / "src" / "urls_db"


class AddUrlDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати посилання")
        self.resize(450, 110)

        layout = QVBoxLayout(self)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://...")
        layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Скасувати", self)
        self.confirm_button = QPushButton("Підтвердити", self)

        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.confirm_button)
        layout.addLayout(button_layout)

    def get_url(self):
        return self.url_input.text().strip()


class ConfigDialog(QDialog):
    def __init__(self, shop_name: str, json_filename: str, parent=None):
        super().__init__(parent)
        self.shop_name = shop_name
        self.json_filename = json_filename
        self.file_path = BASE_DIR / self.json_filename
        self.urls = []
        self.last_clipboard = ""
        self.last_hotkey_time = 0

        self.setWindowTitle(f"Конфігурація - {self.shop_name}")
        self.resize(720, 530)

        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(100)
        self.poll_timer.timeout.connect(self.on_timer_tick)

        self.setup_ui()
        self.load_urls()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.macro_button = QPushButton("Макрос", self)
        self.macro_button.setCheckable(True)
        self.macro_button.setFixedHeight(32)
        self.macro_button.toggled.connect(self.toggle_macro)
        top_layout.addWidget(self.macro_button)

        top_layout.addStretch()

        self.delete_button = QPushButton("Видалити", self)
        self.delete_button.setFixedHeight(32)
        self.delete_button.clicked.connect(self.delete_selected)
        top_layout.addWidget(self.delete_button)

        self.add_button = QPushButton("+", self)
        self.add_button.setFixedSize(36, 32)
        self.add_button.clicked.connect(self.open_add_dialog)
        top_layout.addWidget(self.add_button)

        main_layout.addLayout(top_layout)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Пошук...")
        self.search_input.textChanged.connect(self.filter_urls)
        main_layout.addWidget(self.search_input)

        self.list_widget = QListWidget(self)
        main_layout.addWidget(self.list_widget)

        self.status_label = QLabel(self)
        self.status_label.setStyleSheet("color: #888888; font-size: 11px;")
        main_layout.addWidget(self.status_label)

    def load_urls(self):
        self.list_widget.clear()
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.urls = data
                    else:
                        self.urls = []
            except Exception:
                self.urls = []
        else:
            self.urls = []

        for url in self.urls:
            self.list_widget.addItem(str(url))

    def save_urls(self):
        os.makedirs(BASE_DIR, exist_ok=True)
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.urls, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл: {e}")

    def filter_urls(self, query: str):
        query = query.strip().lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query not in item.text().lower())

    def toggle_macro(self, checked: bool):
        if checked:
            self.macro_button.setText("Макрос (активний)")
            self.status_label.setText("Макрос увімкнено: наведіть курсор на товар і натисніть Ctrl+Q або F8")
            self.last_clipboard = QGuiApplication.clipboard().text().strip()
            self.poll_timer.start()
        else:
            self.macro_button.setText("Макрос")
            self.status_label.setText("")
            self.poll_timer.stop()

    def on_timer_tick(self):
        if not self.macro_button.isChecked():
            return

        VK_CONTROL = 0x11
        VK_Q = 0x51
        VK_F8 = 0x77

        ctrl_pressed = bool(ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL) & 0x8000)
        q_pressed = bool(ctypes.windll.user32.GetAsyncKeyState(VK_Q) & 0x8000)
        f8_pressed = bool(ctypes.windll.user32.GetAsyncKeyState(VK_F8) & 0x8000)

        now = time.time()
        if (ctrl_pressed and q_pressed) or f8_pressed:
            if now - self.last_hotkey_time > 0.4:
                self.last_hotkey_time = now
                self.perform_cursor_copy()

        current_clip = QGuiApplication.clipboard().text().strip()
        if current_clip and current_clip != self.last_clipboard:
            self.last_clipboard = current_clip
            if current_clip.startswith("http://") or current_clip.startswith("https://"):
                self.add_url(current_clip)

    def perform_cursor_copy(self):
        VK_CONTROL = 0x11
        VK_SHIFT = 0x10
        VK_MENU = 0x12
        VK_DOWN = 0x28
        VK_RETURN = 0x0D
        VK_ESCAPE = 0x1B

        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_MENU, 0, 2, 0)
        time.sleep(0.04)

        ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
        time.sleep(0.12)

        for _ in range(5):
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)
            time.sleep(0.02)

        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)
        time.sleep(0.05)

        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 2, 0)

        QTimer.singleShot(100, self.check_copied_result)

    def check_copied_result(self):
        current_clip = QGuiApplication.clipboard().text().strip()
        if current_clip and (current_clip.startswith("http://") or current_clip.startswith("https://")):
            self.add_url(current_clip)

    def add_url(self, url: str):
        if url not in self.urls:
            self.urls.append(url)
            self.save_urls()
            self.load_urls()
            self.filter_urls(self.search_input.text())
            self.status_label.setText(f"Додано: {url}")
            try:
                winsound.MessageBeep(winsound.MB_OK)
            except Exception:
                pass
        else:
            self.status_label.setText(f"Вже є у списку: {url}")

    def delete_selected(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        url_to_remove = current_item.text()
        if url_to_remove in self.urls:
            self.urls.remove(url_to_remove)
            self.save_urls()
            self.load_urls()
            self.filter_urls(self.search_input.text())
            self.status_label.setText(f"Видалено: {url_to_remove}")

    def open_add_dialog(self):
        dialog = AddUrlDialog(self)
        if dialog.exec():
            new_url = dialog.get_url()
            if new_url:
                if new_url not in self.urls:
                    self.add_url(new_url)
                else:
                    QMessageBox.information(self, "Увага", "Це посилання вже є у списку.")

    def closeEvent(self, event):
        self.toggle_macro(False)
        super().closeEvent(event)
