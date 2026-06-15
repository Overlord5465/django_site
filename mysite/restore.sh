# Выполняется через bash из docker-entrypoint-initdb.d (без shebang — совместимость с Windows).
set -euo pipefail

DUMP="/docker-entrypoint-initdb.d/mysite.dump"

if [ ! -f "$DUMP" ]; then
  echo "db-init: mysite.dump не найден — БД будет пустой (только migrate и seed вручную)."
  exit 0
fi

echo "db-init: восстановление из mysite.dump (это может занять несколько минут)..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-acl "$DUMP"
echo "db-init: готово."
