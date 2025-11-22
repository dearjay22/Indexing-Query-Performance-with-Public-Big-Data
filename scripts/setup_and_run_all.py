import subprocess
import os
import time
import requests
from tqdm import tqdm

# -----------------------
# CONFIGURATION
# -----------------------
MYSQL_CONTAINER = "devcontainer-mysql-1"
MYSQL_USER = "root"
MYSQL_PASS = "rootpass"
CSV_FILE_LOCAL = "./data/dataset.csv"
CSV_FILE_CONTAINER = "/var/lib/mysql-files/dataset.csv"
SQL_DIR = "./sql"
DOCKER_COMPOSE_FILE = ".devcontainer/docker-compose.yml"

# -----------------------
# HELPER FUNCTIONS
# -----------------------
def run(cmd):
    print(f"> {cmd}")
    subprocess.check_call(cmd, shell=True)

def is_mysql_running():
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={MYSQL_CONTAINER}", "--filter", "status=running", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return MYSQL_CONTAINER in result.stdout

def free_port_3306():
    result = subprocess.run(
        ["docker", "ps", "--filter", "publish=3306", "--format", "{{.ID}}"],
        capture_output=True, text=True
    )
    container_ids = result.stdout.strip().splitlines()
    for cid in container_ids:
        print(f"Stopping container {cid} that uses port 3306")
        run(f"docker stop {cid}")

def start_mysql_compose():
    if is_mysql_running():
        print("MySQL container already running. Skipping docker-compose up.")
        return
    # Free port if necessary
    free_port_3306()
    print("Starting MySQL container via docker-compose...")
    run(f"docker compose -f {DOCKER_COMPOSE_FILE} up -d")
    wait_for_mysql()

def wait_for_mysql(timeout=60):
    print("Waiting for MySQL to become healthy...", end="")
    for _ in range(timeout):
        result = subprocess.run(
            ["docker", "exec", MYSQL_CONTAINER, "mysqladmin", "ping", f"-u{MYSQL_USER}", f"-p{MYSQL_PASS}"],
            capture_output=True, text=True
        )
        if "alive" in result.stdout:
            print("\nMySQL is alive.")
            return
        print(".", end="", flush=True)
        time.sleep(1)
    raise RuntimeError("MySQL did not become healthy in time.")

def download_csv():
    if os.path.exists(CSV_FILE_LOCAL):
        print(f"CSV already exists: {CSV_FILE_LOCAL}")
        return
    print("Downloading CSV...")
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=150000"
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(CSV_FILE_LOCAL, "wb") as f, tqdm(
        desc="Downloading CSV",
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

def copy_csv_to_container():
    print(f"Copying CSV to container: {CSV_FILE_CONTAINER}")
    run(f"docker cp {CSV_FILE_LOCAL} {MYSQL_CONTAINER}:{CSV_FILE_CONTAINER}")

def docker_exec_mysql(sql_command):
    run(f'docker exec -i {MYSQL_CONTAINER} mysql --local-infile=1 -u{MYSQL_USER} -p{MYSQL_PASS} -e "{sql_command}"')

def run_sql_file_inside_mysql(local_path):
    container_path = f"/tmp/{os.path.basename(local_path)}"
    run(f"docker cp {local_path} {MYSQL_CONTAINER}:{container_path}")
    docker_exec_mysql(f"SOURCE {container_path};")

def load_schema_and_data():
    # Load schema
    run_sql_file_inside_mysql(os.path.join(SQL_DIR, "schema.sql"))

    # Prepare load_data.sql dynamically to use CSV path inside container
    load_data_sql = f"""
    USE bigdata;
    SET GLOBAL local_infile=1;
    LOAD DATA LOCAL INFILE '{CSV_FILE_CONTAINER}'
    INTO TABLE nyc311
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\\n'
    IGNORE 1 LINES
    (unique_key, created_date, closed_date, agency, agency_name, complaint_type, descriptor, location_type,
     incident_zip, city, borough, latitude, longitude, status, resolution_description);
    """
    container_load_file = "/tmp/load_data.sql"
    with open(container_load_file, "w") as f:
        f.write(load_data_sql)

    run_sql_file_inside_mysql(container_load_file)

def run_analysis_queries():
    # Replace these with your own queries if needed
    queries = [
        "USE bigdata; EXPLAIN SELECT * FROM nyc311 WHERE complaint_type='Noise';",
        "USE bigdata; SELECT borough, COUNT(*) FROM nyc311 GROUP BY borough;",
    ]
    for q in queries:
        docker_exec_mysql(q)

# -----------------------
# MAIN EXECUTION
# -----------------------
def main():
    start_mysql_compose()
    download_csv()
    copy_csv_to_container()
    load_schema_and_data()
    run_analysis_queries()
    print("All done!")

if __name__ == "__main__":
    main()

    # Launch Streamlit UI for results in Codespaces
    print("\nLaunching Streamlit UI for query results...")
    try:
        import subprocess

        # Use explicit port 8501 and all interfaces so Codespaces can forward it
        subprocess.Popen([
            "streamlit", "run", "scripts/run_all_ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])

        print("Streamlit UI started.")
        print("Go to the Codespaces 'Ports' tab and forward port 8501.")
        print("You will then get a URL to open the dashboard in your browser.")

    except Exception as e:
        print(f"Failed to launch Streamlit UI: {e}")
