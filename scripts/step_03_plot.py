from pathlib import Path
from eulumdat_plot import plot_ldt_svg
from eulumdat_plot.export import svg_to_png

Path("output").mkdir(exist_ok=True)

# SVG output (vector, opens in any browser)
svg_str = plot_ldt_svg("samples/sample_isym4.ldt")
svg_path = Path("output/plot.svg")
svg_path.write_text(svg_str, encoding="utf-8")
print("SVG written: output/plot.svg")

# PNG output (raster, for Word or presentations)
svg_to_png(svg_path, "output/plot.png")
print("PNG written: output/plot.png")

print("Open output/plot.svg in your browser to see the polar intensity diagram.")
