#!/usr/bin/env bash
# 检索跨工具共享全局记忆（默认 ~/.agents/memory/）。
# 先精确匹配 frontmatter keywords 的每一项（忽略大小写），未命中的文件再查正文。
# 用法: search.sh <关键词...>     多个关键词为 OR
# 可通过环境变量 GLOBAL_MEMORY_DIR 覆盖记忆目录。
set -euo pipefail

[ $# -gt 0 ] || { echo "用法: $0 <关键词...>" >&2; exit 2; }

memory_dir=${GLOBAL_MEMORY_DIR:-"${HOME}/.agents/memory"}
memory_dir=${memory_dir%/}
memory_dir=${memory_dir:-/}
[ -d "$memory_dir" ] || { echo "记忆目录不存在: $memory_dir" >&2; exit 2; }

mapfile -t files < <(find "$memory_dir" -name '*.md' -type f | sort)

patterns=()
for word in "$@"; do patterns+=(-e "$word"); done

if command -v rg >/dev/null 2>&1; then
  search_cmd=(rg -n --no-filename --fixed-strings --ignore-case --max-count 2)
else
  search_cmd=(grep -n -h -F -i -m 2)
fi

kw_hits=()
body_hits=()

for f in "${files[@]}"; do
  [ -n "$f" ] || continue
  rel=${f#"$memory_dir"/}
  mapfile -t items < <(awk '
    NR == 1 && /^---[[:space:]]*$/ { in_fm = 1; next }
    !in_fm { exit }
    /^---[[:space:]]*$/ { exit }
    /^keywords:[[:space:]]*$/ { inblock = 1; next }
    inblock && /^[[:space:]]*- / {
      sub(/^[[:space:]]*- [[:space:]]*/, "")
      sub(/[[:space:]]+$/, "")
      gsub(/^\042|\042$/, ""); gsub(/^\047|\047$/, "")
      print; next
    }
    inblock { exit }
  ' "$f")
  hit=""
  for w in "$@"; do
    for item in "${items[@]}"; do
      if [[ ${item,,} == "${w,,}" ]]; then hit=$item; break 2; fi
    done
  done
  if [[ -n $hit ]]; then
    joined=""
    for item in "${items[@]}"; do joined+="${joined:+、}$item"; done
    type=$(awk -F': *' '/^type:/{print $2; exit}' "$f")
    kw_hits+=("$rel|${type:-unknown}|$joined")
    continue
  fi
  while IFS= read -r line; do
    body_hits+=("$rel|$line")
  done < <("${search_cmd[@]}" "${patterns[@]}" -- "$f" 2>/dev/null || true)
done

if [ ${#kw_hits[@]} -eq 0 ] && [ ${#body_hits[@]} -eq 0 ]; then
  echo "未命中: $*"
  exit 1
fi

if [ ${#kw_hits[@]} -gt 0 ]; then
  echo "== keywords 命中 (${#kw_hits[@]}) =="
  for h in "${kw_hits[@]}"; do
    file=${h%%|*}; rest=${h#*|}
    type=${rest%%|*}; kw=${rest#*|}
    echo "[$type] $file"
    echo "    $kw"
  done
fi

if [ ${#body_hits[@]} -gt 0 ]; then
  echo "== 正文命中 (${#body_hits[@]}) =="
  for h in "${body_hits[@]}"; do
    file=${h%%|*}; line=${h#*|}
    echo "  $file:${line%%:*}  ${line#*:}"
  done
fi
