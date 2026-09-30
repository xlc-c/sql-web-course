# -*- coding: utf-8 -*-
"""新增课程：第三篇函数篇、第四篇补充课、第五篇写入与结构、实战二"""

SCHEMA2_HTML = """
<table class="ref">
<thead><tr><th>表名</th><th>含义</th><th>主要列</th></tr></thead>
<tbody>
<tr><td><code>customers</code></td><td>客户表</td><td><code>customer_id</code> 客户编号、<code>name</code> 姓名、<code>city</code> 城市、<code>level</code> 等级（普通/银卡/金卡/钻石）、<code>join_date</code> 注册日期</td></tr>
<tr><td><code>products</code></td><td>产品表</td><td><code>product_id</code> 编号、<code>name</code> 品名、<code>category</code> 类别（饲料/垫料/耗材/试剂/设备）、<code>price</code> 单价、<code>cost</code> 成本</td></tr>
<tr><td><code>orders</code></td><td>订单表</td><td><code>order_id</code> 订单号、<code>customer_id</code> 客户编号、<code>order_date</code> 下单日期、<code>status</code> 状态（已完成/已取消/退款）、<code>channel</code> 渠道</td></tr>
<tr><td><code>order_items</code></td><td>订单明细表</td><td><code>order_id</code> 订单号、<code>product_id</code> 产品编号、<code>qty</code> 数量、<code>unit_price</code> 成交单价</td></tr>
</tbody>
</table>
"""

def demo(demo_id, label, sql):
    return (f'<div class="bench"><div class="bench-head"><div class="dots"><i></i><i></i><i></i></div>'
            f'<span class="b-label">{label}</span><span class="spacer"></span>'
            f'<button class="btn btn-run" data-demo="{demo_id}">▶ 运行</button></div>'
            f'<pre class="code" id="{demo_id}">{sql}</pre>'
            f'<div class="result" id="{demo_id}-res"></div></div>')

def blk(title, num, inner):
    return f'<section class="blk"><h3><span class="h-num">{num}</span>{title}</h3>{inner}</section>'

def ex(eid, title, desc, prefill, answer, explain="", verify=None):
    d = {"id": eid, "title": title, "desc": desc, "prefill": prefill,
         "answer": answer, "explain": explain}
    if verify:
        d["verify"] = verify
    return d

