# SQL 自学课 · 交接文档

**版本：v2（20 课全功能版）｜ 定格日期：2026-09-30 ｜ 仓库：xlc-c/sql-web-course**

---

## 1. 项目是什么

一门完全在浏览器本地运行的 SQL 交互式课程，交付物是**单文件 HTML**（约 1 MB）：

- 双击 `index.html` 即可学习，无需安装任何软件、无需联网、公司电脑可用
- SQLite 引擎（sql.js 1.10.3）以 WASM base64 形式内嵌在页面里，所有计算在浏览器内存中完成，关闭页面无残留
- 每课配可运行示例 + 自动判题练习；写入类练习（INSERT/UPDATE/DELETE）在独立数据库副本中判题，不污染公共数据
- 学习进度存浏览器 localStorage，支持导出/导入 JSON、一键清空

**当前内容**：6 篇 20 课 + 使用说明 + 自由沙盒 + Python 篇占位，共 50 道练习（49 道自动判题）。两套数据集：模拟动物档案（4 表，84 动物/7 批次/5 项目/28 入组）+ 销售业务（4 表，24 客户/12 产品/80 订单/约 200 条明细）。

## 2. 仓库结构与文件职责

**本仓库是纯源码仓**：数据集、course_final.json、dist/ 成品全部由脚本生成，不入库（见 .gitignore）。sql.js 引擎为第三方组件，由 fetch-engine.sh 按需拉取。

```
├── README.md                  项目简介与使用方法
├── SQL自学课_交接文档.md       本文档
├── .gitignore
└── src/
    ├── template.html          页面骨架 + 全部 CSS（占位符注入式）
    ├── app.js                 前端运行时：渲染/判题/进度/自检
    ├── content.py             课程内容 v1：使用说明 + 第 0–8 课 + 沙盒 + Python 篇预告
    ├── content_ext.py         课程内容 v2：第三篇函数篇（6–9 课）+ SCHEMA2 + helper
    ├── content_ext2.py        课程内容 v2：JOIN全集/集合/窗口/写入结构篇/实战二（11–17、19 课）
    ├── assemble_course.py     v1 课修订 + v2 课合并 + 分组重排 → course_final.json
    ├── gen_data.py            动物档案数据集生成器（函数级种子 42）
    ├── gen_sales.py           销售数据集生成器（函数级种子 20260930）
    ├── fetch-engine.sh        拉取 sql.js 1.10.3 引擎并转 base64
    └── build.py               总装配：模板+课程+数据+引擎 → dist/index.html
```

## 3. 构建（三步，已验证逐字节复现）

```bash
sh src/fetch-engine.sh          # 仅首次/恢复项目时需要（拉引擎，生成 src/sql-wasm.wasm.b64）
python3 src/assemble_course.py  # 产出 src/course_final.json
python3 src/build.py            # 产出 dist/index.html
```

v2 定格版验收基线：产出物 SHA256 = `54a1e052b0557fb5d2bcc42a6378d038d6a6b9ea0c9afff182929c2fa1dbe13c`。改了内容哈希必然变化，但只要自检通过（§4）即视为有效构建。

## 4. 验证方法（每次改完必跑）

### 自动化自检

```bash
chromium --headless=new --disable-gpu --no-sandbox \
  --virtual-time-budget=20000 --dump-dom \
  'file:///绝对路径/dist/index.html#selftest' 2>/dev/null | grep -o 'data-selftest="[^"]*"'
```

- `#selftest` 触发内置自检：遍历全部判题练习，在克隆副本上验证「答案 SQL 能跑通且自判一致、查询结果非空」
- 合格标准：`fail=0`（v2 定格为 `pass=49 fail=0`）
- `data-boot` 属性确认初始化：`ok lessons=23 animals=84,...,order_items=196`

### 人工抽查

- 任意课点示例「▶ 运行」→ 出结果表
- 练习故意写错 → 报错带中文提示；写对 → 绿色判题通过
- 写入课练习（如第 15 课）判题后去沙盒查，公共数据应**未被改动**

## 5. 二次开发指南

### 加一节新课

