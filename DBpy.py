import PySimpleGUI as sg
import mysql.connector

connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database="veritabani1")
mycursor = connection.cursor()
#mycursor.execute()

sg.theme("Dark")

layout = [
	[sg.Text("Name:", size=(7,1)), sg.Input(key= '-NAME-')],
	[sg.Text("Surname:", size=(7,1)), sg.Input(key= '-SURNAME-')],
	[sg.Text("TC:", size=(7,1)), sg.Input(key= '-TC-')],
	[sg.Button("Submit"), sg.Button("Show Data"), sg.Button("Clear"), sg.Exit()]
	]

main_form_window = sg.Window("Form", layout)

def clear():
	for key in values:
		main_form_window['-NAME-'].update('')
		main_form_window['-SURNAME-'].update('')
		main_form_window['-TC-'].update('')
	return None

def save_data_to_DB():
	connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database="veritabani1")
	mycursor = connection.cursor()
# (name varchar,surname varchar,tc varchar)
	query = "INSERT INTO pythontable values(%s, %s, %s)"
	mycursor.execute(query, (name, surname, tc))
	connection.commit()

def retrieve_records():
	results = []
	connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database="veritabani1")
	mycursor = connection.cursor()
	query = "SELECT * FROM pythontable"
	mycursor.execute(query)
	for row in mycursor:
		results.append(list(row))
	return results
def delete_db():
	connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database="veritabani1")
	mycursor = connection.cursor()
	query = "DELETE "
def modify_DB():
	modify_DB_layout = [
		[sg.Text("Modifying DB")],
		[sg.Button("Delete"), sg.Button("Edit")]
	]

	modify_DB_window = sg.Window("Modifying DB", modify_DB_layout)

	while True:
		event, values = modify_DB_window.read()
		if event == sg.WIN_CLOSED:
			break
		if event == 'Delete':
			delete_db()
		
def create_records():
	records_array = retrieve_records() 
	headings = ['Name', 'Surname', 'TC']

	table_layout = [
		[sg.Table(values = records_array, headings = headings, key = '-TABLE-',
		max_col_width = 35, auto_size_columns = True, display_row_numbers = True,
		row_height=60, enable_events = True, justification = 'left', tooltip = 'DB')]
	]

	table_window = sg.Window("DB Data", table_layout, modal = True)
	_table_ = table_window['-TABLE-']
	while True:
		event, values = table_window.read()
		if event == sg.WIN_CLOSED:
			break
		if event == '-TABLE-':
			
	table_window.close() 

while True:
	event, values = main_form_window.read()
	if event == 'Exit' or event == sg.WIN_CLOSED:
		print("Exit event")
		break
	if event == 'Clear':
		print("Clear event")
		clear()
	if event == 'Submit':
		print("Submit event")
		name = values['-NAME-']
		surname = values['-SURNAME-']
		tc = values['-TC-']
		if name == '':
			sg.PopupError("Name is missing.","Enter name.")
		if surname == '':
			sg.PopupError("Surname is missing.", "Enter surname.")
		if tc == '':
			sg.PopupError("TC is missing.", "Enter TC.")
		else:
			summary_list = "Data added!"
			choice = sg.PopupOKCancel(summary_list, 'You are adding new data to the DB.')
			if choice == 'OK':
				clear()
				save_data_to_DB()
				sg.PopupQuick('Done!')
			else:
				sg.PopupOK("Edit your information")
	if event == 'Show Data':
		create_records()

main_form_window.close()
