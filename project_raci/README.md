1)
do a cd project_raci
2)
do a pip install -r /workspaces/WebDev/project_raci/requirements.txt
3)
open de database
sqlite3 database.db
4)
Ctrl K Ctrl 0 for colapse functions
5) run main
/home/codespace/.python/current/bin/python /workspaces/WebDev/project_raci/main.py

6)
get context:
find . -type f \( -name "*.py" -o -name "*.sql" \) -exec sh -c '
echo "\n=== $1 ===\n"
cat "$1"
' _ {} \; > contexto_projeto.txt