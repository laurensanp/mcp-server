from server import mcp
import subprocess

@mcp.tool()
def start_bot() -> str:

    """
    Start for the Discord Bot.
    Args:
        None
    Returns:
        A string with possible Errors or an confirmation for the start of the bot.
    """

    python_executable = r"C:\Users\Laurens\AppData\Local\Programs\Python\Python313\python.exe"
    script_path = r"C:\Users\Laurens\Documents\_shit\pojects\git\py-dc-garmin\main.py"
    try:
        subprocess.run([
            "cmd.exe", "/c", "start", "cmd.exe", "/k",
            f'{python_executable} {script_path}'
        ], check=True)
        return "Garmin program started in a new terminal window."
    except subprocess.CalledProcessError as e:
        return(f"Error starting Garmin program: {e}")
    except FileNotFoundError:
        return(f"Error: Python executable not found at {python_executable}")
