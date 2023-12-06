import subprocess
from converter import VideoConverter
# COMENTARIO COMPARATIVO ABAJO


def compare_codecs(input_video):
    converter = VideoConverter(input_video)
    output1 = converter.convert_resolution(1920, 1080, 'vp9')
    output2 = converter.convert_resolution(1920, 1080, 'vp8')

    comparison_output = 'vp9_vs_vp8.webm'

    subprocess.run([
        'ffmpeg',
        '-i', output1,
        '-i', output2,
        '-filter_complex', f'[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[vid]',
        '-map', '[vid]',
        '-c:v', 'libvpx-vp9',
        '-c:a', 'libvorbis',
        comparison_output
    ])

    print(f'Comparison complete. Output file: {comparison_output}')

# En el video de comparación se puede ver la diferencia entre los codecs desde el principio ya que en la transición de
# oscuro a claro en el video con codec vp8 la imagen llega con un cuadriculado. En general en el video se aprecia una
# menor calidad respecto al video con codec vp9, los detalles se ven más difuminados y la definición es menor.
# La diferencia se nota especialmente cuando hay contraste o transiciones de color (como el principio del vídeo donde
# se pasa de oscuro a claro, o cuando hay movimiento como una ardilla oscura sobre un fondo claro)  donde el vp8 muestra
# claros signos de compresión. La nitidez y claridad es inferior en el codec vp8 durante todo el video.
# Con el codec vp9 las transiciones de color son suaves y la imagen se ve mas nítida en todo momento, se nota que la
# compresión de este codec es más eficiente que la del vp8.
# Hay que tener en cuenta que el video comparativo está en un contenedor codificado en vp9, por lo que el video con
# codec vp8 ha sido recodificado a vp9 lo cual le puede haber supuesto una pérdida adicional de calidad, aunque también
# se podrían estar atenuando las diferencias al estar recodificados.
compare_codecs('BBB.mp4')
