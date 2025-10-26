import requests
import re
import pprint
import json
from bs4 import BeautifulSoup

def main():
    r = requests.get("https://top.baidu.com/board?tab=realtime", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"})
    text = r.text
    soup = BeautifulSoup(text, "lxml")
    list = soup.find_all(class_=re.compile("^category-wrap"))
    hotData = []
    for item in list:
        aTag = item.find("a")
        content = item.find(class_=re.compile("^content_"))
        href = aTag.attrs.get("href")
        pic = aTag.find("img").attrs.get("src")
        hotTitle = content.find("div", class_="c-single-text-ellipsis").get_text(strip=True)
        hotDesc = content.find(class_=re.compile("^hot-desc"))
        hotDescText = hotDesc.find(string=True, recursive=False).get_text(strip=True)
        hotData.append({
            "picUrl": pic,
            "href": href,
            "hotTitle": hotTitle,
            "hotDescText": hotDescText
        })
    hotData = hotData[1:]
    with open('hotsearch.json', "w", encoding="utf-8") as f:
        json.dump(hotData, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
