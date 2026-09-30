# -*- coding: utf-8 -*-
"""课程内容（v1 基础篇）：使用说明 + 第 0–8 课 + 沙盒 + Python 篇预告"""

SCHEMA_HTML = """
<table class="ref">
<thead><tr><th>表名</th><th>含义</th><th>主要列</th></tr></thead>
<tbody>
<tr><td><code>animals</code></td><td>动物个体表（一行一只动物）</td><td><code>tattoo</code> 纹身号、<code>species</code> 种属、<code>sex</code> 性别、<code>birth_date</code> 出生日期、<code>arrival_date</code> 到货日期、<code>batch_no</code> 批次号、<code>status</code> 状态、<code>weight_kg</code> 体重</td></tr>
<tr><td><code>batches</code></td><td>批次表（一行一个批次）</td><td><code>batch_no</code> 批次号、<code>permit_no</code> 引进许可证号、<code>transport_no</code> 运输许可证号（仅猴批次有）、<code>vendor</code> 供应商、<code>arrival_date</code> 到货日期、<code>headcount</code> 只数</td></tr>
<tr><td><code>projects</code></td><td>项目表</td><td><code>project_no</code> 项目号、<code>project_name</code> 项目名称、<code>client</code> 客户名称、<code>start_date</code> 开始日期</td></tr>
<tr><td><code>assignments</code></td><td>入组表（一行=一只动物进一个项目）</td><td><code>tattoo</code> 纹身号、<code>project_no</code> 项目号、<code>dose_group</code> 剂量组、<code>assign_date</code> 入组日期</td></tr>
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

def ex(eid, title, desc, prefill, answer, explain=""):
    return {"id": eid, "title": title, "desc": desc, "prefill": prefill,
            "answer": answer, "explain": explain}

LESSONS_SQL = [
# ================= 第 0 课 =================
{"id": "l0", "num": "0", "crumb": "SQL 篇 · 第 0 课",
 "title": "数据库是什么，以及你的第一个查询",
 "sub": "把 Excel 表格的思维搬过来，10 分钟跑通第一句 SQL。",
 "html":
 blk("先建立一个心智模型", "0.1", """
<p>你已经天天在和"数据库"打交道了——只是它穿着 Excel 的外衣：</p>
<table class="ref">
<thead><tr><th>Excel 里叫</th><th>数据库里叫</th><th>说明</th></tr></thead>
<tbody>
<tr><td>一张工作表（Sheet）</td><td>表（Table）</td><td>比如"动物个体表"就是一张表</td></tr>
<tr><td>一行</td><td>一条记录（Row）</td><td>比如一只动物</td></tr>
<tr><td>一列</td><td>一个字段（Column）</td><td>比如纹身号、体重</td></tr>
<tr><td>筛选器、透视表</td><td>查询（Query）</td><td>用 SQL 语句写出来</td></tr>
</tbody>
</table>
<p><strong>SQL（读作 "S-Q-L" 或 "sequel"）就是向表提问的语言。</strong>它的全名是 Structured Query Language（结构化查询语言），四十多年历史，几乎所有数据库都认它。学会它，你就掌握了和任何数据库对话的通用方式。</p>
""") +
 blk("本课程的练习数据", "0.2", """
<p>网页里内置了一套模拟的动物档案数据（共 4 张表、70 只动物），关掉页面就消失，不上传任何东西：</p>
""" + SCHEMA_HTML + """
<div class="callout"><b>注意：</b>日期在数据库里是 <code class="inl">'2024-03-15'</code> 这样的文本形式，写条件时用英文单引号包起来。</div>
""") +
 blk("第一句 SQL：看看表里有什么", "0.3", """