NEW_LESSONS = [

# ========== 第 6 课 字符串函数 ==========
{"id": "f1", "num": "6", "crumb": "第三篇 · 常用函数 | 第 6 课",
 "title": "字符串函数：截取、拼接、替换",
 "sub": "对应 Excel 的 LEFT / MID / CONCAT / SUBSTITUTE——从编码里拆信息、把字段拼成标签。",
 "html":
 blk("六个最常用的字符串函数", "6.1", """
<table class="ref">
<thead><tr><th>函数 / 写法</th><th>意思</th><th>例子</th><th>结果</th></tr></thead>
<tbody>
<tr><td><code>a || b</code></td><td>拼接（两个竖线）</td><td><code>'纹身号: ' || tattoo</code></td><td>纹身号: 23001D</td></tr>
<tr><td><code>LENGTH(x)</code></td><td>长度</td><td><code>LENGTH('23001D')</code></td><td>6</td></tr>
<tr><td><code>SUBSTR(x, 起点, 长度)</code></td><td>截取（起点从 1 开始）</td><td><code>SUBSTR(tattoo, 1, 2)</code></td><td>23</td></tr>
<tr><td><code>SUBSTR(x, -1)</code></td><td>负数起点＝从右数</td><td><code>SUBSTR(tattoo, -1)</code></td><td>D</td></tr>
<tr><td><code>REPLACE(x, 旧, 新)</code></td><td>替换</td><td><code>REPLACE(species,'豚鼠','荷兰猪')</code></td><td>荷兰猪</td></tr>
<tr><td><code>TRIM(x)</code></td><td>去掉首尾空格</td><td><code>TRIM('  比格犬 ')</code></td><td>比格犬</td></tr>
</tbody>
</table>
<div class="callout"><b>方言差异预告：</b>拼接在 MySQL 里写 <code class="inl">CONCAT(a,b)</code>，SQL Server 里用 <code class="inl">+</code>，SQLite 和 PostgreSQL 用 <code class="inl">||</code>。概念完全一样，换个符号而已——这就是"学会一门，其他查一下就会"的典型例子。</div>
""" + demo("df1a", "示例 · 从纹身号拆出年份和种属代码", "SELECT tattoo, SUBSTR(tattoo,1,2) AS 年份代码, SUBSTR(tattoo,-1) AS 种属代码 FROM animals LIMIT 10;")
 + demo("df1b", "示例 · 拼一个完整标签", "SELECT customer_id, name || '（' || city || ' · ' || level || '）' AS 客户标签 FROM customers LIMIT 8;")),
 "exercises": [
   ex("ef1a", "给产品生成标签",
     "对 products 表，把类别和编号拼成 <code>类别-编号</code> 形式的标签，显示 <code>标签</code> 和 <code>name</code> 两列。",
     "",
     "SELECT category || '-' || product_id AS 标签, name FROM products;"),
   ex("ef1b", "豚鼠改名荷兰猪",
     "查询所有豚鼠，显示 <code>tattoo</code> 和一列 <code>显示名</code>：用 REPLACE 把种属里的「豚鼠」显示为「荷兰猪」（只改显示，不改数据）。",
     "",
     "SELECT tattoo, REPLACE(species, '豚鼠', '荷兰猪') AS 显示名 FROM animals WHERE species = '豚鼠';",
     "REPLACE 只影响查询输出，表里的原始数据不变。"),
   ex("ef1c", "品名里带「饲料」的产品",
     "用 INSTR 函数找出品名中包含「饲料」的产品，显示 <code>product_id</code> 和 <code>name</code>（提示：<code>INSTR(name,'饲料') &gt; 0</code> 表示找得到）。",
     "",
     "SELECT product_id, name FROM products WHERE INSTR(name, '饲料') > 0;",
     "INSTR 返回子串出现的位置（找不到返回 0），效果等价于 LIKE '%饲料%'。")]},

# ========== 第 7 课 日期函数 ==========
{"id": "f2", "num": "7", "crumb": "第三篇 · 常用函数 | 第 7 课",
 "title": "日期与时间函数",
 "sub": "按年按月统计、算间隔天数、推算未来日期——报表里最常用的一组函数。",
 "html":
 blk("SQLite 的日期四件套", "7.1", """
<table class="ref">
<thead><tr><th>写法</th><th>意思</th><th>例子</th><th>结果</th></tr></thead>
<tbody>
<tr><td><code>strftime('%Y', d)</code></td><td>取年份（文本）</td><td><code>strftime('%Y','2024-03-15')</code></td><td>2024</td></tr>
<tr><td><code>strftime('%Y-%m', d)</code></td><td>取年月</td><td></td><td>2024-03</td></tr>
<tr><td><code>julianday(d)</code></td><td>转成连续天数（可相减）</td><td><code>julianday('2024-03-18') - julianday('2024-03-15')</code></td><td>3.0</td></tr>
<tr><td><code>date(d, '+90 day')</code></td><td>日期加减</td><td><code>date('2024-03-15','+90 day')</code></td><td>2024-06-13</td></tr>
</tbody>
</table>
<div class="callout"><b>为什么用 julianday 算间隔：</b>日期文本不能直接相减，julianday 把日期转成"从公元前 4714 年起的天数"，两个数一减就是间隔天数。<b>方言差异：</b>MySQL 用 <code class="inl">DATEDIFF(a,b)</code>，SQL Server 用 <code class="inl">DATEDIFF(day,a,b)</code>，到时候查一下即可。</div>
""" + demo("df2a", "示例 · 按年到货量统计", "SELECT strftime('%Y', arrival_date) AS 年份, COUNT(*) AS 只数 FROM animals GROUP BY 年份 ORDER BY 年份;")
 + demo("df2b", "示例 · 算每只动物到 2025-06-30 的在库天数", "SELECT tattoo, arrival_date, CAST(julianday('2025-06-30') - julianday(arrival_date) AS INTEGER) AS 在库天数 FROM animals ORDER BY 在库天数 DESC LIMIT 8;")),
 "exercises": [
   ex("ef2a", "2024 年逐月订单量",
     "统计 orders 表 2024 年每个月的订单数，显示 <code>月份</code>（YYYY-MM 格式）和 <code>单量</code>，按月份升序。",
     "",
     "SELECT strftime('%Y-%m', order_date) AS 月份, COUNT(*) AS 单量 FROM orders WHERE strftime('%Y', order_date) = '2024' GROUP BY 月份 ORDER BY 月份;",
     "WHERE 里也可以用 strftime 筛年份。"),
   ex("ef2b", "到货 90 天后的复检日",
     "给每只比格犬算一个「复检日」＝到货日期 + 90 天，显示 <code>tattoo</code>、<code>arrival_date</code>、<code>复检日</code>。",
     "",
     "SELECT tattoo, arrival_date, date(arrival_date, '+90 day') AS 复检日 FROM animals WHERE species = '比格犬';"),
   ex("ef2c", "客户注册至今的年份分布",
     "统计 customers 表按注册年份分组的人数，显示 <code>注册年份</code> 和 <code>人数</code>，按年份升序。",
     "",
     "SELECT strftime('%Y', join_date) AS 注册年份, COUNT(*) AS 人数 FROM customers GROUP BY 注册年份 ORDER BY 注册年份;")]},

# ========== 第 8 课 数值与类型转换 ==========
{"id": "f3", "num": "8", "crumb": "第三篇 · 常用函数 | 第 8 课",
 "title": "数值处理与类型转换",
 "sub": "ROUND 四舍五入、CAST 转换类型，以及一个会咬人的整数除法陷阱。",
 "html":
 blk("三个数值函数 + 一个转换", "8.1", """
<table class="ref">
<thead><tr><th>写法</th><th>意思</th><th>例子</th><th>结果</th></tr></thead>
<tbody>
<tr><td><code>ROUND(x, 2)</code></td><td>保留两位小数</td><td><code>ROUND(3.14159, 2)</code></td><td>3.14</td></tr>
<tr><td><code>ABS(x)</code></td><td>绝对值</td><td><code>ABS(-5)</code></td><td>5</td></tr>
<tr><td><code>CAST(x AS INTEGER)</code></td><td>转成整数（直接砍小数）</td><td><code>CAST(3.9 AS INTEGER)</code></td><td>3</td></tr>
<tr><td><code>CAST(x AS TEXT)</code></td><td>转成文本</td><td></td><td></td></tr>
</tbody>
</table>
<div class="callout"><b>整数除法陷阱（很多人都会踩）：</b>两个整数相除，结果还是整数——<code class="inl">5 / 2</code> 得到 2 而不是 2.5！算比例、算均价时一定把其中一个写成小数：<code class="inl">5.0 / 2</code> 或 <code class="inl">CAST(5 AS REAL) / 2</code>。结果莫名少一截，先怀疑这里。</div>
""" + demo("df3a", "示例 · 平均体重保留两位小数", "SELECT species, ROUND(AVG(weight_kg), 2) AS 平均体重 FROM animals GROUP BY species;")
 + demo("df3b", "示例 · 每个产品的毛利率（注意 100.0）", "SELECT name, price, cost, ROUND((price - cost) * 100.0 / price, 1) AS 毛利率百分比 FROM products ORDER BY 毛利率百分比 DESC LIMIT 6;")),
 "exercises": [
   ex("ef3a", "总销售额（保留整数）",
     "计算所有已完成订单的销售总额（明细 qty × unit_price 求和，订单表要 JOIN 明细表并筛状态），用 ROUND 保留 0 位小数，别名 <code>总销售额</code>。",
     "",
     "SELECT ROUND(SUM(i.qty * i.unit_price), 0) AS 总销售额 FROM orders o JOIN order_items i ON o.order_id = i.order_id WHERE o.status = '已完成';",
     "金额计算 = 明细数量 × 成交单价，再 SUM。"),
   ex("ef3b", "体重的整数部分",
     "显示每只新西兰兔的 <code>tattoo</code>、<code>weight_kg</code>，以及用 CAST 取整数后的 <code>体重取整</code> 列。",
     "",
     "SELECT tattoo, weight_kg, CAST(weight_kg AS INTEGER) AS 体重取整 FROM animals WHERE species = '新西兰兔';")]},

# ========== 第 9 课 CASE 与 NULL ==========
{"id": "f4", "num": "9", "crumb": "第三篇 · 常用函数 | 第 9 课",
 "title": "CASE 条件分支与 NULL 空值处理",
 "sub": "SQL 里的 if-else，以及数据库里最特殊的概念——NULL。",
 "html":
 blk("CASE WHEN：查询里的如果-那么", "9.1", """
<p>结构：<code class="inl">CASE WHEN 条件1 THEN 结果1 WHEN 条件2 THEN 结果2 ELSE 默认 END</code>。从上到下匹配，命中即止。最常用来<b>分档、打标签、做行转列透视</b>。</p>
""" + demo("df4a", "示例 · 给动物按体重分级", "SELECT tattoo, species, weight_kg, CASE WHEN weight_kg >= 10 THEN '大型' WHEN weight_kg >= 3 THEN '中型' ELSE '小型' END AS 体型 FROM animals LIMIT 12;")
 + demo("df4b", "示例 · 一行算出各状态订单数（行转列）", "SELECT SUM(CASE WHEN status = '已完成' THEN 1 ELSE 0 END) AS 已完成, SUM(CASE WHEN status = '已取消' THEN 1 ELSE 0 END) AS 已取消, SUM(CASE WHEN status = '退款' THEN 1 ELSE 0 END) AS 退款 FROM orders;") + """
<p>第二个例子是经典技巧「条件计数」：CASE 把每一行变成 1 或 0，SUM 加起来就是满足条件的行数——一行 SQL 干出透视表的效果。</p>
""") +
 blk("NULL：不是 0，也不是空字符串", "9.2", """
<p>NULL 表示「<b>不知道 / 没有值</b>」。它有怪脾气：<code class="inl">NULL = NULL</code> 的结果不是真，而是「不知道」！所以判断空值必须用 <code class="inl">IS NULL</code> / <code class="inl">IS NOT NULL</code>，用等号永远查不到。</p>
<table class="ref">
<thead><tr><th>写法</th><th>意思</th></tr></thead>
<tbody>
<tr><td><code>x IS NULL</code></td><td>是空值</td></tr>
<tr><td><code>COALESCE(x, '替补')</code></td><td>x 是 NULL 就用替补值（可串联多个）</td></tr>
<tr><td><code>NULLIF(a, b)</code></td><td>a 等于 b 就返回 NULL（常用于防除零）</td></tr>
</tbody>
</table>
""" + demo("df4c", "示例 · 运输证号为空时显示「（无运输证）」", "SELECT batch_no, vendor, COALESCE(transport_no, '（无运输证）') AS 运输证 FROM batches;")),
 "exercises": [
   ex("ef4a", "给订单金额分档",
     "先按订单汇总金额（orders JOIN order_items，SUM(qty*unit_price) 别名 <code>金额</code>），再用 CASE 分档：≥2000 为 '大额'，≥500 为 '中额'，其余 '小额'，列名 <code>档位</code>。显示 <code>order_id</code>、<code>金额</code>（ROUND 0 位）、<code>档位</code>。",
     "",
     "SELECT o.order_id, ROUND(SUM(i.qty * i.unit_price), 0) AS 金额, CASE WHEN SUM(i.qty * i.unit_price) >= 2000 THEN '大额' WHEN SUM(i.qty * i.unit_price) >= 500 THEN '中额' ELSE '小额' END AS 档位 FROM orders o JOIN order_items i ON o.order_id = i.order_id GROUP BY o.order_id;",
     "聚合后分档：CASE 里直接用 SUM(...) 或别名都可以（SQLite 两种都支持）。"),
   ex("ef4b", "没有运输证的批次显示「无」",
     "查询 batches 表的 <code>batch_no</code>、<code>vendor</code> 和 <code>运输证</code> 三列：transport_no 为空时显示 '无'（用 COALESCE）。",
     "",
     "SELECT batch_no, vendor, COALESCE(transport_no, '无') AS 运输证 FROM batches;"),
   ex("ef4c", "找出运输证为空的批次",
     "用 IS NULL 查出所有没有运输许可证号的批次，显示 <code>batch_no</code> 和 <code>vendor</code>。",
     "SELECT batch_no, vendor FROM batches WHERE transport_no ???;",
     "SELECT batch_no, vendor FROM batches WHERE transport_no IS NULL;",
     "写成 = NULL 查不到任何行——这正是本课强调的经典坑。")]},
]
