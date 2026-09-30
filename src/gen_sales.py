# -*- coding: utf-8 -*-
"""第二套数据集：电商销售（客户/产品/订单/明细），拼在动物档案数据之后"""
import random
from datetime import date, timedelta

random.seed(20260930)

CITIES = ['苏州', '上海', '北京', '广州', '成都', '南京']
LEVELS = ['普通', '银卡', '金卡', '钻石']
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙']
PRODUCTS = [
    ('P01', '犬用全价饲料 10kg', '饲料', 268.0, 190.0),
    ('P02', '猴用复合饲料 5kg', '饲料', 158.0, 110.0),
    ('P03', '兔用膨化饲料 5kg', '饲料', 98.0, 65.0),
    ('P04', '杨木垫料 20L', '垫料', 45.0, 28.0),
    ('P05', '玉米芯垫料 10kg', '垫料', 38.0, 22.0),
    ('P06', '一次性无菌手套 100只', '耗材', 32.0, 18.0),
    ('P07', '独立通气笼盒 IVC', '设备', 580.0, 420.0),
    ('P08', '不锈钢兔笼', '设备', 890.0, 650.0),
    ('P09', '血清白蛋白检测试剂盒', '试剂', 1280.0, 860.0),
    ('P10', 'ELISA 板条 96孔', '试剂', 460.0, 300.0),
    ('P11', '动物识别耳标 100个', '耗材', 55.0, 30.0),
    ('P12', '环境温湿度记录仪', '设备', 720.0, 510.0),
]

def q(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def gen_sales_sql():
    random.seed(20260930)  # 函数级种子：不受导入顺序影响
    customers = []
    for i in range(24):
        nm = SURNAMES[i % len(SURNAMES)] + ['经理', '主管', '老师', '主任'][i % 4]
        lvl = LEVELS[0] if i % 3 else LEVELS[(i // 3) % 3 + 1]
        join = date(2022, 1, 1) + timedelta(days=random.randint(0, 700))
        customers.append((f'C{i+1:03d}', nm, CITIES[i % 6], lvl, join.isoformat()))

    orders, items = [], []
    oid = 1
    for i in range(80):
        cid = customers[random.randrange(24)][0]
        od = date(2023, 1, 5) + timedelta(days=random.randint(0, 900))
        status = random.choices(['已完成', '已取消', '退款'], weights=[82, 10, 8])[0]
        channel = '线上' if random.random() < 0.6 else '线下'
        order_id = f'SO{od.year}{oid:04d}'
        orders.append((order_id, cid, od.isoformat(), status, channel))
        for _ in range(random.randint(1, 4)):
            p = PRODUCTS[random.randrange(len(PRODUCTS))]
            qty = random.randint(1, 20)
            items.append((order_id, p[0], qty, p[3]))
        oid += 1
    orders.sort(key=lambda x: x[2])

    sql = []
    sql.append("""CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY, name TEXT, city TEXT, level TEXT, join_date TEXT);""")
    sql.append("""CREATE TABLE products (
  product_id TEXT PRIMARY KEY, name TEXT, category TEXT, price REAL, cost REAL);""")
    sql.append("""CREATE TABLE orders (
  order_id TEXT PRIMARY KEY, customer_id TEXT, order_date TEXT, status TEXT, channel TEXT);""")
    sql.append("""CREATE TABLE order_items (
  order_id TEXT, product_id TEXT, qty INTEGER, unit_price REAL);""")

    sql.append("INSERT INTO customers VALUES\n" + ",\n".join(
        "(%s,%s,%s,%s,%s)" % (q(c[0]), q(c[1]), q(c[2]), q(c[3]), q(c[4])) for c in customers) + ";")
    sql.append("INSERT INTO products VALUES\n" + ",\n".join(
        "(%s,%s,%s,%.2f,%.2f)" % (q(p[0]), q(p[1]), q(p[2]), p[3], p[4]) for p in PRODUCTS) + ";")
    sql.append("INSERT INTO orders VALUES\n" + ",\n".join(
        "(%s,%s,%s,%s,%s)" % (q(o[0]), q(o[1]), q(o[2]), q(o[3]), q(o[4])) for o in orders) + ";")
    sql.append("INSERT INTO order_items VALUES\n" + ",\n".join(
        "(%s,%s,%d,%.2f)" % (q(t[0]), q(t[1]), t[2], t[3]) for t in items) + ";")
    return "\n".join(sql), len(customers), len(orders), len(items)

if __name__ == '__main__':
    s, nc, no, ni = gen_sales_sql()
    print(f"customers={nc} orders={no} items={ni} len={len(s)}")
    open('/mnt/agents/build/sales_init.sql', 'w', encoding='utf-8').write(s)
