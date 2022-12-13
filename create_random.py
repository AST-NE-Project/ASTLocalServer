import uuid

act = str(uuid.uuid4())

with open('tokens/' + act, 'w') as f:
    f.write('ok')
print (act)
