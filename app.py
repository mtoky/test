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

def log_system_specs():
    """Logs detailed system specifications."""
    try:
        logging.info("==================== HOSTING SPECS ====================")
        
        # Memory Info
        memory = psutil.virtual_memory()
        total_mem_gb = f"{memory.total / (1024**3):.2f} GB"
        available_mem_gb = f"{memory.available / (1024**3):.2f} GB"
        logging.info(f"RAM: Total = {total_mem_gb}, Available = {available_mem_gb}, Usage = {memory.percent}%")

        # Disk Info
        disk = psutil.disk_usage('/')
        total_disk_gb = f"{disk.total / (1024**3):.2f} GB"
        free_disk_gb = f"{disk.free / (1024**3):.2f} GB"
        logging.info(f"Disk (/): Total = {total_disk_gb}, Free = {free_disk_gb}, Usage = {disk.percent}%")

        # CPU Info
        cpu_cores = psutil.cpu_count(logical=False)
        logical_processors = psutil.cpu_count(logical=True)
        logging.info(f"CPU: Physical Cores = {cpu_cores}, Logical Processors = {logical_processors}")

        # OS Info
        logging.info(f"Operating System: {platform.system()} {platform.release()}")
        
        logging.info("======================================================")
    except Exception as e:
        logging.error(f"Could not retrieve system specs: {e}")

# Log system specs on application startup
log_system_specs()

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