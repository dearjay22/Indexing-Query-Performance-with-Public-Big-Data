import subprocess

MYSQL_CONTAINER = "devcontainer-mysql-1"
MYSQL_USER = "root"
MYSQL_PASS = "rootpass"
SQL_FILE = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/sql/explain_plans.sql"

print("\n===== Running EXPLAIN Plans =====")
subprocess.run(
    f'docker exec -i {MYSQL_CONTAINER} mysql -u{MYSQL_USER} -p{MYSQL_PASS} < {SQL_FILE}',
    shell=True
)
