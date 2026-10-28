# 渡言 Duyan 工作约定

- 这是公开仓库：推送前先问 Sora；不放本机路径、账号和参考字体的渲染图（见 `.gitignore`）。
- 先读 README，再读 [设计与造字方式](docs/DESIGN.md)、[造字规范](docs/RULES.md) 和 [汉字结构规范](docs/STRUCTURE.md) 里和本任务相关的部分；画字、改字按造字规范来。
- 所有字形从零绘制，不引用、不描摹任何现成字体的轮廓。
- 构建和检查用 `python3 build.py`：先按设计意图检查字形，再生成 `sample/Duyan-Sample.otf`。小样页在仓库目录运行 `python3 -m http.server 8766` 后打开 `/sample/`。
- 修改前检查 `git status`，保留别的对话留下的修改；提交只包含本任务文件。
- 合入前检查：`python3 build.py`（检查字形并生成小样字体）。
