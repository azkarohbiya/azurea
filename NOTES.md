# Fix notes — azurea

Working branch for issues found while testing `pip install azurea` (v0.2.1) on
Python 3.14.7 + matplotlib 3.11.1 (Windows).

## Status: the library itself works on a clean modern install

`azurea.use("react_dark" / "react_light")`, `plt.style.use("azurea.react_*")`
(after `import azurea`), `plt.style.context(...)`, `azurea.custom_colors`,
and the bundled Poppins font all render correctly. Line/bar/scatter/histogram
demo notebook executes end-to-end with no errors.

So if `pip install azurea` failed "back then", it was almost certainly an
**install-time** failure, not a bug in azurea:

- matplotlib only shipped cp314 (Python 3.14) wheels from ~matplotlib 3.11.
  Before that, `pip install azurea` on 3.14 tried to **build matplotlib from
  source** and failed with C/compiler errors (freetype/png headers, etc.) —
  cryptic and unrelated to azurea.
- Fix: upgrade pip and matplotlib (`pip install -U pip matplotlib`), or use a
  Python version with matplotlib wheels. Nothing to change in azurea for this,
  but we bumped the metadata to be honest about support (below).

> TODO(azuka): paste the actual traceback you saw so we can confirm.

## Fixed on this branch

| # | File | Problem | Fix |
|---|------|---------|-----|
| 1 | `pyproject.toml` | `Homepage` pointed at `github.com/azkaram/azurea` (wrong user) | → `github.com/azkarohbiya/azurea` |
| 2 | `pyproject.toml` | `requires-python = ">=3.8"` but `__init__.py` uses `importlib.resources.files()`, added in **3.9** — install/import breaks on 3.8 | → `">=3.9"` |
| 3 | `pyproject.toml` | `[project.entry-points."matplotlib.style"]` — matplotlib has **no** `matplotlib.style` entry-point group; these did nothing, and the value syntax `"azurea.styles:react_dark.mplstyle"` isn't a valid entry-point ref | removed; `_register_styles()` in `__init__.py` is what actually registers the styles |

## Still open for discussion

- **`_register_styles()` is doing fragile internals surgery.** Its docstring
  says it's a "fallback" for an entry-point mechanism that doesn't exist — it's
  actually the *only* path. It also pokes `plt.style.core` / `mpl.style.available`
  directly; `matplotlib.style.core` was made private and unimported in mpl 3.11,
  so the `getattr(plt.style, "core", None)` branch is now always `None`. Works
  today via the `mpl.style` fallback, but worth simplifying to just:
  `plt.style.library[name] = ...; plt.style.reload_library()`-free approach, or
  updating `matplotlib.style.available` in a documented way.
- **`font.family: Poppins` hard-coded in the `.mplstyle` files.** If font
  registration ever fails, every plot spams `findfont` warnings. Consider a
  fallback stack: `font.family: Poppins, DejaVu Sans, sans-serif`.
- `dependencies = ["matplotlib>=3.7"]` — the `.mplstyle` keys used
  (`axes.grid.axis`, `xtick.labelcolor`, …) are all ≥3.4, fine, but worth a
  quick CI matrix (3.9–3.14 × matplotlib 3.7/latest).
