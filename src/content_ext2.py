# -*- coding: utf-8 -*-
# 追加：JOIN 全集、集合运算、窗口函数、写入与结构篇、实战二
from content_ext import NEW_LESSONS, demo, blk, ex

NEW_LESSONS.extend([

# ========== 第 11 课 JOIN 类型全集 ==========
{"id": "j1", "num": "11", "crumb": "第四篇 · 多表查询 | 第 11 课",
 "title": "JOIN 全家桶：LEFT / CROSS / 自连接",
 "sub": "INNER JOIN 只留对得上的行；LEFT JOIN 把左表全留下——对不上的用 NULL 补齐。",
 "html":
 blk("四种连接方式", "11.1", """
<table class="ref">
<thead><tr><th>写法</th><th>结果</th><th>典型用途</th></tr></thead>
<tbody>
<tr><td><code>INNER JOIN</code>（可省略 INNER）</td><td>只保留两边都对上的行</td><td>查「有明确关联」的数据</td></tr>
<tr><td><code>LEFT JOIN</code></td><td>左表一行不丢，右表对不上就补 NULL</td><td>「所有动物 + 它们的入组情况（没入组的也要列出来）」</td></tr>
<tr><td><code>CROSS JOIN</code></td><td>笛卡尔积：左表每行 × 右表每行</td><td>生成组合（小心爆炸：100 × 100 = 一万行）</td></tr>
<tr><td>自连接（表和自己 JOIN）</td><td>同一张表起两个别名互相连</td><td>「同批次的动物两两配对」这类行与行的比较</td></tr>
</tbody>
</table>
<div class="callout"><b>RIGHT JOIN / FULL JOIN</b> 也存在（SQLite、PostgreSQL 支持，MySQL 不支持 FULL），但业界习惯把它们改写成 LEFT JOIN——把左右表换个位置即可。实际工作里记住 INNER 和 LEFT 就够用 95% 的场景。</div>
""" + demo("dj1a", "示例 · 所有动物及入组项目（没入组的也列出）", "SELECT a.tattoo, a.species, a.status, s.project_no FROM animals a LEFT JOIN assignments s ON a.tattoo = s.tattoo LIMIT 12;") + """
<p>看结果里 <code class="inl">project_no</code> 为（空）的行——它们在 assignments 里没有记录，LEFT JOIN 照样把它们留了下来。如果用 INNER JOIN，这些行会消失。</p>
""" + demo("dj1b", "示例 · 自连接：同种属体重相差不到 0.3kg 的动物对", "SELECT a.tattoo AS 甲, b.tattoo AS 乙, a.species, a.weight_kg AS 甲体重, b.weight_kg AS 乙体重 FROM animals a JOIN animals b ON a.species = b.species AND a.tattoo < b.tattoo AND ABS(a.weight_kg - b.weight_kg) < 0.3 LIMIT 10;") + """
<div class="callout"><b>自连接读法：</b>把 animals 当成两张表（a 和 b），条件 <code class="inl">a.tattoo &lt; b.tattoo</code> 是为了避免「甲配乙」和「乙配甲」重复出现、以及动物和自己配对。</div>
"""),
 "exercises": [
   ex("ej1a", "从未入过组的动物",
     "用 LEFT JOIN + IS NULL 查出<b>没有入组记录</b>的动物纹身号（提示：LEFT JOIN assignments 后，筛 <code>s.tattoo IS NULL</code>）。显示 <code>tattoo</code>、<code>species</code>。",
     "",
     "SELECT a.tattoo, a.species FROM animals a LEFT JOIN assignments s ON a.tattoo = s.tattoo WHERE s.tattoo IS NULL;",
     "「找出没有某记录的行」是 LEFT JOIN 的招牌用法：连上之后筛 NULL。"),
   ex("ej1b", "每个客户的下单数（零单客户也要）",
     "统计每个客户的订单数，<b>一单没下过的客户也要显示为 0</b>。显示 <code>name</code>、<code>city</code>、<code>单数</code>，按单数从多到少排。（提示：从 customers 出发 LEFT JOIN orders；计数用 COUNT(o.order_id) 而不是 COUNT(*)——想想为什么）",
     "",
     "SELECT c.name, c.city, COUNT(o.order_id) AS 单数 FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name, c.city ORDER BY 单数 DESC;",
     "COUNT(列) 不数 NULL 行，所以零单客户得到 0；用 COUNT(*) 会得到 1（那行补的 NULL 也算一行）。")]},

# ========== 第 13 课 集合运算 ==========
{"id": "s1", "num": "13", "crumb": "第四篇 · 多表查询 | 第 13 课",
 "title": "集合运算：UNION / INTERSECT / EXCEPT",
 "sub": "把两个查询结果当一个集合来合并、取交集、求差集。",
 "html":
 blk("三种集合运算", "13.1", """
<table class="ref">
<thead><tr><th>写法</th><th>意思</th><th>类比</th></tr></thead>
<tbody>
<tr><td><code>查询A UNION 查询B</code></td><td>合并并<b>去重</b></td><td>两份名单合成一份，重复的只留一个</td></tr>
<tr><td><code>查询A UNION ALL 查询B</code></td><td>合并<b>不去重</b>（更快）</td><td>两张流水直接摞一起</td></tr>
<tr><td><code>查询A INTERSECT 查询B</code></td><td>交集：两边都有</td><td>既在名单甲又在名单乙的人</td></tr>
<tr><td><code>查询A EXCEPT 查询B</code></td><td>差集：在 A 不在 B</td><td>名单甲里剔除名单乙的人</td></tr>
</tbody>
</table>
<div class="callout"><b>两个硬规矩：</b>① 两边查询的<b>列数必须相同</b>，对应列的类型要兼容；② 列名以第一个查询为准。<b>方言差异：</b>SQL Server 和 PostgreSQL 都有这三个；MySQL 8.0 之前只有 UNION，INTERSECT/EXCEPT 要用 JOIN 改写。</div>
""" + demo("ds1a", "示例 · 交集：2024 年到货且已入组的动物", "SELECT tattoo FROM animals WHERE arrival_date BETWEEN '2024-01-01' AND '2024-12-31' INTERSECT SELECT tattoo FROM assignments;")
 + demo("ds1b", "示例 · 差集：2024 年到货但没入组的动物", "SELECT tattoo FROM animals WHERE arrival_date BETWEEN '2024-01-01' AND '2024-12-31' EXCEPT SELECT tattoo FROM assignments;")),
 "exercises": [
   ex("es1a", "合并两年的到货清单",
     "把「2024 年到货」和「2025 年到货」的动物纹身号合并成一份去重清单（一列 <code>tattoo</code>）。",
     "",
     "SELECT tattoo FROM animals WHERE arrival_date BETWEEN '2024-01-01' AND '2024-12-31' UNION SELECT tattoo FROM animals WHERE arrival_date BETWEEN '2025-01-01' AND '2025-12-31';"),
   ex("es1b", "入组名单里的比格犬",
     "用 INTERSECT 求：assignments 表纹身号 与 比格犬纹身号 的交集。",
     "",
     "SELECT tattoo FROM assignments INTERSECT SELECT tattoo FROM animals WHERE species = '比格犬';"),
   ex("es1c", "入组名单里不是比格犬的",
     "用 EXCEPT 求：在 assignments 里、但不是比格犬的纹身号。",
     "",
     "SELECT tattoo FROM assignments EXCEPT SELECT tattoo FROM animals WHERE species = '比格犬';")]},

# ========== 第 14 课 窗口函数 ==========
{"id": "w1", "num": "14", "crumb": "第四篇 · 多表查询 | 第 14 课",
 "title": "窗口函数：排名、累计、环比",
 "sub": "GROUP BY 会把行折叠成一行；窗口函数不折叠——每一行都能看到自己所在小组的统计值。",
 "html":
 blk("先理解「窗口」", "14.1", """
<p>写法：<code class="inl">函数() OVER (PARTITION BY 分组列 ORDER BY 排序列)</code>。</p>
<ul class="plain">
<li><code class="inl">PARTITION BY</code>：分窗口（类似 GROUP BY，但行不被折叠）</li>
<li><code class="inl">ORDER BY</code>（在 OVER 里）：窗口内排序，排名类函数靠它定名次</li>
</ul>
<table class="ref">
<thead><tr><th>函数</th><th>意思</th></tr></thead>
<tbody>
<tr><td><code>ROW_NUMBER()</code></td><td>窗口内编号 1,2,3…（并列也继续往下编）</td></tr>
<tr><td><code>RANK()</code></td><td>排名，并列同名次、之后跳号（1,1,3）</td></tr>
<tr><td><code>DENSE_RANK()</code></td><td>排名，并列同名次、不跳号（1,1,2）</td></tr>
<tr><td><code>SUM(x) OVER (...)</code></td><td>窗口内累计/合计</td></tr>
<tr><td><code>LAG(x) / LEAD(x)</code></td><td>取窗口内上一行 / 下一行的值（环比、同比的钥匙）</td></tr>
</tbody>
</table>
""" + demo("dw1a", "示例 · 每个种属内部按体重排名", "SELECT tattoo, species, weight_kg, ROW_NUMBER() OVER (PARTITION BY species ORDER BY weight_kg DESC) AS 种属内排名 FROM animals WHERE species IN ('比格犬','食蟹猴') ORDER BY species, 种属内排名 LIMIT 12;")
 + demo("dw1b", "示例 · 销售额逐月累计", "WITH m AS (SELECT strftime('%Y-%m', o.order_date) AS 月份, SUM(i.qty * i.unit_price) AS 销售额 FROM orders o JOIN order_items i ON o.order_id = i.order_id WHERE o.status = '已完成' GROUP BY 月份) SELECT 月份, ROUND(销售额, 0) AS 月销售额, ROUND(SUM(销售额) OVER (ORDER BY 月份), 0) AS 累计销售额 FROM m LIMIT 12;") + """
<div class="callout"><b>分组 vs 窗口一句话区分：</b>「每组一行」用 GROUP BY；「每行都保留、但带上组内统计/名次」用窗口函数。面试和工作里「每个分组的前 N 名」几乎必考窗口函数。</div>
"""),
 "exercises": [
   ex("ew1a", "全体动物体重总排名",
     "给所有动物按体重从高到低排名（不分种属），显示 <code>tattoo</code>、<code>species</code>、<code>weight_kg</code>、<code>总排名</code>（用 RANK）。",
     "",
     "SELECT tattoo, species, weight_kg, RANK() OVER (ORDER BY weight_kg DESC) AS 总排名 FROM animals;"),
   ex("ew1b", "每月销售额与上月对比",
     "用 LAG 算环比：先按 CTE 算出每月销售额（已完成订单），再显示 <code>月份</code>、<code>月销售额</code>（ROUND 0 位）、<code>比上月增加</code>（本月减上月，ROUND 0 位）。",
     "WITH m AS (\n  SELECT strftime('%Y-%m', o.order_date) AS 月份, SUM(i.qty * i.unit_price) AS 销售额\n  FROM orders o JOIN order_items i ON o.order_id = i.order_id\n  WHERE o.status = '已完成' GROUP BY 月份\n)\n-- 下面用 LAG 取上月销售额\n",
     "WITH m AS (SELECT strftime('%Y-%m', o.order_date) AS 月份, SUM(i.qty * i.unit_price) AS 销售额 FROM orders o JOIN order_items i ON o.order_id = i.order_id WHERE o.status = '已完成' GROUP BY 月份) SELECT 月份, ROUND(销售额, 0) AS 月销售额, ROUND(销售额 - LAG(销售额) OVER (ORDER BY 月份), 0) AS 比上月增加 FROM m;",
     "第一行没有上月，LAG 返回 NULL，「比上月增加」为空是正常的。")]},

# ========== 第 15 课 写入 ==========
{"id": "d1", "num": "15", "crumb": "第五篇 · 写入与结构 | 第 15 课",
 "title": "写入数据：INSERT / UPDATE / DELETE",
 "sub": "前面的查询都是「只读」；这一课开始改数据。本课程的写入练习在独立副本里运行，不会弄坏公共数据，放心大胆试。",
 "html":
 blk("三个写入语句", "15.1", """
<table class="ref">
<thead><tr><th>语句</th><th>意思</th><th>例子</th></tr></thead>
<tbody>
<tr><td><code>INSERT INTO 表 VALUES (...)</code></td><td>插入新行</td><td><code>INSERT INTO batches VALUES ('B2510-017', ...);</code></td></tr>
<tr><td><code>UPDATE 表 SET 列=值 WHERE ...</code></td><td>改已有行</td><td><code>UPDATE animals SET status='已淘汰' WHERE tattoo='23001D';</code></td></tr>
<tr><td><code>DELETE FROM 表 WHERE ...</code></td><td>删行</td><td><code>DELETE FROM orders WHERE status='已取消';</code></td></tr>
</tbody>
</table>
<div class="callout"><b>最重要的安全常识：UPDATE 和 DELETE 不带 WHERE ＝ 对全表动手。</b><code class="inl">DELETE FROM orders;</code> 会把整个表清空。真实工作里的保命流程：先把 WHERE 条件用 SELECT 跑一遍，确认选中的就是要改的行，再把 SELECT 换成 UPDATE/DELETE。</div>
""" + demo("dd1a", "示例 · UPDATE 前先 SELECT 验证目标行", "SELECT tattoo, species, status FROM animals WHERE tattoo = '23001D';")) +
 blk("事务：要么全成，要么全不成", "15.2", """
<p>转账式操作（先删 A 再插 B）最怕做一半出错。<code class="inl">BEGIN;</code> 开始事务，<code class="inl">COMMIT;</code> 提交生效，<code class="inl">ROLLBACK;</code> 撤销回开始前的状态。练习区里可以亲自试：BEGIN 之后 DELETE 一张表，ROLLBACK 之后数据还在。</p>
"""),
 "exercises": [
   ex("ed1a", "插入一个新批次",
     "往 batches 表插入一批新到的兔子：批次号 <code>B2510-017</code>，引进许可 <code>省内不提供</code>，运输证 NULL，供应商 <code>苏州湖景实验动物</code>，到货日期 <code>2025-10-12</code>，10 只。判题时会检查这一行是否正确写入。",
     "INSERT INTO batches VALUES (...);",
     "INSERT INTO batches VALUES ('B2510-017', '省内不提供', NULL, '苏州湖景实验动物', '2025-10-12', 10);",
     "VALUES 里的顺序必须和建表时的列顺序一致：batch_no, permit_no, transport_no, vendor, arrival_date, headcount。",
     verify="SELECT * FROM batches WHERE batch_no = 'B2510-017'"),
   ex("ed1b", "全体比格犬体重加 0.5",
     "一次称重复录后发现秤偏轻：把所有比格犬的体重 <code>weight_kg</code> 更新为原值 + 0.5（用 ROUND 保留 1 位小数）。判题时检查更新后的平均体重。",
     "",
     "UPDATE animals SET weight_kg = ROUND(weight_kg + 0.5, 1) WHERE species = '比格犬';",
     "SET 右侧可以直接用旧值参与计算。",
     verify="SELECT ROUND(AVG(weight_kg), 2) AS avg_w FROM animals WHERE species = '比格犬'"),
   ex("ed1c", "删除所有已取消订单",
     "把 orders 表里状态为「已取消」的订单删掉。判题时检查剩余数量。",
     "",
     "DELETE FROM orders WHERE status = '已取消';",
     "想想遗留问题：order_items 里这些订单的明细还在，成了「孤儿数据」——真实系统里要么连带删，要么用外键约束拦住。",
     verify="SELECT COUNT(*) AS n FROM orders WHERE status = '已取消'")]},

# ========== 第 16 课 建表与约束 ==========
{"id": "d2", "num": "16", "crumb": "第五篇 · 写入与结构 | 第 16 课",
 "title": "建表与约束：CREATE TABLE / ALTER / DROP",
 "sub": "约束是数据库的「门卫」——把脏数据挡在门外，比事后清洗便宜一百倍。",
 "html":
 blk("CREATE TABLE 与数据类型", "16.1", """
<p>SQLite 的主要类型：<code class="inl">TEXT</code>（文本）、<code class="inl">INTEGER</code>（整数）、<code class="inl">REAL</code>（小数）。建表时逐列声明名字和类型：</p>
""" + demo("dd2a", "示例 · 建一张笼位表", "CREATE TABLE IF NOT EXISTS cages_demo (\n  cage_no TEXT PRIMARY KEY,\n  room TEXT NOT NULL,\n  species TEXT,\n  capacity INTEGER DEFAULT 2\n);")) +
 blk("五种约束（门卫规则）", "16.2", """
<table class="ref">
<thead><tr><th>约束</th><th>作用</th></tr></thead>
<tbody>
<tr><td><code>PRIMARY KEY</code></td><td>主键：唯一且非空，一行的「身份证」</td></tr>
<tr><td><code>NOT NULL</code></td><td>不许为空</td></tr>
<tr><td><code>UNIQUE</code></td><td>不许重复</td></tr>
<tr><td><code>DEFAULT 值</code></td><td>不写就自动填默认值</td></tr>
<tr><td><code>CHECK(条件)</code></td><td>自定义校验，如 <code>CHECK(weight &gt; 0)</code></td></tr>
</tbody>
</table>
<p>还有 <code class="inl">FOREIGN KEY</code>（外键，保证「引用的行必须存在」）——SQLite 默认不强制执行，MySQL/PostgreSQL 默认强制，概念一致。</p>
""") +
 blk("改表与删表", "16.3", """
<ul class="plain">
<li><code class="inl">ALTER TABLE 表 ADD COLUMN 列名 类型;</code> ——加列（最常用）</li>
<li><code class="inl">DROP TABLE 表;</code> ——整表删除，不可恢复，三思</li>
<li><code class="inl">IF NOT EXISTS / IF EXISTS</code> ——加这两个保险，避免重复执行报错</li>
</ul>
<div class="callout"><b>方言差异：</b>自增编号 SQLite 写 <code class="inl">INTEGER PRIMARY KEY AUTOINCREMENT</code>，MySQL 是 <code class="inl">AUTO_INCREMENT</code>，SQL Server 是 <code class="inl">IDENTITY(1,1)</code>。</div>
"""),
 "exercises": [
   ex("ed2a", "亲手建一张笼位表并插入数据",
     "建表 <code>cages</code>：cage_no TEXT 主键、room TEXT 非空、species TEXT、capacity INTEGER 默认 2；然后插入两行：<code>A-101 / 犬舍一 / 比格犬 / 2</code> 和 <code>A-102 / 犬舍一 / 比格犬 / 2</code>。判题时检查行数。",
     "CREATE TABLE cages (\n  ...\n);\nINSERT INTO cages VALUES (...), (...);",
     "CREATE TABLE cages (cage_no TEXT PRIMARY KEY, room TEXT NOT NULL, species TEXT, capacity INTEGER DEFAULT 2); INSERT INTO cages VALUES ('A-101', '犬舍一', '比格犬', 2), ('A-102', '犬舍一', '比格犬', 2);",
     "INSERT 可以一条语句插多行：VALUES (...), (...)。",
     verify="SELECT COUNT(*) AS n FROM cages"),
   ex("ed2b", "给动物表加一列房间号",
     "用 ALTER TABLE 给 animals 加一列 <code>room_no</code>（TEXT）。判题时检查这一列是否存在。",
     "",
     "ALTER TABLE animals ADD COLUMN room_no TEXT;",
     "SQLite 的 ALTER 只支持加列等少数操作；要改列类型得「建新表-搬数据-删旧表-改名」四步走，这是它和 MySQL 的主要差别。",
     verify="SELECT COUNT(*) AS n FROM pragma_table_info('animals') WHERE name = 'room_no'"),
   ex("ed2c", "建一张带 CHECK 的称重记录表",
     "建表 <code>weights_log</code>：tattoo TEXT、weight REAL，且 weight 必须大于 0（CHECK 约束）。判题时检查表是否建成。建完后可以自己试试插入一条 weight = -1 的数据，看约束如何把它挡下。",
     "",
     "CREATE TABLE weights_log (tattoo TEXT, weight REAL CHECK(weight > 0));",
     "约束生效时，非法数据会直接报错拒绝写入——脏数据进不来，比对账轻松得多。",
     verify="SELECT COUNT(*) AS n FROM sqlite_master WHERE type = 'table' AND name = 'weights_log'")]},

# ========== 第 17 课 视图与索引 ==========
{"id": "d3", "num": "17", "crumb": "第五篇 · 写入与结构 | 第 17 课",
 "title": "视图与索引：把查询存起来，把速度提上去",
 "sub": "视图是「存起来的 SELECT」，索引是「书的目录」——两个生产环境天天用的东西。",
 "html":
 blk("视图 VIEW", "17.1", """
<p>一条复杂的三表 JOIN，每次重写一遍既累又容易错。<code class="inl">CREATE VIEW 名字 AS 查询</code> 把它存成「虚拟表」，之后当普通表查。视图本身不存数据，每次查视图都会实时跑里面的 SQL，所以底层数据变了视图结果跟着变。</p>
<ul class="plain">
<li>删掉视图：<code class="inl">DROP VIEW 名字;</code></li>
<li>典型用途：给常用关联查询起个固定的名字、给下游报表提供稳定接口、隐藏敏感列</li>
</ul>
""") +
 blk("索引 INDEX", "17.2", """
<p>没有索引时，数据库找一行要<b>全表扫描</b>（逐行翻）；建了索引就像给书加目录，直接定位。写法：<code class="inl">CREATE INDEX 名字 ON 表(列);</code></p>
<ul class="plain">
<li>该建：经常出现在 WHERE / JOIN 里的列（如 tattoo、batch_no）</li>
<li>别乱建：索引占空间，还会拖慢写入（每次写都要维护目录）</li>
<li>主键自动有索引，不用重复建</li>
<li>想看查询有没有用上索引：<code class="inl">EXPLAIN QUERY PLAN 你的查询</code></li>
</ul>
<div class="callout"><b>本课程数据量小</b>（百行级），索引的快慢差异感觉不出来；到了百万行的真实库，有没有索引就是毫秒和分钟的差别。</div>
"""),
 "exercises": [
   ex("ed3a", "把入组清单存成视图",
     "创建视图 <code>v_roster</code>：三表关联的入组清单（assignments JOIN animals JOIN projects，含 tattoo、species、project_no、client、dose_group 五列）。判题时检查视图能否查出正确的行数。",
     "CREATE VIEW v_roster AS\nSELECT ...\n",
     "CREATE VIEW v_roster AS SELECT a.tattoo, a.species, p.project_no, p.client, s.dose_group FROM assignments s JOIN animals a ON s.tattoo = a.tattoo JOIN projects p ON s.project_no = p.project_no;",
     "建完可以试试 SELECT * FROM v_roster; ——像普通表一样用。",
     verify="SELECT COUNT(*) AS n FROM v_roster"),
   ex("ed3b", "给种属列建索引",
     "给 animals 表的 <code>species</code> 列建一个名为 <code>idx_animals_species</code> 的索引。判题时检查索引是否存在。",
     "",
     "CREATE INDEX idx_animals_species ON animals(species);",
     "命名惯例：idx_表名_列名，一眼能看懂。",
     verify="SELECT COUNT(*) AS n FROM sqlite_master WHERE type = 'index' AND name = 'idx_animals_species'")]},

# ========== 第 19 课 综合实战二 ==========
{"id": "x2", "num": "19", "crumb": "第六篇 · 综合实战 | 第 19 课",
 "title": "综合实战二：经营数据简报",
 "sub": "换一套业务（销售数据）独立走完整流程：取数 → 加工 → 排名 → 趋势——检验你是不是真的会了。",
 "html":
 blk("任务背景", "19.1", """
<p>你在分析一套销售数据：customers（客户）、products（产品）、orders（订单）、order_items（订单明细）四张表。关系链：<code class="inl">orders.customer_id → customers</code>，<code class="inl">order_items.order_id → orders</code>，<code class="inl">order_items.product_id → products</code>。金额 = <code class="inl">qty × unit_price</code>，只有「已完成」订单计入销售。</p>
""" + demo("dx2a", "示例 · 先跑通：每个产品类别的销售额", "SELECT p.category, ROUND(SUM(i.qty * i.unit_price), 0) AS 销售额 FROM order_items i JOIN products p ON i.product_id = p.product_id JOIN orders o ON i.order_id = o.order_id WHERE o.status = '已完成' GROUP BY p.category ORDER BY 销售额 DESC;")),
 "exercises": [
   ex("ex2a", "2024 年消费 TOP 10 客户",
     "统计 2024 年「已完成」订单中每个客户的消费总额，关联出客户姓名和城市，取前 10。显示 <code>name</code>、<code>city</code>、<code>年消费</code>（ROUND 0 位），按年消费从高到低。",
     "",
     "SELECT c.name, c.city, ROUND(SUM(i.qty * i.unit_price), 0) AS 年消费 FROM orders o JOIN order_items i ON o.order_id = i.order_id JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = '已完成' AND strftime('%Y', o.order_date) = '2024' GROUP BY o.customer_id, c.name, c.city ORDER BY 年消费 DESC LIMIT 10;",
     "三表链式 JOIN：orders 是中间桥梁，一头连客户一头连明细。"),
   ex("ex2b", "各等级客户贡献了多少销售额",
     "按客户等级（level）统计已完成订单的销售额，显示 <code>level</code> 和 <code>销售额</code>（ROUND 0 位），从高到低排。",
     "",
     "SELECT c.level, ROUND(SUM(i.qty * i.unit_price), 0) AS 销售额 FROM orders o JOIN order_items i ON o.order_id = i.order_id JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = '已完成' GROUP BY c.level ORDER BY 销售额 DESC;"),
   ex("ex2c", "期末考：月度经营简报",
     "一条 SQL 出月度简报：<code>月份</code>、<code>单量</code>（已完成订单数，注意一笔订单有多条明细——用 COUNT(DISTINCT ...)）、<code>销售额</code>（ROUND 0 位）、<code>累计销售额</code>（窗口函数累计，ROUND 0 位），按月份升序。",
     "WITH m AS (\n  -- 先按月汇总：月份、单量、销售额\n)\n-- 再用窗口函数加累计列\n",
     "WITH m AS (SELECT strftime('%Y-%m', o.order_date) AS 月份, COUNT(DISTINCT o.order_id) AS 单量, SUM(i.qty * i.unit_price) AS 销售额 FROM orders o JOIN order_items i ON o.order_id = i.order_id WHERE o.status = '已完成' GROUP BY 月份) SELECT 月份, 单量, ROUND(销售额, 0) AS 销售额, ROUND(SUM(销售额) OVER (ORDER BY 月份), 0) AS 累计销售额 FROM m ORDER BY 月份;",
     "做完这题，SQL 的完整版图你就走完了：查询、分组、函数、多表、集合、窗口、写入、结构。")]},
])