<p>最基础的查询长这样：<code class="inl">SELECT 列名 FROM 表名;</code>。SELECT 是"选"，FROM 是"从哪张表"。<code class="inl">*</code> 表示"所有列"，<code class="inl">LIMIT 5</code> 表示"只要前 5 行"。点下面的「运行」试试：</p>
""" + demo("d0a", "示例 · 查看动物表前 5 行", "SELECT * FROM animals LIMIT 5;") + """
<p>再来一个只取两列的——就像你在 Excel 里只复制 B 列和 D 列：</p>
""" + demo("d0b", "示例 · 只看纹身号和体重", "SELECT tattoo, weight_kg FROM animals LIMIT 8;") + """
<div class="callout"><b>三个小规矩：</b>① 关键词大小写都行（SELECT 和 select 一样），但课程里统一大写，方便你一眼认出"这是 SQL 的词"；② 语句末尾的分号表示"我说完了"；③ 列名、表名都是英文，值里的中文要用单引号包住。</div>
"""),
 "exercises": [ex("e0", "你的第一个查询",
   "从 <code>animals</code> 表里查出 <code>tattoo</code>（纹身号）和 <code>sex</code>（性别）两列，只看前 10 行。",
   "-- 把下面的列名补全，然后点「提交判题」\nSELECT tattoo, ??? FROM animals LIMIT 10;",
   "SELECT tattoo, sex FROM animals LIMIT 10;",
   "列名之间用英文逗号隔开，列的顺序就是你想要的显示顺序。")]},

# ================= 第 1 课 =================
{"id": "l1", "num": "1", "crumb": "SQL 篇 · 第 1 课",
 "title": "WHERE：按条件筛选",
 "sub": "对应 Excel 的筛选器——只看你关心的行。",
 "html":
 blk("WHERE 就是筛选器", "1.1", """
<p><code class="inl">WHERE 条件</code> 跟在 FROM 后面，意思是"只要满足条件的行"。</p>
<table class="ref">
<thead><tr><th>写法</th><th>意思</th><th>例子</th></tr></thead>
<tbody>
<tr><td><code>=</code></td><td>等于（注意：只有一个等号）</td><td><code>species = '比格犬'</code></td></tr>
<tr><td><code>!=</code> 或 <code>&lt;&gt;</code></td><td>不等于</td><td><code>status != '死亡'</code></td></tr>
<tr><td><code>&gt; &nbsp;&lt; &nbsp;&gt;= &nbsp;&lt;=</code></td><td>大于、小于、大于等于、小于等于</td><td><code>weight_kg &gt; 10</code></td></tr>
</tbody>
</table>
<div class="callout"><b>新手最容易踩的坑：</b>文本值必须用<b>英文单引号</b>包住：<code class="inl">'比格犬'</code>。写成中文引号'比格犬'或者不加引号都会报错。数字不用引号。</div>
""" + demo("d1a", "示例 · 所有比格犬", "SELECT tattoo, sex, weight_kg FROM animals WHERE species = '比格犬' LIMIT 10;")),
 "exercises": [
   ex("e1a", "找出所有食蟹猴",
     "查出所有食蟹猴的 <code>tattoo</code>、<code>sex</code>、<code>weight_kg</code>。",
     "SELECT tattoo, sex, weight_kg\nFROM animals\nWHERE species = ???;",
     "SELECT tattoo, sex, weight_kg FROM animals WHERE species = '食蟹猴';",
     "WHERE 后面的文本值记得用英文单引号。"),
   ex("e1b", "体重超标的大个子",
     "查出体重超过 10 kg 的动物，显示 <code>tattoo</code>、<code>species</code>、<code>weight_kg</code>。",
     "",
     "SELECT tattoo, species, weight_kg FROM animals WHERE weight_kg > 10;",
     "数字比较不需要引号：weight_kg > 10。")]},

# ================= 第 2 课 =================
{"id": "l2", "num": "2", "crumb": "SQL 篇 · 第 2 课",
 "title": "组合条件：AND / OR / IN / BETWEEN / LIKE",
 "sub": "一个条件不够用时，把多个条件组合起来。",
 "html":
 blk("五个组合工具", "2.1", """
