import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def get_url_list():
    conn = sqlite3.connect('sqlite_db.db').cursor()
    quert = f'''SELECT URL FROM TheVerge'''
    conn.execute(quert)
    ls = conn.fetchall()
    new_db = []
    for item in ls:
        new_db.append(item[0])
    conn.close()
    return new_db



conn = sqlite3.connect('sqlite_db.db')
current_db = get_url_list()
# print(current_db)
t1 = time.time()
for i in range(1,16):
    URL ='https://www.theverge.com/archives/' + str(i) + '/'
    r = requests.get(URL)

    Soup = BeautifulSoup(r.text, 'lxml')
    
    for tags in Soup.find_all('div', attrs={'class':'c-entry-box--compact__body'}):

        try:
            heading = (str(tags.find('h2').text)).strip()
            url = (str(tags.find('a')['href'])).strip()
            if url in current_db:
                continue

            try:
                author = (str(tags.find('span').span.a.text)).strip()
            except:
                author =  (tags.find('div').span.span.text.replace("\n","")).strip()
            try:
                date = (str(tags.span.time['datetime'][0:10])).strip()
            except:
                date = (str(tags.find('div').span.time['datetime'][0:10])).strip()
        except Exception as e:
            print(e)
        
        lst = [url,heading,author,date]
        lst = str(lst).replace("[","").replace("]","")
        quert = f'''INSERT INTO TheVerge (URL,Headline,Author,Date) VALUES ({lst})'''
        conn.execute(quert)
        conn.commit()
        print("Added")
        

conn.close()
t2 = time.time()
print(t2-t1)


