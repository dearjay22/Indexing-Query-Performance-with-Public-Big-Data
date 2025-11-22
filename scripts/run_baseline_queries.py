import subprocess
import time
import os

MYSQL_CONTAINER = "devcontainer-mysql-1"
MYSQL_USER = "root"
MYSQL_PASS = "rootpass"
SQL_FILE = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/sql/queries_baseline.sql"

print("\n===== Running Baseline Queries =====")
start = time.time()

# Open the SQL file and pipe it into the mysql command inside the container
with open(SQL_FILE, "rb") as f:
    subprocess.run(
        ["docker", "exec", "-i", MYSQL_CONTAINER, "mysql", f"-u{MYSQL_USER}", f"-p{MYSQL_PASS}"],
        stdin=f,
        check=True
    )

end = time.time()
print(f"\nTotal execution time: {end-start:.2f} seconds")