<table class="ref">
<thead><tr><th>写法</th><th>意思</th><th>例子</th></tr></thead>
<tbody>
<tr><td><code>AND</code></td><td>并且（两个条件都要满足）</td><td><code>species='比格犬' AND sex='雄'</code></td></tr>
<tr><td><code>OR</code></td><td>或者（满足一个就行）</td><td><code>status='死亡' OR status='已淘汰'</code></td></tr>
<tr><td><code>IN (...)</code></td><td>在名单里（相当于一串 OR）</td><td><code>species IN ('比格犬','巴马猪')</code></td></tr>
<tr><td><code>BETWEEN a AND b</code></td><td>在 a 和 b 之间（含两头）</td><td><code>weight_kg BETWEEN 5 AND 12</code></td></tr>
<tr><td><code>LIKE '模式'</code></td><td>模糊匹配，<code>%</code> 代表任意内容</td><td><code>tattoo LIKE '24%'</code>（24 开头）</td></tr>
</tbody>
</table>
<div class="callout"><b>AND 和 OR 混用时</b>，AND 优先执行，容易出错。保险做法：用括号明确分组，例如 <code class="inl">(species='比格犬' OR species='巴马猪') AND weight_kg &gt; 5</code>。</div>
""" + demo("d2a", "示例 · 2024 年到货的动物", "SELECT tattoo, species, arrival_date FROM animals WHERE arrival_date BETWEEN '2024-01-01' AND '2024-12-31' LIMIT 10;")
 + demo("d2b", "示例 · 犬和猪里的中等体重", "SELECT tattoo, species, weight_kg FROM animals WHERE species IN ('比格犬','巴马猪') AND weight_kg BETWEEN 8 AND 20;")),
 "exercises": [
   ex("e2a", "母的食蟹猴",
     "查出所有<b>雌性</b>食蟹猴的 <code>tattoo</code> 和 <code>weight_kg</code>（提示：两个条件用 AND 连接，性别列的值是 '雌' 或 '雄'）。",
     "",
     "SELECT tattoo, weight_kg FROM animals WHERE species = '食蟹猴' AND sex = '雌';"),
   ex("e2b", "纹身号 24 开头的动物",
     "用 LIKE 查出纹身号以 <code>24</code> 开头的动物所有列（提示：模式写 '24%'）。",
     "SELECT * FROM animals WHERE tattoo LIKE ???;",
     "SELECT * FROM animals WHERE tattoo LIKE '24%';",
     "% 是通配符，'24%' 表示「24 开头，后面随便」。"),
   ex("e2c", "在库或已入组的兔子和豚鼠",
     "查出种属是新西兰兔或豚鼠、且状态为在库或已入组的动物，显示 <code>tattoo</code>、<code>species</code>、<code>status</code>。（提示：两个 IN，中间用 AND）",
     "",
     "SELECT tattoo, species, status FROM animals WHERE species IN ('新西兰兔','豚鼠') AND status IN ('在库','已入组');")]},

# ================= 第 3 课 =================
{"id": "l3", "num": "3", "crumb": "SQL 篇 · 第 3 课",
 "title": "ORDER BY：排序与取前几名",
 "sub": "对应 Excel 的排序——谁最重、谁最新到，一眼看出来。",
 "html":
 blk("排序语法", "3.1", """
<p><code class="inl">ORDER BY 列名</code> 放在语句最后：<code class="inl">DESC</code> 从大到小，<code class="inl">ASC</code> 从小到大（不写默认 ASC）。可以多列排序：先按第一列，相同再按第二列。</p>
""" + demo("d3a", "示例 · 最重的 5 只动物", "SELECT tattoo, species, weight_kg FROM animals ORDER BY weight_kg DESC LIMIT 5;")
 + demo("d3b", "示例 · 按种属排，同种属按体重从轻到重", "SELECT tattoo, species, weight_kg FROM animals ORDER BY species ASC, weight_kg ASC LIMIT 12;") + """
<div class="callout"><b>日期也能排序。</b>因为日期存成 '2024-03-15' 这种「年-月-日」格式，文本顺序正好就是时间顺序，直接 ORDER BY 日期列即可。</div>
"""),
 "exercises": [
   ex("e3a", "最新到货的 10 只动物",
     "查到货日期最晚的 10 只动物，显示 <code>tattoo</code>、<code>arrival_date</code>、<code>batch_no</code>，最新到货的排在最前。",
     "",
     "SELECT tattoo, arrival_date, batch_no FROM animals ORDER BY arrival_date DESC LIMIT 10;",
     "「最新在前」就是按日期从大到小：DESC。"),
   ex("e3b", "比格犬按体重排队",
     "只查比格犬，按体重从轻到重排列，显示 <code>tattoo</code> 和 <code>weight_kg</code>。",
     "",
     "SELECT tattoo, weight_kg FROM animals WHERE species = '比格犬' ORDER BY weight_kg ASC;",
     "WHERE 在前、ORDER BY 在后，这个顺序不能换。")]},

# ================= 第 4 课 =================
{"id": "l4", "num": "4", "crumb": "SQL 篇 · 第 4 课",
 "title": "聚合函数：COUNT / AVG / SUM / MAX / MIN",
 "sub": "对应 Excel 的状态栏统计——总数、平均、最大最小。",
 "html":
 blk("五个统计函数", "4.1", """
