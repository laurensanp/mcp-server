# MCP-Server

## Übersicht
Dies ist ein Serverprojekt, das als Backend für eine Anwendung dient. Es implementiert das **Model Context Protocol (MCP)**, um es KI-Modellen wie LM Studio zu ermöglichen, sicher mit lokalen Daten und benutzerdefinierten Tools zu interagieren. Beispiel: Der Server verarbeitet Daten, die in CSV- und Parquet-Formaten vorliegen können, und bietet Tools zur Datenverarbeitung und -analyse.

## Projektstruktur
- `main.py`: Hauptdatei zum Starten des MCP-Servers.
- `server.py`: Enthält die Logik für den MCP-Server und registriert die Tools.
- `generate_parquet.py`: Skript zur Generierung von Parquet-Dateien aus anderen Datenquellen (z.B. `sample.csv`).
- `data/`: Verzeichnis für Beispieldaten (`sample.csv`, `sample.parquet`).
- `tools/`: Enthält die MCP-Tool-Definitionen:
    - `csv_tools.py`: Funktionen zur Verarbeitung von CSV-Dateien.
    - `parquet_tools.py`: Funktionen zur Verarbeitung von Parquet-Dateien.
- `utils/`: Enthält wiederverwendbare Hilfsfunktionen zum Lesen von Dateien:
    - `file_reader.py`: Hilfsfunktionen zum Lesen von CSV- und Parquet-Dateien und zur Zusammenfassung ihrer Inhalte.
- `pyproject.toml`: Projektkonfigurationsdatei, die die Abhängigkeiten des Projekts verwaltet.
- `uv.lock`: Sperrdatei für Abhängigkeiten, generiert von `uv`.

## Installation
Es wird dringend empfohlen, **uv** für die Installation und Verwaltung der Abhängigkeiten zu verwenden, da es sich um einen schnellen und modernen Python-Projektmanager handelt.

1.  **uv installieren:**
    Stellen Sie sicher, dass `uv` auf Ihrem System installiert ist. Falls nicht, können Sie es wie folgt installieren:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    **Oder für Windows (falls curl nicht verfügbar):**
    ```bash
    pip install uv
    ```
    **or**
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    
    Starten Sie Ihr Terminal neu, damit der `uv`-Befehl verfügbar ist. Überprüfen Sie die Installation mit `uv --version`.

2.  **Repository klonen:**
    ```bash
    git clone <repository-url>
    cd mcp-server
    ```

3.  **Virtuelle Umgebung einrichten und Abhängigkeiten installieren:**
    ```bash
    uv venv
    .venv\Scripts\activate # Auf MacOS oder Linux: source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

## Nutzung

### MCP-Server starten
Um den MCP-Server zu starten, navigieren Sie zum Projekt-Root-Verzeichnis und führen Sie aus:
```bash
uv run main.py
```
Der Server wartet nun auf eine Verbindung von einem Client wie LM Studio. Jedoch ist der Sever nicht dauerhaft anzuhaben, da LM Studio ihn auch automatisch startet (im hintergrund).

### Integration mit LM Studio
Um LM Studio mit Ihrem MCP-Server zu verbinden, müssen Sie die Konfigurationsdatei von LM Studio anpassen.

1.  **mcp.json in LM Studio bearbeiten:**
    Bearbeiten Sie die Datei `mcp.json` in LM Studio.

2.  **Server zur Konfiguration hinzufügen:**
    Fügen Sie den folgenden JSON-Code in die `mcp.json`-Datei ein und ersetzen Sie `/ABSOLUTE/PATH/TO/mcp-server` durch den tatsächlichen absoluten Pfad zu Ihrem Projektordner. Stellen Sie sicher, dass `uv` im Systempfad ist oder geben Sie den vollständigen Pfad zur `uv`-Ausführungsdatei an:
    ```json
    {
      "mcpServers": {
        "mcp-server": {
          "command": "uv",
          "args": [
            "--directory",
            "/ABSOLUTE/PATH/TO/mcp-server",
            "run",
            "main.py"
          ]
        }
      }
    }
    ```

3.  **LM Studio neu starten:**
    Nach dem Neustart von LM Studio sollten die Tools Ihres MCP-Servers verfügbar sein. Überprüfen Sie die Einstellungen oder das Interface von LM Studio, um die registrierten Tools (`summarize_csv_file`, `summarize_parquet_file`) zu finden.

### Beispielabfragen in LM Studio
Sie können LM Studio nun bitten, Ihre Tools zu verwenden, z.B.:
*   "Fasse die CSV-Datei namens `sample.csv` zusammen."
*   "Wie viele Zeilen hat `sample.parquet`?"

## Daten
Beispieldaten finden Sie im `data/`-Verzeichnis.

## Tools
Die Tools in diesem Verzeichnis (`csv_tools.py`, `parquet_tools.py`) sind primär für die Integration mit dem MCP-Server über `main.py` und `server.py` gedacht. Sie müssen nicht direkt ausgeführt werden, da der MCP-Server sie bei Bedarf aufruft.

## Utilities (`utils/`)
Das `utils/`-Verzeichnis enthält wiederverwendbare Hilfsfunktionen (z.B. `file_reader.py`) die von den Tools verwendet werden, um Daten zu verarbeiten und zusammenzufassen.

## Danksagungen
Dieses Projekt basiert auf der Inspiration und den Erkenntnissen von [@llm-guy](https://github.com/llm-guy).

["Building a Basic MCP Server with Python"](https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed)