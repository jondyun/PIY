import subprocess
import os

SUPERSLICER_PATH = "/Applications/SuperSlicer.app/Contents/MacOS/SuperSlicer"


def slice_stl(stl_path, printer_ini, infill_percent=None):
    output_gcode = os.path.splitext(stl_path)[0] + ".gcode"

    cmd = [
        SUPERSLICER_PATH,
        "--slice",
        "--load", printer_ini,
        "--output", output_gcode,
        stl_path
    ]

    if infill_percent is not None:
        cmd.append(f"--fill-density={infill_percent}%")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_gcode