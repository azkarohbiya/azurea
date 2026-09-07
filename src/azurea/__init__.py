"""azurea — matplotlib themes by azuka."""
from importlib.resources import files
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

__version__ = "0.2.2"

custom_colors = [
    '#5778a4', '#e49444', '#d1615d', '#85b6b2', '#6a9f58',
    '#e7ca60', '#a87c9f', '#f1a2b1', '#967662', '#b8b0ac',
    '#c47596', '#d3a7bc', '#7abf73', '#c4a444', '#4d9490',
    '#82b4b0', '#eec96a', '#9dc6e0', '#f5c07a', '#979797',
    '#c9aac6', '#82b4b0', '#e0705a',
]

_FONTS_REGISTERED = False
_STYLES_REGISTERED = False


def _register_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    fonts_dir = files(__package__) / "fonts"
    for f in fonts_dir.iterdir():
        if f.suffix.lower() in (".ttf", ".otf"):
            fm.fontManager.addfont(str(f))
    _FONTS_REGISTERED = True


def _register_styles():
    """Fallback loader in case the entry-point mechanism doesn't pick them up."""
    global _STYLES_REGISTERED
    if _STYLES_REGISTERED:
        return
    styles_dir = files(__package__) / "styles"
    for f in styles_dir.iterdir():
        if f.suffix == ".mplstyle":
            name = f"azurea.{f.stem}"
            plt.style.library[name] = mpl.rc_params_from_file(
                str(f), use_default_template=False
            )
    _core = getattr(plt.style, "core", None) or getattr(mpl, "style", None)
    if _core is not None and hasattr(_core, "available"):
        _core.available[:] = sorted(plt.style.library.keys())
    _STYLES_REGISTERED = True


def use(name: str = "react_dark"):
    """Convenience: azurea.use('react_dark') or azurea.use('react_light')."""
    _register_fonts()
    _register_styles()
    if not name.startswith("azurea."):
        name = f"azurea.{name}"
    plt.style.use(name)


def available():
    _register_styles()
    return sorted(n for n in plt.style.available if n.startswith("azurea."))


_register_fonts()
_register_styles()
