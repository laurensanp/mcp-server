from server import mcp
from utils.file_reader import read_parquet_summary
@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Gibt eine Zusammenfassung einer Parquet-Datei zurück, indem die Anzahl der Zeilen und Spalten angegeben wird.
    Args:
        filename: Name der Parquet-Datei im /data Verzeichnis (z.B. 'sample.parquet')
    Returns:
        Ein String, der die Dimensionen der Datei beschreibt.
    """
    return read_parquet_summary(filename)