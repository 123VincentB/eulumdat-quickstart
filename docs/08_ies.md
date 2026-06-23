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
from pyldt import LdtReader, LdtWriter
from eulumdat_ies import ldt_to_ies, ies_to_ldt
from ldt_symmetry import LdtAutoDetector

Path("output").mkdir(exist_ok=True)

# LDT → IES
ldt = LdtReader.read("samples/sample_isym4.ldt")
ldt_to_ies(ldt, "output/sample_isym4.ies")
print("IES written: output/sample_isym4.ies")

# IES → LDT (round-trip)
ldt_back = ies_to_ldt("output/sample_isym4.ies")
LdtWriter.write(ldt_back, "output/sample_isym4_roundtrip.ldt", overwrite=True)
print("LDT written: output/sample_isym4_roundtrip.ldt")

# After IES -> LDT the result always carries ISYM=0 (the IES format does not
# encode EULUMDAT symmetry). Use LdtAutoDetector to recover the correct value.
print(f"ISYM on roundtrip object : {ldt_back.header.isym}")
detected = LdtAutoDetector().detect(ldt_back)
print(f"Detected symmetry        : ISYM={detected}")
```

Expected output:

```
IES written: output/sample_isym4.ies
LDT written: output/sample_isym4_roundtrip.ldt
ISYM on roundtrip object : 0
Detected symmetry        : ISYM=4
```

> After an IES → LDT conversion the resulting object always carries `ISYM=0`
> because the IES format does not encode the EULUMDAT symmetry class.
> Use `LdtAutoDetector().detect(ldt)` from `eulumdat-symmetry` to recover
> the correct `ISYM` value before running UGR calculations or writing the
> file for downstream tools that rely on symmetry metadata.

---

Script: [`scripts/step_08_ies.py`](../scripts/step_08_ies.py)

**Back to start →** [Step 0 — Setting up your environment](00_setup.md)
