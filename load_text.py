"""This module is responsible for the cleaning and normalisation of the
bibliographic data from the library. It creates a data basis that can be used
in the RAG process.

Functions:
- load_json(): Loads all JSON files from a directory.
- find_subfield(field, key): Finds the relevants subfields.
- find_subfield(field, key): Combines subfields when necessary.
- clean_code(text): Removes unwanted characters.
- adapt_text(records): Returns revised data basis for RAG processing.

Exceptions:
- JSONDecodeError: Raised if JSON files cannot be loaded.
"""

__file__ = "load_text.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

import json
from pathlib import Path


def load_json():
    """Open all JSON files in the directory and retrun the content as a list."""
    directory_path = Path("./Bibliotheksdaten")
    json_files = list(directory_path.glob("*.json"))

    results = []
    for path in json_files:
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)
            except json.JSONDecodeError as e:
                print(f"Fehler beim Laden von {path}: {e}")
                exit(1)
    return results


def find_subfield(field, key):
    """Find the subfield with corresponding key and return its content.

    Keyword arguments:
    field -- hands over the MARC field
    key -- hands over the key from the MARC field
    """
    if not field:
        return ""
    subfields = []
    # Iterate over all positions in field
    for position in field:
        # return key-subfields from position sub
        for subfield in position.get("sub", []):
            if key in subfield:
                subfields.append(subfield[key])
    return subfields


def list_to_string(subfield):
    """
    Keyword arguments:
    list -- 
    """
    # Converts elements into string and returns them comma separated
    if subfield:
        string = ', '.join(str(x) for x in subfield)
        return string
    else:
        return ""


def clean_code(text):
    """Remove all unwanted characters and return the result.
    
    Keyword arguments:
    text - hands over the data basis afer it is normalised.
    """
    text = text.translate(str.maketrans('', '', '<<>>()[]+'))
    text = text.lower()
    return text


def find_material_type(leader, field_008):
    """Return the correct material typ.
    
    Keyword arguments:
    leader -- hands over the content of the MARC field
    field_008 -- hands over the content of the MARC field
    """
    l_position_7 = leader[7]
    f8_position_23 = field_008[23]
    
    if l_position_7 == 'm':
        if f8_position_23 in ['s', 'o', 'q']:
            return "Das E-Book"
        else:
            return "Das Buch"
    elif l_position_7 == 's':
        if f8_position_23 in ['s', 'o', 'q']:
            return "Das E-Journal"
        else:
            return "Die Zeitschrift"
    else:
        return "Das Medium"


def adapt_text(records):
    """After cleaning and normalising the data return the new data basis.

    Keyword arguments:
    records -- hands over the orginal content form the JSON files.

    Help functions:
    - find_subfield: Finds corresponding subfield.
    - list_to_string: Combines the content when a subfield occurs multiple times.
    - clean_code: Removes unwanted characters.
    """
    titles = []
    for record in records:
        t = ""

        leader = record.get('leader')
        MMS_ID = record.get('001')
        field_008 = record.get('008')
        ISBN = find_subfield(record.get('020'),'a')
        ISBN = list_to_string(ISBN)
        author = find_subfield(record.get("100"), "a")
        author = list_to_string(author)
        title = find_subfield(record.get('245'),'a')
        title = list_to_string(title)
        subtitle = find_subfield(record.get('245'),'b')
        subtitle = list_to_string(subtitle)
        if subtitle:
            subtitle = f", {subtitle}"
        else:
            subtitle = ""
        responsible = find_subfield(record.get("245"),"c")
        responsible = list_to_string(responsible)
        content = find_subfield(record.get("520"), "a")
        content = list_to_string(content)
        keyword = find_subfield(record.get('650'),'a')
        keyword = list_to_string(keyword)
        co_author = find_subfield(record.get("700"), "a")
        co_author = list_to_string(co_author)

        material_type = find_material_type(leader, field_008)

        # Write variables to text
        t += (f"{material_type} mit dem Titel {title}{subtitle} hat die MMS_ID "
              f"{MMS_ID}.")
        if ISBN:
            t += (f" Der Titel {title}{subtitle} hat die ISBN {ISBN}.")
        if author:
            t += (f" Der Titel {title}{subtitle} wurde von {author} verfasst.")
        if responsible:
            t += (f" Die inhaltliche Verantwortung des {title}{subtitle} liegt "
                  f"bei {responsible}.")
        if keyword:
            t += (f" Der Fokus des Titels {title}{subtitle} liegt auf den "
                  f"Themenbereichen {keyword}.")
        if content:
            t += (f" Der Inhaltstext des Titels {title}{subtitle} lautet: "
                  f"{content}")
        t = clean_code(t)
        titles.append(t)
    return titles


# Save data in file
results = load_json()
text = adapt_text(results)
# print(text)

with open("ausgabe.txt", "w", encoding="utf-8") as f:
    f.write(", ".join(str(element) for element in text))