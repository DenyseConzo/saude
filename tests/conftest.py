import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class FakePage:
    """Página mínima para construir ecrãs sem abrir janela."""

    width = 400
    height = 800

    def __init__(self):
        self.dialogs = []
        self.urls = []
        self.tasks = []
        self.controls = []

    def update(self, *a):
        pass

    def add(self, *controls):
        self.controls.extend(controls)

    def show_dialog(self, d):
        self.dialogs.append(d)

    def pop_dialog(self):
        if self.dialogs:
            self.dialogs.pop()

    def launch_url(self, url, **kw):
        self.urls.append(url)

    def run_task(self, handler, *args, **kw):
        self.tasks.append(handler)


@pytest.fixture
def app():
    from ui.app import App

    a = App(FakePage())
    a.store.onboarded = True
    return a
