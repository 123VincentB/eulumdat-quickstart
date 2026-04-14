from pathlib import Path
from pyldt import LdtReader
from eulumdat_ugr import UgrCalculator

Path("output").mkdir(exist_ok=True)

ldt = LdtReader.read("samples/sample_isym4.ldt")
result = UgrCalculator.compute(ldt)

# result.values is a numpy array of shape (19, 10)
# Rows  : 19 standard CIE 190 room configurations
#         indices 0-5  : X=2H, Y=2H..12H
#         indices 6-11 : X=4H, Y=2H..12H  →  4H x 8H = index 10
#         indices 12-15: X=8H, Y=4H..12H  →  8H x 4H = index 12
#         indices 16-18: X=12H, Y=4H..8H
# Columns: 0-4 = crosswise,  5-9 = endwise
#          column 0 / 5 = 70/50/20
#          column 1 / 6 = 70/30/20
#          column 2 / 7 = 50/50/20
#          column 3 / 8 = 50/30/20
#          column 4 / 9 = 30/30/20

IDX_4x8 = 10   # room 4H x 8H
IDX_8x4 = 12   # room 8H x 4H

print("Standard UGR catalogue values (reflectances 70/50/20, SHR=0.25):")
print(f"  4H x 8H  crosswise : {result.values[IDX_4x8, 0]:.1f}")
print(f"  4H x 8H  endwise   : {result.values[IDX_4x8, 5]:.1f}")
print(f"  8H x 4H  crosswise : {result.values[IDX_8x4, 0]:.1f}")
print(f"  8H x 4H  endwise   : {result.values[IDX_8x4, 5]:.1f}")

# Export the full 19-room table
result.to_csv("output/ugr_table.csv")
print("\nFull 19-room table written: output/ugr_table.csv")
Path("output/ugr_table.json").write_text(result.to_json(decimals=1, indent=2), encoding="utf-8")
print("Full 19-room table written: output/ugr_table.json")
