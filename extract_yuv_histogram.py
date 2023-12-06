import subprocess


class ExtractYuvHistogram:
    def __init__(self, input_video, output_video):
        self.input_video = input_video
        self.output_video = output_video

    def extract_yuv_histogram(self):
        subprocess.run([
            'ffmpeg',
            '-i', self.input_video,
            '-vf', 'split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay',
            '-c:a', 'copy',
            self.output_video
        ])