<table class="ref">
<thead><tr><th>函数</th><th>意思</th><th>例子</th></tr></thead>
<tbody>
<tr><td><code>COUNT(*)</code></td><td>数行数</td><td>一共多少只动物</td></tr>
<tr><td><code>COUNT(列名)</code></td><td>数该列非空的行数</td><td>有运输证号的批次有几个</td></tr>
<tr><td><code>AVG(列名)</code></td><td>平均值</td><td>平均体重</td></tr>
<tr><td><code>SUM(列名)</code></td><td>求和</td><td>到货总只数</td></tr>
<tr><td><code>MAX / MIN</code></td><td>最大 / 最小</td><td>最重、最轻</td></tr>
</tbody>
</table>
<p>统计结果是一行"汇总值"，不再是明细。可以用 <code class="inl">AS 别名</code> 给结果列起个好读的名字：</p>
""" + demo("d4a", "示例 · 食蟹猴的数量和平均体重", "SELECT COUNT(*) AS 猴子数量, AVG(weight_kg) AS 平均体重 FROM animals WHERE species = '食蟹猴';")
 + demo("d4b", "示例 · COUNT(*) 和 COUNT(列) 的区别", "SELECT COUNT(*) AS 全部批次, COUNT(transport_no) AS 有运输证的批次 FROM batches;") + """
<div class="callout"><b>看到区别了吗：</b><code class="inl">COUNT(*)</code> 数所有行，<code class="inl">COUNT(transport_no)</code> 只数该列<b>不为空</b>的行——猴批次才有运输证号，其余批次这一列是空的。这就是"空值不计数"，对账时常用。</div>
"""),
 "exercises": [
   ex("e4a", "在库动物有多少只",
     "统计状态为「在库」的动物数量，结果列起别名为 <code>在库数量</code>。",
     "",
     "SELECT COUNT(*) AS 在库数量 FROM animals WHERE status = '在库';"),
   ex("e4b", "比格犬的体重范围",
     "查出比格犬的最重体重和最轻体重，两列分别叫 <code>最重</code> 和 <code>最轻</code>。",
     "",
     "SELECT MAX(weight_kg) AS 最重, MIN(weight_kg) AS 最轻 FROM animals WHERE species = '比格犬';"),
   ex("e4c", "各批次一共到了多少只",
     "对 batches 表求 <code>headcount</code>（只数）的总和，别名 <code>总只数</code>。",
     "",
     "SELECT SUM(headcount) AS 总只数 FROM batches;")]},

# ================= 第 5 课 =================
{"id": "l5", "num": "5", "crumb": "SQL 篇 · 第 5 课",
 "title": "GROUP BY：分组统计（就是透视表）",
 "sub": "每个种属多少只、每个供应商供了多少货——透视表能干的事它都能干。",
 "html":
 blk("GROUP BY ＝ 数据透视表", "5.1", """
<p><code class="inl">GROUP BY 列名</code> 表示"按这一列分组，每组算一次统计"。把它想成透视表：GROUP BY 的列就是拖到「行」区域的字段，聚合函数就是「值」区域的汇总方式。</p>
""" + demo("d5a", "示例 · 每个种属各多少只", "SELECT species, COUNT(*) AS 数量 FROM animals GROUP BY species;")
 + demo("d5b", "示例 · 每个种属的平均体重", "SELECT species, AVG(weight_kg) AS 平均体重 FROM animals GROUP BY species;")) +
 blk("HAVING：对分组结果再筛选", "5.2", """
