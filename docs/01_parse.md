# Step 1 — Parsing an LDT file

`eulumdat-py` is the foundation of the ecosystem. It reads and writes EULUMDAT
files with zero external dependencies (Python standard library only). Every
other package builds on top of it.

An EULUMDAT file has two sections:
- **Header** — luminaire metadata (name, manufacturer, geometry), lamp data
  (flux, wattage), and photometric factors (LORL, DFF)
- **Intensity matrix** — values in cd/klm across C-planes and gamma-angles

**Key rule:** `eulumdat-py` always reconstructs the full `[C-planes × gamma-angles]`
matrix regardless of the ISYM symmetry code stored in the file. All downstream
packages always receive a complete matrix.

---

```python
from pyldt import LdtReader

ldt = LdtReader.read("samples/sample_isym0.ldt")

# Identification
print(f"Company          : {ldt.header.company}")
print(f"Luminaire name   : {ldt.header.luminaire_name}")
print(f"Date / user      : {ldt.header.date_user}")

# Geometry (mm)
print(f"Length           : {ldt.header.length} mm")
print(f"Width            : {ldt.header.width} mm")
print(f"Height           : {ldt.header.height} mm")

# Lamp data
print(f"Lamp flux        : {ldt.header.lamp_flux} lm")
print(f"Lamp wattage     : {ldt.header.lamp_watt} W")

# Symmetry and angular grid
print(f"ISYM             : {ldt.header.isym}  (0 = raw measurement, all C-planes stored)")
print(f"C-planes (mc)    : {ldt.header.mc}")
print(f"Gamma angles (ng): {ldt.header.ng}")

# Intensity matrix — always fully expanded by pyldt
print(f"Matrix shape     : {len(ldt.intensities)} C-planes x {len(ldt.intensities[0])} gamma-angles")
print(f"I(C=0, g=0)      : {ldt.intensities[0][0]:.4f} cd/klm")
```

Expected output:

```
Company          : company
Luminaire name   : sample
Date / user      : 21.03.2025/TC
Length           : 1480.0 mm
Width            : 65.0 mm
Height           : 10.0 mm
Lamp flux        : [12334.0] lm
Lamp wattage     : [66.8] W
ISYM             : 0  (0 = raw measurement, all C-planes stored)
C-planes (mc)    : 24
Gamma angles (ng): 37
Matrix shape     : 24 C-planes x 37 gamma-angles
I(C=0, g=0)      : 1461.5000 cd/klm
```

> `lamp_flux` and `lamp_watt` are lists — one element per lamp set. Most
> luminaires have a single lamp set, so index `[0]` is the only one.

---

Script: [`scripts/step_01_parse.py`](../scripts/step_01_parse.py)

**Next step →** [Step 2 — Detecting and applying photometric symmetry](02_symmetry.md)
