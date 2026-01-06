# Simply Note It

Simply Note It is a minimalist desktop text editor written in Python with Tkinter. It focuses on the exact set of features needed for daily note taking: split panes (up to four at once), fast file operations, find, undo/redo, and customizable font sizing. The app is developed and run from WSL2 but renders natively on Windows via the Tk GUI toolkit, so it stays lightweight and portable with zero external dependencies beyond standard Python.

## Usage

```bash
python3 main_simple.py
```

Use the toolbar or familiar shortcuts (`Ctrl+N`, `Ctrl+O`, `Ctrl+S`, `Ctrl+Shift+H/V/W`, etc.) to work with files and panels. All linting is enforced via GitHub Actions using pylint. To contribute, ensure `pylint main_simple.py` passes locally before opening a pull request.
