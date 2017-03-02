from __future__ import print_function, absolute_import
import requests
from urlparse import urlsplit, parse_qsl
from bs4 import BeautifulSoup

_ARASAAC_URL = "http://www.arasaac.org"
_ARASAAC_SEARCH_ENDPOINT = "buscar.php"
_ARASAAC_IMAGE_DIR = "repositorio/originales"
_ARASAAC_SEARCH_PARAMS = {
    "id_tipo": 10,
    "buscar_por": 3,
    "idiomasearch": 7,
}


def find_images(query):
    results = {}
    params = _ARASAAC_SEARCH_PARAMS
    params['s'] = query
    r = requests.post("/".join((_ARASAAC_URL, _ARASAAC_SEARCH_ENDPOINT)),
                      params=params)
    soup = BeautifulSoup(r.content, "html.parser")
    for li in soup.find(id="ultimas_imagenes").find_all("li"):
        a = li.find("font").parent
        item_url_params = dict(parse_qsl(urlsplit(a['href']).query))
        image_url = "/".join((_ARASAAC_URL, _ARASAAC_IMAGE_DIR,
                              item_url_params["id"] + ".png"))
        results[a.text] = image_url
    return results


if __name__ == "__main__":
    print(find_images("hand"))
