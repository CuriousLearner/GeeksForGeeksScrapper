#!/usr/bin/python

import requests

from os import system
from sys import exit
from time import sleep
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup

from article import Article


BASE_URL = 'http://www.geeksforgeeks.org/'
articles = []

CHOICE_TO_CATEGORY_MAPPING = {
    1: 'c',
    2: 'c-plus-plus',
    3: 'java',
    4: 'python',
    5: 'fundamentals-of-algorithms',
    6: 'data-structures'
}


def display_menu():
    print("Choose category to scrape: ")
    print("1. C Language")
    print("2. C++ Language")
    print("3. Java")
    print("4. Python")
    print("5. Algorithms")
    print("6. Data Structures")


def get_category_choice():
    choice = int(raw_input("Enter choice: "))
    try:
        category_url = CHOICE_TO_CATEGORY_MAPPING[choice]
    except KeyError:
        print("Wrong Choice Entered. Exiting!")
        exit(1)
    return category_url


def save_articles_as_html_and_pdf():
    print("All links scraped, extracting articles")
    # Formatting the html for articles
    all_articles = (
        '<!DOCTYPE html>'
        '<html><head>'
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
        '<link rel="stylesheet" href="style.min.css" type="text/css" media="all" />'
        '<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>'
        '</head><body>'
    )

    all_articles += '<h1 style="text-align:center;font-size:40px">' + \
                    category_url.title() + ' Archive</h1><hr>'
    all_articles += '<h1 style="padding-left:5%;font-size:200%;">Index</h1><br/>'

    for x in range(len(articles)):
        all_articles += '<a href =\"#' + str(x+1) + '\">' + \
                        '<h1 style="padding-left:5%;font-size:20px;">' + \
                        str(x+1) + ".\t\t"+articles[x].title + '</h1></a> <br/>'
    for x in range(len(articles)):
        all_articles += '<hr id=\"' + str(x+1) +'\">' + articles[x].content.decode("utf-8")

    all_articles += '''</body></html>'''
    html_file_name = 'G4G_' + category_url.title() + '.html'
    html_file = open(html_file_name, "w")
    html_file.write(all_articles.encode("utf-8"))
    html_file.close()

    pdf_file_name = 'G4G_' + category_url.title() + '.pdf'
    print("Generating PDF " + pdf_file_name)
    html_to_pdf_command = 'wkhtmltopdf ' + html_file_name + ' ' + pdf_file_name
    system(html_to_pdf_command)


def scrape_category(category_url):
    try:
        soup = BeautifulSoup(requests.get(BASE_URL + category_url).text)
    except ConnectionError:
        print("Couldn't connect to Internet! Please check your connection & Try again.")
        exit(1)

    # Selecting links which are in the category page
    links = [a.attrs.get('href') for a in soup.select('article li a')]
    # Removing links for the categories with anchor on same page
    links = [link for link in links if not link.startswith('#')]

    print("Found: " + str(len(links)) + " links")
    i = 1

    # Traverse each link to find article and save it.
    for link in links:
        try:
            if i % 10 == 0:
                sleep(5)  # Sleep for 5 seconds before scraping every 10th link
            link = link.strip()
            print("Scraping link no: " + str(i) + " Link: " + link)
            i += 1
            link_soup = BeautifulSoup(requests.get(link).text)
            # Remove the space occupied by Google Ads (Drop script & ins node)
            [script.extract() for script in link_soup(["script", "ins"])]
            for code_tag in link_soup.find_all('pre'):
                code_tag['class'] = code_tag.get('class', []) + ['prettyprint']
            article = link_soup.find('article')
            # Now add this article to list of all articles
            page = Article(title=link_soup.title.string, content=article.encode('UTF-8'))
            articles.append(page)
        # Sometimes hanging. So Ctrl ^ C, and try the next link.
        # Find out the reason & improve this.
        except KeyboardInterrupt:
            continue
        except ConnectionError:
            print("Internet disconnected! Please check your connection & Try again.")
            if articles:
                print("Making PDF of links scraped till now.")
                break
            else:
                exit(1)


if __name__ == '__main__':
    display_menu()
    category_url = get_category_choice()
    scrape_category(category_url)
    save_articles_as_html_and_pdf()
