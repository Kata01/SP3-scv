import subprocess


class VideoConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_resolution(self, width, height, codec):
        output_file = f'{width}x{height}_{codec}_BBB'

        container_format = 'mkv'

        if codec == 'vp8' or codec == 'vp9':
            container_format = 'webm'

        subprocess.run([
            'ffmpeg',
            '-i', self.input_file,
            '-vf', f'scale={width}:{height}',
            '-c:v', codec,
            f'-c:a', 'libvorbis',
            f'{output_file}.{container_format}'
        ])

        print(f'Conversion to {width}x{height} with {codec} complete. Output file: {output_file}.{container_format}')
        output_vid = f'{output_file}.{container_format}'
        return output_vid

    def convert(self):
        resolutions = [(1280, 720), (854, 480), (360, 240), (160, 120)]
        codecs = ['vp8', 'vp9', 'libx265', 'libaom-av1']

        print("Available resolutions:")
        for i, (width, height) in enumerate(resolutions):
            print(f"{i}. {width}x{height}")

        choice_resolution = int(input("Choose a resolution: "))
        chosen_resolution = resolutions[choice_resolution]

        print("\nAvailable codecs:")
        for i, codec in enumerate(codecs):
            print(f"{i}. {codec}")

        choice_codecs = int(input("Choose a codec: "))
        chosen_codec = codecs[choice_codecs]

        self.convert_resolution(chosen_resolution[0], chosen_resolution[1], chosen_codec)


if __name__ == "__main__":
    input_video = 'BBB.mp4'
    converter = VideoConverter(input_video)
    converter.convert()
