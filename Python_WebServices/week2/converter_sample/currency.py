from decimal import Decimal
from bs4 import BeautifulSoup


def convert(amount, cur_from, cur_to, date, requests):
    params = {"date_req": date}
    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", params=params)

    soap = BeautifulSoup(response.content, 'xml')
    if cur_from != "RUR":
        from_cur_value = soap.find('CharCode', text=cur_from).find_next_sibling("Value").string
        from_cur_dec_value = Decimal(from_cur_value.replace(',', '.'))
        from_cur_nominal = int(soap.find('CharCode', text=cur_from).find_next_sibling("Nominal").string)
        amount = amount * from_cur_dec_value / from_cur_nominal

    to_cur_value = soap.find('CharCode', text=cur_to).find_next_sibling("Value").string
    to_cur_nominal = int(soap.find('CharCode', text=cur_to).find_next_sibling("Nominal").string)
    to_cur_dec_value = Decimal(to_cur_value.replace(',', '.'))
    result = (amount * to_cur_nominal / to_cur_dec_value).quantize(Decimal('.0001'))

    return result