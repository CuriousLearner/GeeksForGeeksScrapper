#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from os import system
from sys import exit
from time import sleep
from requests.exceptions import ConnectionError
from article import Article

BASE_URL = 'http://www.geeksforgeeks.org/'
articles = []

choice_to_category = {1: 'c', 2: 'c-plus-plus', 3: 'java', 4: 'python',
                      5: 'fundamentals-of-algorithms',
                      6: 'data-structures'}


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
        categoryUrl = choice_to_category[choice]
    except KeyError:
        print("Wrong Choice Entered. Exiting!")
        exit(1)
    return categoryUrl


def save_articles_as_html_and_pdf():
    print("All links scraped, extracting articles")
    # Formatting the html for articles
    allArticles = ('<!DOCTYPE html>'
                    '<html><head>'
                    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
                    '<link rel="stylesheet" href="style.min.css" type="text/css" media="all" />'
                    '<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>'
                    '</head><body>'
                    )
    allArticles += '<h1 style="text-align:center;font-size:40px">' + categoryUrl.title() + ' Archive</h1><hr>'
    allArticles += '<h1 style="padding-left:5%;font-size:200%;"> Index</h1><Br/>'
    for x in range(len(articles)):
        allArticles += '<a href =\"#' + str(x+1) + '\">' + '<h1 style="padding-left:5%;font-size:20px;">' + str(x+1) + ".\t\t"+articles[x].title + '</h1></a> <br/>'
    for x in range(len(articles)):
        allArticles += '<hr id=\"' + str(x+1) +'\">' + articles[x].content.decode("utf-8")
    allArticles += '''
                    </body></html>
                   '''
    html_file_name = 'G4G_' + categoryUrl.title() + '.html'
    Html_file = open(html_file_name, "w")
    Html_file.write(allArticles.encode("utf-8"))
    Html_file.close()
    pdf_file_name = 'G4G_' + categoryUrl.title() + '.pdf'
    print("Generating PDF " + pdf_file_name)
    html_to_pdf_command = 'wkhtmltopdf ' + html_file_name + ' ' + pdf_file_name
    system(html_to_pdf_command)


def scrape_category(categoryUrl):
    try:
        soup = BeautifulSoup(requests.get(BASE_URL + categoryUrl).text)
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
            if(i % 10 == 0):
                sleep(5)  # Sleep for 5 seconds before scraping every 10th link
            link = link.strip()
            print("Scraping link no: " + str(i) + " Link: " + link)
            i = i + 1
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
    categoryUrl = get_category_choice()
    scrape_category(categoryUrl)
    save_articles_as_html_and_pdf()
