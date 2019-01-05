import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep


def scrape_quotes():
	main_url = "http://quotes.toscrape.com/"
	page_url = "/page/1"
	quote_dicts = []
	while page_url:
		response = requests.get(f"{main_url}{page_url}")
		print(f"Currently scraping {main_url}{page_url}...")
		soup = BeautifulSoup(response.text, "html.parser")
		quotes = soup.find_all(class_="quote")
		for quote in quotes:
			quote_dicts.append({
				"text": quote.find(class_="text").get_text(),
				"author": quote.find(class_="author").get_text(),
				"link": quote.find("a")['href']
			})
		next_page = soup.find(class_="next")
		page_url = next_page.find("a")["href"] if next_page else None
		sleep(1)
	return quote_dicts


def write_quotes(quotes):
	with open("quote_data.csv", "w") as file:
		headers = ["text", "author", "link"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for quote in quotes:
			csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)
