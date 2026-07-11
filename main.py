from vedo import Mesh, Plotter, Sphere, Spheres, Points
import customtkinter as ctk
from PIL import Image
import numpy as np
import sys
import os
from typing import Tuple
from pathlib import Path

from components import ValuesTable
from utils import update_textbox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Class variable initialization
        self._model_ = None
        self._linked_operation_ = True
        self._plot_ = None
        self._last_opened_dir_ = Path("/")
        self._linked_icon_ = ctk.CTkImage(
            Image.open("resources/link.jpg"), size=(20, 20)
        )
        self._unlinked_icon_ = ctk.CTkImage(
            Image.open("resources/broken.jpg"), size=(20, 20)
        )

        # Configure application window dimensions
        self.title("CNC Router STL Application")
        self.geometry("800x800")
        self.grid_rowconfigure(3, weight=1)

        # Set up load controls
        load_control_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        load_control_frame.grid_rowconfigure(0, weight=1)
        load_control_frame.grid_columnconfigure(2, weight=1)
        load_control_frame.grid(row=0, pady=(20, 5))
        self._set_load_controls_(load_control_frame)

        self._values_table_ = ValuesTable(self)

        viz_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        viz_frame.grid(row=2, pady=(20, 5))
        self._set_viz_controls_(viz_frame)

    def _open_file_prompt_(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select a File",
            initialdir=self._last_opened_dir_,
            filetypes=[("STL Files", "*.stl")],
        )

        if file_path:
            self._last_opened_dir_ = Path(file_path).parent
            self._model_ = Mesh(file_path)

            # Update the file path
            update_textbox(self.my_textbox, file_path)

            # Update the size values
            x_values = tuple(x / 25.4 for x in self._model_.xbounds())
            y_values = tuple(y / 25.4 for y in self._model_.ybounds())
            z_values = tuple(z / 25.4 for z in self._model_.zbounds())
            thickest_edge_thickness = self._get_thickest_edge_thickness_() / 25.4
            thinnest_edge_thickness = self._get_thinnest_edge_thickness_() / 25.4

            self._values_table_.set_initial_values(
                x_values[1] - x_values[0],
                y_values[1] - y_values[0],
                z_values[1] - z_values[0],
                thickest_edge_thickness,
                thinnest_edge_thickness,
            )

            # Enable visualize button
            self._viz_button_.configure(state=ctk.NORMAL)

    def _set_load_controls_(self, frame: ctk.CTkFrame):
        # Create label for load box
        self.my_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="Current File:",
            font=("Arial", 14, "bold"),
        )
        self.my_label.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="ns")

        # Create textbox
        self.my_textbox = ctk.CTkTextbox(
            master=frame, width=400, height=20, corner_radius=8, state=ctk.DISABLED
        )
        self.my_textbox.grid(row=0, column=1, padx=10, pady=(0, 20), sticky="ns")

        # Create load button
        self.button = ctk.CTkButton(
            frame, text="Load file", command=self._open_file_prompt_
        )
        self.button.grid(row=0, column=2, padx=10, pady=(0, 20))

    def _set_viz_controls_(self, frame: ctk.CTkFrame):
        self._viz_button_ = ctk.CTkButton(
            frame, text="Visualize", command=self._visualize_, state=ctk.DISABLED
        )
        self._viz_button_.grid(row=0, column=0, padx=10, pady=(0, 20))

    def _get_max_marker_(self, color) -> Sphere:
        max_z_index = np.argmax(self._model_.points[:, 2])
        return Sphere(self._model_.points[max_z_index], r=2, c=color)

    def _get_min_marker_(self, color) -> Sphere:
        min_z_index = np.argmin(self._model_.points[:, 2])
        min_z_marker = Sphere(self._model_.points[min_z_index], r=2, c=color)

    def _get_edge_points_(self) -> Points:
        # 1. Get all 3D coordinates of the mesh vertices
        points = self._model_.points

        # 2. Find the center of the mesh in X and Y
        center_x = (self._model_.bounds()[0] + self._model_.bounds()[1]) / 2
        center_y = (self._model_.bounds()[2] + self._model_.bounds()[3]) / 2

        # 3. Calculate how far each point is from the center along the X/Y plane
        distances = np.sqrt(
            (points[:, 0] - center_x) ** 2 + (points[:, 1] - center_y) ** 2
        )

        # 4. Grab points that are right at the maximum radius (the outer edge)
        # We use a tiny tolerance (e.g., 0.5mm) to account for mesh density
        max_distance = np.max(distances)
        edge_indices = np.where(distances >= (max_distance - 0.5))[0]
        edge_points = points[edge_indices]

        return edge_points

    def _get_thickest_edge_thickness_(self) -> float:
        edge_points = self._get_edge_points_()
        # 5. Extract Z heights of these outer edge vertices
        edge_z_values = edge_points[:, 2]

        z_min = np.min(edge_z_values)
        z_max = np.max(edge_z_values)

        return z_max - z_min

    def _get_thinnest_edge_thickness_(self) -> float:
        edge_points = self._get_edge_points_()

        grid_size = 30  # Number of segments to check along X and Y. Increase for more precision.
        x_bins = np.linspace(
            np.min(edge_points[:, 0]), np.max(edge_points[:, 0]), grid_size
        )
        y_bins = np.linspace(
            np.min(edge_points[:, 1]), np.max(edge_points[:, 1]), grid_size
        )

        min_thickness = float("inf")

        # This variable is for visualizations
        # thinnest_points = None

        # Loop through the grid columns to find local edge thickness
        for i in range(len(x_bins) - 1):
            for j in range(len(y_bins) - 1):
                # Isolate points falling inside the current local X/Y grid column
                in_column = (
                    (edge_points[:, 0] >= x_bins[i])
                    & (edge_points[:, 0] < x_bins[i + 1])
                    & (edge_points[:, 1] >= y_bins[j])
                    & (edge_points[:, 1] < y_bins[j + 1])
                )
                col_points = edge_points[in_column]

                # We need at least 2 points (a top and a bottom) to calculate a thickness
                if len(col_points) >= 2:
                    z_vals = col_points[:, 2]
                    local_thickness = np.max(z_vals) - np.min(z_vals)

                    # Check if this is the thinnest section found so far
                    # (Ignoring near-zero errors if the column only captured flat bottom points)
                    if local_thickness < min_thickness and local_thickness > 0.01:
                        min_thickness = local_thickness
                        # thinnest_points = col_points

        return min_thickness

    def _edge_points_visual_(self, max_color, min_color) -> Tuple[Points, Points]:
        edge_points = self._get_edge_points_()

        edge_z_values = edge_points[:, 2]
        z_min_val = np.min(edge_z_values)
        z_max_val = np.max(edge_z_values)

        z_max_points = edge_points[np.isclose(edge_z_values, z_max_val)]
        z_min_points = edge_points[np.isclose(edge_z_values, z_min_val)]

        # 5. Create vedo Points objects for the extremes
        # Green for the highest points, Blue for the lowest points
        visual_max_points = (
            Points(z_max_points).c(max_color).ps(4).render_points_as_spheres()
        )
        visual_min_points = (
            Points(z_min_points).c(min_color).ps(4).render_points_as_spheres()
        )

        return (visual_max_points, visual_min_points)

    def _visualize_(self):
        print(f"Before Scale{self._model_.zbounds()}")

        scale_factors = self._values_table_.get_set_percentages()
        self._model_.scale(scale_factors)
        print(f"After Scale{self._model_.zbounds()}")

        max_points, min_points = self._edge_points_visual_("green", "black")

        plotter = Plotter(axes=1)
        plotter.add(self._get_max_marker_("red"))
        plotter.add(self._get_min_marker_("blue"))
        plotter.add(max_points)
        plotter.add(min_points)
        plotter.show(self._model_).close()

        scale_factors = [1 / x for x in scale_factors]
        self._model_.scale(scale_factors)

        print(f"Before Exit {self._model_.zbounds()}")


if __name__ == "__main__":
    vtk_path = os.path.join(sys.prefix, "Lib", "site-packages", "vtkmodules")

    if os.path.exists(vtk_path):
        os.add_dll_directory(vtk_path)

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
