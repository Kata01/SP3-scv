# Used tkinter and tkinter theme Forest-tkk-theme from https://github.com/rdbende/Forest-ttk-theme to implement GUI
from threading import Thread
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label, messagebox, StringVar
from pathlib import Path
import os
from codec_res_converter import CodecConverter
from extract_yuv_histogram import ExtractYuvHistogram
from p2 import Converter
from rgb_yuv import BlackAndWhite
from s2 import s2

SCRIPT_DIR = Path(__file__).parent
OUTPUT_PATH = SCRIPT_DIR / "output_folder"
ASSETS_PATH = SCRIPT_DIR / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def is_video_file(file_path):
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.ogg', '.m4v', '.3gp'}

    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in video_extensions


class VideoConverterGUI:
    def __init__(self, master):
        self.progress_window = None
        self.master = master
        master.geometry("1280x720")
        master.configure(bg="#DA2323")

        self.canvas = Canvas(
            master,
            bg="#DA2323",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Entry for input video
        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(265.5, 87.0, image=entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#2D2D2D", fg="#FFFFFF", highlightthickness=0)
        self.entry_1.place(x=92.5, y=67.0, width=346.0, height=38.0)

        # Button for browsing input video
        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=self.browse_input, relief="flat")
        button_1.place(x=410, y=79.4000244140625, width=16.0, height=15.200017929077148)

        # Output name
        entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(265.5, 206.0, image=entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#2D2D2D", fg="#FFFFFF", highlightthickness=0)
        self.entry_3.place(x=92.5, y=186.0, width=346.0, height=38.0)
        self.entry_3.insert(0, "output.mp4")

        self.canvas.create_text(
            90.0,
            160.0,
            anchor="nw",
            text="Output name",
            fill="#FFFFFF",
            font=("Helvetica 15 bold")
        )

        self.canvas.create_text(
            90.0,
            40.0,
            anchor="nw",
            text="Input video",
            fill="#FFFFFF",
            font=("Helvetica 15 bold")
        )

        # Codec and resolution
        self.canvas.create_text(57.0, 378.0, anchor="nw", text="Change resolution and codec", fill="#FFFFFF", font=("Helvetica", 10, "bold"))

        self.resolutions = ["1920x1080", "1280x720", "854x480", "360x240", "160x120"]
        self.codecs = ["vp8", "vp9", "libx265", "libaom-av1"]

        self.resolution_option_menu = ttk.Combobox(values=self.resolutions)
        self.resolution_option_menu.place(x=76, y=414.0, width=192.0, height=40.0)

        self.codec_option_menu = ttk.Combobox(values=self.codecs, state="readonly")
        self.codec_option_menu.place(x=75, y=475, width=192.0, height=40.0)

        # Generate resolution codec
        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.generate_video_codec,
            relief="flat",
            bg="#DB2424"
        )
        button_2.place(x=76.0, y=536.0, width=188.0, height=47.0)

        image_image_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(
            405.0,
            434.0,
            image=image_image_5
        )
        self.entry_4 = Entry(bd=0, bg="#2D2D2D", fg="#FFFFFF", highlightthickness=0)
        self.entry_4.place(x=320, y=418.0, width=175.0, height=33.0)
        self.entry_4.insert(0, "yuv420p")

        self.canvas.create_text(
            294.0,
            377.0,
            anchor="nw",
            text="Change chroma subsampling\n               (yuv***p)",
            fill="#FFFFFF",
            font=("Helvetica 10 bold")
        )


        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.change_chroma_subsampling,
            relief="flat",
            bg="#DB2424"
        )
        button_3.place(
            x=309.0,
            y=472.0,
            width=192.0,
            height=47.0
        )

        image_image_6 = PhotoImage(
            file=relative_to_assets("image_6.png"))
        image_6 = self.canvas.create_image(
            649.0,
            434.0,
            image=image_image_6
        )

        self.canvas.create_text(
            575.0,
            378.0,
            anchor="nw",
            text="Modify resolution",
            fill="#FFFFFF",
            font=("Helvetica 10 bold")
        )

        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        button_4 = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.modify_resolution,
            relief="flat",
            bg="#DB2424"
        )
        button_4.place(
            x=553.0,
            y=472.0,
            width=192.0,
            height=47.0
        )

        # Enter resolution
        entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(648.5, 434.0, image=entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#2D2D2D", fg="#FFFFFF", highlightthickness=0)
        self.entry_2.place(x=561.0, y=414.0, width=175.0, height=38.0)
        self.entry_2.insert(0, "1280x720")

        button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        button_5 = Button(
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.cut_and_analyze,
            relief="flat",
            bg="#DB2424"
        )
        button_5.place(
            x=797.0,
            y=148.0,
            width=411.0,
            height=56.0
        )

        self.canvas.create_text(
            833.0,
            67.0,
            anchor="nw",
            text="Press and generate:",
            fill="#FFFFFF",
            font=("Helvetica 22 bold")
        )

        self.canvas.create_text(
            111.0,
            284.0,
            anchor="nw",
            text="Choose parameters and generate:",
            fill="#FFFFFF",
            font=("Helvetica 22 bold")
        )

        button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        button_6 = Button(
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.extractYUV,
            relief="flat",
            bg="#DB2424"
        )
        button_6.place(
            x=799.0,
            y=299.0,
            width=411.0,
            height=56.0
        )

        button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        button_7 = Button(
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.bw,
            relief="flat",
            bg="#DB2424"
        )
        button_7.place(
            x=801.0,
            y=450.0,
            width=411.0,
            height=56.0
        )

        button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        button_8 = Button(
            image=button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=self.convert_mp2,
            relief="flat",
            bg="#DB2424"
        )
        button_8.place(
            x=801.0,
            y=601.0,
            width=411.0,
            height=56.0
        )

        image_image_7 = PhotoImage(
            file=relative_to_assets("image_7.png"))
        image_7 = self.canvas.create_image(
            642.0,
            143.0,
            image=image_image_7
        )

        image_image_8 = PhotoImage(
            file=relative_to_assets("image_8.png"))
        image_8 = self.canvas.create_image(
            644,
            142.99999663422307,
            image=image_image_8
        )

        self.canvas.create_rectangle(
            763.0,
            274.0,
            769.9999998673668,
            678.9999675128092,
            fill="#FFFFFF",
            outline="")
        master.resizable(False, False)
        master.mainloop()

    def browse_input(self):
        self.input_file = filedialog.askopenfilename()

        if self.input_file:
            if is_video_file(self.input_file):
                self.entry_1.delete(0, 'end')
                self.entry_1.insert(0, self.input_file)
            else:
                error_message = f"The selected file '{self.input_file}' is not a valid video file."
                messagebox.showerror("Error", error_message)

    def generate_video_codec(self):
        try:
            selected_resolution_str = self.resolution_option_menu.get()
            selected_codec = self.codec_option_menu.get()
            height, width = tuple(map(int, selected_resolution_str.split('x')))

            codec_res = CodecConverter(self.input_file)

            progress_thread = Thread(target=self.show_progress_bar)
            progress_thread.start()

            codec_res.convert_resolution(height, width, selected_codec)
            self.close_progress_bar()

        except Exception as e:
            self.show_error_window(str(e))

    def modify_resolution(self):
        entered_resolution = self.entry_2.get()
        output_file = self.entry_3.get()
        width, height = map(int, entered_resolution.split('x'))
        p2 = Converter(self.input_file)
        p2.modify_resolution(output_file, width, height)

    def change_chroma_subsampling(self):
        output_file = self.entry_3.get()
        subsampling = self.entry_4.get()
        p2 = Converter(self.input_file)
        p2.change_chroma_subsampling(output_file, subsampling)

    def cut_and_analyze(self):
        output_file = self.entry_3.get()
        s2_instance = s2(self.input_file)
        s2_instance.cut_and_analyze_video(output_file)

    def extractYUV(self):
        output_file = self.entry_3.get()
        yuv_histogram_processor = ExtractYuvHistogram(self.input_file, output_file)
        yuv_histogram_processor.extract_yuv_histogram()

    def bw(self):
        output_file = self.entry_3.get()
        black_and_white_processor = BlackAndWhite()
        black_and_white_processor.image_to_bw(self.input_file, output_file)

    def convert_mp2(self):
        output_file = self.entry_3.get()
        converter = Converter(self.input_file)
        converter.convert_to_mp2(output_file)
    def show_progress_bar(self):
        self.progress_window = Tk()
        self.progress_window.title("Converting Video")
        self.progress_window.geometry("300x50")

        progress_bar = ttk.Progressbar(self.progress_window, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        self.progress_window.mainloop()

    def close_progress_bar(self):
        self.progress_window.destroy()

    def show_error_window(self, error_message):
        messagebox.showerror("Error", error_message)

