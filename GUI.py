import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from converter import VideoConverter


class VideoConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Converter GUI")

        self.converter = VideoConverter('BBB.mp4')

        # Input File
        self.input_label = tk.Label(self, text="Input File:")
        self.input_label.pack()

        self.input_entry = ttk.Entry(self, state='readonly')
        self.input_entry.pack(side=tk.LEFT, padx=5)

        self.browse_input_button = ttk.Button(self, text="Browse", command=self.browse_input)
        self.browse_input_button.pack(side=tk.RIGHT, padx=5)

        # Output File
        self.output_label = tk.Label(self, text="Output File:")
        self.output_label.pack()

        self.output_entry = ttk.Entry(self, state='readonly')
        self.output_entry.pack(side=tk.LEFT, padx=5)

        self.browse_output_button = ttk.Button(self, text="Browse", command=self.browse_output)
        self.browse_output_button.pack(side=tk.RIGHT, padx=5)

        # Resolution
        self.resolution_label = tk.Label(self, text="Choose Resolution:")
        self.resolution_label.pack()

        self.resolution_combobox = ttk.Combobox(self, values=["1280x720", "854x480", "360x240", "160x120"])
        self.resolution_combobox.pack()

        # Codecs
        self.codec1_label = tk.Label(self, text="Choose Codec 1:")
        self.codec1_label.pack()

        self.codec1_combobox = ttk.Combobox(self, values=["vp8", "vp9", "libx265", "libaom-av1"])
        self.codec1_combobox.pack()

        # Conversion Buttons
        self.convert_button = ttk.Button(self, text="Convert", command=self.start_conversion)
        self.convert_button.pack()

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def browse_input(self):
        input_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)

    def browse_output(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])
        if output_file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

    def start_conversion(self):
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()
        resolution = self.resolution_combobox.get()
        codec1 = self.codec1_combobox.get()

        if not input_file:
            self.status_label.config(text="Please select an input file.")
            return

        if not output_file:
            self.status_label.config(text="Please select an output file.")
            return

        if not resolution:
            self.status_label.config(text="Please choose a resolution.")
            return

        if not codec1:
            self.status_label.config(text="Please choose Codec 1.")
            return

        command = [
            "ffmpeg",
            "-i", input_file,
            "-s", resolution,
            "-c:v", codec1,
            output_file
        ]

        try:
            subprocess.run(command, check=True)
            self.status_label.config(text="Conversion successful!", fg="green")
        except subprocess.CalledProcessError as e:
            self.status_label.config(text=f"Error: {e}", fg="red")


if __name__ == "__main__":
    app = VideoConverterGUI()
    app.mainloop()