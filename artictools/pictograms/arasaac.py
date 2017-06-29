import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlsplit, parse_qsl

_ARASAAC_URL = "http://www.arasaac.org"
_ARASAAC_SEARCH_ENDPOINT = "buscar.php"
_ARASAAC_SEARCH_PARAMS = {
    "id_tipo": 10,
    "buscar_por": 3,
    "idiomasearch": 7,
}
_ARASAAC_IMAGE_DIR = "repositorio/originales"
_PICTOGRAM_ID_REGEX = re.compile(r"\/(?P<pictogram_id>\d+)\.png$")


class ArasaacResponse(object):
    def __init__(self, result, page, max_pages):
        self.result = result
        self.page = page
        self.max_pages = max_pages


def find_pictograms(query, page):
    resultdict = defaultdict(set)
    params = _ARASAAC_SEARCH_PARAMS
    params['s'] = query
    params["pg"] = page
    max_pages = 0

    r = requests.post("/".join((_ARASAAC_URL, _ARASAAC_SEARCH_ENDPOINT)), params=params)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    item_list = soup.find(id="ultimas_imagenes")
    if item_list is not None:
        for li in item_list.find_all("li"):
            term = li.img["title"]
            pictogram_id = _PICTOGRAM_ID_REGEX.search(li.img["src"]).group("pictogram_id")
            resultdict[term].add(pictogram_id)

    pagination = soup.find(id="pagination")
    if pagination is not None:
        last_page_url = pagination.find_all("a")[-1]["href"]
        last_page_url_params = dict(parse_qsl(urlsplit(last_page_url).query))
        max_pages = int(last_page_url_params["pg"])

    result = [[term, list(resultdict[term])] for term in resultdict.viewkeys()]
    return ArasaacResponse(result, page, max_pages)
