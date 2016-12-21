from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
from datetime import datetime
import time


class createBrowser:
    logs = list()
    _baseDir = './screenshots/'

    def createPicPath(self, num):
        return self._baseDir + 'pic-' + str(num) + '.jpg'

    def getNumOfFiles(self):
        i = 0
        while True:
            path = self.createPicPath(i)
            print('path: ' + path)
            if os.path.exists(path):
                i = i + 1
            else:
                return i

    def setNumOfPics(self):
        self.numOfPics = self.getNumOfFiles()
        print('numOfPics: ' + str(self.numOfPics))

    def __init__(self, url):
        self.setNumOfPics()
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(10)
        print('getting page data with the url: ' + url)
        self.driver.get(url)
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, 'header')))
        except Exception as e:
            print(e)
        finally:
            print(element)

        self.logs.append(datetime.now().strftime(
            '%Y/%m/%d %H:%M:%S') + ' : ' + 'got page data with the url: ' + url)
        print('done...')

    def getPageData(self):
        return self.driver.page_source.encode('utf-8')

    def takeScreenshot(self):
        path = self.createPicPath(self.numOfPics)
        print('path' + path)
        self.driver.save_screenshot(path)
        self.logs.append(
            datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' : ' + 'saved a screenshot with the path: ' + path)
        self.numOfPics = self.numOfPics + 1
        return 'succeeded in taking a screenshot'

    def saveLog(self):
        print('saving the logs...')
        with open('crawler.log', mode='a', encoding='utf-8') as f:
            f.write('\n')
            for log in self.logs:
                print(log)
                f.write(log + '\n')
        print('done...')

    def quit(self):
        self.driver.quit()
        print('quitted crawling')


def createDirIfNotExists():
    if os.path.exists('./screenshots'):
        pass
    else:
        os.makedirs('./screenshots')
    return


def readURLs():
    browsers = list()
    with open('./url.list', 'r') as f:
        for line in f:
            browsers.append(line)
    return browsers


def getLinesOfFile():
    return sum(1 for line in open('./url.list'))


def checkExistenceOfValidFile():
    if os.path.exists('./url.list'):
        if getLinesOfFile() > 0:
            return True
        else:
            return False
    else:
        return False


def useBrowser(url, waitFor=10):
    result = [0, 0]
    browser = createBrowser(url)
    result[0] = browser.getPageData()
    time.sleep(waitFor)
    result[1] = browser.takeScreenshot()
    browser.saveLog()
    browser.quit()
    return result


def useBrowsers():
    results = list()
    urls = readURLs()
    for url in urls:
        results.append(useBrowser(url))
    return results


def main(arg=None):
    results = 0
    createDirIfNotExists()
    if arg is None:
        if checkExistenceOfValidFile():
            results = useBrowsers()
        else:
            print('A Valid File For URLS Is In Need.')
    else:
        url = arg
        results = useBrowser(url)
    return results


if __name__ == '__main__':
    argument = []
    if len(sys.argv) > 1:
        argument[0] = sys.argv[0]
    main(argument)
