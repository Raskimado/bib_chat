import json

#import document
with open('books_physical.json', 'r') as file:
    records = json.load(file)

# help funkction, find subfiled with corresponding key
def find_subfield(field, key):
    if not field:
        return ""
    for subfield in field[0].get("sub", []):
        if key in subfield:
            return subfield[key]
    return ""

# Create new text file base on the context of the import
def adapt_text():
    titles = ""
    for record in records:
        #create variables
        MMS_ID = record.get('001')
        ISBN = find_subfield(record.get('020'),'a')
        author = find_subfield(record.get("100"), "a")
        title = find_subfield(record.get('245'),'a')
        subtitle = find_subfield(record.get('245'),'b')
        responsible = find_subfield(record.get("245"),"c")
        content = find_subfield(record.get("500"), "a") # How to add subfield 4 = aut?
        keyword = find_subfield(record.get('650'),'a')
        co_author = find_subfield(record.get("700"), "a")

        #write to variable
        titles += (f"Die MMS-ID des Titels {title}, {subtitle} lautet {MMS_ID}.\n")
        titles += (f"Die ISBN des Titles {title}, {subtitle} lautet {ISBN}.\n")
        titles += (f"Der Titels {title}, {subtitle} wurde von {author} verfasst.\n")
        titles += (f"Die inhaltliche Verantwortung des Titels {title} liegt " \
                    f"bei {responsible}.\n")
        titles += (f"Der Titel {title} befasst sich mit den Themenbereichen " \
                    f"{keyword}.\n")
        titles += (f"{content}\n\n")
    # print(type(titles))
    # print(titles)
    return titles