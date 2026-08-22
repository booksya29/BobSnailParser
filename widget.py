# This Python file uses the following encoding: utf-8

import asyncio
import os
import sys
from pathlib import Path

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

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QObject, QThread, Signal

from ui_form import Ui_Widget
from config_dialog import ConfigDialog


class Worker(QObject):
    finished = Signal()
    failed = Signal(str)
    progress = Signal(str, int)

    def run(self):
        try:
            asyncio.run(self._parse_all_shops())
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            self.finished.emit()

    async def _parse_all_shops(self):
        parsers = self._load_parsers()
        if not parsers:
            return

        active_shops = []
        for shop_key, parser_func, json_name in parsers:
            urls = await json_manager.read_json(json_name)
            if urls:
                active_shops.append((shop_key, parser_func, urls))
            else:
                self.progress.emit(shop_key, 100)

        if not active_shops:
            self.failed.emit("Не знайдено жодного посилання. Будь ласка, додайте посилання у конфігурацію магазинів через 'Edit Config'.")
            return

        from patchright.async_api import async_playwright

        async def run_shop(shop_key, parser_func, page):
            def on_progress(p):
                self.progress.emit(shop_key, p)

            on_progress(0)
            try:
                import inspect
                if "on_progress" in inspect.signature(parser_func).parameters:
                    await parser_func(page, on_progress=on_progress)
                else:
                    await parser_func(page)
            except Exception as e:
                print(f"Error parsing {shop_key}: {e}")
            finally:
                on_progress(100)

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--window-position=-2000,-2000",
                    "--window-size=1280,800"
                ]
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800}
            )
            try:
                semaphore = asyncio.Semaphore(3)

                async def process_shop(shop_key, parser_func):
                    async with semaphore:
                        page = await context.new_page()
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
                    await context.close()
                    await browser.close()
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

        self.start_button = self.ui.StartButton
        self.start_button.clicked.connect(self.start_worker)

        self.ui.AshanButton.clicked.connect(lambda: self.open_config("Ашан", "ashan.json"))
        self.ui.SilpoButton.clicked.connect(lambda: self.open_config("Сільпо", "silpo.json"))
        self.ui.ATBButton.clicked.connect(lambda: self.open_config("АТБ", "atb.json"))
        self.ui.FozzyButton.clicked.connect(lambda: self.open_config("Фоззі", "fozzy.json"))
        self.ui.NovusButton.clicked.connect(lambda: self.open_config("Новус", "novus.json"))
        self.ui.ForaButton.clicked.connect(lambda: self.open_config("Фора", "fora.json"))
        self.ui.VarusButton.clicked.connect(lambda: self.open_config("Варус", "varus.json"))
        self.ui.MetroButton.clicked.connect(lambda: self.open_config("Метро", "metro.json"))
        self.ui.TavriaButton.clicked.connect(lambda: self.open_config("Таврія", "tavria.json"))

    def open_config(self, shop_name: str, json_filename: str):
        dialog = ConfigDialog(shop_name, json_filename, self)
        dialog.exec()

    def update_progress(self, shop_key: str, value: int):
        if shop_key in self.progress_bars:
            self.progress_bars[shop_key].setValue(value)

    def start_worker(self):
        if self.thread is not None and self.thread.isRunning():
            return

        for pb in self.progress_bars.values():
            pb.setValue(0)

        self.start_button.setEnabled(False)
        self.thread = QThread(self)

        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.show_error)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker_finished)

        self.thread.start()

    def show_error(self, message):
        print(f"Parser error: {message}")
        QMessageBox.warning(self, "Інформація", str(message))

    def worker_finished(self):
        self.start_button.setEnabled(True)
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)
        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = Widget()
    widget.show()

    sys.exit(app.exec())