<p>WHERE 筛的是<b>原始行</b>，HAVING 筛的是<b>分组后的结果</b>。比如"只要平均体重超过 6kg 的种属"——平均值是分组算出来的，WHERE 管不着，得用 HAVING：</p>
""" + demo("d5c", "示例 · 平均体重超 6kg 的种属", "SELECT species, AVG(weight_kg) AS 平均体重 FROM animals GROUP BY species HAVING AVG(weight_kg) > 6;") + """
<div class="callout"><b>执行顺序记住这条链：</b>FROM → WHERE（筛行）→ GROUP BY（分组）→ HAVING（筛组）→ SELECT（出列）→ ORDER BY（排序）→ LIMIT（截取）。写的时候也是这个顺序。</div>
"""),
 "exercises": [
   ex("e5a", "每个批次收了多少只动物",
     "按批次号分组，统计每个批次在 animals 表里的动物数量，显示 <code>batch_no</code> 和数量（别名 <code>只数</code>）。",
     "",
     "SELECT batch_no, COUNT(*) AS 只数 FROM animals GROUP BY batch_no;"),
   ex("e5b", "数量超过 15 只的种属",
     "统计每个种属的数量，只显示数量超过 15 的种属（提示：HAVING）。显示 <code>species</code> 和 <code>数量</code>。",
     "",
     "SELECT species, COUNT(*) AS 数量 FROM animals GROUP BY species HAVING COUNT(*) > 15;"),
   ex("e5c", "各状态的动物数，从多到少排",
     "按 <code>status</code> 分组统计数量，别名 <code>数量</code>，按数量从多到少排序。",
     "",
     "SELECT status, COUNT(*) AS 数量 FROM animals GROUP BY status ORDER BY 数量 DESC;",
     "ORDER BY 可以直接用别名。")]},

# ================= 第 6 课 =================
{"id": "l6", "num": "6", "crumb": "SQL 篇 · 第 6 课",
 "title": "JOIN：把多张表连起来",
 "sub": "动物信息在 animals，供应商在 batches——一次查询同时拿到。",
 "html":
 blk("为什么要分表？", "6.1", """
<p>想一想：如果供应商名称、许可证号直接塞进动物表，那同一批 12 只狗，许可证号就要重复抄 12 遍——改一处就得改 12 行，迟早对不上。所以规范做法是<b>拆开存</b>：批次信息存 batches，动物存 animals，两边用共同的 <code class="inl">batch_no</code>（批次号）关联。查询时再"连"起来。</p>
""") +
 blk("JOIN 语法", "6.2", """
<p>核心写法：<code class="inl">FROM 表1 JOIN 表2 ON 表1.列 = 表2.列</code>。ON 后面写两张表"靠什么对上"。</p>
<p>表名太长，通常起个短别名：<code class="inl">FROM animals a</code>，之后用 <code class="inl">a.tattoo</code> 指代"动物表的纹身号"。</p>
""" + demo("d6a", "示例 · 每只动物的供应商是谁", "SELECT a.tattoo, a.species, b.vendor FROM animals a JOIN batches b ON a.batch_no = b.batch_no LIMIT 10;") + """
<div class="callout"><b>怎么读这句：</b>从 animals 表出发，每一行拿自己的 batch_no 去 batches 表里找同一批次的那行，然后把两边的列拼在一起输出。JOIN 默认只保留<b>两边都能对上的</b>行。</div>
"""),
 "exercises": [
   ex("e6a", "猴子的运输许可证号",
     "查出所有食蟹猴的纹身号和所在批次的运输许可证号，显示 <code>tattoo</code> 和 <code>transport_no</code>（提示：先 JOIN 两张表，再 WHERE 筛种属）。",
     "SELECT a.tattoo, b.transport_no\nFROM animals a\nJOIN batches b ON ???\nWHERE ???;",
     "SELECT a.tattoo, b.transport_no FROM animals a JOIN batches b ON a.batch_no = b.batch_no WHERE a.species = '食蟹猴';",
     "ON 写关联条件（两边 batch_no 相等），WHERE 写筛选条件。顺序：JOIN…ON 在前，WHERE 在后。"),
   ex("e6b", "每个供应商供了多少只动物",
     "关联 animals 和 batches，按供应商分组统计动物数量，显示 <code>vendor</code> 和 <code>只数</code>，按只数从多到少排。",
     "",
     "SELECT b.vendor, COUNT(*) AS 只数 FROM animals a JOIN batches b ON a.batch_no = b.batch_no GROUP BY b.vendor ORDER BY 只数 DESC;",
     "分组列来自 batches，所以写 b.vendor。")]},

# ================= 第 7 课 =================
{"id": "l7", "num": "7", "crumb": "SQL 篇 · 第 7 课",
 "title": "子查询与 WITH：查询套查询",
 "sub": "「超过平均体重的动物」——平均值本身也得先查出来。",
 "html":
 blk("子查询：括号里的查询先跑", "7.1", """
