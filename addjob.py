from bs4 import BeautifulSoup
from job import Job
from urllib.request import Request, urlopen



URL = "https://www.enchantedlearning.com/wordlist/jobs.shtml"
req = Request(URL , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, "html.parser")
results = soup.find_all("div", class_="wordlist-item")
print(results)
jobdb=Job()
for link in results:
  jobdb.create({"name":link.get_text()})
  
