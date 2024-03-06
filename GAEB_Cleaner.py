#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module name: GAEB_Cleaner.py
Author: Hendrik Bark
Created on: 06.03.2024
Last modified: 06.03.2024
Version: 1.0
Description:
    This Python program takes an XML file as input, removes all empty <span> tags, 
    and then formats the XML file with an indentation of 4 characters. The formatted 
    XML is then written to a new file.
"""

import xml.dom.minidom

def format_xml_minidom(file_path, new_file_path):
    # Open and read XML file
    with open(file_path, 'r', encoding='UTF-8') as file:
        xml_string = file.read()

    # Convert XML string to a DOM object
    dom = xml.dom.minidom.parseString(xml_string)

    # Create list of all <span> tags to remove
    spans_to_remove = [span for span in dom.getElementsByTagName('span') if not span.firstChild]

    # Iterate through the list of <span> tags to remove and remove them
    for span in spans_to_remove:
        span.parentNode.removeChild(span)

    # Save XML file with an indentation of 4 characters
    pretty_xml = dom.toprettyxml(indent="    ", encoding='UTF-8')

    with open(new_file_path, 'wb') as file:
        file.write(pretty_xml)

# Call the function
format_xml_minidom('GAEB-XML_examples/example.X83', 'new_GAEB_file.X83')
