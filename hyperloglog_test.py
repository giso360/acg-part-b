from datasketch import HyperLogLog

data = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]

data = ['maria', 
        'george', 
        'WhiteHouse', 
        'whitehouse',
        'maria']

hll = HyperLogLog()
for element in data:
    hll.update(str(element).encode('utf8'))

print(f'estimate: {hll.count()}')
print(f'real: {len(set(data))}')
print(hll._get_alpha(8))