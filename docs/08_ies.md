# Bonus — Working with IES files

The `eulumdat-ies` package bridges the EULUMDAT (.ldt) and IES LM-63-2002
(.ies) formats. It provides two conversion functions and two matching CLI
commands.

> **Note:** IES files encode luminous intensity in a different coordinate
> system. The conversion is lossy for some metadata fields (manufacturer,
> lamp type, etc. map to IES keywords), but the photometric data (intensity
> matrix) is preserved exactly.

---

## Install

`eulumdat-ies` is not included in the base `requirements.txt` because it is an
optional add-on. Install it separately:

```bash
pip install eulumdat-ies
```

---

## Via CLI

```bash
# IES → LDT
ies-to-ldt samples/sample.ies -o output/

# LDT → IES
ldt-to-ies samples/sample_isym4.ldt -o output/
```

Both commands accept a single file argument and an optional `-o / --output-dir`
flag (defaults to the source file's directory).

---

## Via Python API

```python
from pathlib import Path
from eulumdat_ies import ies_to_ldt, ldt_to_ies
from pyldt import LdtReader, LdtWriter

Path("output").mkdir(exist_ok=True)

# LDT → IES
ldt = LdtReader.read("samples/sample_isym4.ldt")
ldt_to_ies(ldt, "output/sample_isym4.ies")
print("IES written: output/sample_isym4.ies")

# IES → LDT (round-trip)
ldt_back = ies_to_ldt("output/sample_isym4.ies")
LdtWriter.write(ldt_back, "output/sample_isym4_roundtrip.ldt", overwrite=True)
print("LDT written: output/sample_isym4_roundtrip.ldt")

# After IES → LDT the symmetry is always ISYM=0 (full 360-degree matrix).
# Use eulumdat-symmetry to re-detect the actual symmetry class:
from ldt_symmetry import detect_symmetry
isym = detect_symmetry(ldt_back)
print(f"Detected symmetry: ISYM={isym}")
```

Expected output:

```
IES written: output/sample_isym4.ies
LDT written: output/sample_isym4_roundtrip.ldt
Detected symmetry: ISYM=4
```

> After an IES → LDT conversion the resulting object always carries `ISYM=0`
> (no assumed symmetry) because the IES format does not encode the EULUMDAT
> symmetry class. Call `detect_symmetry` from `eulumdat-symmetry` to recover
> the correct `ISYM` value before running UGR calculations or writing the
> file for downstream tools that rely on symmetry metadata.

---

**Back to start →** [Step 0 — Setting up your environment](00_setup.md)
