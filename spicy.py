import requests


API = "http://127.0.0.1:3333"


def obtener_serie(url):

    slug = url.rstrip("/").split("/")[-1]

    try:
        r = requests.get(
            f"{API}/serie/{slug}",
            timeout=30
        )

        if r.status_code != 200:
            return None

        data = r.json()

        serie = data["serie"]

        return {
            "titulo": serie["name"],
            "slug": serie["slug"],
            "capitulos": serie["chapters"]
        }

    except Exception as e:
        print("Error API:", e)
        return None



def obtener_capitulo(slug, capitulo):

    try:
        r = requests.get(
            f"{API}/serie/{slug}/{capitulo}",
            timeout=60
        )

        if r.status_code != 200:
            return None

        return r.json()

    except Exception as e:
        print("Error capítulo:", e)
        return None
