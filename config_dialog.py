import json
import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
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

        self.setWindowTitle(f"Конфігурація - {self.shop_name}")
        self.resize(700, 500)

        self.setup_ui()
        self.load_urls()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.add_button = QPushButton("+", self)
        self.add_button.setFixedSize(36, 32)
        self.add_button.clicked.connect(self.open_add_dialog)
        top_layout.addWidget(self.add_button)
        main_layout.addLayout(top_layout)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Пошук")
        self.search_input.textChanged.connect(self.filter_urls)
        main_layout.addWidget(self.search_input)

        self.list_widget = QListWidget(self)
        main_layout.addWidget(self.list_widget)

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

    def open_add_dialog(self):
        dialog = AddUrlDialog(self)
        if dialog.exec():
            new_url = dialog.get_url()
            if new_url:
                if new_url not in self.urls:
                    self.urls.append(new_url)
                    self.save_urls()
                    self.load_urls()
                    self.filter_urls(self.search_input.text())
                else:
                    QMessageBox.information(self, "Увага", "Це посилання вже є у списку.")
