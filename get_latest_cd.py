from bs4 import BeautifulSoup
import re
import requests
import sys

page = requests.get("https://chromedriver.chromium.org/")
soup = BeautifulSoup(page.content, "html.parser")
version_tags = soup.findAll(text=re.compile("Latest stable release"))
if not version_tags:
    sys.exit(1)

version_links = version_tags[0].parent.findAll("a")
if not version_links:
    sys.exit(1)

dl_page_link = version_links[0]
if not dl_page_link.has_attr("href"):
    sys.exit(1)

dl_page_href = dl_page_link["href"]
dl_href = re.sub(r"index\.html\?path=([^/&]+).*", r"\1/chromedriver_win32.zip", dl_page_href)
print(dl_href)
