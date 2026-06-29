import os
import subprocess
import sys
import typer

def _clean_env():
    """Return an environment with PyInstaller's LD_LIBRARY_PATH undone."""
    env = os.environ.copy()
    orig = env.pop("LD_LIBRARY_PATH_ORIG", None)
    if orig is not None:
        env["LD_LIBRARY_PATH"] = orig
    else:
        env.pop("LD_LIBRARY_PATH", None)
    return env

def perform_update():
    """
    Pulls the latest release and runs the bash installer.
    """
    typer.secho("Starting update process...", fg=typer.colors.CYAN)

    install_cmd = "curl -sL https://raw.githubusercontent.com/gobbolab/goblin-speaks/main/linux/setup.sh | sudo bash"

    try:
        subprocess.run(install_cmd, shell=True, check=True, env=_clean_env())
        
        typer.secho("Update successfully applied!", fg=typer.colors.GREEN)
        
        # Gracefully exit so systemd/tmux can restart the process
        sys.exit(0)
        
    except subprocess.CalledProcessError as e:
        typer.secho(f"The update script failed with exit code {e.returncode}.", fg=typer.colors.RED)
        raise typer.Exit(code=1)