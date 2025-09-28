import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder="frontend", static_url_path="")

GCODE_DIR = "/app/gcodes"
CONFIG_PATH = "/app/config.ini"
SUPERSLICER = "/opt/superslicer/bin/superslicer"

os.makedirs(GCODE_DIR, exist_ok=True)

@app.route("/")
def index():
    # Serve the frontend UI
    return app.send_static_file("index.html")

@app.route("/slice", methods=["POST"])
def slice_stl():
    stl_file = request.files.get("stlFile")
    if not stl_file:
        return jsonify({"error": "No STL file provided"}), 400

    layer_height = request.form.get("layerHeight", "0.2")
    infill = request.form.get("infill", "20")

    # Save STL
    input_path = os.path.join(GCODE_DIR, "input.stl")
    stl_file.save(input_path)

    # Output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"sliced_{timestamp}.gcode"
    output_path = os.path.join(GCODE_DIR, output_file)

    # Build SuperSlicer command
    cmd = [
        SUPERSLICER,
        "--export-gcode",
        "--load", CONFIG_PATH,
        "--layer-height", str(layer_height),
        "--fill-density", str(infill),
        "--output", output_path,
        input_path
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return jsonify({
                "error": f"Slicing failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            }), 500

        return jsonify({
            "message": "Sliced OK",
            "download_url": f"/gcodes/{output_file}",
            "filename": output_file
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gcodes/<path:filename>")
def download_gcode(filename):
    return send_from_directory(GCODE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)