1. 在 content_ext 系列文件追加 lesson dict：`id / num / crumb / title / sub / html / exercises`
2. exercise 字段：`id, title, desc(支持HTML), prefill, answer, explain`；可选：
   - `verify`：写入类练习专用。判题时用户 SQL 与答案 SQL 分别在独立副本执行后，用 verify 查询的结果比对
   - `noJudge: true`：自由练习，隐藏判题按钮
3. 在 assemble_course.py 把新课挂进分组 → 重建 → 自检

### 判题原理（改之前必读）

- 判题 = 用户 SQL 与答案 SQL 各自在 **`db.export()` 字节克隆的独立副本** 上执行，比对结果集
- 答案含 `ORDER BY` → 有序比对；否则按多重集合无序比对
- 查询题比最后一条语句的结果集；写入题比 verify 查询的结果
- **绝不能在公共 db 上判题**（踩坑 4）

### 设计规范

- 配色：`--paper:#fafafa` 底 / `--ink:#0a0a0a` 字 / `--accent:#ff8528` 唯一强调色 / 细线 `--line:#e5e5e5`
- 代码工作台深色（`--bench:#101010`），运行按钮橙底胶囊；中文禁用斜体
- 段落入场动画 IntersectionObserver（opacity+blur+位移 700ms），尊重 `prefers-reduced-motion`

## 6. 踩坑清单（递增编号，后来者先看这个）

| # | 坑 | 解法 |
|---|---|---|
| 1 | 课程内容 dict 里多个 `blk(...)` 之间误用逗号 → `SyntaxError: ':' expected after dictionary key`（构建期两次踩中） | blk 之间一律用 `+` 连接；改完先 `python3 -c "import content_ext2"` 验证 |
| 2 | `/tmp` 每轮对话清空：v1 的 gen_data.py 曾因此丢失，靠从成品 index.html 逆向提取才救回数据 | 工作区必须放持久目录；源码即真相，本仓库全部可复现（已用 SHA256 逐字节验证） |
| 3 | sql.js 离线内嵌：`locateFile` 方案必须有网络/文件路径，单文件场景不可用 | `instantiateWasm` 回调 + base64 解码 wasm；JS 内嵌时 `</script` 必须转义为 `<\/script` |
| 4 | 写入类练习若在公共 db 上判题，INSERT/DELETE 会污染沙盒数据 | judge() 与练习运行一律 `new SQL.Database(db.export())` 开独立副本，用完 `.close()` |
| 5 | `julianday('now')` 类非确定性函数会让判题结果漂移 | 课程与答案只用固定基准日期（如 '2025-06-30'） |
| 6 | `LEFT JOIN` 后统计零单客户：`COUNT(*)` 会把补 NULL 的行数成 1 | 用 `COUNT(右表.列)`（不数 NULL）——第 11 课练习 ej1b 围绕此设计 |
| 7 | 多模块共用 Python `random` 全局种子：模块级 `seed()` 会被后导入的模块覆盖，同一管线产出的数据跑偏（order_items 196→208 实测暴露） | 种子写在**函数内**第一行；验收以 dist 哈希比对为准 |
| 8 | GitHub `push_files` 推送后必须 SHA 验证（沿袭 OCR 项目教训） | 推后 `curl raw.githubusercontent.com/...` 拉回，比对 git blob SHA1（`sha1("blob "+len+"\0"+内容)`），不一致用 difflib 定位差异重推 |

## 7. 版本历史

| 版本 | 版本卡 ID | 内容 |
|---|---|---|
| v1 | b40bd4f | 9 课（查询主线）+ 动物档案数据集 |
| v2 | 2a5feed | 扩至 20 课：函数篇/写入与结构篇/窗口函数/集合运算 + 销售数据集 + 写入判题 + 沙盒重置；源码推送 GitHub |

## 8. 待办与路线图

- **Python 篇（占位中）**：大纲已在页面「展望」区；实施时用 Pyodide 内嵌（体积约 10MB+，需评估单文件体积上限，或按「SQL 篇一个文件、Python 篇另一个文件」拆分）
- SQL 篇用户通关后再启动，勿提前实现
- 可选增强：练习通过状态在侧栏可视化（`_pass_` 数据已记录未展示）、错题本
