# PS4 Ghidra AIO — ausführbare statische Analyse

## Dateien und Ordner

- `.github/workflows/ghidra.yml` — GitHub Actions Workflow; lädt Ghidra und die Release-`eboot.bin`, startet Analyse und lädt Ergebnisse als Artifact hoch.
- `ghidra_scripts/ExportFunctions.java` — Ghidra-Script; exportiert gefundene Funktionen, Adressen, Größen und Flags als CSV.
- `scripts/download_release_asset.py` — lädt genau ein Release-Asset anhand des Dateinamensmusters herunter.
- `scripts/merge_function_reports.py` — kombiniert CSV-Dateien und baut `index.html`.
- `game/sce_module/` — hier optionale eigene `.prx`- und `.sprx`-Plugins ablegen.
- `game/eboot.bin` — optional; falls diese Datei vorhanden ist, wird sie statt des Release-Downloads analysiert.

## Start

1. ZIP entpacken und alle enthaltenen Dateien in ein GitHub-Repository hochladen.
2. Auf GitHub **Actions** öffnen.
3. **PS4 Ghidra AIO (static)** wählen.
4. **Run workflow** klicken.
5. Nach Abschluss im Workflow unter **Artifacts** `PS4-Ghidra-AIO-Analysis` herunterladen.
6. Entpacken und `reports/index.html` im Browser öffnen oder `reports/all_functions.csv` mit Excel/LibreOffice öffnen.

## Release-Asset

Der Workflow ist auf das Release `ashps4/freeware`, Tag `untagged-4e0c2ac505eec4a32227` konfiguriert und sucht nach einem Asset, dessen Name `eboot.bin` enthält (Groß-/Kleinschreibung wird ignoriert). Falls das Asset anders benannt ist, den `--match`-Wert in `.github/workflows/ghidra.yml` ändern.

## Grenzen

Das ist statische Analyse. Funktionen, die erst in laufendem Spiel-RAM vorhanden sind, dynamisch erzeugt werden oder aus nicht mitgelieferten Modulen stammen, können hier nicht sicher aufgelistet werden. Dafür wäre ein separater Runtime-Debugger/Collector auf einer autorisierten Verbindung zu deiner eigenen PS4 erforderlich.

Ghidra wird aus dem offiziellen NSA-GitHub-Release geladen; der Workflow verwendet JDK 25 für die aktuelle Ghidra-Version.
