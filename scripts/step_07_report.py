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
