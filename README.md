# sxmqwq · 个人主页

主页：<https://sxmqwq.github.io/>

| 入口 | 内容 | 源码 |
| --- | --- | --- |
| [blog](https://sxmqwq.github.io/blog/) | 博客、算法与题解 | 本仓库，使用 [Gmeek](https://github.com/Meekdai/Gmeek) 从 Issues 生成 |
| [scorem](https://sxmqwq.github.io/scorem/) | 算法竞赛评价站 | [sxmqwq/scorem](https://github.com/sxmqwq/scorem) |
| [rhythm](https://sxmqwq.github.io/rhythm/) | 网易云歌词接龙 | [sxmqwq/rhythm](https://github.com/sxmqwq/rhythm) |
| [Tellshift](https://sxmqwq.github.io/tellshift/) | 双向识别秘密策略的游戏 | [sxmqwq/tellshift](https://github.com/sxmqwq/tellshift) |

## 目录

- `home/`：主页、图标和 404 页的源码。
- `docs/`：GitHub Pages 发布目录。根目录是导航主页，`docs/blog/` 是完整博客。
- `docs/post/`、`docs/tag.html`、分页页面：旧博客地址的跳转页，保留查询参数与文章锚点。
- `docs/rss.xml`：兼容旧订阅地址，与 `/blog/rss.xml` 使用相同内容。
- `config.json`：Gmeek 配置，`homeUrl` 固定为 `https://sxmqwq.github.io/blog`。
- `blogBase.json`、`backup/`：博客元信息和 Markdown 备份。
- `scripts/`：博客生成、站点组装和发布前检查。

rhythm、Tellshift、scorem 由各自仓库单独部署，本仓库只提供入口。

## 本地修改

需要 Python 3.10 或更新版本，无须安装前端依赖：

```sh
python3 scripts/assemble_site.py
python3 scripts/validate_site.py
python3 -m http.server 8080 --directory docs
```

修改 `home/` 后重新组装，提交源码及相应的 `docs/` 产物。校验脚本检查所有站内页面链接、四个应用入口、文章元信息、旧地址跳转及 RSS。

## 博客生成与发布

继续通过本仓库 Issues 撰写文章，并添加文章标签。作者编辑、关闭、重新打开文章或调整标签时，`build Gmeek` 工作流重新生成博客；每天也会自动检查一次，可以在 Actions 手动运行。

生成器在临时工作目录运行上游 Gmeek，使用独立的 Python 虚拟环境和 `GITHUB_WORKSPACE`。Gmeek 的清理、README 更新和默认 `docs/` 输出只发生在该临时目录。生成成功后，将博客导入本仓库的 `docs/blog/`，校正分页、搜索、RSS、文章首页按钮和 canonical 地址，并更新备份。

主站和博客共用 `Publish personal site` 发布流程。博客生成完成后直接调用这个可复用工作流，避免 `GITHUB_TOKEN` 的自动提交无法触发 push 工作流的问题。发布始终检出最新 `main`，组装并校验后部署 `docs/`。生成任务推送遇到冲突会停止，不会忽略失败或部署未提交的旧产物。

GitHub Pages 的 Source 继续使用 **GitHub Actions**。生成与部署权限分别限制为所需的 `contents`、`pages`、`id-token` 权限。

