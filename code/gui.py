# gui.py
import os, pathlib
from functools import partial
from typing import Callable, Dict

os.environ["KIVY_WINDOW"] = "egl_rpi"        # before importing Kivy
from kivy.config import Config               # type: ignore
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'minimum_width',  '800')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '1')
Config.write()

from kivy.app import App                     # type: ignore
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel

from motors import TARGETS

# ---------------------------------------------------------------------------
_IMAGE_DIR = pathlib.Path("/home/pi/telescope/images")
DEFAULT_IMG = _IMAGE_DIR / "haumea.png"
IMAGE_MAP: Dict[str, pathlib.Path] = {
    "Earth": _IMAGE_DIR / "—Pngtree—beautiful_earth_elements_3704319.png",
    "Moon":  _IMAGE_DIR / "image-from-rawpixel-id-6731107-png.png",
    "Sun":   _IMAGE_DIR / "sun.png",
    "Mercury": _IMAGE_DIR / "mercury.png",
    "Venus":   _IMAGE_DIR / "venus.png",
    "Mars":    _IMAGE_DIR / "mars.png",
    "Jupiter": _IMAGE_DIR / "jupiter.png",
    "Saturn":  _IMAGE_DIR / "saturn.png",
    "Uranus":  _IMAGE_DIR / "uranus.png",
    "Neptune": _IMAGE_DIR / "neptune.png",
}

# ---------------------------------------------------------------------------
class TelescopeGUI(TabbedPanel):
    """A single-tab panel that shows target data and selection buttons."""

    def __init__(self, on_select: Callable[[str], None], snapshot: Callable[[], Dict[str,str]], **kw):
        super().__init__(**kw)
        self.on_select  = on_select
        self.snapshot   = snapshot
        self.tab_pos    = "bottom_left"
        self.default_tab_text = "Select Target"

        self._planet_img   = Image(size_hint=(None,1), width=500)
        self._target_label = Label(font_size=50, size_hint=(None,None), size=(400,80))
        self._info_labels  = [Label(font_size=35, size_hint=(None,None), size=(400,40))
                              for _ in range(3)]  # alt/az, vis, dist/phase

        self._build_layout()
        self._refresh()                # initial fill

    # --------------------------------------------------------------------
    def _build_layout(self) -> None:
        parent = BoxLayout(orientation='vertical')
        top    = BoxLayout(size_hint_y=0.5, padding=10)
        text_v = BoxLayout(orientation='vertical', size_hint=(None,None),
                           size=(400,300), padding=[300,0,0,100])

        text_v.add_widget(self._target_label)
        for lab in self._info_labels:
            text_v.add_widget(lab)

        top.add_widget(self._planet_img)
        top.add_widget(text_v)

        # bottom grid of buttons
        bottom = GridLayout(cols=3, size_hint_y=0.5, padding=10, spacing=10)
        for tgt in TARGETS:
            nice = tgt.replace(" BARYCENTER","").title()
            btn = Button(text=nice, font_size=40)
            btn.bind(on_press=partial(self._clicked, tgt))
            bottom.add_widget(btn)

        parent.add_widget(top)
        parent.add_widget(bottom)
        self.default_tab_content = parent

    # --------------------------------------------------------------------
    def _clicked(self, target_raw: str, *_) -> None:
        self.on_select(target_raw)
        self._refresh()

    def _refresh(self, *_):
        data = self.snapshot()
        nice = data["target"]
        img  = IMAGE_MAP.get(nice, DEFAULT_IMG)
        self._planet_img.source = str(img)
        self._planet_img.reload()
        self._target_label.text = f"Current target: {nice}"
        self._info_labels[0].text = data["altaz"]
        self._info_labels[1].text = data["vis"]
        self._info_labels[2].text = f'{data["dist"]}  {data["phase"]}'
