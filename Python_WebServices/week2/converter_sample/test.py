from decimal import Decimal

import requests

from Python_WebServices.week2.converter_sample.currency import convert
import Python_WebServices.week2.converter_sample.cur_prepod as cur2

correct = Decimal('3754.8057')
data = "17/02/2005"
# req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+data)
# req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
# result1 = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
result1 = convert(Decimal("1000"), 'EUR', 'USD', None, requests)
result2 = cur2.convert(Decimal("1000"), 'EUR', 'USD', None, requests)

print(result1)
print(result2)

if result1 == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result1, correct))
