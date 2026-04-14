# Step 4 — Luminance table and polar diagram

Luminance (cd/m²) is derived from intensity (cd/klm) and the luminous area
geometry. It is the quantity directly responsible for glare perception — a
luminaire with high luminance at shallow angles above the horizontal will cause
discomfort regardless of total flux. It is also the input required for UGR
calculation (Step 5).

The conversion formula is:

```
L(C, gamma) = I(C, gamma) / A_proj(C, gamma)
```

where `A_proj` is the projected luminous area of the luminaire as seen from
direction (C, gamma). `eulumdat-luminance` computes both.

---

```python
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
```

Expected output:

```
Peak luminance: 5603 cd/m2
Table written: output/luminance_table.csv
Table written: output/luminance_table.json
SVG written: output/luminance.svg
PNG written: output/luminance.png
```

The table covers 5 elevation angles (65°, 70°, 75°, 80°, 85°) across 24
C-planes (0° to 345° in 15° steps) — the standard UGR grid defined by
CIE 190. The polar diagram shows all 24 C-planes simultaneously, with a red
dashed circle at 3 000 cd/m² marking the typical glare threshold.

> The peak luminance of 5 603 cd/m² indicates that this luminaire exceeds
> the 3 000 cd/m² threshold — this is clearly visible in the polar diagram
> as curves that extend beyond the red circle.

---

Script: [`scripts/step_04_luminance.py`](../scripts/step_04_luminance.py)

**Next step →** [Step 5 — UGR catalogue](05_ugr.md)
