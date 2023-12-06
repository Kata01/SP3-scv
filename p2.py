import subprocess
import re


class Converter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_to_mp2(self, output_file):
        # Ejecuta comando 'ffmpeg -i BBB.mp4 -c:v mpeg2video BBB.mp2, el cual convierte BBB.mp4 a un video en mpeg2
        subprocess.run(['ffmpeg', '-i', self.input_file, '-c:v', 'mpeg2video', f'{output_file}.mp2'])
        self.get_video_info(output_file)

    def modify_resolution(self, output_file, width, height):
        # Ejecuta comando 'ffmpeg -i input -vf f'scalex:x' output', el cual redimensiona el video a las dimensiones indicadas
        subprocess.run(['ffmpeg', '-i', self.input_file, '-vf', f'scale={width}:{height}', output_file])

        self.get_video_info(output_file)

    def change_chroma_subsampling(self, output_file, subsampling):
        # Ejecuta comando 'ffmpeg -i input -c:v libx264 -pix_fmt formato output', el cual cambia el chromatic sumsamplin al indicado en la variable subsampling
        subprocess.run(['ffmpeg', '-i', self.input_file, '-c:v', 'libx264', '-pix_fmt', subsampling, output_file])

        self.get_video_info(output_file)

    def get_video_info(self, video_file):
        # Encuentra y muestra la duracion, codec, resolución, bitrate y formato del video

        # Inicia el proceso de obtener información detallada del video utilizando 'ffmpeg -i video_file'
        result = subprocess.Popen(['ffmpeg', '-i', video_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = result.stderr.read().decode()

        # Busca y muestra la duración del video si se encuentra en LA salida de FFmpeg
        match_duration = re.search(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})", output)
        if match_duration:
            duration = match_duration.group(1)
            print(f"Duration: {duration}")

        # Busca y muestra el códec de video si se encuentra en la salida de FFmpeg
        match_codec = re.search(r"Stream #0:0: Video: ([\w]+)", output)
        if match_codec:
            video_codec = match_codec.group(1)
            print(f"Codec: {video_codec}")

        # Busca y muestra la resolución del video si se encuentra en la salida de FFmpeg
        match_resolution = re.search(r"Stream #0:0: Video: .+?, (\d+)x(\d+)", output)
        if match_resolution:
            width = match_resolution.group(1)
            height = match_resolution.group(2)
            print(f"Resolution: {width}x{height}")

        # Busca y muestra el bitrate del video si se encuentra en la salida de FFmpeg
        match_bitrate = re.search(r"bitrate: (\d+) kb/s", output)
        if match_bitrate:
            bitrate = match_bitrate.group(1)
            print(f"Bitrate: {bitrate} kb/s")

        # Busca y muestra el formato del video si se encuentra en la salida de FFmpeg
        match_format = re.search(r"Input #0, ([\w]+),", output)
        if match_format:
            video_format = match_format.group(1)
            print(f"Video format: {video_format}")



