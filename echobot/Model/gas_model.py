

import ssl
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as BS


class Fuel_price():
	url = 'http://www.taiwanoil.org'
	f = None
	fuels_types = None
	typeToPric = None
	soup = None
	fuels_pric = None

	def __init__(self):
		ssl._create_default_https_context = ssl._create_unverified_context
		self.fuels_types = ["98", "95", "92", "Diesel"]
		self.typeToPric = dict()

		self.f = urllib.request.urlopen(self.url).read().decode("utf-8")
		self.parse()

	def parse(self):
		self.soup = BS(self.f, 'html.parser')

		self.fuels_pric = self.soup.find_all('td', {
				"align" : "right", 
				"style" : "text-shadow:none;color:#0000ff;font-color:#0000ff;text-align:right;"
		})

		for i in range(len(self.fuels_types)):
			self.typeToPric[self.fuels_types[i]] = self.fuels_pric[i].text
			# print(self.fuels_types[i], self.fuels_pric[i].text)
			
		# print(self.typeToPric)

	def getPrice(self, nam):
		if nam.find('d') != -1 or nam.find('D') != -1:
			return self.typeToPric["Diesel"]
		try:
			return self.typeToPric[nam]
		except:
			return 0.0


