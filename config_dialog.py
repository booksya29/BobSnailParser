import ctypes
from ctypes import wintypes, byref, c_void_p, Structure, POINTER, WINFUNCTYPE, HRESULT, c_long, c_int
import json
import os
import re
import time
import winsound
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QGuiApplication, QDragEnterEvent, QDropEvent
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

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent / "src" / "urls_db"
else:
    BASE_DIR = Path(__file__).resolve().parent / "src" / "urls_db"

ole32 = ctypes.windll.ole32
user32 = ctypes.windll.user32
oleaut32 = ctypes.windll.oleaut32

try:
    ole32.CoInitialize(None)
except Exception:
    pass


class GUID(Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


class VARIANT(Structure):
    _fields_ = [
        ("vt", wintypes.WORD),
        ("wReserved1", wintypes.WORD),
        ("wReserved2", wintypes.WORD),
        ("wReserved3", wintypes.WORD),
        ("data", c_void_p),
        ("data2", c_void_p),
    ]


CLSID_CUIAutomation = GUID(
    0xFF48DBA4,
    0x60EF,
    0x4201,
    (wintypes.BYTE * 8)(0xAA, 0x87, 0x54, 0x10, 0x3E, 0xEF, 0x59, 0x4E),
)
IID_IUIAutomation = GUID(
    0x30CBE57D,
    0xD9D0,
    0x452A,
    (wintypes.BYTE * 8)(0xAB, 0x13, 0x7A, 0xC5, 0xAC, 0x48, 0x25, 0xEE),
)

_uia_instance = None
_walker_instance = None


def get_uia():
    global _uia_instance, _walker_instance
    if _uia_instance is None:
        try:
            uia_ptr = c_void_p()
            hr = ole32.CoCreateInstance(
                byref(CLSID_CUIAutomation),
                None,
                1,
                byref(IID_IUIAutomation),
                byref(uia_ptr),
            )
            if hr == 0 and uia_ptr:
                _uia_instance = uia_ptr
                vtable = ctypes.cast(
                    ctypes.cast(uia_ptr, POINTER(c_void_p)).contents,
                    POINTER(c_void_p),
                )
                GetControlViewWalker = WINFUNCTYPE(
                    HRESULT, c_void_p, POINTER(c_void_p)
                )(vtable[14])
                walker_ptr = c_void_p()
                if GetControlViewWalker(uia_ptr, byref(walker_ptr)) == 0:
                    _walker_instance = walker_ptr
        except Exception:
            _uia_instance = None
    return _uia_instance, _walker_instance


def get_prop_string(elem_ptr, prop_id):
    if not elem_ptr:
        return None
    try:
        elem_vtable = ctypes.cast(
            ctypes.cast(elem_ptr, POINTER(c_void_p)).contents, POINTER(c_void_p)
        )
        GetCurrentPropertyValue = WINFUNCTYPE(
            HRESULT, c_void_p, c_int, POINTER(VARIANT)
        )(elem_vtable[10])
        var = VARIANT()
        hr = GetCurrentPropertyValue(elem_ptr, prop_id, byref(var))
        if hr == 0 and var.vt == 8 and var.data:
            val = ctypes.wstring_at(var.data)
            oleaut32.VariantClear(byref(var))
            return val
        oleaut32.VariantClear(byref(var))
    except Exception:
        pass
    return None


def extract_url_under_cursor():
    uia, walker = get_uia()
    if not uia or not walker:
        return None

    try:
        vtable = ctypes.cast(
            ctypes.cast(uia, POINTER(c_void_p)).contents, POINTER(c_void_p)
        )
        ElementFromPoint = WINFUNCTYPE(HRESULT, c_void_p, POINT, POINTER(c_void_p))(
            vtable[7]
        )

        walker_vtable = ctypes.cast(
            ctypes.cast(walker, POINTER(c_void_p)).contents, POINTER(c_void_p)
        )
        GetParentElement = WINFUNCTYPE(
            HRESULT, c_void_p, c_void_p, POINTER(c_void_p)
        )(walker_vtable[3])

        pt = POINT()
        user32.GetCursorPos(byref(pt))
        elem = c_void_p()
        hr = ElementFromPoint(uia, pt, byref(elem))
        if hr != 0 or not elem:
            return None

        curr = elem
        for _ in range(15):
            if not curr:
                break
            for prop_id in (30045, 30093, 30013, 30094, 30005):
                val = get_prop_string(curr, prop_id)
                if val and ("http://" in val or "https://" in val):
                    m = re.search(r"https?://[^\s\"\'<>]+", val)
                    if m:
                        return m.group(0)

            parent = c_void_p()
            hr_p = GetParentElement(walker, curr, byref(parent))
            if hr_p != 0 or not parent:
                break
            curr = parent
    except Exception:
        pass
    return None


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


class UrlListWidget(QListWidget):
    def __init__(self, parent_dialog):
        super().__init__(parent_dialog)
        self.parent_dialog = parent_dialog
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasText() or event.mimeData().hasHtml():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText() or event.mimeData().hasHtml():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        mime = event.mimeData()
        added = False

        if mime.hasUrls():
            for url in mime.urls():
                url_str = url.toString().strip()
                if url_str.startswith("http://") or url_str.startswith("https://"):
                    self.parent_dialog.add_url(url_str)
                    added = True

        if not added and mime.hasText():
            text = mime.text().strip()
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("http://") or line.startswith("https://"):
                    self.parent_dialog.add_url(line)
                    added = True

        if not added and mime.hasHtml():
            html = mime.html()
            links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
            for link in links:
                self.parent_dialog.add_url(link)
                added = True

        if added:
            event.acceptProposedAction()
        else:
            event.ignore()


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
        self.setAcceptDrops(True)

        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(80)
        self.poll_timer.timeout.connect(self.on_timer_tick)

        self.setup_ui()
        self.load_urls()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.macro_button = QPushButton("Макрос (Ctrl+Q)", self)
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

        self.list_widget = UrlListWidget(self)
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
            self.status_label.setText("Макрос увімкнено: наведіть курсор на товар у каталозі та натисніть Ctrl+Q")
            self.last_clipboard = QGuiApplication.clipboard().text().strip()
            self.poll_timer.start()
        else:
            self.macro_button.setText("Макрос (Ctrl+Q)")
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
            if now - self.last_hotkey_time > 0.35:
                self.last_hotkey_time = now
                self.handle_macro_trigger()

        current_clip = QGuiApplication.clipboard().text().strip()
        if current_clip and current_clip != self.last_clipboard:
            self.last_clipboard = current_clip
            if current_clip.startswith("http://") or current_clip.startswith("https://"):
                self.add_url(current_clip)

    def handle_macro_trigger(self):
        url = extract_url_under_cursor()
        if url:
            self.add_url(url)
        else:
            self.fallback_browser_grab()

    def fallback_browser_grab(self):
        VK_CONTROL = 0x11
        VK_MENU = 0x12
        VK_D = 0x44
        VK_C = 0x43
        VK_ESCAPE = 0x1B

        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
        time.sleep(0.02)

        ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_D, 0, 0, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(VK_D, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_MENU, 0, 2, 0)
        time.sleep(0.06)

        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_C, 0, 0, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(VK_C, 0, 2, 0)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
        time.sleep(0.04)

        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 2, 0)

        QTimer.singleShot(80, self.check_copied_result)

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

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasText() or event.mimeData().hasHtml():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        self.list_widget.dropEvent(event)

    def closeEvent(self, event):
        self.toggle_macro(False)
        super().closeEvent(event)
