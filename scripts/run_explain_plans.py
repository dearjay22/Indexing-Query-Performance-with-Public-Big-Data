import subprocess
import json

MYSQL_CONTAINER = "devcontainer-mysql-1"
MYSQL_USER = "root"
MYSQL_PASS = "rootpass"
SQL_FILE = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/sql/explain_plans.sql"

print("\n===== Running EXPLAIN Plans =====")
def run_explain():
    print("\n===== Running EXPLAIN Plans =====")
    result = subprocess.run(
        f'docker exec -i {MYSQL_CONTAINER} mysql -u{MYSQL_USER} -p{MYSQL_PASS} --batch --raw < {SQL_FILE}',
        shell=True,
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                data = json.loads(line)
                print(json.dumps(data, indent=2))  # pretty print JSON
                print("-" * 60)
            except json.JSONDecodeError:
                print(line)
        else:
            print(line)

if __name__ == "__main__":
    run_explain()
