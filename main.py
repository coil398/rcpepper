import crawler



def main(url):
    page = crawler.main(url)
    print(page)
    

if __name__ == '__main__':
    URL = 'http://nao:nao@atelier34.local'
    main(URL)
