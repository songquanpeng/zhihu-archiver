import datetime
import os
from shutil import copyfile

import requests
from bs4 import BeautifulSoup

base_path = "docs"


def fetcher():
    res = requests.get("https://www.zhihu.com/hot", headers={
        "authority": "www.zhihu.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    })
    if res.status_code != 200:
        print("Failed to fetch html.")
        exit(-1)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    main_tag = soup.findAll('main')[0]
    list_tag = None
    for child in main_tag.children:
        if child.name == 'div':
            list_tag = child
            break
    if list_tag is None:
        print("Failed to find list tag.")
        exit(-1)
    results = []
    for item in list_tag.children:
        try:
            if item.name != "a":
                continue
            link = item.attrs['href']
            texts = []
            is_second_div = False
            for tag in item.children:
                if tag.name == 'div':
                    if is_second_div:
                        for sub_tag in tag.children:
                            if sub_tag.name in ['div', 'h1']:
                                texts.append(sub_tag.text)
                    else:
                        is_second_div = True
            if len(texts) == 2:
                result = {
                    "link": link,
                    "title": texts[0],
                    "description": "",
                    "hot": texts[1]
                }
            else:
                result = {
                    "link": link,
                    "title": texts[0],
                    "description": texts[1],
                    "hot": texts[2]
                }
        except Exception as e:
            result = {
                "link": "",
                "title": "Error",
                "description": str(e),
                "hot": ""
            }
            print(e)
        results.append(result)
    return results


def write_content(data, title, time, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"抓取于：`{time}`\n\n")
        for i, item in enumerate(data):
            link = item['link']
            title = item['title']
            description = item['description']
            hot = item['hot']
            f.write(f"### {i + 1}. {title}\n")
            f.write(f"{hot} 链接：[{link}]({link})\n\n")
            f.write(f"{description}\n\n")


def build_toc():
    with open(os.path.join(base_path, 'toc.md'), 'w', encoding='utf-8') as f:
        f.write(f"* [介绍](/)\n")
        paths = os.listdir(base_path)
        paths.sort()
        for path in paths:
            full_path = os.path.join(base_path, path)
            if not os.path.isdir(full_path):
                continue
            f.write(f"* [{path}]({path}/)\n")
            sub_files = os.listdir(full_path)
            sub_files.sort()
            for file in sub_files:
                if file == 'README.md':
                    continue
                f.write(f"  * [{file}]({path}/{file})\n")


def main():
    data = fetcher()
    time = datetime.datetime.now()
    year, month, day = time.year, time.month, time.day
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    chapter_str = f"{year}-{month}"
    page_str = f"{day:02}.md"
    title = f"{year} 年 {month} 月 {day} 日的知乎热榜存档"
    if not os.path.exists(os.path.join(base_path, chapter_str)):
        os.mkdir(os.path.join(base_path, chapter_str))
        with open(os.path.join(base_path, chapter_str, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(f"# {year} 年 {month} 月")

    file_path = os.path.join(base_path, chapter_str, page_str)
    write_content(data, title, time_str, file_path)
    copyfile("./README.md", "./docs/README.md")
    build_toc()


if __name__ == '__main__':
    main()
