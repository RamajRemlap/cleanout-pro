import click
import os
import subprocess
import sys
import time

PID_FILE = "jules_runner.pid"
LOG_FILE = "backend.log"

@click.group()
def cli():
    """A command-line tool to manage the Jules runner."""
    pass

@cli.command("start-backend")
def start_backend():
    """Starts the backend server."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
            if pid:
                try:
                    os.kill(int(pid), 0)
                    click.echo(f"Backend server is already running with PID: {pid}.")
                    return
                except (OSError, ValueError):
                    os.remove(PID_FILE)

    click.echo("Starting backend server...")
    command = f"nohup {sys.executable} app.py > {LOG_FILE} 2>&1 & echo $! > {PID_FILE}"
    try:
        subprocess.run(command, shell=True, check=True)
        time.sleep(2)
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        click.echo(f"Backend server started with PID: {pid}. Output is in {LOG_FILE}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        click.echo(f"Failed to start backend server: {e}")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

@cli.command("stop-backend")
def stop_backend():
    """Stops the backend server."""
    if not os.path.exists(PID_FILE):
        click.echo("Backend server is not running (no PID file found).")
        return

    with open(PID_FILE, "r") as f:
        pid_str = f.read().strip()
        if not pid_str:
            click.echo("PID file is empty. The server may have failed to start.")
            os.remove(PID_FILE)
            return

    pid = int(pid_str)

    try:
        os.kill(pid, 15)
        click.echo(f"Sent SIGTERM to backend server with PID: {pid}. Waiting for graceful shutdown...")
        time.sleep(5)
        os.kill(pid, 9)
        click.echo(f"Backend server with PID: {pid} stopped forcefully.")
    except ProcessLookupError:
        click.echo(f"Process with PID: {pid} not found. It might have already been stopped.")
    except Exception as e:
        click.echo(f"Failed to stop backend server: {e}")
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

@cli.command("test-backend")
def test_backend():
    """Runs the backend tests."""
    click.echo("Running backend tests...")

    click.echo("Installing dependencies from backend/requirements.txt...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"],
            capture_output=True,
            text=True,
            check=True
        )
        click.echo("Backend dependencies installed.")
    except subprocess.CalledProcessError as e:
        click.echo("Failed to install backend dependencies:")
        click.echo(e.stdout)
        click.echo(e.stderr)
        return

    click.echo("Running pytest...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            cwd="backend",
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            click.echo("Backend tests passed.")
            click.echo(result.stdout)
        else:
            click.echo("Backend tests failed.")
            click.echo(result.stdout)
            click.echo(result.stderr)

    except FileNotFoundError:
        click.echo("pytest not found. Make sure it's installed (`pip install -r backend/requirements.txt`).")
    except Exception as e:
        click.echo(f"An error occurred while running tests: {e}")

if __name__ == "__main__":
    cli()
