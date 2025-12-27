# piy/ui/stl_viewer.py

import numpy as np
import trimesh
import pyqtgraph.opengl as gl
from PySide6.QtWidgets import QWidget, QVBoxLayout


class STLViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=200)

        grid = gl.GLGridItem()
        grid.scale(10, 10, 1)
        self.view.addItem(grid)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.mesh_item = None

    def load_stl(self, path):
        mesh = trimesh.load(path)

        vertices = np.array(mesh.vertices)
        faces = np.array(mesh.faces)

        meshdata = gl.MeshData(vertexes=vertices, faces=faces)

        if self.mesh_item:
            self.view.removeItem(self.mesh_item)

        self.mesh_item = gl.GLMeshItem(
            meshdata=meshdata,
            smooth=True,
            color=(0.2, 0.6, 1.0, 1.0),
            shader="shaded",
            drawEdges=False
        )

        self.view.addItem(self.mesh_item)
        self.view.setCameraPosition(distance=max(mesh.extents) * 2)