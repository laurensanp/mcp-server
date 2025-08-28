from server import mcp
from utils.file_reader import read_csv_summary
@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Gibt eine Zusammenfassung einer CSV-Datei zurück, indem die Anzahl der Zeilen und Spalten angegeben wird.
    Args:
        filename: Name der CSV-Datei im /data Verzeichnis (z.B. 'sample.csv')
    Returns:
        Ein String, der die Dimensionen der Datei beschreibt.
    """
    return read_csv_summary(filename)