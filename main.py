import re
from pprint import pprint
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

header = contacts_list.pop(0)

# 'name': {'lastname': ..., 'firstname': ..., 'surname': ..., 'organization': ..., 'position': ..., 'phone': ...,
# 'email': ...}
address_book = {}

pattern = r'[А-ЯЁ][\w]+[,\s]+[А-ЯЁ][\w]+[,\s]*[А-ЯЁ]*[\w]*'
pattern_for_phone = r'(\+)?([7,8])\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})'
replace_phone = r'\2(\3)\4-\5-\6'
pattern_for_additional_phone = r'\(*(доб.) (\d+)\)*'
replace_additional_phone = r'\1\2.'
for key, value in enumerate(contacts_list):
    name = value[0] + ' ' + value[1] + ' ' + value[2]
    phone = value[5]
    result1 = re.sub(pattern_for_phone, replace_phone, phone)
    result1 = re.sub(pattern_for_additional_phone, replace_additional_phone, result1)
    result = re.match(pattern, name)
    if len(result.group().strip().split()) == 3:
        lastname, firstname, surname = result.group().strip().split()
        address_book[result.group().strip()] = {'lastname': lastname, 'firstname': firstname, 'surname': surname,
                                                'organization': value[3], 'position': value[4], 'phone': result1,
                                                'email': value[6]}

with open("phonebook.csv", "w", newline='', encoding='UTF-8') as f:
    fields_name = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    writer = csv.DictWriter(f, fields_name)
    writer.writeheader()
    for value in address_book.values():
        writer.writerow(value)

# pprint(address_book)
