import datetime
import os
from shutil import copyfile

from fetcher import fetch

base_path = "docs"


def write_content(data, title, time, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"抓取于：`{time}`\n\n")
        for i, item in enumerate(data):
            link = item['link']
            title = item['title']
            description = item['description']
            hot = item['hot']
            f.write(f"### [{i + 1}. {title}]({link})\n")
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
            year, month = path.split('-')
            f.write(f"* [{year} 年 {month} 月]({path}/)\n")
            sub_files = os.listdir(full_path)
            sub_files.sort()
            for file in sub_files:
                if file == 'README.md':
                    continue
                day = file.split('.')[0]
                f.write(f"  * [{month} 月 {day} 日]({path}/{file})\n")


def update_chapter(chapter_str):
    with open(os.path.join(base_path, chapter_str, "README.md"), 'w', encoding='utf-8') as f:
        year, month = chapter_str.split('-')
        f.write(f"# {year} 年 {month} 月\n\n")
        paths = os.listdir(os.path.join(base_path, chapter_str))
        paths.sort()
        for path in paths:
            if path == 'README.md':
                continue
            day = path.split('.')[0]
            f.write(f"+ [{month} 月 {day} 日的知乎热榜存档](/{chapter_str}/{day})\n")


def main():
    data = fetch()
    time = datetime.datetime.now()
    year, month, day = time.year, time.month, time.day
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    chapter_str = f"{year}-{month}"
    page_str = f"{day:02}.md"
    title = f"{year} 年 {month} 月 {day} 日的知乎热榜存档"
    if not os.path.exists(os.path.join(base_path, chapter_str)):
        os.mkdir(os.path.join(base_path, chapter_str))

    file_path = os.path.join(base_path, chapter_str, page_str)
    write_content(data, title, time_str, file_path)
    update_chapter(chapter_str)
    copyfile("./README.md", "./docs/README.md")
    build_toc()


if __name__ == '__main__':
    main()
