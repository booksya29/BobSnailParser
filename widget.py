# This Python file uses the following encoding: utf-8

import asyncio
import importlib
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QObject, QThread, Signal

from ui_form import Ui_Widget
from config_dialog import ConfigDialog


SRC_DIR = Path(__file__).resolve().parent / "src"


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
        if str(SRC_DIR) not in sys.path:
            sys.path.insert(0, str(SRC_DIR))

        parsers = self._load_parsers()
        if not parsers:
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
            finally:
                on_progress(100)

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(viewport={"height": 1, "width": 1})
            try:
                pages = await asyncio.gather(*(context.new_page() for _ in parsers))
                results = await asyncio.gather(
                    *(run_shop(key, parser, page) for (key, parser), page in zip(parsers, pages)),
                    return_exceptions=True,
                )
                errors = [str(result) for result in results if isinstance(result, Exception)]
                if errors:
                    raise RuntimeError("\n".join(errors))
            finally:
                await browser.close()

    @staticmethod
    def _load_parsers():
        if str(SRC_DIR) not in sys.path:
            sys.path.insert(0, str(SRC_DIR))

        module_names = (
            ("atb", "atb_async_parser_product", "atb_all_parsing"),
            ("ashan", "ashan_parser_product", "ashan_parsing_all"),
            ("novus", "novus_parser_product", "novus_parsing_all"),
            ("fozzy", "fozzy_parser_product", "fozzy_parsing_all"),
            ("fora", "fora_parser_product", "fora_parsing_all"),
            ("tavria", "tavria_parser_product", "tavria_parsing_all"),
            ("silpo", "silpo_parser_product", "silpo_parsing_all"),
            ("varus", "varus_parser_product", "varus_parsing_all"),
            ("metro", "metro_[arser_product", "metro_parsing_all"),
        )

        original_run = asyncio.run

        def skip_standalone_runner(coroutine):
            coroutine.close()

        try:
            asyncio.run = skip_standalone_runner
            modules = [importlib.import_module(name) for _, name, _ in module_names]
        finally:
            asyncio.run = original_run

        return [(key, getattr(module, function_name)) for module, (key, _, function_name) in zip(modules, module_names)]


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

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

    def worker_finished(self):
        self.start_button.setEnabled(True)
        self.thread = None
        self.worker = None


if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = Widget()
    widget.show()

    sys.exit(app.exec())
