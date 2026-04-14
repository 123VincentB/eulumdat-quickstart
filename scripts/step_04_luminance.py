from pathlib import Path
from pyldt import LdtReader
from eulumdat_luminance import LuminanceCalculator, LuminancePlot

Path("output").mkdir(exist_ok=True)

ldt = LdtReader.read("samples/sample_isym4.ldt")
result = LuminanceCalculator.compute(ldt)

print(f"Peak luminance: {result.maximum:.0f} cd/m2")

# Export CSV and JSON tables
result.to_csv("output/luminance_table.csv")
print("Table written: output/luminance_table.csv")
result.to_json("output/luminance_table.json")
print("Table written: output/luminance_table.json")

# Polar diagram — SVG (vector)
plot = LuminancePlot(result)
svg_str = plot.polar_svg()
Path("output/luminance.svg").write_text(svg_str, encoding="utf-8")
print("SVG written: output/luminance.svg")

# Polar diagram — PNG (raster)
plot.polar("output/luminance.png")
print("PNG written: output/luminance.png")
