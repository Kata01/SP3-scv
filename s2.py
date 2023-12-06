import subprocess

class s2:
    def __init__(self, input_file):
        self.input_file = input_file

    def cut_and_analyze_video(self, output_file):
        # Cortar 9 primeros segundos de video con el comando "ffmpeg -i input.mp4 -t 9 output.mp4"
        subprocess.run(['ffmpeg', '-i', self.input_file, '-t', '9', output_file])

        # Obtener video con vectores de movimiento y macrobloques con el comando "ffmpeg -flags2 +export_mvs -i input.mp4 -vf codecview=mv=pf+bf+bb output.mp4"
        # pf: para vectores de movimiento predichos hacia adelante de imágenes P
        # bf: para vectores de movimiento predichos hacia adelante de imágenes B
        # bb: para vectores de movimiento predichos hacia atrás de imágenes B
        subprocess.run(['ffmpeg', '-flags2', '+export_mvs', '-i', output_file, '-vf', 'codecview=mv=pf+bf+bb',
                        'output_analyzed.mp4', ])

        # Limpiar archivos temporales
        subprocess.run(['rm', output_file])

    def create_new_container(self, output_file):
        # Cortar 50 primeros segundos de video con el comando "ffmpeg -i input.mp4 -t 50 output.mp4"
        cut_video_file = 'bbb_50s.mp4'
        subprocess.run(['ffmpeg', '-i', self.input_file, '-t', '50', cut_video_file])

        # Exportar audio en MP3 mono
        mp3_mono_file = 'bbb_mono.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-ac', '1', '-q:a', '2', mp3_mono_file])

        # Exportar audio en mp3 estéreo con bajo bitrate
        mp3_stereo_low_bitrate_file = 'bbb_stereo_low_bitrate.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-q:a', '6', mp3_stereo_low_bitrate_file])

        # Exportar audio en codec aac
        aac_file = 'bbb_aac.aac'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-c:a', 'aac', aac_file])

        # Fusionar en un contenedor mp4
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-i', mp3_mono_file, '-i', mp3_stereo_low_bitrate_file, '-i',
                        aac_file, '-filter_complex',
                        "[0:v]concat=n=1:v=1:a=0[vout];[1:a][2:a][3:a]concat=n=3:v=0:a=1[aout]",
                        '-map', "[vout]", '-map', '[aout]', '-c:v', 'libx264', '-c:a', 'aac', output_file])

        # Limpiar archivos temporales
        # subprocess.run(['rm', cut_video_file, mp3_mono_file, mp3_stereo_low_bitrate_file, aac_file])

    def get_num_tracks(self, input_file):
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries',
                                 'stream=index,codec_name', '-of', 'csv=p=0', input_file], text=True,
                                capture_output=True)

        num_tracks = len(result.stdout.strip().split('\n'))

        if num_tracks > 0:
            print(f"The MP4 container contains {num_tracks} audio track(s):")
        else:
            print(f"The MP4 container does not contain any audio track")