<p>「找出体重超过全体平均值的动物」——平均值是多少？不知道，得先查。子查询就是把一个查询塞进另一个查询的条件里：</p>
""" + demo("d7a", "示例 · 超过全体平均体重的动物", "SELECT tattoo, species, weight_kg FROM animals WHERE weight_kg > (SELECT AVG(weight_kg) FROM animals);") + """
<p>括号里的 <code class="inl">SELECT AVG(...)</code> 先执行，算出一个数，外面的查询再拿这个数去比较。</p>
""") +
 blk("WITH：给中间结果起名，复杂查询也能读", "7.2", """
<p>更复杂的需求：「超过<b>本种属</b>平均体重的动物」。这要分两步：先算每种属的平均体重（一张临时小表），再把动物表和它 JOIN 起来比。<code class="inl">WITH 名字 AS (...)</code> 就是给临时小表起名：</p>
""" + demo("d7b", "示例 · 超过本种属平均体重的动物", "WITH avg_w AS (\n  SELECT species, AVG(weight_kg) AS aw FROM animals GROUP BY species\n)\nSELECT a.tattoo, a.species, a.weight_kg\nFROM animals a\nJOIN avg_w w ON a.species = w.species\nWHERE a.weight_kg > w.aw;") + """
<div class="callout"><b>读法：</b>WITH 部分先生成一张叫 avg_w 的临时表（两列：种属、平均体重），主查询再像普通表一样 JOIN 它。这种写法也叫 CTE（公用表表达式），是写复杂查询的主力工具——先拆开，再组合。</div>
"""),
 "exercises": [
   ex("e7a", "比最重的猴子还重的动物",
     "用子查询找出：体重超过「食蟹猴最大体重」的所有动物，显示 <code>tattoo</code>、<code>species</code>、<code>weight_kg</code>。",
     "",
     "SELECT tattoo, species, weight_kg FROM animals WHERE weight_kg > (SELECT MAX(weight_kg) FROM animals WHERE species = '食蟹猴');"),
   ex("e7b", "每个供应商的平均体重（用 WITH）",
     "用 WITH 写：先从 animals JOIN batches 得到「动物+供应商」的中间表 <code>t</code>，再按供应商分组算平均体重，显示 <code>vendor</code> 和 <code>平均体重</code>。",
     "WITH t AS (\n  SELECT a.weight_kg, b.vendor\n  FROM animals a JOIN batches b ON a.batch_no = b.batch_no\n)\n-- 下面补全：从 t 分组统计\n",
     "WITH t AS (SELECT a.weight_kg, b.vendor FROM animals a JOIN batches b ON a.batch_no = b.batch_no) SELECT vendor, AVG(weight_kg) AS 平均体重 FROM t GROUP BY vendor;")]},

# ================= 第 8 课 =================
{"id": "l8", "num": "8", "crumb": "SQL 篇 · 第 8 课",
 "title": "综合实战：按纹身号聚合多源信息",
 "sub": "把前面 8 课串成一条完整链路——这正是你日常工作里「数据分散在多个表」的解法。",
 "html":
 blk("场景还原", "8.1", """
<p>真实任务：动物基本信息在 animals 表，入组信息在 assignments 表，项目信息在 projects 表。现在要出一份<b>入组动物清单</b>——每只入组动物的纹身号、种属、所在项目、客户、剂量组。</p>
<p>思路：以 assignments 为主表（它记录"谁进了哪个项目"），向左分别 JOIN animals（补动物信息）和 projects（补项目信息）。</p>
""") +
 blk("三表关联", "8.2", """
<p>JOIN 可以连着写，像链条一样：</p>
""" + demo("d8a", "示例 · 入组动物清单", "SELECT a.tattoo, a.species, p.project_no, p.client, s.dose_group, s.assign_date\nFROM assignments s\nJOIN animals a ON s.tattoo = a.tattoo\nJOIN projects p ON s.project_no = p.project_no\nORDER BY s.assign_date DESC LIMIT 15;") + """
<div class="callout"><b>注意三处细节：</b>① 每张表都起了别名（s / a / p），列前面带别名前缀，一眼知道数据来自哪张表；② tattoo 在两张表里都有，必须写 <code class="inl">a.tattoo</code> 指明用哪张的，否则数据库会报「列名含糊」；③ 这就是「按纹身号聚合多源数据」的标准做法——先在 SQL 层面对齐，再交给后续工具。</div>
""") +
 blk("把统计叠上去", "8.3", """
