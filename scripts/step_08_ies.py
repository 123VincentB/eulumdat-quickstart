from pathlib import Path
from pyldt import LdtReader, LdtWriter
from eulumdat_ies import ldt_to_ies, ies_to_ldt
from ldt_symmetry import LdtAutoDetector

Path("output").mkdir(exist_ok=True)

# ── LDT → IES ──────────────────────────────────────────────────────────────
ldt = LdtReader.read("samples/sample_isym4.ldt")
ldt_to_ies(ldt, "output/sample_isym4.ies")
print("IES written: output/sample_isym4.ies")

# ── IES → LDT (round-trip) ─────────────────────────────────────────────────
ldt_back = ies_to_ldt("output/sample_isym4.ies")
LdtWriter.write(ldt_back, "output/sample_isym4_roundtrip.ldt", overwrite=True)
print("LDT written: output/sample_isym4_roundtrip.ldt")

# After IES -> LDT the result always carries ISYM=0 (the IES format does not
# encode EULUMDAT symmetry). Use LdtAutoDetector to recover the correct value.
print(f"ISYM on roundtrip object : {ldt_back.header.isym}")
detected = LdtAutoDetector().detect(ldt_back)
print(f"Detected symmetry        : ISYM={detected}")
