# This Python file uses the following encoding: utf-8

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

if getattr(sys, "frozen", False):
    app_dir = Path(sys.executable).resolve().parent
    local_browsers = app_dir / "_internal" / "patchright" / "driver" / "package" / ".local-browsers"
    if local_browsers.exists():
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(local_browsers)

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import excel_add
import json_manager
import atb_async_parser_product
import ashan_parser_product
import novus_parser_product
import fozzy_parser_product
import fora_parser_product
import tavria_parser_product
import silpo_parser_product
import varus_parser_product
import metro_parser_product

from PySide6.QtWidgets import (
    QApplication, QWidget, QMessageBox, QPlainTextEdit, QPushButton,
    QLabel, QHBoxLayout,
)
from PySide6.QtCore import QObject, QThread, Signal

from ui_form import Ui_Widget
from config_dialog import ConfigDialog
class GuiLogStream(QObject):
    """Routes print() output from the parser thread into the app window."""

    line_written = Signal(str)

    def __init__(self):
        super().__init__()
        self._buffer = ""

    def write(self, text):
        if not text:
            return 0
        self._buffer += str(text)
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.line_written.emit(line.rstrip())
        return len(text)

    def flush(self):
        if self._buffer.strip():
            self.line_written.emit(self._buffer.rstrip())
        self._buffer = ""


