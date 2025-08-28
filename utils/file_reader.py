import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
def read_csv_summary(filename: str) -> str:
    """
    Lese eine CSV Datei und gebe eine einfache zusammenfassung zurueck.
    Args:
        filename: Name der CSV Datei (e.g. 'sample.csv')
    Returns:
        Ein string, welcher den Inhalt der Datei beschreibts.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    return f"CSV Datei '{filename}' hat {len(df)} Zeilen und {len(df.columns)} Spalten."
def read_parquet_summary(filename: str) -> str:
    """
    Lese eine Parquet Datei und gebe eine einfache zusammenfassung zurueck.
    Args:
        filename: Name der Parquet Datei (e.g. 'sample.parquet')
    Returns:
       Ein string, welcher den Inhalt der Datei beschreibts.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    return f"Parquet Datei '{filename}' hat {len(df)} Zeilen und {len(df.columns)} Spalten."