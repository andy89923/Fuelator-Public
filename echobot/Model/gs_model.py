import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

class Fuel_Gspread():
	_gss_scopes = ['https://spreadsheets.google.com/feeds']
	_auth_json_path = ""
	_spreadsheet_key = ""
	
	_credentials = None
	_gss_client = None
	_file = None
	
	def __init__(self, auth_path, spreadsheet_key):
		self._auth_json_path = auth_path
		self._spreadsheet_key = spreadsheet_key

	def connect(self):
		self._credentials = ServiceAccountCredentials.from_json_keyfile_name(self._auth_json_path, self._gss_scopes)
		self._gss_client = gspread.authorize(self._credentials)
		
		self._file = self._gss_client.open_by_key(self._spreadsheet_key)


	def append(self, user_name, gas, liq, mil):
		mes = ""
		try:
			sh = self._file.worksheet(user_name)
		except:
			sh = self._file.add_worksheet(title = user_name, rows = "1", cols = "5")
			mes = "New User! Welcome~\n"

		time = datetime.datetime.now()
		sh.append_row([str(time), str(gas), str(liq), str(mil)], value_input_option = 'USER_ENTERED')

		return mes + "Add success"

	def getCostUse(self, user_name):
		try:
			sh = self._file.worksheet(user_name)
		except:
			return [0]

		gas_pirc = sh.col_values(2)
		gas_list = sh.col_values(3)

		ful_cos = list()
		for i in range(len(gas_list)):
			p = float(gas_pirc[i])
			v = float(gas_list[i])

			ful_cos.append(round(p * v))

		return ful_cos


	def getFuelUse(self, user_name):
		try:
			sh = self._file.worksheet(user_name)
		except:
			return [0.0]

		gas_list = sh.col_values(3)
		mil_list = sh.col_values(4)

		ful_cous = list()
		for i in range(len(gas_list) - 1):
			d_gas = float(gas_list[i + 1])
			d_mil = float(mil_list[i + 1]) - float(mil_list[i])

			if d_mil == 0:
				continue
			ful_cous.append(d_gas / d_mil * 100.0)

		return ful_cous

