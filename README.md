# sxmqwq's blog

博客：<https://sxmqwq.github.io/>

使用 [Gmeek](https://github.com/Meekdai/Gmeek) 从本仓库 Issues 生成文章。

- `docs/`：博客的 GitHub Pages 发布目录。
- `docs/blog/`：原 `/blog/` 地址的兼容跳转和 RSS。
- `config.json`：博客配置。
- `blogBase.json`、`backup/`：文章元信息和 Markdown 备份。
- `scripts/`：生成、组装和发布前检查。

本地检查与预览（Python 3.10+）：

```sh
python3 scripts/assemble_site.py
python3 scripts/validate_site.py
python3 -m http.server 8080 --directory docs
```

在 Issues 撰写文章并添加标签后，`build Gmeek` 自动生成博客；也可在 Actions 手动运行。生成器在独立临时目录运行上游 Gmeek，将文章导入 `docs/`，更新备份，再调用 `Publish blog` 发布。GitHub Pages 的 Source 使用 **GitHub Actions**。

