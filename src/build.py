# -*- coding: utf-8 -*-
"""总装配：模板 + 课程内容 + 数据集 + 引擎 → dist/index.html（单文件成品）
用法：
  sh src/fetch-engine.sh        # 首次或恢复项目时：拉取 sql.js 引擎并转 base64
  python3 src/assemble_course.py
  python3 src/build.py
"""
import base64, json, os, sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
B = SRC + '/../'
from gen_data import gen as gen_animal
from gen_sales import gen_sales_sql

init_sql = gen_animal()[0] + "\n" + gen_sales_sql()[0]

tpl = open(SRC + '/template.html', encoding='utf-8').read()
sqljs = open(SRC + '/sql-wasm.js', encoding='utf-8').read()
wasm_b64 = open(SRC + '/sql-wasm.wasm.b64').read().strip()
appjs = open(SRC + '/app.js', encoding='utf-8').read()
course = open(SRC + '/course_final.json', encoding='utf-8').read()

esc = lambda js: js.replace('</script', '<\\/script')
html = tpl.replace('/*__SQLJS__*/', esc(sqljs))
html = html.replace('__WASM_B64__', wasm_b64)
html = html.replace('__INIT_SQL__', json.dumps(init_sql))
html = html.replace('__COURSE_JSON__', course)
html = html.replace('/*__APP_JS__*/', esc(appjs))

for ph in ('__WASM_B64__', '__COURSE_JSON__', '__INIT_SQL__', '__SQLJS__', '__APP_JS__'):
    assert ph not in html, 'placeholder left: ' + ph

out = B + 'dist/index.html'
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(html)
print(f"written {out}, size={len(html)/1024:.0f} KB")
