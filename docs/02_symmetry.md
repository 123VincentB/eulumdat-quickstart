# Step 2 — Detecting and applying photometric symmetry

EULUMDAT files store the `ISYM` field to declare the symmetry of the
photometric distribution. When a luminaire is symmetric, only a subset of
C-planes needs to be stored — the rest can be reconstructed.

| ISYM | Description | C-planes stored |
|------|-------------|-----------------|
| 0 | No symmetry — raw measurement | All |
| 1 | Full rotational symmetry | 1 (C=0° only) |
| 2 | Symmetry about C0–C180 | C=0°…180° |
| 3 | Symmetry about C90–C270 | C=90°…270° |
| 4 | Quarter symmetry | C=0°…90° |

Our two sample files represent the same luminaire:
- `sample_isym0.ldt` — ISYM=0, 991 lines (raw measurement)
- `sample_isym4.ldt` — ISYM=4, 362 lines (symmetrised, quarter symmetry)

Applying symmetry reduces file size and is a prerequisite for UGR calculation
(which requires ISYM=1 or ISYM=4).

---

```python
from pathlib import Path
from pyldt import LdtReader, LdtWriter
from ldt_symmetry import LdtAutoDetector, LdtSymmetriser

Path("output").mkdir(exist_ok=True)

ldt = LdtReader.read("samples/sample_isym0.ldt")
print(f"Original ISYM    : {ldt.header.isym}")
print(f"C-planes stored  : {ldt.header.mc}")

# Automatic detection
detector = LdtAutoDetector()
detected_isym = detector.detect(ldt)
print(f"Detected symmetry: ISYM={detected_isym}")

# Apply symmetrisation — returns a new Ldt, original is never modified
ldt_sym = LdtSymmetriser.symmetrise(ldt, isym=detected_isym)
print(f"After symmetrisation: ISYM={ldt_sym.header.isym}, C-planes={ldt_sym.header.mc}")

# Write the symmetrised file
LdtWriter.write(ldt_sym, "output/sample_symmetrised.ldt", overwrite=True)
print("Written: output/sample_symmetrised.ldt")
```

Expected output:

```
Original ISYM    : 0
C-planes stored  : 24
Detected symmetry: ISYM=4
After symmetrisation: ISYM=4, C-planes=24
Written: output/sample_symmetrised.ldt
```

> **Note:** the `Ldt` object in memory always keeps the full 24-C-plane matrix.
> `LdtWriter` compresses it to 7 C-planes when writing to disk
> (`compress_symmetry=True` by default). When the file is read back by
> `LdtReader`, the full matrix is reconstructed automatically. All downstream
> packages always work with the complete matrix — symmetry handling is
> transparent.

---

Script: [`scripts/step_02_symmetry.py`](../scripts/step_02_symmetry.py)

**Next step →** [Step 3 — Polar intensity diagram](03_plot.md)
