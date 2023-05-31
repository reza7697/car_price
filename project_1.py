from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from sklearn import tree
from sklearn import preprocessing
from collections import OrderedDict

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=""
)

#At the firs you should give a name for your 'database':
db_name = input("Please enter a name for your database: ")

mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE {}" .format(db_name))
except:
    print("This database exist.")


cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database=db_name)

cursor = cnx.cursor()
# table_name = 'vehicle'
#You should give the program a name for your 'table':
table_name = input("Please enter your table name: ")
try:
    cursor.execute("CREATE TABLE {} (name VARCHAR(40), model int(11), mileage int(11), price int(11))".format(table_name))
except:
    print("This table exist.")

for page in range(1,3):
    r = requests.get('https://www.cars.com/shopping/results/?page=%i&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=all&mileage_max=&sort=best_match_desc&stock_type=used&year_max=&year_min=&zip=' % (page))
    soup = BeautifulSoup(r.text, 'html.parser')

    val = soup.find_all('div', attrs = {'class' : 'vehicle-details'})

    for i in range(0,len(val)):
        name = val[i].find(attrs = {'class' : 'title'})
        price = val[i].find(attrs = {'class' : 'primary-price'})
        mileage = val[i].find(attrs = {'class' : 'mileage'})
        n = re.findall(r'(>.*<)', str(name))
        mo = re.findall(r'(\d{4})', str(name))
        p = re.findall(r'(\d)', str(price))
        m = re.findall(r'(\d)', str(mileage))
        gheymat = ''
        karkard = ''
        esm1 = n[0].split()
        for i in range(0, len(p)):
            gheymat += p[i]
        gheymat = int(gheymat)
        for j in range(0, len(m)):
            karkard += m[j]
        karkard = int(karkard)
        esm = ''
        model = ''
        esm += esm1[1]
        model += mo[0]
        model = int(model)   
        cursor.execute('INSERT INTO %s VALUES (\'%s\', %i, %i, %i)' % (table_name, esm, model, karkard, gheymat))

query = ('SELECT * FROM {};' .format(table_name))
cursor.execute(query)

x = []
z = []
y = []
X_data = []
for line in cursor:
    z.append(line[0])
    x.append(line[1:3])
    y.append(line[3])

cnx.commit()

cnx.close()

le = preprocessing.LabelEncoder()
le.fit(z)
t = list(le.transform(z))
#X_data = list(zip(le.transform(z),x))
for i in range(0, len(t)):
    l = []
    l.append(t[i])
    l.append(x[i][0])
    l.append(x[i][1])
    X_data.append(l)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_data, y)

od = OrderedDict()

for i in range(0, len(t)):
    od[z[i]] = t[i]

#You should enter a "car name","the mileage" and "car model":
esme_mashin = input('enter car name: ')   #for example: Honda, Ford,...
karkard_mashin = int(input('enter the mileage: '))
model_mashin = int(input('enter model: ')) #for example: 2018, 2011,...
#car_name = le.transform(esme_mashin)
ans = clf.predict([[od[esme_mashin],model_mashin,karkard_mashin]])

#At the end, program give you the approximate price of car:
print('Your car price is {}$'.format(ans[0]))
