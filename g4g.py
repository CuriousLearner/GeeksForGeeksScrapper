import requests
import subprocess
from bs4 import BeautifulSoup
from os import system


BASE_URL = 'http://www.geeksforgeeks.org/'

categoryUrl = raw_input("Enter category url: ")
soup = BeautifulSoup(requests.get(BASE_URL + categoryUrl).text)

articles = []

def print_articles_to_pdf():
    print("All links scraped, extracting articles")
    allArticles = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
    allArticles += '<br><br><br><br>'.join(articles)
    Html_file= open("temp.html","w")
    Html_file.write(allArticles)
    Html_file.close()
    print("Generating PDF GeeksForGeeks_" + categoryUrl)
    html_to_pdf_command = 'wkhtmltopdf temp.html GeeksForGeeks_' + categoryUrl + '.pdf'
    system(html_to_pdf_command)
    

# Selecting links which are in the category page
links = [a.attrs.get('href') for a in soup.select('article li a')]
# Removing links for the categories with anchor on same page
links = [link for link in links if not link.startswith('#')]

print("Found: " + str(len(links)) + " links")
i = 1

for link in links:
    try:
        print("Scraping link no: " + str(i) + " Link: " + link )
        link_soup = BeautifulSoup(requests.get(link).text)
        article = link_soup.find('article')
        articles.append(article.encode('UTF-8'))
        i = i + 1
    except KeyboardInterrupt:
        break


print_articles_to_pdf()
