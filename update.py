import requests
import os
import datetime
from dateutil import tz

token = ''
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
top_repo_num = 10
recent_repo_num = 10

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


def fetcher(username: str):
    result = {
        'name': '',
        'public_repos': 0,
        'top_repos': [],
        'recent_repos': []
    }
    user_info_url = "https://api.github.com/users/{}".format(username)
    header = {} if token == "" else {"Authorization": "bearer {}".format(token)}
    res = requests.get(user_info_url, header)
    user = res.json()
    result['name'] = user['name']
    repos = []
    for i in range(1, 2 + user['public_repos'] // 100):
        all_repos_url = "https://api.github.com/users/{}/repos?per_page=100&page={}".format(username, i)
        res = requests.get(all_repos_url, header)
        repos.extend(res.json())
    processed_repos = []
    for repo in repos:
        if repo['fork']:
            continue
        processed_repo = {
            'score': repo['stargazers_count'] + repo['watchers_count'] + repo['forks_count'],
            'star': repo['stargazers_count'],
            'link': repo['html_url'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'pushed_at': repo['pushed_at'],
            'name': repo['name'],
            'description': repo['description']
        }
        date = datetime.datetime.strptime(processed_repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
        date = date.replace(tzinfo=from_zone)
        date = date.astimezone(to_zone)
        processed_repo['pushed_at'] = date.strftime('%Y-%m-%d %H:%M:%S')
        processed_repos.append(processed_repo)
    top_repos = sorted(processed_repos, key=lambda x: x['score'], reverse=True)
    top_repos = top_repos[:top_repo_num]
    result['top_repos'] = top_repos
    recent_repos = sorted(processed_repos, key=lambda x: x['pushed_at'], reverse=True)
    recent_repos = recent_repos[:recent_repo_num]
    result['recent_repos'] = recent_repos
    return result


abstract_tpl = """## Abstract
<p>
  <img src="https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&hide_border=true" alt="{github_name}'s Github Stats" width="58%" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={github_username}&layout=compact&hide_border=true&langs_count=10" alt="{github_name}'s Top Langs" width="37%" /> 
</p>

<p>
  <img src="https://stats.justsong.cn/api/leetcode/?username=quanpeng&theme=light" alt="JustSong's LeetCode Stats" width="49%" />
  <img src="https://stats.justsong.cn/api/zhihu/?username=songwonderful&theme=light" alt="JustSong's Zhihu Stats" width="49%" /> 
</p>

*Cards provided by [https://github.com/songquanpeng/stats-cards](https://github.com/songquanpeng/stats-cards).*

"""

zhihu_tpl = "[![{github_name}'s Zhihu Stats](https://stats.justsong.cn/api/zhihu?username={zhihu_username})](https://github.com/songquanpeng/readme-stats)\n"

recent_repos_tpl = """\n## Recent Repos
|Repo|Description|Last Update|
|:--|:--|:--|
"""

top_repos_tpl = """\n## Top Repos
|Repo|Description|Star|
|:--|:--|:--|
""".format(current_time)

footer_tpl = """
\n
*Last automatic update at {} by [https://github.com/songquanpeng/songquanpeng/blob/master/update.py](https://github.com/songquanpeng/songquanpeng/blob/master/update.py).*
""".format(current_time)


def render(github_username, github_data, zhihu_username='') -> str:
    markdown = ""
    global abstract_tpl
    if zhihu_username:
        abstract_tpl += zhihu_tpl
    markdown += abstract_tpl.format(github_username=github_username, github_name=github_data['name'],
                                    zhihu_username=zhihu_username)
    global recent_repos_tpl
    for repo in github_data['recent_repos']:
        recent_repos_tpl += "|[{name}]({link})|{description}|`{pushed_at}`|\n".format(**repo)
    markdown += recent_repos_tpl
    global top_repos_tpl
    for repo in github_data['top_repos']:
        top_repos_tpl += "|[{name}]({link})|{description}|`{star}`|\n".format(**repo)
    markdown += top_repos_tpl
    markdown += footer_tpl
    return markdown


def writer(markdown) -> bool:
    ok = True
    try:
        with open('./README.md', 'w') as f:
            f.write(markdown)
    except IOError:
        ok = False
        print('unable to write to file')
    return ok


def pusher():
    commit_message = ":pencil2: update on {}".format(current_time)
    os.system('git add ./README.md')
    if os.getenv('DEBUG'):
        return
    os.system('git commit -m "{}"'.format(commit_message))
    os.system('git push')


def main():
    global top_repo_num
    global recent_repo_num
    top_repo_num = 10
    recent_repo_num = 10
    github_username = os.getenv('GITHUB_USERNAME')
    if not github_username:
        cwd = os.getcwd()
        github_username = os.path.split(cwd)[-1]
    zhihu_username = os.getenv('ZHIHU_USERNAME')
    github_data = fetcher(github_username)
    markdown = render(github_username, github_data, zhihu_username)
    if writer(markdown):
        pass
        # pusher()


if __name__ == '__main__':
    main()
