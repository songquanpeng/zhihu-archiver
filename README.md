# 知乎热榜备份

## 描述
每日自动备份知乎热榜，并构建静态网站。

在线预览：https://zhihu.justsong.cn/

仓库地址：https://github.com/songquanpeng/zhihu-archiver

Fork 示例仓库地址：https://github.com/justsong-lab/zhihu-archiver

## 部署
### 部署方式 #1：GitHub Action + GitHub Pages
1. 首先 fork 本项目；
2. 之后去 Actions 页面启动 workflow。
3. 去仓库设置页面启用 GitHub Pages，选择 master 分支下的 docs 目录。

### 部署方式 #2：自己的服务器 + GitHub Pages
1. 首先 fork 本项目；
2. 之后在你的服务器下 clone 你的 fork，并进入项目目录；
3. 配置 Python 环境并安装依赖：
   ```shell
   sudo apt install python-is-python3 python3-pip
   pip install -r requirements.txt
   ```
4. 给脚本执行权限：`chmod u+x ./update.sh`；
5. 之后设置 crontab 如下：
    ```
    0 18 * * * cd /path/to/zhihu-archiver && ./update.sh
    ```
6. 再之后去仓库设置页面启用 GitHub Pages，选择 master 分支下的 docs 目录。