import requests
from bs4 import BeautifulSoup

headers = {
    "authority": "www.zhihu.com",
    "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def fetch_by_html():
    res = requests.get("https://www.zhihu.com/hot", headers=headers)
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


def fetch_by_api():
    res = requests.get("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total", headers=headers)
    data = res.json()
    results = []
    for item in data['data']:
        result = {
            "link": f"https://www.zhihu.com/question/{item['target']['id']}",
            "title": item['target']['title'],
            "description": item['target']['excerpt'],
            "hot": item['detail_text']
        }
        results.append(result)
    return results


def fetch():
    try:
        data = fetch_by_api()
    except:
        print("Failed to fetch from api.")
        data = fetch_by_html()
    return data
