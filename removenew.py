#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os
import hashlib
import sys
import datetime

# Variables to keep track of progress
fileschecked = 0
issues = 0
xmlerrors = 0
fileschanged = 0


# Calculate md5 hash to check for changes in file.
def md5_for_file(f, block_size=2 ** 20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()


# Nicely indents the XML output
def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



# Loop over all files and  create new data
for filename in glob.glob("systems*/*.xml"):
    fileschecked += 1

    # Open file
    f = open(filename, 'rt')

    # Try to parse file
    try:
        root = ET.parse(f).getroot()
        planets = root.findall(".//planet")
    except ET.ParseError as error:
        print '{}, {}'.format(filename, error)
        xmlerrors += 1
        issues += 1
        continue
    finally:
        f.close()

    for planet in planets:
        newtags = planet.findall(".//new")
	for newtag in newtags:
		planet.remove(newtag)

    # Cleanup XML
    indent(root)

    # Write XML to file.
    ET.ElementTree(root).write(filename, encoding="UTF-8", xml_declaration=False)


