import xmlschema
from lxml import etree
import json

def validate_xml(xml_path, xsd_path):
    # Lade das XSD-Schema
    schema = xmlschema.XMLSchema(xsd_path)

    # Lade die XML-Datei
    doc = etree.parse(xml_path)

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
    with open('validation_results.json', 'w') as f:
        json.dump({
            "is_valid": len(errors) == 0,
            "errors": errors,
            "used_xsd_files": locations
        }, f, indent=4)

    if len(errors) == 0:
        print("Die XML-Datei ist gültig.")
    else:
        print("Die XML-Datei ist ungültig. Die Fehler wurden in der Datei 'validation_results.json' gespeichert.")

# Pfad zu den verwendeten Dateien (Pfad zu der 83-GAEB-XML-Datei)
validate_xml('example.X83', 'GAEB_DA_XML_83_3.3_2021-05.xsd')
