# Step 6 — Beam half-angle (HAHM)

The half-angle at half maximum (HAHM) is the gamma-angle at which intensity
drops to 50% of its peak value, measured from the peak toward 90°. It
characterises beam spread in a single number per C-plane.

For a linear luminaire like our sample, C0/C180 (the narrow transversal plane)
and C90/C270 (the wide longitudinal plane) give very different results — this
is physically correct and expected.

The FWHM (Full Width at Half Maximum) combines two complementary C-planes:
`FWHM = half_angle(C) + half_angle(C+180°)`.

---

```python
from pathlib import Path
from pyldt import LdtReader
from ldt_analysis import half_angle

Path("output").mkdir(exist_ok=True)

ldt = LdtReader.read("samples/sample_isym4.ldt")

# Compute half-angles at half maximum (HAHM) for 4 C-planes
angles = half_angle(ldt, [0.0, 90.0, 180.0, 270.0])

print("Half-angles at half maximum (HAHM):")
for c_plane, angle in angles.items():
    if angle is not None:
        print(f"  C={c_plane:.0f} deg : gamma = {angle:.1f} deg")
    else:
        print(f"  C={c_plane:.0f} deg : not defined (wide beam or multi-peak)")

# FWHM from complementary C-planes
print()
ha_0   = angles.get(0.0)
ha_180 = angles.get(180.0)
if ha_0 is not None and ha_180 is not None:
    print(f"FWHM C0/C180   : {ha_0 + ha_180:.1f} deg")
else:
    print("FWHM C0/C180   : not defined")

ha_90  = angles.get(90.0)
ha_270 = angles.get(270.0)
if ha_90 is not None and ha_270 is not None:
    print(f"FWHM C90/C270  : {ha_90 + ha_270:.1f} deg")
else:
    print("FWHM C90/C270  : not defined")
```

Expected output:

```
Half-angles at half maximum (HAHM):
  C=0 deg : gamma = 14.8 deg
  C=90 deg : gamma = 29.7 deg
  C=180 deg : gamma = 14.8 deg
  C=270 deg : gamma = 29.7 deg

FWHM C0/C180   : 29.6 deg
FWHM C90/C270  : 59.4 deg
```

The narrow FWHM of 29.6° in C0/C180 reflects the thin 63 mm luminous area,
while the wide 59.4° in C90/C270 reflects the 1 480 mm length. `half_angle`
returns `None` for distributions that are too wide (intensity never crosses
I_max/2 before 90°), multi-peaked, or for C-planes not present in the data.

---

Script: [`scripts/step_06_analysis.py`](../scripts/step_06_analysis.py)

**Next step →** [Step 7 — Full photometric report](07_report.md)
