import subprocess
import time
import streamlit as st
import pandas as pd
import json

st.title("NYC311 Query Performance Dashboard")

# Paths to your existing scripts
BASELINE_SCRIPT = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/scripts/run_baseline_queries.py"
AFTER_SCRIPT = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/scripts/run_after_queries.py"
EXPLAIN_SCRIPT = "/workspaces/Indexing-Query-Performance-with-Public-Big-Data/scripts/run_explain_plans.py"

option = st.sidebar.radio("Select View:", ["Baseline Queries", "Post-Index Queries", "EXPLAIN Plans"])

def run_script(script_path):
    """Runs an existing Python script and returns stdout, stderr"""
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

if option == "Baseline Queries":
    st.subheader("Baseline Queries (Before Indexing)")
    out, err = run_script(BASELINE_SCRIPT)
    if err:
        st.error(err)
    st.text(out)

elif option == "Post-Index Queries":
    st.subheader("Post-Index Queries (After Indexing)")
    out, err = run_script(AFTER_SCRIPT)
    if err:
        st.error(err)
    st.text(out)

elif option == "EXPLAIN Plans":
    st.subheader("EXPLAIN Plans (JSON)")
    out, err = run_script(EXPLAIN_SCRIPT)
    if err:
        st.error(err)

    plans = []
    # Split by 'EXPLAIN' and extract JSON
    for block in out.split("EXPLAIN"):
        block = block.strip()
        if not block:
            continue
        start = block.find("{")
        end = block.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = block[start:end]
            try:
                plans.append(json.loads(json_str))
            except json.JSONDecodeError:
                continue

    if not plans:
        st.warning("No EXPLAIN plans found. Make sure the SQL script is correct and the table exists.")
    else:
        for i, plan in enumerate(plans):
            st.markdown(f"**EXPLAIN Plan {i+1}:**")
            st.json(plan)