<p>清单之上还可以直接出统计——每个项目用了多少只动物、分几个剂量组：</p>
""" + demo("d8b", "示例 · 每个项目的入组统计", "SELECT p.project_no, p.client, COUNT(*) AS 入组只数, COUNT(DISTINCT s.dose_group) AS 剂量组数\nFROM assignments s\nJOIN projects p ON s.project_no = p.project_no\nGROUP BY p.project_no, p.client\nORDER BY 入组只数 DESC;") + """
<p><code class="inl">COUNT(DISTINCT 列)</code> 是「去重后计数」——同一个剂量组出现多次只算一次。</p>
""") +
 blk("SQL 篇小结", "8.4", """
<ul class="plain">
<li><strong>取数</strong>：SELECT 列 FROM 表</li>
<li><strong>筛行</strong>：WHERE + AND/OR/IN/BETWEEN/LIKE</li>
<li><strong>排序截取</strong>：ORDER BY + LIMIT</li>
<li><strong>统计</strong>：COUNT/AVG/SUM/MAX/MIN，分组用 GROUP BY，筛组用 HAVING</li>
<li><strong>连表</strong>：JOIN … ON 共同列，多表连写</li>
<li><strong>复杂逻辑</strong>：子查询和 WITH，先拆后组</li>
</ul>
<p>这六板斧覆盖了数据岗位日常 80% 的查询。剩下的 20%（窗口函数、日期函数等）用到再查就行。</p>
"""),
 "exercises": [
   ex("e8", "期末考：完整入组清单",
     "独立完成最终任务：查出所有入组动物的 <code>tattoo</code>、<code>species</code>、<code>project_no</code>、<code>client</code>、<code>dose_group</code>、<code>assign_date</code>，按入组日期从早到晚排序（ASC）。",
     "-- 提示：主表 assignments s\n-- JOIN animals a：纹身号对上\n-- JOIN projects p：项目号对上\n",
     "SELECT a.tattoo, a.species, p.project_no, p.client, s.dose_group, s.assign_date FROM assignments s JOIN animals a ON s.tattoo = a.tattoo JOIN projects p ON s.project_no = p.project_no ORDER BY s.assign_date ASC;",
     "恭喜！完成这题，SQL 篇的核心你就全部拿下了。")]},
]

GUIDE = {"id": "guide", "num": "★", "crumb": "开篇",
 "title": "使用说明：这门课怎么用",
 "sub": "三分钟看完，然后直接从第 0 课开始。",
 "html":
 blk("这是什么", "1", """
<p>一门完全在网页里运行的 SQL 入门课：左侧选课，右边看讲解，讲解里的代码块都可以直接点「运行」看结果。每课末尾有练习题，写完点「提交判题」，系统会自动运行你的 SQL 并和参考答案的结果比对——<b>结果一致才算过</b>，背答案没用，得真会。</p>
""") +
 blk("为什么这样设计", "2", """
<ul class="plain">
<li><strong>不用装任何软件</strong>：数据库引擎（SQLite）已经编译进这个网页，双击打开就能学，公司电脑也能用</li>
<li><strong>数据不离本机</strong>：所有计算都在你的浏览器里完成，不上传任何东西，关掉页面不留痕迹</li>
<li><strong>练习数据是你熟悉的场景</strong>：动物个体、批次、项目、入组四张表，例子里全是纹身号、种属、供应商——学完能直接迁移到工作</li>
</ul>
""") +
 blk("学习规矩（重要）", "3", """
<ul class="plain">
<li><strong>先自己写</strong>：练习先独立思考 5 分钟，写不出来再看提示，最后才看参考答案</li>
<li><strong>看完答案要合书重写</strong>：参考答案看懂了 ≠ 会了。关掉答案，凭记忆重敲一遍，判题通过才算数</li>
<li><strong>报错是最好的老师</strong>：报错信息会告诉你哪错了，课程还会给中文提示。认真读报错，这个习惯值一半学费</li>
<li><strong>每天 30–45 分钟，一课一练</strong>：别贪多，第 0–3 课是基础，第 6 课（JOIN）是分水岭</li>
</ul>
""") +
 blk("进度与换电脑", "4", """
