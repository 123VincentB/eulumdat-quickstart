# Step 7 — Full photometric report

`eulumdat-report` orchestrates the entire `eulumdat-*` ecosystem to generate a
complete photometric datasheet in HTML (and optionally PDF). It is available as
a CLI command and a Python API.

The report includes: identification bar, geometry card, lamp data card, polar
intensity diagram, polar luminance diagram, UGR table (ISYM=1 or 4 only), and
optionally a numerical luminance table. With `sample_isym4.ldt` (ISYM=4), the
UGR section will be present.

---

## Via CLI (simplest)

```bash
# HTML only (no Playwright required)
eulumdat-report samples/sample_isym4.ldt --no-pdf -o output/

# HTML + PDF (requires: pip install playwright && playwright install chromium)
eulumdat-report samples/sample_isym4.ldt -o output/
```

---

## Via Python API

```python
from pathlib import Path
from eulumdat_report import render_ugr_image, render_luminance_image
from eulumdat_report.collector import ReportCollector
from eulumdat_report.renderer import ReportRenderer

Path("output").mkdir(exist_ok=True)

# Collect all data from the LDT file
data = ReportCollector.collect("samples/sample_isym4.ldt")

# Generate HTML report
html = ReportRenderer.render_html(data)
Path("output/report.html").write_text(html, encoding="utf-8")
print("Report written: output/report.html")
print("Open output/report.html in your browser.")

# Bonus — PNG exports for Word / docxtpl
try:
    ugr_png = render_ugr_image(data)
    Path("output/ugr_table.png").write_bytes(ugr_png)
    print("PNG written: output/ugr_table.png")

    lum_png = render_luminance_image(data)
    Path("output/luminance_table.png").write_bytes(lum_png)
    print("PNG written: output/luminance_table.png")
except ImportError:
    print("Playwright not installed — skipping PNG exports.")
    print("Run: pip install playwright && playwright install chromium")
```

Expected output:

```
Report written: output/report.html
Open output/report.html in your browser.
PNG written: output/ugr_table.png
PNG written: output/luminance_table.png
```

> Open `output/report.html` in your browser. This is the complete A4
> photometric datasheet including all diagrams and the UGR catalogue table.

> `ReportRenderer` and `ReportCollector` are imported from submodules —
> only `render_ugr_image` and `render_luminance_image` are exported directly
> from the `eulumdat_report` package.

---

Script: [`scripts/step_07_report.py`](../scripts/step_07_report.py)

**Next step →** [Bonus — Working with IES files](08_ies.md)
