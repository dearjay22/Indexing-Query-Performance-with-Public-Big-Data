import subprocess
import time

MYSQL_CONTAINER = "devcontainer-mysql-1"
MYSQL_USER = "root"
MYSQL_PASS = "rootpass"
SQL_FILE = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/sql/queries_after.sql"

print("\n===== Running Queries After Indexing =====")
start = time.time()
subprocess.run(
    f'docker exec -i {MYSQL_CONTAINER} mysql -u{MYSQL_USER} -p{MYSQL_PASS} < {SQL_FILE}',
    shell=True
)
end = time.time()
print(f"\nTotal execution time: {end-start:.2f} seconds")
