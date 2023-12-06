import subprocess
import numpy as np
from scipy.fftpack import dct, idct

class RgbYuv:
    def __init__(self, output_format='int'):
        if output_format not in ['float', 'int']:
            raise ValueError("Output must be 'float' or 'int'")
        self.output_format = output_format

    def rgb_to_yuv(self, rgb):
        yuv = [0, 0, 0]
        r, g, b = rgb
        # Convertimos los valores rgb en yuv usando las formulas de y, u y v.
        yuv[0] = 0.299 * r + 0.587 * g + 0.114 * b
        yuv[1] = -0.14713 * r - 0.288862 * g + 0.436 * b
        yuv[2] = 0.615 * r - 0.51498 * g - 0.10001 * b
        if self.output_format == 'int':
            yuv[0], yuv[1], yuv[2] = int(yuv[0]), int(yuv[1]), int(yuv[2])
        return yuv

    def yuv_to_rgb(self, yuv):
        rgb = [0, 0, 0]
        y, u, v = yuv
        # Transformamos los valores yuv en rgb usando las fórmulas para obtener r, g y b a partir de los valores yuv.
        rgb[0] = y + 1.13983 * v
        rgb[1] = y - 0.39465 * u - 0.5806 * v
        rgb[2] = y + 2.03211 * u
        if self.output_format == 'int':
            rgb[0], rgb[1], rgb[2] = int(rgb[0]), int(rgb[1]), int(rgb[2])
        return rgb


class FfmpegResize:
    def __init__(self):
        output = 1
        self.output = output

    def resize(self, input, output, width, quality):
        # la función ejecuta este comando (ffmpeg -i input.jpg -vf "scale=width:-1" -q:v quality output.jpg)
        # en la terminal
        command = ["ffmpeg","-i", input,"-vf", f"scale={width}:-1","-q:v", str(quality),output]
        subprocess.run(command)
        print("Image resized")


class Serpentine:
    def __init__(self):
        out = 1
        self.out = out

    def serpentine(self, input_matrix):
        # La función lee una matriz en vez de una imagen debido a un error con el entorno virtual y el módulo Pillow.
        # Se debe aplicar una conversion de imagen a matriz antes de ejecutar la función de lectura.
        width = len(input_matrix[0])
        height = len(input_matrix)
        serpentine_data = []
        x, y = 0, 0
        # Dirección cuando image_half = 1 (1 a la derecha, 2 en diagonal hacia abajo, 3 hacia abajo, 4 en diagonal hacia arriba)
        # Dirección cuando image_half = 2 (1 a la derecha, 2 en diagonal hacia arriba, 3 hacia abajo, 4 en diagonal hacia abajo)
        direction = 1
        image_half = 1
        while x != width and y != height:
                pixel_value = input_matrix[y][x]
                serpentine_data.append(pixel_value)
                print(pixel_value)
                # Avanza un píxel a la derecha
                if (width > height and y == height - 1 and x == width - height):

                   image_half = 2
                   direction = 1

                if (height >= width and x == width - 1 and y == height - width - 1):
                    image_half = 2
                    direction = 5
                if image_half == 1:
                        if direction == 1:
                            x += 1
                            direction = 2
                        elif direction == 2:
                            y += 1
                            x -= 1
                            if x == 0:
                                direction = 3
                        elif direction == 3:
                            y += 1
                            direction = 4
                        elif direction == 4:
                            y -= 1
                            x += 1
                            if y == 0:
                                direction = 1
                elif image_half == 2:
                        if direction == 1:
                            x += 1
                            direction = 2
                        elif direction == 2:
                            y -= 1
                            x += 1
                            if x == width - 1:
                                direction = 3
                        elif direction == 3:
                            y += 1
                            direction = 4
                        elif direction == 4:
                            y += 1
                            x -= 1
                            if y == height-1:
                                direction = 1
                        elif direction == 5:
                            y += 1
                            direction = 4
        return serpentine_data

class BlackAndWhite:
    def __init__(self):
        out = 1
        self.out = out

    def image_to_bw(self,input, output):
            # funcion para ejecutar el comando ffmpeg: ffmpeg -i input.jpg -vf "format=gray" -q:v 0 output.jpg
            command = ["ffmpeg","-i", input,"-vf", "format=gray","-q:v", "0", output]
            subprocess.run(command)
            print("Image converted to black and white.")


class RunLength:
    def __init__(self):
        out = 1

    def run_length_encode(self, bytes):
            encoded_bytes = []
            count = 1

            for i in range(1, len(bytes)):
                if bytes[i] == bytes[i - 1]:
                    count += 1
                else:
                    encoded_bytes.append(bytes[i - 1])
                    encoded_bytes.append(count)
                    count = 1

            encoded_bytes.append(bytes[-1])
            encoded_bytes.append(count)

            return encoded_bytes


class DCTConverter:
    def __init__(self):
        out = 0

    def convert_to_dct(self, data):
        return dct(dct(data, axis=0, type=2, norm='ortho'), axis=1, type=2, norm='ortho')

    def convert_to_idct(self, data):
        return idct(idct(data, axis=0, type=2, norm='ortho'), axis=1, type=2, norm='ortho')

