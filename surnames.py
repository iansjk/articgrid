from __future__ import absolute_import, print_function
import urllib
import contextlib
import re
import codecs
from bs4 import BeautifulSoup

DUPLICATE_SURNAME_REGEX = re.compile(r" \(\d+\)$")
BTN_URL = "http://surnames.behindthename.com/names/browse.php"
BTN_URL_PARAMS = {
    "type_options": 1,
    "operator_options": "is",
    "displayoperator_options": "is",
    "display_options[]": "ultracompact",
}


def _scrape_surnames():
    surnames = set()
    looping = True
    i = 1
    while looping:
        BTN_URL_PARAMS['page'] = i
        url = "{0}?{1}".format(BTN_URL, urllib.urlencode(BTN_URL_PARAMS))
        with contextlib.closing(urllib.urlopen(url)) as html:
            soup = BeautifulSoup(html.read(), 'html5lib')
        try:
            for anchor in soup.find(id="div_results").find_next_sibling("table").find_all("a"):
                surname = re.sub(DUPLICATE_SURNAME_REGEX, "", anchor.get_text())
                surnames.add(surname.lower())
        except AttributeError:
            looping = False
        i += 1
    return surnames

try:
    with codecs.open("surnames.txt", "r", "utf-8") as infile:
        surnames = set()
        for line in infile.read().splitlines():
            surnames.add(line)
except IOError:
    surnames = _scrape_surnames()

if __name__ == "__main__":
    with codecs.open("surnames.txt", "w", "utf-8") as outfile:
        for surname in sorted(surnames):
            print(surname, file=outfile)
