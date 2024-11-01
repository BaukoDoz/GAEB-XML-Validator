import xmlschema
from lxml import etree
import json
import os
import re
import sys
from datetime import datetime

def validate_xml(xml_path, schema_directory):
    # Überprüfe, ob der Dateipfad korrekt ist
    if not os.path.exists(xml_path):
        print(f"Fehler: Die XML-Datei {xml_path} wurde nicht gefunden. Bitte überprüfen Sie den Pfad und versuchen Sie es erneut.")
        sys.exit(1)
    xml_path = os.path.abspath(xml_path)

    # Lade die XML-Datei und extrahiere den Namespace
    try:
        with open(xml_path, 'r') as file:
            doc = etree.parse(file)
            root = doc.getroot()
            namespace = root.nsmap.get(None)  # Extrahiere den Standard-Namespace
    except etree.XMLSyntaxError as e:
        raise ValueError(f"XML-Syntaxfehler in der Datei {xml_path}: {e}")
    except OSError as e:
        raise FileNotFoundError(f"Fehler beim Zugriff auf die XML-Datei {xml_path}: {e}")

    if not namespace:
        raise ValueError(f"Kein Namespace in der XML-Datei {xml_path} gefunden. Bitte überprüfen Sie die Datei auf korrektes Namespace-Format.")

    # Lade alle XSD-Dateien und extrahiere deren Namespaces und TargetNamespaces
    xsd_files = []
    for file in os.listdir(schema_directory):
        if file.endswith('.xsd'):
            xsd_path = os.path.join(schema_directory, file)
            try:
                # Lade das XSD und analysiere es
                with open(xsd_path, 'r') as f:
                    xsd_content = f.read()
                    target_namespace_match = re.search(r'targetNamespace="(.*?)"', xsd_content)
                    if target_namespace_match:
                        target_namespace = target_namespace_match.group(1)
                        xsd_files.append((xsd_path, target_namespace))
            except OSError as e:
                print(f"Fehler beim Laden der XSD-Datei {file}: {e}")

    # Finde die passende XSD-Datei basierend auf dem Namespace und analysiere auch verlinkte XSD-Dateien
    matched_xsd_files = []
    def find_matching_xsd_files(xsd_path, target_namespace, visited):
        if xsd_path in visited:
            return
        visited.add(xsd_path)
        matched_xsd_files.append(xsd_path)

        try:
            with open(xsd_path, 'r') as f:
                xsd_content = f.read()
                redefine_matches = re.findall(r'<xs:redefine\s+schemaLocation="(.*?)"', xsd_content)
                for redefine_location in redefine_matches:
                    redefine_path = os.path.join(schema_directory, redefine_location)
                    if os.path.exists(redefine_path):
                        find_matching_xsd_files(redefine_path, target_namespace, visited)
        except OSError as e:
            print(f"Fehler beim Analysieren der XSD-Datei {xsd_path}: {e}")

    xsd_path = None
    for path, target_namespace in xsd_files:
        if target_namespace == namespace:
            xsd_path = path
            find_matching_xsd_files(xsd_path, target_namespace, set())
            break

    if xsd_path is None:
        raise FileNotFoundError(f"Keine passende XSD-Schemadatei für Namespace {namespace} im Ordner {schema_directory} gefunden. Bitte stellen Sie sicher, dass die XSD-Dateien mit den XML-Namespaces übereinstimmen.")

    # Lade das XSD-Schema
    try:
        schema = xmlschema.XMLSchema(xsd_path)
    except (xmlschema.XMLSchemaParseError, OSError) as e:
        raise ValueError(f"Fehler beim Laden des XSD-Schemas aus {xsd_path}: {e}")

    # Validiere die XML-Datei gegen das XSD-Schema und speichere die Fehler
    errors = []
    for error in schema.iter_errors(doc):
        full_line = None
        if error.elem is not None:
            try:
                line_number = error.elem.sourceline
                with open(xml_path, 'r') as file:
                    lines = file.readlines()
                    if line_number <= len(lines):
                        full_line = lines[line_number - 1].strip()
            except OSError as e:
                print(f"Fehler beim Lesen der XML-Datei für die vollständige Zeile: {e}")

        if "unexpected child" in str(error).lower():
            hint = "Ein unerwartetes Element wurde gefunden. Überprüfen Sie die XML-Struktur und vergleichen Sie diese mit der erwarteten Struktur im Schema."
        elif "value must be one of" in str(error).lower():
            hint = "Ein ungültiger Wert wurde gefunden. Überprüfen Sie, ob der Wert den erlaubten Werten im Schema entspricht."
        else:
            hint = "Allgemeiner Validierungsfehler. Überprüfen Sie den spezifischen Fehler und die betroffene Zeile."

        errors.append({
            "path": error.path,
            "message": f"{str(error)} Hinweis: {hint}",
            "full_line": full_line
        })

    # verwendeten XSD-Dateien ausgeben (nur die passenden XSD-Dateien und deren verlinkte Dateien)
    locations = matched_xsd_files

    # Ergebnisse in einer JSON-Datei speichern
    try:
        with open('validation_results.json', 'w') as f:
            json.dump({
                "checked_file": os.path.basename(xml_path),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_valid": len(errors) == 0,
                "errors": errors,
                "used_xsd_files": locations
            }, f, indent=4)
    except OSError as e:
        raise ValueError(f"Fehler beim Schreiben der Datei 'validation_results.json': {e}")

    if len(errors) == 0:
        print("Die XML-Datei ist gültig und entspricht dem angegebenen Schema.")
    else:
        print(f"Die XML-Datei entspricht nicht dem Schema. {len(errors)} Fehler wurden gefunden und in der Datei 'validation_results.json' gespeichert.")

# Überprüfe, ob ein Dateipfad als Argument übergeben wurde
if len(sys.argv) != 2:
    print("Verwendung: python validate_gaeb.py <Pfad/zur/XML-Datei>")
    sys.exit(1)

# Pfad zu der übergebenen Datei
xml_path = sys.argv[1]
xml_path = os.path.abspath(xml_path)  # Absoluten Pfad sicherstellen
validate_xml(xml_path, 'GAEB-XSD_schema_files')
