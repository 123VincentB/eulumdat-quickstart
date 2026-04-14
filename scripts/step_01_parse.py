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
