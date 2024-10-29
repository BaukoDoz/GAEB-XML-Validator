import xmlschema
from lxml import etree
import json
import os
import re
import sys

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
        raise ValueError(f"Fehler beim Parsen der XML-Datei {xml_path}: {e}")
    except OSError as e:
        raise FileNotFoundError(f"Fehler beim Zugriff auf die XML-Datei {xml_path}: {e}")

    if not namespace:
        raise ValueError(f"Kein Namespace in der XML-Datei {xml_path} gefunden.")

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

    # Finde die passende XSD-Datei basierend auf dem Namespace
    xsd_path = None
    for path, target_namespace in xsd_files:
        if target_namespace == namespace:
            xsd_path = path
            break

    if xsd_path is None:
        raise FileNotFoundError(f"Keine passende XSD-Schemadatei für Namespace {namespace} im Ordner {schema_directory} gefunden.")

    # Lade das XSD-Schema
    try:
        schema = xmlschema.XMLSchema(xsd_path)
    except (xmlschema.XMLSchemaParseError, OSError) as e:
        raise ValueError(f"Fehler beim Laden des XSD-Schemas aus {xsd_path}: {e}")

    # Validiere die XML-Datei gegen das XSD-Schema und speichere die Fehler
    errors = []
    for error in schema.iter_errors(doc):
        errors.append({
            "message": str(error),
            "path": error.path,
            "schema_url": error.schema_url,
            "line": error.elem.sourceline if error.elem is not None else None,
            "annotations": dict(error.elem.attrib) if error.elem is not None else None
        })

    # verwendeten XSD-Dateien ausgeben
    locations = [location for location in schema.locations]

    # Ergebnisse in einer JSON-Datei speichern
    try:
        with open('validation_results.json', 'w') as f:
            json.dump({
                "is_valid": len(errors) == 0,
                "errors": errors,
                "used_xsd_files": locations
            }, f, indent=4)
    except OSError as e:
        raise ValueError(f"Fehler beim Schreiben der Datei 'validation_results.json': {e}")

    if len(errors) == 0:
        print("Die XML-Datei ist gültig.")
    else:
        print(f"Die XML-Datei ist ungültig. {len(errors)} Fehler wurden in der Datei 'validation_results.json' gespeichert.")

# Überprüfe, ob ein Dateipfad als Argument übergeben wurde
if len(sys.argv) != 2:
    print("Verwendung: python validate_gaeb.py path/to/your/file.xml")
    sys.exit(1)

# Pfad zu der übergebenen Datei
xml_path = sys.argv[1]
xml_path = os.path.abspath(xml_path)  # Absoluten Pfad sicherstellen
validate_xml(xml_path, 'GAEB-XSD_schema_files')