class Worker(QObject):
    finished = Signal()
    failed = Signal(str)
    progress = Signal(str, int)

    def __init__(self, target_shop: str = None):
        super().__init__()
        self.target_shop = target_shop
        self._is_stopped = False
        self._browser = None
        self._context = None
        self._loop = None

    def stop(self):
        """Signals worker to stop and cancels all running tasks."""
        self._is_stopped = True
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._cancel_all_tasks)

    def _cancel_all_tasks(self):
        try:
            for task in asyncio.all_tasks(self._loop):
                task.cancel()
        except Exception:
            pass

    def run(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._parse())
        except BaseException as error:
            if not self._is_stopped and not isinstance(error, asyncio.CancelledError):
                self.failed.emit(str(error))
        finally:
            try:
                if self._loop and not self._loop.is_closed():
                    self._loop.close()
            except Exception:
                pass
            self.finished.emit()

    async def _parse(self):
        parsers = self._load_parsers()
        if not parsers:
            return

        if self.target_shop:
            parsers = [p for p in parsers if p[0] == self.target_shop]
            if not parsers:
                self.failed.emit(f"Не знайдено конфігурації для магазину {self.target_shop}.")
                return

        active_shops = []
        for shop_key, parser_func, json_name in parsers:
            urls = await json_manager.read_json(json_name)
            if urls:
                active_shops.append((shop_key, parser_func, urls))
            else:
                self.progress.emit(shop_key, 100)

        if not active_shops:
            if self.target_shop:
                self.failed.emit("Не знайдено жодного посилання для цього магазину. Додайте посилання через 'Edit Config'.")
            else:
                self.failed.emit("Не знайдено жодного посилання. Будь ласка, додайте посилання у конфігурацію магазинів через 'Edit Config'.")
            return

        from patchright.async_api import async_playwright

        async def run_shop(shop_key, parser_func, page):
            def on_progress(p):
                if not self._is_stopped:
                    self.progress.emit(shop_key, p)

            on_progress(0)
            print(f"[{shop_key.upper()}] Початок обробки.")
            try:
                import inspect
                if "on_progress" in inspect.signature(parser_func).parameters:
                    await parser_func(page, on_progress=on_progress)
                else:
                    await parser_func(page)
            except Exception as e:
                if not self._is_stopped:
                    print(f"Error parsing {shop_key}: {e}")
            finally:
                if not self._is_stopped:
                    on_progress(100)
                print(f"[{shop_key.upper()}] Обробку завершено.")

        async with async_playwright() as playwright:
            self._browser = await playwright.chromium.launch(
    headless=False,
    args=[
        "--blink-settings=imagesEnabled=false",  
        "--disk-cache-size=1",                  
        "--media-cache-size=1",                
        "--disable-dev-shm-usage",              
    ]
)
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 800}
            )
            try:
                semaphore = asyncio.Semaphore(3 if not self.target_shop else 1)

                async def process_shop(shop_key, parser_func):
                    if self._is_stopped:
                        return
                    async with semaphore:
                        if self._is_stopped:
                            return
                        page = await self._context.new_page()
                        try:
                            await run_shop(shop_key, parser_func, page)
                        finally:
                            try:
                                await page.close()
                            except Exception:
                                pass

                await asyncio.gather(
                    *(process_shop(shop_key, parser_func) for shop_key, parser_func, _ in active_shops),
                    return_exceptions=True
                )
            finally:
                try:
                    if self._context:
                        await asyncio.shield(self._context.close())
                except Exception:
                    pass
                try:
                    if self._browser:
                        await asyncio.shield(self._browser.close())
                except Exception:
                    pass

    @staticmethod
    def _load_parsers():
        return [
            ("atb", atb_async_parser_product.atb_all_parsing, "atb.json"),
            ("ashan", ashan_parser_product.ashan_parsing_all, "ashan.json"),
            ("novus", novus_parser_product.novus_parsing_all, "novus.json"),
            ("fozzy", fozzy_parser_product.fozzy_parsing_all, "fozzy.json"),
            ("fora", fora_parser_product.fora_parsing_all, "fora.json"),
            ("tavria", tavria_parser_product.tavria_parsing_all, "tavria.json"),
            ("silpo", silpo_parser_product.silpo_parsing_all, "silpo.json"),
            ("varus", varus_parser_product.varus_parsing_all, "varus.json"),
            ("metro", metro_parser_product.metro_parsing_all, "metro.json"),
        ]


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("Bob Snail")

        self.log_output = QPlainTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(3000)
        self.log_output.setPlaceholderText("Тут з'являться повідомлення про роботу парсера…")
        self.log_output.setMinimumHeight(190)
        self.log_output.setStyleSheet(
            "QPlainTextEdit { background: #151515; color: #e6e6e6; "
            "font-family: Consolas, monospace; font-size: 10pt; }"
        )
        log_label = QLabel("Журнал роботи", self)
        clear_log_button = QPushButton("Очистити журнал", self)
        clear_log_button.clicked.connect(self.log_output.clear)
        log_header = QHBoxLayout()
        log_header.addWidget(log_label)
        log_header.addStretch()
        log_header.addWidget(clear_log_button)
        self.ui.verticalLayout_2.addLayout(log_header)
        self.ui.verticalLayout_2.addWidget(self.log_output)

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._log_stream = GuiLogStream()
        self._log_stream.line_written.connect(self.append_log)
        sys.stdout = self._log_stream
        sys.stderr = self._log_stream
        self.append_log("Програма запущена. Журнал готовий.")

        self.thread = None
        self.worker = None

        self.progress_bars = {
            "ashan": self.ui.AshanProgressBar,
            "silpo": self.ui.SilpoProgressBar,
            "atb": self.ui.ATBProgressBar,
            "fozzy": self.ui.FozzyProgressBar,
            "novus": self.ui.NovusProgressBar,
            "fora": self.ui.ForaProgressBar,
            "varus": self.ui.VarusProgressBar,
            "metro": self.ui.MetroProgressBar,
            "tavria": self.ui.TavriaProgressBar,
        }

        self.solo_buttons = {
            "ashan": self.ui.AshanParsingButton,
            "silpo": self.ui.SilpoParsing,
            "atb": self.ui.ATBParsing,
            "fozzy": self.ui.FozzyParsing,
            "novus": self.ui.ParsingNovus,
            "fora": self.ui.ForaParsing,
            "varus": self.ui.VarusParsing,
            "metro": self.ui.MatroParsing,
            "tavria": self.ui.TavriaParsing,
        }

        # Підключення головних кнопок Start / Stop
        self.ui.StartButton.clicked.connect(lambda: self.start_worker(target_shop=None))
        self.ui.StopButton.clicked.connect(self.stop_worker)

        # Підключення конфігурацій магазинів (Edit Config)
        self.ui.AshanButton.clicked.connect(lambda: self.open_config("Ашан", "ashan.json"))
        self.ui.SilpoButton.clicked.connect(lambda: self.open_config("Сільпо", "silpo.json"))
        self.ui.ATBButton.clicked.connect(lambda: self.open_config("АТБ", "atb.json"))
        self.ui.FozzyButton.clicked.connect(lambda: self.open_config("Фоззі", "fozzy.json"))
        self.ui.NovusButton.clicked.connect(lambda: self.open_config("Новус", "novus.json"))
        self.ui.ForaButton.clicked.connect(lambda: self.open_config("Фора", "fora.json"))
        self.ui.VarusButton.clicked.connect(lambda: self.open_config("Варус", "varus.json"))
        self.ui.MetroButton.clicked.connect(lambda: self.open_config("Метро", "metro.json"))
        self.ui.TavriaButton.clicked.connect(lambda: self.open_config("Таврія", "tavria.json"))

        # Підключення кнопок сольного запуску
        for shop_key, btn in self.solo_buttons.items():
            btn.clicked.connect(lambda checked=False, k=shop_key: self.start_worker(target_shop=k))

    def set_running_state(self, is_running: bool):
        """Вмикає або вимикає кнопки в залежності від того, чи працює парсер."""
        self.ui.StartButton.setEnabled(not is_running)
        for btn in self.solo_buttons.values():
            btn.setEnabled(not is_running)
        self.ui.StopButton.setEnabled(is_running)

    def open_config(self, shop_name: str, json_filename: str):
        dialog = ConfigDialog(shop_name, json_filename, self)
        dialog.exec()

    def update_progress(self, shop_key: str, value: int):
        if shop_key in self.progress_bars:
            self.progress_bars[shop_key].setValue(value)

    def append_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.appendPlainText(f"[{timestamp}] {message}")
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def start_worker(self, target_shop: str = None):
        if self.thread is not None and self.thread.isRunning():
            if self.worker is not None and self.worker._is_stopped:
                self.thread.quit()
                self.thread.wait(500)
            else:
                return

        if target_shop:
            if target_shop in self.progress_bars:
                self.progress_bars[target_shop].setValue(0)
            self.append_log(f"Запуск парсингу для магазину: {target_shop.upper()}.")
        else:
            for pb in self.progress_bars.values():
                pb.setValue(0)
            self.append_log("Запуск парсингу всіх налаштованих магазинів.")

        self.set_running_state(True)
        self.thread = QThread(self)

        self.worker = Worker(target_shop=target_shop)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.show_error)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker_finished)

        self.thread.start()

    def stop_worker(self):
        self.append_log("Запит на зупинку парсингу... Закриваємо браузер.")
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
        self.set_running_state(False)

    def show_error(self, message):
        print(f"Parser error: {message}")
        QMessageBox.warning(self, "Інформація", str(message))

    def worker_finished(self):
        self.append_log("Парсинг завершено.")
        self.set_running_state(False)
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
