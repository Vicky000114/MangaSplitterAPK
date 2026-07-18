import os
import shutil
import zipfile
import tempfile
from PIL import Image

CUT_HEIGHT = 10000


def split_zip(zip_path):

    temp_dir = tempfile.mkdtemp()
    output_dir = tempfile.mkdtemp()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):

        dirs[:] = [
            d for d in dirs
            if os.path.abspath(os.path.join(root, d)) != os.path.abspath(output_dir)
        ]

        for file in sorted(files):

            if not file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            ruta = os.path.join(root, file)

            img = Image.open(ruta)

            ancho, alto = img.size

            nombre = os.path.splitext(file)[0]
            extension = os.path.splitext(file)[1].lower()

            if alto <= CUT_HEIGHT:

                destino = os.path.join(output_dir, file)

                if os.path.abspath(ruta) != os.path.abspath(destino):
                    shutil.copy2(ruta, destino)

                continue

            parte = 1

            for y in range(0, alto, CUT_HEIGHT):

                corte = img.crop(
                    (
                        0,
                        y,
                        ancho,
                        min(y + CUT_HEIGHT, alto)
                    )
                )

                destino = os.path.join(
                    output_dir,
                    f"{nombre}_{parte}{extension}"
                )

                if extension in (".jpg", ".jpeg"):

                    corte.save(
                        destino,
                        format="JPEG",
                        quality=95,
                        optimize=True
                    )

                elif extension == ".png":

                    corte.save(
                        destino,
                        format="PNG",
                        optimize=True
                    )

                elif extension == ".webp":

                    corte.save(
                        destino,
                        format="WEBP",
                        quality=95,
                        method=6
                    )

                parte += 1

    salida_zip = zip_path.replace(".zip", "_cortado.zip")

    carpeta = os.path.splitext(
        os.path.basename(zip_path)
    )[0]

    with zipfile.ZipFile(
        salida_zip,
        "w",
        zipfile.ZIP_DEFLATED
    ) as nuevo:

        for archivo in sorted(os.listdir(output_dir)):

            nuevo.write(
                os.path.join(output_dir, archivo),
                os.path.join(carpeta, archivo)
            )

    shutil.rmtree(temp_dir)
    shutil.rmtree(output_dir)

    return salida_zip


def split_folder(folder_path, nombre_salida):

    output_dir = tempfile.mkdtemp()

    for file in sorted(os.listdir(folder_path)):

        if not file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        ruta = os.path.join(folder_path, file)

        img = Image.open(ruta)

        ancho, alto = img.size

        nombre = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1].lower()

        if alto <= CUT_HEIGHT:

            destino = os.path.join(output_dir, file)

            if os.path.abspath(ruta) != os.path.abspath(destino):
                shutil.copy2(ruta, destino)

            continue

        parte = 1

        for y in range(0, alto, CUT_HEIGHT):

            corte = img.crop(
                (
                    0,
                    y,
                    ancho,
                    min(y + CUT_HEIGHT, alto)
                )
            )

            destino = os.path.join(
                output_dir,
                f"{nombre}_{parte}{extension}"
            )

            if extension in (".jpg", ".jpeg"):

                corte.save(
                    destino,
                    format="JPEG",
                    quality=95,
                    optimize=True
                )

            elif extension == ".png":

                corte.save(
                    destino,
                    format="PNG",
                    optimize=True
                )

            elif extension == ".webp":

                corte.save(
                    destino,
                    format="WEBP",
                    quality=95,
                    method=6
                )

            parte += 1

    zip_final = f"{nombre_salida}.zip"

    with zipfile.ZipFile(
        zip_final,
        "w",
        zipfile.ZIP_DEFLATED
    ) as nuevo:

        carpeta = nombre_salida

        for archivo in sorted(os.listdir(output_dir)):

            nuevo.write(
                os.path.join(output_dir, archivo),
                os.path.join(carpeta, archivo)
            )

    shutil.rmtree(output_dir)

    return zip_final