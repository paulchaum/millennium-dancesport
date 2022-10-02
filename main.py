# pip install requests lxml
import requests
from lxml import html, etree

response = requests.get('http://www.comp-mngr.com/millennium2022/Millennium2022_HeatLists.htm')

tree = html.fromstring(response.text, parser=etree.HTMLParser(encoding='utf-8'))

tables = tree.xpath('//*[contains(@id, "TABLE_CODE_")]')

entries = []
for table in tables:
    title = next(iter(table.xpath('.//strong[contains(text(), "Entries for ")]//text()')), '')
    sub_tables = table.xpath('.//table')
    for sub_table in sub_tables:
        sub_title = next(iter(sub_table.getprevious().xpath(".//text()")), '')
        for tr in sub_table.xpath('.//tr')[1:]:
            session_cell, number_cell, heat_cell, event_cell = iter(tr.xpath('.//td'))
            entries.append({
                "person": title,
                "sub_person": sub_title,
                "session": ' '.join(session_cell.itertext()),
                "number_cell": ' '.join(number_cell.itertext()),
                "heat_cell": ' '.join(heat_cell.itertext()),
                "event_cell": ' '.join(event_cell.itertext()),
            })