# main.py
import asyncio
import threading
import os

from kivy.app import App          # type: ignore

from motors import TelescopeMount
from gui import TelescopeGUI

os.putenv('SDL_MOUSEDRV', 'TSLIB')  # for your touchscreen driver

mount = TelescopeMount('MOON')      # default target

def _start_asyncio_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.create_task(mount.run_loop())
    loop.run_forever()

class _App(App):
    def build(self):
        return TelescopeGUI(
            on_select=self._on_select,
            snapshot=mount.snapshot
        )

    def _on_select(self, new_target: str) -> None:
        mount.target = new_target

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    thread = threading.Thread(
        target=_start_asyncio_in_thread,
        args=(loop,),
        daemon=True
    )
    thread.start()
    _App().run()
