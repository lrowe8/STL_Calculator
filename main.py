from vedo import Mesh, show
import customtkinter as ctk
from PIL import Image

# Set up global styling and theme configurations
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Class variable initialization
        self._model_ = None
        self._linked_icon_ = ctk.CTkImage(
            light_image=Image.open("broken.jpg"),
            dark_image=Image.open("link.jpg"),
            size=(20, 20)
        )
        
        # Configure application window dimensions
        self.title("CNC Router STL Application")
        self.geometry("800x800")

        # self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        load_control_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        load_control_frame.grid_rowconfigure(0, weight=1)
        load_control_frame.grid_columnconfigure(2, weight=1)
        load_control_frame.grid(row=0, pady=(20, 5))
        self._set_load_controls_(load_control_frame)

        calc_control_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        calc_control_frame.grid_rowconfigure(2, weight=1)
        calc_control_frame.grid_columnconfigure(1, weight=1)
        calc_control_frame.grid(row=1, pady=(20, 5))
        self._set_calc_controls_(calc_control_frame)

    def _set_load_controls_(self, frame: ctk.CTkFrame):
        # Create label for load box
        self.my_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="Current File:",
            font=("Arial", 14, "bold"),
        )
        self.my_label.grid(row=0, column=0, padx=10, pady=(20, 5))

        # Create textbox
        self.my_textbox = ctk.CTkTextbox(
            master=frame,
            width=400,
            height=20,
            corner_radius=8,
            state=ctk.DISABLED
        )
        self.my_textbox.grid(row=0, column=1, padx=10, pady=(0, 20))
        
        # Create load button
        self.button = ctk.CTkButton(frame, text="Load file", command=self._open_file_prompt_)
        self.button.grid(row=0, column=2, padx=10, pady=(0, 20))

    def _set_calc_controls_(self, frame: ctk.CTkFrame):
        self.x_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="X Distance:",
            font=("Arial", 14, "bold"),
        )
        self.x_label.grid(row=0, column=0, padx=10, pady=(20, 5))

        # Create textbox
        self.x_textbox = ctk.CTkTextbox(
            master=frame,
            width=75,
            height=20,
            corner_radius=8,
            state=ctk.DISABLED
        )
        self.x_textbox.grid(row=0, column=1, padx=10, pady=(0, 20))

        self.y_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="Y Distance:",
            font=("Arial", 14, "bold"),
        )
        self.y_label.grid(row=1, column=0, padx=10, pady=(20, 5))

        # Create textbox
        self.y_textbox = ctk.CTkTextbox(
            master=frame,
            width=75,
            height=20,
            corner_radius=8,
            state=ctk.DISABLED
        )
        self.y_textbox.grid(row=1, column=1, padx=10, pady=(0, 20))

        self._linked_button_ = ctk.CTkButton(
            master=frame,
            text="",
            height=20,
            width=20,
            fg_color="transparent",
            bg_color="transparent",
            image=self._linked_icon_,
            command=lambda: print("Button clicked!")
        )
        self._linked_button_.grid(row=1, column=2, padx=10, pady=(0, 20))

        self.z_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="Z Distance:",
            font=("Arial", 14, "bold"),
        )
        self.z_label.grid(row=2, column=0, padx=10, pady=(20, 5))

        # Create textbox
        self.z_textbox = ctk.CTkTextbox(
            master=frame,
            width=75,
            height=20,
            corner_radius=8,
            state=ctk.DISABLED
        )
        self.z_textbox.grid(row=2, column=1, padx=10, pady=(0, 20))

    def _update_size_values_(self):
        x_values = tuple(x / 25.4 for x in self._model_.xbounds())
        y_values = tuple(y / 25.4 for y in self._model_.ybounds())
        z_values = tuple(z / 25.4 for z in self._model_.zbounds())

        self.x_textbox.configure(state=ctk.NORMAL)
        self.x_textbox.delete("0.0", "end")
        self.x_textbox.insert("0.0", f'{(x_values[1] - x_values[0]):.2f}')
        self.x_textbox.configure(state=ctk.DISABLED)

        self.y_textbox.configure(state=ctk.NORMAL)
        self.y_textbox.delete("0.0", "end")
        self.y_textbox.insert("0.0", f'{(y_values[1] - y_values[0]):.2f}')
        self.y_textbox.configure(state=ctk.DISABLED)

        self.z_textbox.configure(state=ctk.NORMAL)
        self.z_textbox.delete("0.0", "end")
        self.z_textbox.insert("0.0", f'{(z_values[1] - z_values[0]):.2f}')
        self.z_textbox.configure(state=ctk.DISABLED)

    def _open_file_prompt_(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select a File",
            initialdir="/",
            filetypes=[("STL Files", "*.stl")]
        )
        
        if file_path:
            self._model_ = Mesh(file_path)

            # Update the file path
            self.my_textbox.configure(state=ctk.NORMAL)
            self.my_textbox.delete("0.0", "end")
            self.my_textbox.insert("0.0", file_path)
            self.my_textbox.configure(state=ctk.DISABLED)

            # Update the size values
            self._update_size_values_()

            

if __name__ == "__main__":
    app = App()
    app.mainloop()
