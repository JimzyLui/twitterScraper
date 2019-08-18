#!/usr/local/bin/python3

import argparse
import requests
from bs4 import BeautifulSoup
import sys
import moment
from datetime import datetime
import re
# import downloadUrlImage


def searchForTwitterImages_interactive(strIgnore=''):
    print(f"Interactive mode enabled.{strIgnore}\r\n")

    strQueryString = input('Please enter Twitter search terms:  ')
    arrSearchTerms = strQueryString.split()
    searchForTwitterImages(arrSearchTerms)


def searchForTwitterImages(arrSearchTerms):
    url = 'https://twitter.com/search'
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

    strQueryString = ' '.join(arrSearchTerms)
    if len(arrSearchTerms) == 0:
        print(f"No search terms entered.  Exiting program.\r\n")
        return
    print(f"Searching on: {strQueryString}...\r\n")

    response = requests.get(url, params={'q': strQueryString}, headers={
                            'user-agent': userAgent})
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    arrImages = []
    for img in soup.select('div.AdaptiveMedia-photoContainer img'):
        if img:
            arrImages.append(img['src'])

    iResults = len(arrImages)
    if iResults > 0:
        fileName = print_image_urls(strQueryString, arrImages)
        print(f"{len(arrImages)} results found and written to {fileName}\r\n")
    else:
        print(f"No results found.")


def print_image_urls(searchTerms, listUrls):
    try:
        fileName = generateFileName(searchTerms)
        strTimestamp = moment.now().format('YYYYMMDD HH:mm')
        with open(fileName, 'a') as f:
            f.write(
                f"[{strTimestamp}] {len(listUrls)} results for Twitter search on: {searchTerms}\r\n")
            for url in listUrls:
                f.write(f"  {url}\r\n")
            f.write(f"\r\n")
    except IOError as e:
        print(f"IO Error: \r\n{e}")
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")
        raise
    finally:
        return fileName


def generateFileName(strSearchTerms):
    strYYYYMMDD = moment.now().format('YYYYMMDD')
    strSearch = strSearchTerms.replace(' ', '_')
    fileName = f"{strYYYYMMDD}.search.{strSearch}.txt"
    return fileName


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get profile image URLs from Twitter.')
    parser.add_argument('-i', '--interactive',
                        dest='i',
                        action='store_true',
                        help='makes this program interactive where it will prompt the user for input')
    parser.add_argument('-s', '--search_terms',
                        dest='search',
                        nargs='+',
                        help='search terms upon which to query twitter')
    parser.add_argument('searchDefault', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.i:
        strIgnore = ''
        if args.search and len(args.search) > 0:
            strIgnore = ' Ignoring command line search criteria.'
        searchForTwitterImages_interactive(strIgnore)
    else:
        print(f"Search terms: {args}")
        if args.search:
            searchForTwitterImages(args.search)
        elif args.searchDefault:
            searchForTwitterImages(args.searchDefault)
        else:
            print(f"No search terms given.  Switching to interactive mode.")
            searchForTwitterImages_interactive()
