from server import mcp
import subprocess

@mcp.tool()
def start_bot() -> str:

    """
    Start des Discord Bottes.
    Args:
        None
    Returns:
        Ein string mit moeglichen Errors oder einer Bestaetigung fuer den Start des Discord Bottes.
    """

    python_executable = r"C:\Users\Laurens\AppData\Local\Programs\Python\Python313\python.exe"
    script_path = r"C:\Users\Laurens\Documents\_shit\pojects\git\py-dc-garmin\main.py"
    try:
        subprocess.run([
            "cmd.exe", "/c", "start", "cmd.exe", "/k",
            f'{python_executable} {script_path}'
        ], check=True)
        return "Garmin Programm wurde in einem neuem Fenster geoefnett."
    except subprocess.CalledProcessError as e:
        return(f"Error beim starten vom Garmin Programm: {e}")
    except FileNotFoundError:
        return(f"Error: Python Datei nicht gefuenden: {python_executable}")