<p>完成一节课点底部「标记完成」。进度和练习代码自动保存在<b>本机浏览器</b>里（localStorage），下次打开还在。换电脑：左侧底部「导出进度」存成文件，新电脑上「导入进度」恢复。</p>
<div class="callout"><b>键盘快捷键：</b>练习区里 <b>Ctrl + Enter</b> 快捷运行；<b>Tab</b> 缩进。</div>
"""),
 "exercises": []}

SANDBOX = {"id": "sandbox", "num": "⚒", "crumb": "自由练习",
 "title": "沙盒：随便查，尽情折腾",
 "sub": "这里没有判题——把四张表翻来覆去地查，是巩固 SQL 最好的办法。",
 "html":
 blk("四张表的结构", "1", SCHEMA_HTML + """
<p>忘记表里有什么？运行 <code class="inl">SELECT * FROM animals LIMIT 5;</code> 这类语句直接看。</p>
""") +
 blk("折腾建议", "2", """
<ul class="plain">
<li>把课里的练习换个条件重做一遍（换个种属、换个日期区间）</li>
<li>试试故意写错，看看报错长什么样——熟悉报错就不怕报错</li>
<li>挑战题：每个种属里体重第二重的动物是谁？（提示：WITH + 子查询，或查资料了解窗口函数 ROW_NUMBER）</li>
</ul>
"""),
 "exercises": [ex("sandbox-ex", "自由练习区",
   "想写什么写什么，「运行」看结果。这里没有标准答案，「提交判题」不可用。",
   "SELECT * FROM animals LIMIT 10;",
   "SELECT * FROM animals LIMIT 10;")]}

PYTHON_PREVIEW = {"id": "py", "num": "▶", "crumb": "Python 篇 · 预告",
 "title": "下一步：Python 篇",
 "sub": "SQL 负责「从库里取数」，Python 负责「取数之后的一切」。",
 "html":
 blk("SQL 和 Python 的分工", "1", """
<table class="ref">
<thead><tr><th>任务</th><th>谁来做</th><th>你的旧经验</th></tr></thead>
<tbody>
<tr><td>从数据库取数、筛选、汇总</td><td>SQL</td><td>≈ Power Query 筛选 + 透视表</td></tr>
<tr><td>读 Excel / PDF 文件、批量改名、合并拆分</td><td>Python</td><td>≈ VBA 自动化</td></tr>
<tr><td>复杂判断、循环处理、定时任务</td><td>Python</td><td>≈ VBA / PowerShell</td></tr>
<tr><td>出报表、画图</td><td>Python（pandas + matplotlib）</td><td>≈ Excel 图表</td></tr>
</tbody>
</table>
""") +
 blk("Python 篇大纲（将内置到本页面，同样免安装、网页内运行）", "2", """
<ul class="plain">
<li>第 0 课：变量与数据类型——数字、文本、真假值</li>
<li>第 1 课：列表与字典——装一排数据、装一张表</li>
<li>第 2 课：循环与判断——让电脑重复干活</li>
<li>第 3 课：函数——把一段逻辑打包复用</li>
<li>第 4 课：pandas 上手——用代码操作表格（就是加强版 Power Query）</li>
<li>第 5 课：筛选、分组、聚合——和第 5 课 SQL 对照着学</li>
<li>第 6 课：多表合并 merge——和第 6 课 JOIN 对照着学</li>
<li>第 7 课：读写 Excel 文件——替代你的 VBA 日常</li>
<li>实战：用 Python 重写一遍「按纹身号聚合多源信息」</li>
</ul>
<div class="callout"><b>现在该做什么：</b>先把 SQL 篇学透（预计 4–6 周，每天半小时）。Python 篇上线时，你的 SQL 基础会让 pandas 学起来快一倍——它们的思路几乎是同一套。</div>
"""),
 "exercises": []}

COURSE = {"groups": [
    {"title": "开篇", "lessons": [GUIDE]},
    {"title": "SQL 篇", "lessons": LESSONS_SQL},
    {"title": "练手", "lessons": [SANDBOX]},
    {"title": "展望", "lessons": [PYTHON_PREVIEW]},
]}
