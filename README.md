### NOTICE

**This repository is just my personal learning field to deepen my knowledge about Python, Git, GitHub, XML, JSON and VSCode.**

# GAEB-XML-Validator
GAEB-XML-Checker for the comparison of GAEB exchange files with the GAEB schema.

The **GAEB-XML-Validator** is a simple script for checking the correctness of GAEB (Gemeinsamer Ausschuss Elektronik im Bauwesen) exchange files. By using GAEB schema files, this script ensures that your XML files comply with the specified standards.

The GAEB schema files must be downloaded separately from the [GAEB website](https://www.gaeb.de/de/service/downloads/gaeb-datenaustausch/)
Alternatively, you can use the script "GAEB-XSD_downloader.py" to download the files.

## Functions

- Validates GAEB exchange files using schema definitions.

## Usage

1. clone this repository.
2. install the necessary dependencies (Python, etc.).
3. run the validation script for your GAEB XML files.

## Example for a future function

```bash
python validate_gaeb.py path/to/your/file.xml
```

## Contributions

Contributions and feedback are welcome! Feel free to report problems or submit pull requests.
