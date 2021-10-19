from json import load

with open('jsonKeys.json', 'rb') as fp:
    KEYS = load(fp)
KEYS_OFTEN_USED = {
'доллар': 'USD',
'евро': 'EUR',
'рубль': 'RUB',
}
