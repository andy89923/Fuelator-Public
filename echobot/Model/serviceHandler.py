
from echobot.Model.gas_model import Fuel_price
from echobot.Model.gs_model import Fuel_Gspread
from echobot.Model.imageHandle import ImageHandler

import json
import matplotlib.pyplot as plt
import numpy as np

# event.message.text
# event.source.user_id

class ServiceHandler():
	_auth_json_path = None
	_spreadsheet_key = None

	_fpTake = None
	_fgMang = None

	def __init__(self):
		data = open('info.json')
		js = json.load(data)

		self._auth_json_path = js['auth_json_path']
		self._spreadsheet_key = js['spreadsheet_key']
		return

	# Add new record to user's sheet 
	def addData(self, user, info):
		now = Fuel_Gspread(self._auth_json_path,self._spreadsheet_key)
		now.connect()
		now.append(user, info['gas'], info['liter'], info['miles'])

	# return fuel consumptions report url
	def report_f(self, user):
		now = Fuel_Gspread(self._auth_json_path,self._spreadsheet_key)
		now.connect()
		lis = now.getFuelUse(user)
		gap = list()
		for i in range(len(lis)):
			gap.append(i + 1)

		fig, ax = plt.subplots()

		ax.plot(gap, lis, '-ro')
		ax.set(xlabel = 'Time', ylabel = 'liters/100km', title = 'Fuel Consumption Report')
		ax.grid()
		
		fig.savefig('report.png')
		rep = ImageHandler()
		return rep.upload('report.png')

	# return fuel consumptions report url
	def report_c(self, user):
		now = Fuel_Gspread(self._auth_json_path,self._spreadsheet_key)
		now.connect()

		lis = now.getCostUse(user)
		gap = list()
		for i in range(len(lis)):
			gap.append(i + 1)

		fig, ax = plt.subplots()

		ax.plot(gap, lis, '-ro')
		ax.set(xlabel = 'Time', ylabel = 'Cost(NTD$)', title = 'Fuel Cost Report')
		ax.grid()
		
		fig.savefig('report.png')
		rep = ImageHandler()
		return rep.upload('report.png')


	# deal with what kind of command
	def cmd(self, event):
		user_in = event.message.text
		user_id = event.source.user_id

		if user_in == "p" or user_in == "P":
			tmp = self.report_f(user_id)
			return tmp

		if user_in == "c" or user_in == "C":
			tmp = self.report_c(user_id)
			return tmp


		try:
			ll = user_in.split(' ')
			
			gty = ll[0]
			liq = float(ll[1])
			mil = float(ll[2])

			gas = Fuel_price()
			gty = gas.getPrice(gty)

			if str(gty) == "0.0" or len(ll) != 3:
				return "Error input"

			info = dict()
			info['gas'] = gty
			info['liter'] = liq
			info['miles'] = mil

			self.addData(user_id, info)
		except:
			return "Error input"

		return "Add record success" 



