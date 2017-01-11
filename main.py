import crawler
from bs4 import BeautifulSoup


class scraping:

    def __init__(self, page, settings):
        self.settings = settings
        self.soup = BeautifulSoup(page, 'lxml')

    def setStatus(self):
        print(self.soup.find('div', class_='table_myrobot_left').find(
            'div', class_='basictext'))
        self.settings['volume'] = self.soup.find('div', class_='table_myrobot_left').find(
            'div', class_='basictext').find('div', class_='volume_text').text
        self.settings['battery'] = self.soup.find(
            'div', class_='table_myrobot_right').find('div', class_='basictext').text

    def displaySettings(self):
        print(self.settings)


def actions(driver, url):
    pages = list()
    driver.find_element_by_css_selector("#menu-network > img").click()
    pages.append(driver.page_source)
    driver.find_element_by_css_selector("#menu-apps > img").click()
    pages.append(driver.page_source)


def main(url, settings):
    page = crawler.main(url, actions)[0]
    # with open('./html.txt', 'r') as f:
    #    page = f.read()

    scraper = scraping(page, settings)
    scraper.setStatus()
    scraper.displaySettings()


if __name__ == '__main__':
    URL = 'http://nao:nao@atelier40.local'
    settings = {
        'volume': None,
        'battery': None,
        'network': None,
        'updated': None
    }
    main(URL, settings)
