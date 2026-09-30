# -*- coding: utf-8 -*-
"""组装最终课程：v1 基础课修订 + v2 新课合并 + 分组重排
用法：python3 assemble_course.py  （产出 course_final.json）"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_ext2 import NEW_LESSONS
from content_ext import SCHEMA2_HTML
from content import COURSE as OLD_COURSE

lessons = {}
for g in OLD_COURSE['groups']:
    for l in g['lessons']:
        lessons[l['id']] = l

def L(lid):
    return lessons[lid]

# ---------- l0-l5 篇章归属 ----------
for i in range(4):
    L(f'l{i}')['crumb'] = f"第一篇 · 查询基础 | 第 {i} 课"
for i in (4, 5):
    L(f'l{i}')['crumb'] = f"第二篇 · 分组统计 | 第 {i} 课"

# ---------- l3 增加 DISTINCT ----------
L('l3')['html'] += ('<section class="blk"><h3><span class="h-num">3.2</span>DISTINCT：结果去重</h3>'
 '<p><code class="inl">SELECT DISTINCT 列</code> 把重复的结果行合并成一行——「出现过哪些种属」「客户都分布在哪些城市」这类问题就靠它。它作用于<b>整行</b>：选多列时，组合相同才算重复。</p>'
 '<div class="bench"><div class="bench-head"><div class="dots"><i></i><i></i><i></i></div>'
 '<span class="b-label">示例 · 有哪些种属、哪些城市</span><span class="spacer"></span>'
 '<button class="btn btn-run" data-demo="d3c">▶ 运行</button></div>'
 '<pre class="code" id="d3c">SELECT DISTINCT species FROM animals;</pre>'
 '<div class="result" id="d3c-res"></div></div>'
 '<div class="callout"><b>和 GROUP BY 的关系：</b>SELECT DISTINCT 列 等价于 SELECT 列 GROUP BY 列。只做去重时用 DISTINCT 更直白；要配统计函数时用 GROUP BY。</div></section>')
L('l3')['exercises'].append({
  "id": "e3c", "title": "客户分布在哪些城市",
  "desc": "用 DISTINCT 列出 customers 表里出现过的所有城市（一列 <code>city</code>，去重，按城市名升序）。",
  "prefill": "",
  "answer": "SELECT DISTINCT city FROM customers ORDER BY city;",
  "explain": "不加 DISTINCT 会列出 24 行（每个客户一行），加了只剩 6 个城市。"})

# ---------- l6 / l7 / l8 重新编号 ----------
L('l6')['num'] = '10'; L('l6')['crumb'] = '第四篇 · 多表查询 | 第 10 课'
L('l7')['num'] = '12'; L('l7')['crumb'] = '第四篇 · 多表查询 | 第 12 课'
L('l8')['num'] = '18'; L('l8')['crumb'] = '第六篇 · 综合实战 | 第 18 课'
L('l8')['title'] = '综合实战一：按纹身号聚合多源信息'
L('l8')['html'] = L('l8')['html'].replace('SQL 篇小结', '查询部分小结')
L('l8')['html'] = L('l8')['html'].replace(
  '这六板斧覆盖了数据岗位日常 80% 的查询。剩下的 20%（窗口函数、日期函数等）用到再查就行。',
  '这六板斧加上第三、四篇的函数、集合、窗口函数，查询部分就齐了。下一站：第五篇（写入与结构），然后第 19 课换一套陌生业务独立实战。')
L('l8')['exercises'][0]['title'] = '实战一考核：完整入组清单'
L('l8')['exercises'][0]['explain'] = '恭喜！查询主线全部拿下，第五篇开始学「改数据」。'

# ---------- guide 更新 ----------
g = L('guide')
g['html'] = g['html'].replace(
  '<strong>练习数据是你熟悉的场景</strong>：动物个体、批次、项目、入组四张表，例子里全是纹身号、种属、供应商——学完能直接迁移到工作',
  '<strong>两套练习数据</strong>：一套模拟动物档案（个体/批次/项目/入组），贴近你熟悉的场景；一套销售订单（客户/产品/订单/明细），训练你把技能迁移到陌生业务')
g['html'] = g['html'].replace(
  '别贪多，第 0–3 课是基础，第 6 课（JOIN）是分水岭',
  '别贪多，第一篇是地基，第四篇的 JOIN 是分水岭，窗口函数是天花板')
g['html'] += """
<section class="blk"><h3><span class="h-num">5</span>课程地图</h3>
<table class="ref">
<thead><tr><th>篇章</th><th>课号</th><th>内容</th><th>目标</th></tr></thead>
<tbody>
<tr><td>第一篇 · 查询基础</td><td>0–3</td><td>SELECT、WHERE、组合条件、排序、去重</td><td>能从单表取到想要的数据</td></tr>
<tr><td>第二篇 · 分组统计</td><td>4–5</td><td>聚合函数、GROUP BY、HAVING</td><td>能干透视表的活</td></tr>
<tr><td>第三篇 · 常用函数</td><td>6–9</td><td>字符串、日期、数值、CASE 与 NULL</td><td>数据加工信手拈来</td></tr>
<tr><td>第四篇 · 多表查询</td><td>10–14</td><td>JOIN 全集、子查询、CTE、集合运算、窗口函数</td><td>多源数据随便整合</td></tr>
<tr><td>第五篇 · 写入与结构</td><td>15–17</td><td>增删改、事务、建表、约束、视图、索引</td><td>能建库改库，懂安全规矩</td></tr>
<tr><td>第六篇 · 综合实战</td><td>18–19</td><td>两套业务各做一次完整实战</td><td>独立走完数据分析全流程</td></tr>
</tbody>
</table>
<p>全篇 20 课，每天 30–45 分钟，预计 8–10 周。学完整套 = 覆盖数据岗位面试和日常所需的 SQL 全功能。</p>
</section>"""

# ---------- sandbox 更新 ----------
s = L('sandbox')
s['html'] = s['html'].replace('四张表的结构', '两套数据 · 八张表的结构')
s['html'] = s['html'].replace(
  '<p>忘记表里有什么？运行',
  '<p><strong>第二套：销售业务数据</strong>（从第三篇起加入练习）</p>' + SCHEMA2_HTML + '<p>忘记表里有什么？运行')
s['html'] = s['html'].replace(
  '<li>把课里的练习换个条件重做一遍（换个种属、换个日期区间）</li>',
  '<li>把课里的练习换个条件重做一遍（换个种属、换个年份、换个类别）</li>\n<li>第五篇学完后，可以在沙盒里随便 INSERT / UPDATE / DELETE——玩坏了点下方「重置练习数据」一键还原</li>')
s['exercises'][0]['noJudge'] = True
s['after'] = """<section class="blk"><h3><span class="h-num">3</span>玩坏了怎么办</h3>
<p>沙盒里的写入操作会直接改公共数据。搞乱了不用慌，一键还原：</p>
<p><button class="btn btn-light" id="reset-data">↺ 重置练习数据（恢复全部 8 张表）</button></p>
<p style="font-size:13px;color:var(--ink-3)">只重置课程自带的 8 张表；你自己 CREATE 的表和学习进度都不受影响。注意：第五篇的练习题是在独立副本里判题的，不会弄脏这里的数据。</p>
</section>"""

# ---------- 组装 ----------
new = {l['id']: l for l in NEW_LESSONS}
COURSE = {"groups": [
    {"title": "开篇", "lessons": [g]},
    {"title": "第一篇 · 查询基础", "lessons": [L('l0'), L('l1'), L('l2'), L('l3')]},
    {"title": "第二篇 · 分组统计", "lessons": [L('l4'), L('l5')]},
    {"title": "第三篇 · 常用函数", "lessons": [new['f1'], new['f2'], new['f3'], new['f4']]},
    {"title": "第四篇 · 多表查询", "lessons": [L('l6'), new['j1'], L('l7'), new['s1'], new['w1']]},
    {"title": "第五篇 · 写入与结构", "lessons": [new['d1'], new['d2'], new['d3']]},
    {"title": "第六篇 · 综合实战", "lessons": [L('l8'), new['x2']]},
    {"title": "练手", "lessons": [s]},
    {"title": "展望", "lessons": [L('py')]},
]}
json.dump(COURSE, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_final.json'), 'w', encoding='utf-8'), ensure_ascii=False)
total = sum(len(gr['lessons']) for gr in COURSE['groups'])
nex = sum(len(l.get('exercises', [])) for gr in COURSE['groups'] for l in gr['lessons'])
print(f"lessons={total} exercises={nex}")
