from bs4 import BeautifulSoup
import requests
import pandas as pd


book_base_url = 'https://books.toscrape.com/catalogue/'

base_url = 'https://books.toscrape.com/catalogue/page-{}.html'


def change_to_number(str_value):
            values = {
                'One':1,
                'Two':2,
                'Three':3,
                'Four':4,
                'Five':5
            }
            value = values[str_value]
            return value

def get_category(link):
       response = requests.get(link)
       soup = BeautifulSoup(response.content, 'html.parser')
       breadcrumbs = soup.find('ul', class_='breadcrumb')
       categories = breadcrumbs.find_all('li')
       category = categories[2].text.strip()
       return category


books = []

def book_scraper(soup, page):
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a["title"]
        price = book.find('p',class_='price_color').text
        availability = book.find('p',class_='instock availability').text.strip()
        rating_text = book.p['class'][1]
        rating = change_to_number(rating_text)
        link = book_base_url + book.h3.a['href']
        category = get_category(link)


        book = {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Category': category,
            'Link': link
            

        }

        books.append(book)



for page in range(1,11):
      url = base_url.format(page)
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      book_scraper(soup, page)


df = pd.DataFrame(books)

df['Price'] = df['Price'].str.replace("£", "").astype(float)

df.to_csv('books_data.csv') 