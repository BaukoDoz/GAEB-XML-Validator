### NOTICE

**This repository is just my personal learning field to deepen my knowledge about Python, Git, GitHub, XML, JSON and VSCode.**

# GAEB-XML-Validator

This project contains a simple Python script that validates an XML file against a collection of XSD schema files. It enables the verification of GAEB-XML files to ensure that they comply with the specified schemas. The validation results are saved in a JSON file.

## Requirements

- Python 3.6 or higher
- The following Python libraries:
  - `lxml`
  - `xmlschema`

These libraries can be installed via `pip`:

```bash
pip install lxml xmlschema
```

## Installation

1. Clone the repository to your local machine:

```bash
git clone <URL of your repository>
```

2. Navigate into the project folder:

```bash
cd GAEB-XML-Validator
```

3. Ensure the required libraries are installed (see "Requirements" section).

## Usage

The script `validate_gaeb.py` checks an XML file that is passed as an argument. The appropriate XSD file is searched for in the directory `GAEB-XSD_schema_files`.

### Note on XSD Schema Files

If no suitable schema files are present in the directory `GAEB-XSD_schema_files`, they must first be downloaded. You can do this manually from the [GAEB website](https://www.gaeb.de/de/service/downloads/gaeb-datenaustausch/) or use the script `GAEB-XSD_downloader.py` to download the necessary files.

### Syntax

```bash
python validate_gaeb.py path/to/your/file.xml
```

- **path/to/your/file.xml**: Path to the XML file to be validated.

### Example

```bash
python validate_gaeb.py GAEB-XML_examples/example.X83
```

### Error Handling

The script provides basic error handling:
- If the specified XML file is not found, you will receive an error message indicating that the path may be incorrect.
- Errors during parsing the XML file or loading the XSD files are reported accordingly.

### Output

- After validation, the script saves the results in a file called `validation_results.json` in the current directory. This file contains:
  - **is_valid**: Indicates whether the XML file is valid.
  - **errors**: A list of encountered errors (if any).
  - **used_xsd_files**: A list of used XSD files.

- If the XML file is valid, the message "The XML file is valid." will be displayed.
- If errors are found, the number of errors along with information on storing the results will be displayed.

## Folder Structure

- **GAEB-XML_examples/**: Contains example XML files for validation.
- **GAEB-XSD_schema_files/**: Contains the XSD files used for XML validation.
- **validate_gaeb.py**: The Python script for validating XML files.
- **GAEB-XSD_downloader.py**: Script for downloading the required GAEB schema files.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contribution

Contributions to this project are welcome. Please create a pull request or an issue if you have suggestions or found a bug.

---

# GAEB-XML-Validator

Dieses Projekt enthält ein einfaches Python-Skript, das eine XML-Datei gegen eine Sammlung von XSD-Schemadateien validiert. Es ermöglicht eine Überprüfung von GAEB-XML-Dateien, um sicherzustellen, dass diese den spezifizierten Schemata entsprechen. Die Ergebnisse der Validierung werden in einer JSON-Datei gespeichert.

## Voraussetzungen

- Python 3.6 oder höher
- Die folgenden Python-Bibliotheken:
  - `lxml`
  - `xmlschema`

Diese Bibliotheken können über `pip` installiert werden:

```bash
pip install lxml xmlschema
```

## Installation

1. Klonen Sie das Repository auf Ihren lokalen Rechner:

```bash
git clone <URL Ihres Repositories>
```

2. Navigieren Sie in den Projektordner:

```bash
cd GAEB-XML-Validator
```

3. Stellen Sie sicher, dass die erforderlichen Bibliotheken installiert sind (siehe Abschnitt "Voraussetzungen").

## Verwendung

Das Skript `validate_gaeb.py` überprüft eine XML-Datei, die als Argument übergeben wird. Die passende XSD-Datei wird im Verzeichnis `GAEB-XSD_schema_files` gesucht.

### Hinweis zu den XSD-Schemadateien

Falls noch keine passenden Schemadateien im Verzeichnis `GAEB-XSD_schema_files` vorhanden sind, müssen diese zunächst heruntergeladen werden. Sie können dies manuell von der [GAEB-Website](https://www.gaeb.de/de/service/downloads/gaeb-datenaustausch/) tun oder das Skript `GAEB-XSD_downloader.py` verwenden, um die benötigten Dateien herunterzuladen.

### Syntax

```bash
python validate_gaeb.py path/to/your/file.xml
```

- **path/to/your/file.xml**: Pfad zur XML-Datei, die validiert werden soll.

### Beispiel

```bash
python validate_gaeb.py GAEB-XML_examples/example.X83
```

### Fehlerbehandlung

Das Skript bietet eine grundlegende Fehlerbehandlung:
- Wenn die angegebene XML-Datei nicht gefunden wird, erhalten Sie eine Fehlermeldung, die darauf hinweist, dass der Pfad falsch sein könnte.
- Bei Fehlern während des Parsens der XML-Datei oder beim Laden der XSD-Dateien werden entsprechende Fehlermeldungen ausgegeben.

### Ausgabe

- Nach der Validierung speichert das Skript die Ergebnisse in einer Datei namens `validation_results.json` im aktuellen Verzeichnis. Diese Datei enthält:
  - **is_valid**: Gibt an, ob die XML-Datei gültig ist.
  - **errors**: Eine Liste der aufgetretenen Fehler (falls vorhanden).
  - **used_xsd_files**: Eine Liste der verwendeten XSD-Dateien.

- Wenn die XML-Datei gültig ist, wird die Nachricht "Die XML-Datei ist gültig." ausgegeben.
- Wenn Fehler gefunden werden, wird die Anzahl der Fehler zusammen mit der Information über die Speicherung der Ergebnisse angezeigt.

## Ordnerstruktur

- **GAEB-XML_examples/**: Enthält Beispiel-XML-Dateien zur Validierung.
- **GAEB-XSD_schema_files/**: Enthält die XSD-Dateien, die zur Validierung der XML-Dateien verwendet werden.
- **validate_gaeb.py**: Das Python-Skript zur Validierung der XML-Dateien.
- **GAEB-XSD_downloader.py**: Skript zum Herunterladen der benötigten GAEB-Schemadateien.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der Datei `LICENSE`.

