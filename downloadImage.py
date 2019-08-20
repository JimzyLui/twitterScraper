import urllib.request
import os
import sys


def downloadImages(strQueryString, arrUrls):
    for url in arrUrls:
        downloadImage(strQueryString, url)


def downloadImage(strQueryString, url):
    try:
        strPath = setup(strQueryString)
        print(f"Downloading {url} to {strQueryString}")
        image_name = str(url).split('/')[-1]
        download_jpg(url, strPath, image_name)
    except Exception as error:
        print(error)


def download_jpg(url, filePath, fileName):
    fullPath = f"{filePath}/{fileName}"
    urllib.request.urlretrieve(url, fullPath)


def setup(strQueryString):
    dirName = 'images_' + strQueryString.replace(' ', '_')
    strPath = f"{dirName}"
    try:
        os.mkdir(strPath)
    except:
        pass
    return strPath
