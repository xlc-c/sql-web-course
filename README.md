# SQL 自学课 · 网页版

完全在浏览器本地运行的交互式 SQL 课程：**双击 HTML 即学，无需安装、无需联网、数据不出本机**。

> 本仓库为**纯源码仓**。成品 `index.html`（约 1 MB 单文件）由构建产出、不入库；三条命令即可构建（见下）。

## 课程内容（6 篇 20 课 · 50 道自动判题练习）

| 篇章 | 内容 |
|---|---|
| 一、查询基础 | SELECT / WHERE / 组合条件 / 排序 / DISTINCT |
| 二、分组统计 | 聚合函数 / GROUP BY / HAVING |
| 三、常用函数 | 字符串 / 日期 / 数值与类型转换 / CASE / NULL |
| 四、多表查询 | JOIN 全集 / 子查询 / CTE / 集合运算 / 窗口函数 |
| 五、写入与结构 | INSERT / UPDATE / DELETE / 事务 / 建表 / 约束 / 视图 / 索引 |
| 六、综合实战 | 两套业务数据各做一次完整实战 |

特性：示例一键运行、练习自动判题（报错带中文提示）、写入练习在独立副本判题不弄脏数据、沙盒一键重置、进度本地保存可导出导入。内置两套数据集：模拟动物档案（4 表）+ 销售业务（4 表）。

## 构建

```bash
sh src/fetch-engine.sh          # 首次：拉取 sql.js 1.10.3 引擎并转 base64
python3 src/assemble_course.py  # 组装课程内容
python3 src/build.py            # 产出 dist/index.html
```

构建、自检（`#selftest`）、二次开发、踩坑清单详见 [SQL自学课_交接文档.md](SQL自学课_交接文档.md)。

## 技术

单文件 HTML，内嵌 [sql.js](https://github.com/sql-js/sql.js)（SQLite 编译为 WASM，base64 内联，浏览器本地执行）。
