from pathlib import Path
from pyldt import LdtReader, LdtWriter
from ldt_analysis import (
    half_angle,
    resample,
    luminous_flux, luminous_flux_range,
    lorl_computed, dff_computed, check_photometric_consistency,
    rotate,
)

Path("output").mkdir(exist_ok=True)

ldt0 = LdtReader.read("samples/sample_isym0.ldt")
ldt4 = LdtReader.read("samples/sample_isym4.ldt")

# ── 1. half_angle ──────────────────────────────────────────────────────────
print("=== 1. half_angle ===")
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

# ── 2. resample ────────────────────────────────────────────────────────────
print()
print("=== 2. resample ===")
n_c_src = len(ldt0.header.c_angles)
n_g_src = len(ldt0.header.g_angles)

# sample_isym0 is already at 15x5 deg — resample to 30x10 to demonstrate
ldt_r = resample(ldt0, c_step=30.0, g_step=10.0)
if ldt_r is not None:
    n_c_dst = len(ldt_r.header.c_angles)
    n_g_dst = len(ldt_r.header.g_angles)
    print(f"resample (15x5 deg -> 30x10 deg): {n_c_src}x{n_g_src} -> {n_c_dst}x{n_g_dst}")
else:
    print("resample: source already at target resolution or finer")

# returns None when target is finer than source
ldt_r_fail = resample(ldt0, c_step=5.0, g_step=1.0)
print(f"resample (to 5x1 deg, finer than source): {ldt_r_fail}")

# ── 3. photometric consistency ─────────────────────────────────────────────
print()
print("=== 3. photometric consistency ===")
rep = check_photometric_consistency(ldt4)
print("check_photometric_consistency (sample_isym4):")
print(f"  LORL  header={rep['lorl_header']:.1f}%  computed={rep['lorl_computed']:.1f}%  delta={rep['lorl_delta']:+.2f} pp")
print(f"  DFF   header={rep['dff_header']:.1f}%  computed={rep['dff_computed']:.1f}%  delta={rep['dff_delta']:+.2f} pp")
print(f"  Flux  {rep['flux_lm_klm']:.1f} lm/klm", end="")
if rep["flux_lm_abs"] is not None:
    print(f"  ({rep['flux_lm_abs']:.0f} lm absolute)")
else:
    print("  (absolute flux: n/a)")

# ── 4. luminous_flux_range ─────────────────────────────────────────────────
print()
print("=== 4. luminous_flux_range ===")
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

# ── 5. rotate ──────────────────────────────────────────────────────────────
print()
print("=== 5. rotate ===")
ldt_rot = rotate(ldt0, 90.0)
print(f"rotate sample_isym0 by 90 deg:")
print(f"  input  ISYM={ldt0.header.isym}, {len(ldt0.header.c_angles)} C-planes")
print(f"  output ISYM={ldt_rot.header.isym}, {len(ldt_rot.header.c_angles)} C-planes")

# After +90 deg rotation, the profile at C=0 moves to C=90
idx_src = ldt0.header.c_angles.index(0.0)
idx_dst = ldt_rot.header.c_angles.index(90.0)
profiles_match = all(
    abs(a - b) < 1e-9
    for a, b in zip(ldt0.intensities[idx_src], ldt_rot.intensities[idx_dst])
)
print(f"  C=0 before == C=90 after : {profiles_match}")

LdtWriter.write(ldt_rot, "output/sample_isym0_rotated90.ldt", overwrite=True)
print("  written: output/sample_isym0_rotated90.ldt")
