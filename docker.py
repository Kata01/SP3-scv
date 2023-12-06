# Your Python script (meme_generator.py)
import subprocess

def generate_meme(input_text, input_video, output_video):
    subprocess.run([
        'ffmpeg',
        '-i', input_video,
        '-vf', f'drawtext=text={input_text}:fontsize=24:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        output_video
    ])

# Example usage
generate_meme("Hello, Docker!", "BBB.mp4", "output_meme.mp4")
