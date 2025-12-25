import subprocess
from pathlib import Path

def slice_stl(stl_path: str, printer_ini: str, output_path: str = None):
    """
    Slice an STL file using SuperSlicer headless with static INI.
    """
    stl_path = Path(stl_path)
    printer_ini = Path(printer_ini)
    if output_path is None:
        output_path = stl_path.with_suffix(".gcode")

    cmd = [
        "/Applications/SuperSlicer.app/Contents/MacOS/SuperSlicer",
        "--load", str(printer_ini),
        "--output", str(output_path),
        "--gcode",           # slice to G-code
        str(stl_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"Slicing finished! Output: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"Error during slicing:\n{e.stderr}"