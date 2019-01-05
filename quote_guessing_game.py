import requests
from bs4 import BeautifulSoup
from csv import DictReader
from random import choice
from time import sleep

main_url = "http://quotes.toscrape.com/"


def read_quotes(filename):
	with open(filename, "r") as file:
		csv_reader = DictReader(file)
		quotes = list(csv_reader)
	return quotes


def replay():
	return input('Would you like to play again? Yes or No: ').lower().startswith('y')


def win(guess, answer):
	return guess.lower() == answer.lower()


def play(quotes):
	while True:
		quote = choice(quotes)
		print(quote["text"])
		guess = ""
		answer = quote["author"]
		guesses_remaining = 4

		while not win(guess, answer) and guesses_remaining >= 0:
			guess = input(f"Who said this? You have {guesses_remaining} guesses.\n")
			guesses_remaining -= 1
			if win(guess, answer):
				print("Congratulations! You are correct.")
				break
			elif guesses_remaining == 3:
				res = requests.get(f"{main_url}{quote['link']}")
				soup = BeautifulSoup(res.text, "html.parser")
				date = soup.find(class_="author-born-date").get_text()
				place = soup.find(class_="author-born-location").get_text()
				print(f"Here is a clue:\nThey were born on {date} {place}.")
			elif guesses_remaining == 2:
				first_initial = quote["author"][0]
				print(f"Here is a clue:\nTheir first name starts with {first_initial}.")
			elif guesses_remaining == 1:
				last_initial = quote["author"].split()[1][0]
				print(f"Here is a clue:\nTheir last name starts with {last_initial}.")
			else:
				print(f"You are out of guesses.\nThe answer was: {quote['author']}")
				break

		if not replay():
			print("Goodbye!")
			break


quotes = read_quotes("quote_data.csv")
play(quotes)
