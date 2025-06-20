from flask import Flask, render_template
import os
import psutil
import platform
import logging

# Configure logging to output to console
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

def get_cgroup_value(path):
    """Reads a numeric value from a cgroup file if it exists."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r') as f:
            return int(f.read().strip())
    except (IOError, ValueError):
        return None

def log_allocated_specs():
    """Logs container-allocated system specifications."""
    logging.info("================== ALLOCATED CONTAINER SPECS ==================")

    # Memory Info (from cgroups)
    mem_limit_path = "/sys/fs/cgroup/memory/memory.limit_in_bytes"
    mem_usage_path = "/sys/fs/cgroup/memory/memory.usage_in_bytes"
    
    # Support for cgroup v2 paths
    if not os.path.exists(mem_limit_path):
        mem_limit_path = "/sys/fs/cgroup/memory.max"
        mem_usage_path = "/sys/fs/cgroup/memory.current"

    mem_limit = get_cgroup_value(mem_limit_path)
    mem_usage = get_cgroup_value(mem_usage_path)

    if mem_limit and mem_limit < 2**60:  # Sanity check for 'no limit' values
        total_mem_gb = f"{mem_limit / (1024**3):.2f} GB"
        if mem_usage:
            usage_percent = f"{(mem_usage / mem_limit) * 100:.1f}%"
            logging.info(f"Allocated RAM: Limit = {total_mem_gb}, Current Usage = {usage_percent}")
        else:
            logging.info(f"Allocated RAM: Limit = {total_mem_gb}")
    else:
        # Fallback to host memory if cgroup limit is not found
        host_mem = psutil.virtual_memory()
        total_host_mem_gb = f"{host_mem.total / (1024**3):.2f} GB"
        logging.info(f"Allocated RAM: Limit not found. (Host Total RAM: {total_host_mem_gb})")

    # CPU Info (from cgroups)
    try:
        quota_us = get_cgroup_value("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
        period_us = get_cgroup_value("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
        if quota_us and period_us and quota_us > 0:
            cpu_cores = quota_us / period_us
            logging.info(f"Allocated CPU Cores: {cpu_cores:.2f}")
        else:
            host_cores = psutil.cpu_count(logical=True)
            logging.info(f"Allocated CPU Cores: Not specified. (Host Total Cores: {host_cores})")
    except Exception:
        host_cores = psutil.cpu_count(logical=True)
        logging.info(f"Allocated CPU Cores: Could not determine. (Host Total Cores: {host_cores})")

    # Disk Info Explanation
    logging.info("Allocated Disk: Quota is managed by the platform and is not visible from within the container.")
    
    logging.info("=============================================================")


# Log allocated specs on application startup
log_allocated_specs()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 