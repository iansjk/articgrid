from __future__ import print_function, absolute_import

from collections import defaultdict
from urlparse import urlsplit, parse_qsl

import requests
import requests_cache
from bs4 import BeautifulSoup

ARASAAC_URL = "http://www.arasaac.org"
ARASAAC_SEARCH_ENDPOINT = "buscar.php"
ARASAAC_SEARCH_PARAMS = {
    "id_tipo": 10,
    "buscar_por": 3,
    "idiomasearch": 7,
}
ARASAAC_IMAGE_DIR = "repositorio/originales"
requests_cache.install_cache(backend="sqlite", allowable_methods=("GET", "POST"))


def find_pictograms(query):
    if not query:
        raise ValueError("Empty query")

    resultdict = defaultdict(list)
    params = ARASAAC_SEARCH_PARAMS
    params['s'] = query
    page = 0
    max_pages = 0
    while page <= max_pages:
        params["pg"] = page
        r = requests.post("/".join((ARASAAC_URL, ARASAAC_SEARCH_ENDPOINT)), params=params)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        item_list = soup.find(id="ultimas_imagenes")
        if item_list is not None:
            for li in item_list.find_all("li"):
                a = li.find("font").parent
                item_url_params = dict(parse_qsl(urlsplit(a['href']).query))
                image_url = "/".join((ARASAAC_URL, ARASAAC_IMAGE_DIR, item_url_params["id"] + ".png"))
                resultdict[a.text].append(image_url)

        pagination = soup.find(id="pagination")
        if max_pages == 0 and pagination is not None:
            last_page_url = pagination.find_all("a")[-1]["href"]
            last_page_url_params = dict(parse_qsl(urlsplit(last_page_url).query))
            max_pages = int(last_page_url_params["pg"])
        page += 1
    results = [[term, resultdict[term]] for term in resultdict.viewkeys()]
    return results
