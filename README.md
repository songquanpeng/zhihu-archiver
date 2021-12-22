# 知乎热榜备份

## 描述
每日自动备份知乎热榜，并构建静态网站。

## 部署
目前提供两张部署方式，一种利用 Github Action，全自动部署，fork 之后去 Actions 页面启动 workflow 即可。

第二种方式是用自己的服务器进行抓取操作，
首先给脚本执行权限：`chmod u+x ./update.sh`

之后设置 crontab 如下：
```
0 18 * * * cd /path/to/zhihu-archiver && ./update.sh
```
