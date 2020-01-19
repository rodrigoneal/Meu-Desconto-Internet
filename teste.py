import DB
data = []
db = DB.select('queda')
for i in db:
    data.append(str(i)[2:12])
print(data)