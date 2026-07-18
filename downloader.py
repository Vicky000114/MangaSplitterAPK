import os
import json
import requests
import time


def descargar_capitulo(cap):

    carpeta = f"downloads/{cap['project']['slug']}/{cap['slug']}"
    os.makedirs(carpeta, exist_ok=True)

    paginas = cap["pageches"]

    urls = json.loads(paginas[0]["urlImg"])

    archivos = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://spicyseries.com/"
    }

    for i, url in enumerate(urls):

        extension = url.split(".")[-1]
        nombre = f"{i+1:03d}.{extension}"

        destino = os.path.join(carpeta, nombre)

        intento = 0

        while intento < 5:

            try:
                print("Descargando:", url)

                with requests.get(
                    url,
                    headers=headers,
                    stream=True,
                    timeout=60
                ) as r:

                    r.raise_for_status()

                    with open(destino, "wb") as f:
                        for chunk in r.iter_content(1024*64):
                            if chunk:
                                f.write(chunk)

                break

            except Exception as e:

                intento += 1
                print(
                    f"Error descarga {nombre}, intento {intento}/5",
                    e
                )

                time.sleep(3)


        archivos.append(destino)

    return archivos
