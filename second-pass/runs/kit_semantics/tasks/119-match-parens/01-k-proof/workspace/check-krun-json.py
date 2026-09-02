import json
import sys


document = json.load(sys.stdin)
top = document['term']
cells = {
    argument['label']['name']: argument['args'][0]
    for argument in top['args']
    if argument.get('node') == 'KApply'
}

assert cells['<k>']['node'] == 'KSequence'
assert cells['<k>']['arity'] == 0
assert cells['<exc>']['label']['name'].startswith('NoExc')
assert cells['<exit-code>']['token'] == '0'
print('krun-json: .K, NoExc, exit-code 0')
