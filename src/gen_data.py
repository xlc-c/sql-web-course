# -*- coding: utf-8 -*-
"""生成确定性的模拟动物档案数据（INIT_SQL 第一部分）"""
import random
from datetime import date, timedelta

random.seed(42)

SPECIES_INFO = {
    '比格犬':  dict(letter='D', wmin=8.0,  wmax=14.0, age_min=240, age_max=380),
    '食蟹猴':  dict(letter='M', wmin=3.0,  wmax=6.2,  age_min=730, age_max=1500),
    '巴马猪':  dict(letter='P', wmin=15.0, wmax=30.0, age_min=120, age_max=200),
    '新西兰兔': dict(letter='R', wmin=2.5,  wmax=4.0,  age_min=90,  age_max=160),
    '豚鼠':    dict(letter='G', wmin=0.4,  wmax=0.75, age_min=60,  age_max=110),
}

BATCHES = [
    # batch_no, species, count, vendor, permit, transport, arrival, headcount
    ('B2303-015', '比格犬', 20, '北京维通实验动物', '苏林动审字〔2023〕118号', None, '2023-03-20', 20),
    ('B2401-003', '食蟹猴', 10, '广东春盛生物',   '苏林动审字〔2024〕012号', '琼林许准〔2024〕033号', '2024-01-15', 10),
    ('B2405-008', '巴马猪', 10, '江苏明珠农牧',   '苏林动审字〔2024〕096号', None, '2024-05-10', 10),
    ('B2409-021', '新西兰兔', 16, '苏州湖景实验动物', '省内不提供', None, '2024-09-02', 16),
    ('B2411-030', '豚鼠',   8, '苏州湖景实验动物', '省内不提供', None, '2024-11-11', 8),
    ('B2502-002', '食蟹猴', 8, '广西雄森灵长类',  '苏林动审字〔2025〕008号', '琼林许准〔2025〕171号', '2025-02-18', 8),
    ('B2504-009', '比格犬', 12, '北京维通实验动物', '苏林动审字〔2025〕051号', None, '2025-04-08', 12),
]

PROJECTS = [
    ('SP-2023-032', '医疗器械植入试验（猪）',      '无锡安泰医疗', '2023-11-10'),
    ('SP-2024-006', '某单抗注射液重复给药毒性试验', '苏州启元生物', '2024-03-01'),
    ('SP-2024-019', '小分子化合物犬毒理试验',      '上海瀚峰药业', '2024-06-15'),
    ('SP-2025-002', '双特异性抗体安全性评价',      '北京诺健生物', '2025-01-20'),
    ('SP-2025-011', '疫苗佐剂局部刺激性试验',      '广州康乐生物', '2025-04-01'),
]

DOSE_GROUPS = ['对照组', '低剂量组', '中剂量组', '高剂量组']

def q(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def gen():
    random.seed(42)  # 函数级种子：不受导入顺序影响
    animals = []
    seq_by_year = {}
    for batch_no, species, count, vendor, permit, transport, arrival, headcount in BATCHES:
        info = SPECIES_INFO[species]
        y = arrival[2:4]
        arr_d = date.fromisoformat(arrival)
        for i in range(count):
            seq_by_year.setdefault(y, 0)
            seq_by_year[y] += 1
            tattoo = f"{y}{seq_by_year[y]:03d}{info['letter']}"
            sex = '雄' if random.random() < 0.5 else '雌'
            age = random.randint(info['age_min'], info['age_max'])
            birth = (arr_d - timedelta(days=age)).isoformat()
            weight = round(random.uniform(info['wmin'], info['wmax']), 1)
            animals.append(dict(tattoo=tattoo, species=species, sex=sex,
                                birth=birth, arrival=arrival, batch=batch_no,
                                status='在库', weight=weight))
    # 状态：少量死亡/淘汰
    dead = random.sample([a for a in animals if a['batch'] == 'B2303-015'], 2)
    for a in dead: a['status'] = '死亡'
    culled = random.sample([a for a in animals if a['species'] in ('新西兰兔', '豚鼠')], 3)
    for a in culled: a['status'] = '已淘汰'

    # 入组：28 只
    pool = [a for a in animals if a['status'] == '在库' and a['species'] in ('比格犬', '食蟹猴', '巴马猪', '新西兰兔')]
    random.shuffle(pool)
    chosen = pool[:28]
    assignments = []
    proj_cycle = ['SP-2024-006', 'SP-2024-019', 'SP-2025-002', 'SP-2025-011', 'SP-2023-032']
    for i, a in enumerate(chosen):
        proj = proj_cycle[i % 5]
        a['status'] = '已入组'
        arr_d = date.fromisoformat(a['arrival'])
        start_d = date.fromisoformat(dict((p[0], p[3]) for p in PROJECTS)[proj])
        base = max(arr_d, start_d)
        assign = base + timedelta(days=random.randint(10, 60))
        assignments.append((a['tattoo'], proj, DOSE_GROUPS[i % 4], assign.isoformat()))
    assignments.sort(key=lambda x: x[3])

    sql = []
    sql.append("""CREATE TABLE animals (
  tattoo TEXT PRIMARY KEY, species TEXT, sex TEXT, birth_date TEXT,
  arrival_date TEXT, batch_no TEXT, status TEXT, weight_kg REAL);""")
    sql.append("""CREATE TABLE batches (
  batch_no TEXT PRIMARY KEY, permit_no TEXT, transport_no TEXT,
  vendor TEXT, arrival_date TEXT, headcount INTEGER);""")
    sql.append("""CREATE TABLE projects (
  project_no TEXT PRIMARY KEY, project_name TEXT, client TEXT, start_date TEXT);""")
    sql.append("""CREATE TABLE assignments (
  tattoo TEXT, project_no TEXT, dose_group TEXT, assign_date TEXT);""")

    vals = []
    for a in animals:
        vals.append("(%s,%s,%s,%s,%s,%s,%s,%s)" % (
            q(a['tattoo']), q(a['species']), q(a['sex']), q(a['birth']),
            q(a['arrival']), q(a['batch']), q(a['status']), a['weight']))
    sql.append("INSERT INTO animals VALUES\n" + ",\n".join(vals) + ";")

    vals = []
    for b in BATCHES:
        vals.append("(%s,%s,%s,%s,%s,%d)" % (q(b[0]), q(b[4]), q(b[5]), q(b[3]), q(b[6]), b[7]))
    sql.append("INSERT INTO batches VALUES\n" + ",\n".join(vals) + ";")

    vals = []
    for p in PROJECTS:
        vals.append("(%s,%s,%s,%s)" % (q(p[0]), q(p[1]), q(p[2]), q(p[3])))
    sql.append("INSERT INTO projects VALUES\n" + ",\n".join(vals) + ";")

    vals = []
    for s in assignments:
        vals.append("(%s,%s,%s,%s)" % (q(s[0]), q(s[1]), q(s[2]), q(s[3])))
    sql.append("INSERT INTO assignments VALUES\n" + ",\n".join(vals) + ";")

    return "\n".join(sql), len(animals), len(assignments)

if __name__ == '__main__':
    sql, na, ns = gen()
    print(f"animals={na} assignments={ns} sql_len={len(sql)}")
