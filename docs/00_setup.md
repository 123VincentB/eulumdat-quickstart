# Setting up your environment

This guide walks through creating a Python virtual environment and installing
all `eulumdat-*` packages. All steps are run from the root of this repository.

---

## 1. Check Python version

Python 3.9 or later is required.

```bash
python --version      # Windows
python3 --version     # Linux / macOS
```

> Throughout this guide, Linux and macOS users should replace `python` with
> `python3` where needed.

---

## 2. Create a virtual environment

```bash
# Windows
python -m venv .venv

# Linux / macOS
python3 -m venv .venv
```

---

## 3. Activate the virtual environment

```bash
# Windows — Command Prompt
.venv\Scripts\activate.bat

# Windows — Git Bash
source .venv/Scripts/activate

# Linux / macOS
source .venv/bin/activate
```

Your prompt should now show `(.venv)`.

---

## 4. Install all packages

```bash
pip install eulumdat-py eulumdat-symmetry eulumdat-plot \
            eulumdat-luminance eulumdat-ugr eulumdat-analysis \
            eulumdat-report eulumdat-ies
```

---

## 5. Install Playwright (required only for PDF generation)

```bash
pip install playwright
playwright install chromium
```

> `playwright install chromium` downloads ~150 MB. If you don't need PDF
> output, you can skip this step — the HTML report works without Playwright.

---

## 6. Clone this repository

```bash
git clone https://github.com/123VincentB/eulumdat-quickstart.git
cd eulumdat-quickstart
```

---

**Next step →** [Step 1 — Parsing an LDT file](01_parse.md)
