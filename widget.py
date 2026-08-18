# This Python file uses the following encoding: utf-8

import asyncio
import importlib
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QObject, QThread, Signal

from ui_form import Ui_Widget


SRC_DIR = Path(__file__).resolve().parent / "src"


class Worker(QObject):
    finished = Signal()
    failed = Signal(str)

    def run(self):
        try:
            asyncio.run(self._parse_all_shops())
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            self.finished.emit()

    async def _parse_all_shops(self):
        """Run every existing `*_parsing_all` backend function concurrently."""
        if str(SRC_DIR) not in sys.path:
            sys.path.insert(0, str(SRC_DIR))

        parsers = self._load_parsers()
        from patchright.async_api import async_playwright

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(viewport={"height": 1, "width": 1})
            try:
                pages = await asyncio.gather(*(context.new_page() for _ in parsers))
                results = await asyncio.gather(
                    *(parser(page) for parser, page in zip(parsers, pages)),
                    return_exceptions=True,
                )
                errors = [str(result) for result in results if isinstance(result, Exception)]
                if errors:
                    raise RuntimeError("\n".join(errors))
            finally:
                await browser.close()

    @staticmethod
    def _load_parsers():
        """Import backend modules without executing their standalone test runners."""
        if str(SRC_DIR) not in sys.path:
            sys.path.insert(0, str(SRC_DIR))

        module_names = (
            ("atb_async_parser_product", "atb_all_parsing"),
            ("ashan_parser_product", "ashan_parsing_all"),
            ("novus_parser_product", "novus_parsing_all"),
            ("fozzy_parser_product", "fozzy_parsing_all"),
            ("fora_parser_product", "fora_parsing_all"),
            ("tavria_parser_product", "tavria_parsing_all"),
            ("silpo_parser_product", "silpo_parsing_all"),
        )

        original_run = asyncio.run

        def skip_standalone_runner(coroutine):
            coroutine.close()

        try:
            asyncio.run = skip_standalone_runner
            modules = [importlib.import_module(name) for name, _ in module_names]
        finally:
            asyncio.run = original_run

        return [getattr(module, function_name) for module, (_, function_name) in zip(modules, module_names)]


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)


        self.thread = None
        self.worker = None

        self.start_button = self.ui.StartButton
        self.start_button.clicked.connect(self.start_worker)

    def start_worker(self):
        if self.thread is not None and self.thread.isRunning():
            return

        self.start_button.setEnabled(False)
        self.thread = QThread(self)


        self.worker = Worker()


        self.worker.moveToThread(self.thread)


        self.thread.started.connect(self.worker.run)

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
