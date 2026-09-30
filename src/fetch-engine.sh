#!/bin/sh
# 拉取 sql.js 引擎文件（构建用，版本锁定 1.10.3）
# 引擎是第三方标准组件，不入库；执行本脚本即可复原
set -e
cd "$(dirname "$0")"
curl -sL -o sql-wasm.js   https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js
curl -sL -o sql-wasm.wasm https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.wasm
# 转成 base64 文本（build.py 读这个）；macOS 用: base64 -i sql-wasm.wasm -o sql-wasm.wasm.b64
base64 -w0 sql-wasm.wasm > sql-wasm.wasm.b64 2>/dev/null || base64 -i sql-wasm.wasm -o sql-wasm.wasm.b64
echo "ok: wasm $(wc -c < sql-wasm.wasm) bytes, b64 $(wc -c < sql-wasm.wasm.b64) bytes"
