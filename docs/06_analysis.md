# Step 6 — Photometric analysis

`ldt_analysis` is a collection of standalone functions for practical
photometric calculations on EULUMDAT data. Each function takes a `Ldt`
object as its first argument and returns `None` for undefined or
pathological inputs — it never raises unhandled exceptions.

---

## 1. Beam half-angle (HAHM)

The half-angle at half maximum (HAHM) is the gamma-angle at which intensity
drops to 50% of its peak value, measured from the peak toward 90°. It
characterises beam spread in a single number per C-plane.

The FWHM (Full Width at Half Maximum) combines two complementary C-planes:
`FWHM = half_angle(C) + half_angle(C+180°)`.

```python
from pyldt import LdtReader
from ldt_analysis import half_angle

ldt4 = LdtReader.read("samples/sample_isym4.ldt")

angles = half_angle(ldt4, [0.0, 90.0, 180.0, 270.0])
print("HAHM per C-plane:")
for c_plane, angle in angles.items():
    if angle is not None:
        print(f"  C={c_plane:.0f} deg : gamma = {angle:.1f} deg")
    else:
        print(f"  C={c_plane:.0f} deg : not defined (wide beam or multi-peak)")

ha_0, ha_180 = angles.get(0.0), angles.get(180.0)
ha_90, ha_270 = angles.get(90.0), angles.get(270.0)
print()
if ha_0 is not None and ha_180 is not None:
    print(f"FWHM C0/C180  : {ha_0 + ha_180:.1f} deg")
if ha_90 is not None and ha_270 is not None:
    print(f"FWHM C90/C270 : {ha_90 + ha_270:.1f} deg")
```

Expected output:

```
HAHM per C-plane:
  C=0 deg : gamma = 14.8 deg
  C=90 deg : gamma = 29.7 deg
  C=180 deg : gamma = 14.8 deg
  C=270 deg : gamma = 29.7 deg

FWHM C0/C180  : 29.6 deg
FWHM C90/C270 : 59.4 deg
```

The narrow FWHM of 29.6° in C0/C180 reflects the thin 63 mm luminous area,
while the wide 59.4° in C90/C270 reflects the 1 480 mm length. `half_angle`
returns `None` for distributions that are too wide (intensity never crosses
I_max/2 before 90°), multi-peaked, or for C-planes absent from the data.

---

## 2. Angular resampling

`resample` resamples an LDT to a target angular resolution via linear
interpolation — first along gamma (per C-plane), then along C with circular
continuity at 360°. The source object is never mutated.

It returns `None` if the target resolution is finer than the source (it
will not extrapolate), or if the grid is too coarse to interpolate (fewer
than 2 planes or angles).

The main use case is normalising files from goniophotometers that produce
non-standard resolutions (e.g., 2.5°×1° or 5°×2°) to the standard 15°×5°
grid required by most downstream tools.

```python
from pyldt import LdtReader
from ldt_analysis import resample

ldt0 = LdtReader.read("samples/sample_isym0.ldt")

# sample_isym0 is already at 15x5 deg (24x37); resample to 30x10 to demonstrate
ldt_r = resample(ldt0, c_step=30.0, g_step=10.0)
if ldt_r is not None:
    n_c_src, n_g_src = len(ldt0.header.c_angles), len(ldt0.header.g_angles)
    n_c_dst, n_g_dst = len(ldt_r.header.c_angles), len(ldt_r.header.g_angles)
    print(f"resample (15x5 deg -> 30x10 deg): {n_c_src}x{n_g_src} -> {n_c_dst}x{n_g_dst}")

# Requesting finer than source returns None
ldt_r_fail = resample(ldt0, c_step=5.0, g_step=1.0)
print(f"resample (to 5x1 deg, finer than source): {ldt_r_fail}")
```

Expected output:

```
resample (15x5 deg -> 30x10 deg): 24x37 -> 12x19
resample (to 5x1 deg, finer than source): None
```

In production, the typical call is `resample(ldt_raw)` with default
arguments (`c_step=15.0, g_step=5.0`) to normalise a fine-resolution
measurement file to the standard grid.

---

## 3. Photometric consistency

`check_photometric_consistency` compares the LORL and DFF values declared
in the header against values computed by integrating the intensity matrix.
It returns a dict with both values, the delta, and the total luminous flux.

```python
from pyldt import LdtReader
from ldt_analysis import check_photometric_consistency

ldt4 = LdtReader.read("samples/sample_isym4.ldt")

rep = check_photometric_consistency(ldt4)
print("check_photometric_consistency (sample_isym4):")
print(f"  LORL  header={rep['lorl_header']:.1f}%  computed={rep['lorl_computed']:.1f}%  delta={rep['lorl_delta']:+.2f} pp")
print(f"  DFF   header={rep['dff_header']:.1f}%  computed={rep['dff_computed']:.1f}%  delta={rep['dff_delta']:+.2f} pp")
print(f"  Flux  {rep['flux_lm_klm']:.1f} lm/klm", end="")
if rep["flux_lm_abs"] is not None:
    print(f"  ({rep['flux_lm_abs']:.0f} lm absolute)")
else:
    print("  (absolute flux: n/a)")
```

