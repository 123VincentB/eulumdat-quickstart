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
