import asyncio
import httpx
from bs4 import BeautifulSoup
import re

urls = ["http://books.tosefscrape.com/catalogue/page-2.html",
        "http://books.toscrape.com/catalogue/page-2.html",
        "http://books.toscrape.com/catalogue/page-3.html",
        "http://books.toscrape.com/catalogue/page-4.html"]


async def get_urls(soups):
    urls = set()
    for soup in soups:
        for link in soup.find_all('a', {'href' : re.compile("(?:http)")}):
            urls.add(link.get('href'))
    return list(urls)

async def fetch():
    async with httpx.AsyncClient() as client:
        tasks = []
        # for url in urls:
        #     try:
        #         tasks.append(client.get(url))
        #     except:
        #         print("error con url: ",url)
        tasks = (client.get(url) for url in urls)
        print(type(tasks))
        try:
            reqs = await asyncio.gather(*tasks)
        except:
            print("Error!")
    
    
    soups = [BeautifulSoup(req, 'html.parser') for req in reqs]
    
    

    print("Finished")
    
    print("Finished")
    
    
    
    
    
    
if __name__ == "__main__":
    asyncio.run(fetch())