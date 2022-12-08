from bs4 import BeautifulSoup
import re
import requests
import sys
import platform

SYSTEM_TO_SUFFIX = {
    "Windows": "win32",
    "Darwin": {
        "arm64": "mac_arm64",
        None: "mac64"
    },
    None: "linux64",
}

page = requests.get("https://chromedriver.chromium.org/")
soup = BeautifulSoup(page.content, "html.parser")
version_tags = soup.find_all(text=re.compile("Latest"))
if not version_tags:
    print("No version tags!")
    sys.exit(1)

stable_tags = [tag.parent for tag in version_tags if "stable" in tag.parent.text]
if not stable_tags:
    print("No stable tags!")
    sys.exit(1)
assert len(stable_tags) == 1

version_links = stable_tags[0].parent.findAll("a")
if not version_links:
    print("No version links!")
    sys.exit(1)

dl_page_link = version_links[0]
if not dl_page_link.has_attr("href"):
    print("No version href!")
    sys.exit(1)

uname = platform.uname()
suffix = SYSTEM_TO_SUFFIX.get(uname.system, SYSTEM_TO_SUFFIX.get(None))
if isinstance(suffix, dict):
    suffix = suffix.get(uname.machine, suffix.get(None, ""))

dl_page_href = dl_page_link["href"]
dl_href = re.sub(r"index\.html\?path=([^/&]+).*", rf"\1/chromedriver_{suffix}.zip", dl_page_href)
print(dl_href)