Expected output:

```
check_photometric_consistency (sample_isym4):
  LORL  header=100.0%  computed=101.2%  delta=+1.19 pp
  DFF   header=100.0%  computed=100.0%  delta=-0.00 pp
  Flux  1011.9 lm/klm  (12481 lm absolute)
```

The +1.19 pp LORL delta is within the expected range for real-world files
— it comes from measurement uncertainty and the fact that the lamp flux
declared in the header is typically rounded by the manufacturer.

The individual functions are also available directly:

```python
from ldt_analysis import luminous_flux, lorl_computed, dff_computed

flux = luminous_flux(ldt4)    # lm/klm, independent of declared lamp flux
lorl = lorl_computed(ldt4)   # %  — equals flux / 10
dff  = dff_computed(ldt4)    # %  — downward hemisphere only
```

---

## 4. Flux by angular zone

`luminous_flux_range` integrates flux over any gamma window [g_min, g_max],
using the same CIE 190 trapezoidal method as `luminous_flux`. Zones
partially overlapping the window boundaries are handled by linear
interpolation.

A typical use: split total flux into direct (downward, 0–90°) and upward
(90–180°) fractions to characterise the luminaire's optical distribution.

```python
from pyldt import LdtReader
from ldt_analysis import luminous_flux, luminous_flux_range

ldt4 = LdtReader.read("samples/sample_isym4.ldt")

flux_total = luminous_flux(ldt4)
flux_down  = luminous_flux_range(ldt4, 0.0, 90.0)
flux_up    = luminous_flux_range(ldt4, 90.0, 180.0)

print("Flux by angular zone (sample_isym4):")
if flux_total is not None:
    print(f"  total (0-180 deg)   : {flux_total:.1f} lm/klm")
if flux_down is not None:
    print(f"  downward (0-90 deg) : {flux_down:.1f} lm/klm")
if flux_up is not None:
    print(f"  upward (90-180 deg) : {flux_up:.1f} lm/klm")
```

Expected output:

```
Flux by angular zone (sample_isym4):
  total (0-180 deg)   : 1011.9 lm/klm
  downward (0-90 deg) : 1011.9 lm/klm
  upward (90-180 deg) : 0.0 lm/klm
```

The upward fraction of 0.0 lm/klm confirms that this is a purely direct
luminaire — all emitted light falls between 0° (nadir) and 90° (horizontal).
`luminous_flux(ldt)` is exactly equivalent to
`luminous_flux_range(ldt, 0.0, 180.0)`.

---

## 5. Azimuthal rotation

`rotate` shifts every C-plane profile by `alpha` degrees, producing a new
`Ldt` object with `ISYM=0`. The source object is never mutated. `alpha`
must be a multiple of the file's C-plane step (±1e-9 tolerance);
a `ValueError` is raised otherwise.

The main use case is reorienting an asymmetric luminaire measurement before
archiving, symmetrising, or feeding into a lighting design tool.

```python
from pathlib import Path
from pyldt import LdtReader, LdtWriter
from ldt_analysis import rotate

ldt0 = LdtReader.read("samples/sample_isym0.ldt")

ldt_rot = rotate(ldt0, 90.0)
print(f"rotate sample_isym0 by 90 deg:")
print(f"  input  ISYM={ldt0.header.isym}, {len(ldt0.header.c_angles)} C-planes")
print(f"  output ISYM={ldt_rot.header.isym}, {len(ldt_rot.header.c_angles)} C-planes")

# After +90 deg, the profile at C=0 moves to C=90
idx_src = ldt0.header.c_angles.index(0.0)
idx_dst = ldt_rot.header.c_angles.index(90.0)
profiles_match = all(
    abs(a - b) < 1e-9
    for a, b in zip(ldt0.intensities[idx_src], ldt_rot.intensities[idx_dst])
)
print(f"  C=0 before == C=90 after : {profiles_match}")

LdtWriter.write(ldt_rot, "output/sample_isym0_rotated90.ldt", overwrite=True)
print("  written: output/sample_isym0_rotated90.ldt")
```

Expected output:

```
rotate sample_isym0 by 90 deg:
  input  ISYM=0, 24 C-planes
  output ISYM=0, 24 C-planes
  C=0 before == C=90 after : True
  written: output/sample_isym0_rotated90.ldt
```

The rotated file can be passed directly to any other package in the
ecosystem (`eulumdat-plot`, `eulumdat-luminance`, etc.).

---

Script: [`scripts/step_06_analysis.py`](../scripts/step_06_analysis.py)

**Next step →** [Step 7 — Full photometric report](07_report.md)
