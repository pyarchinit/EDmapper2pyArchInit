"""
This is a Python GUI application that allows users to convert CSV files
into a uniform format. It uses Qt to create a GUI window and displays two tables,
one with template fields and the other with the data fields. Users are then able
to map the data fields to the corresponding template fields, and click on the 'Convert'
button to generate a new, uniform CSV file.
Additionally, this application also provides a way to generate
unique UUID values for each data row and also provide mapping to concepts from a JSON file.
"""

try:
    import pyi_splash
except:
    pass
else:
	pyi_splash.update_text("Welcome")
	pyi_splash.close()

from PyQt5.QtCore import QAbstractTableModel,Qt
from PyQt5.QtWidgets import *#QTableWidgetItem,QTextEdit,QWidget,QTableWidget,QTableView,QMainWindow,QApplication,QComboBox
from PyQt5.uic import loadUiType
import os
import csv
global csv_file_path
import pandas as pd


MAIN_DIALOG_CLASS, _ = loadUiType(
    os.path.join(os.path.dirname(__file__),  'ui', 'pyArchInit_mapper.ui'))


class CSVMapper(QMainWindow,MAIN_DIALOG_CLASS):
	"""
	This code is defining a class CSVMapper which is a subclass of QMainWindow.
	"""
	CONVERSION=['',

		'template_us'
	]
	def __init__(self, parent=None):



		super(CSVMapper, self).__init__(parent = parent)
		self.setupUi(self)
		self.template_fields = []
		self.data_fields = []
		self.mapping = {}
		self.comboBox_template.currentTextChanged.connect(self.on_template_changed)
		self.custumize_gui()
		self.toolButton_load.setEnabled(False)
		self.convert_data.setEnabled(False)
		self.add_mapping.setEnabled(False)
		self.remove_mapping.setEnabled(False)
		self.out=''

	def on_template_changed(self,text):

		if text:
			self.template_path = os.path.join('templates/', text+'.csv')
			self.load_template(self.template_path)
			self.toolButton_load.setEnabled(True)
		if not text:
			self.template_table.clear()
			self.toolButton_load.setEnabled(False)
			self.convert_data.setEnabled(False)

	def load_template(self,path):
		self.template_table.clear()
		self.mapping_table.clear()

		with open(path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			self.template_fields = next(reader)
		self.template_table.setHorizontalHeaderLabels(['Template Field'])

		self.template_table.setRowCount(len(self.template_fields))
		#self.template_table.setVerticalHeaderLabels(self.template_fields)
		#self.template_table = QTableWidget(len(header), 1)
		for i, field in enumerate(self.template_fields):
			item = QTableWidgetItem(field)
			self.template_table.setItem(i, 0, item)
		self.mapping_table.setHorizontalHeaderLabels(['Template Field', 'Data Field'])
		self.mapping_table.setRowCount(len(self.template_fields))
		#self.mapping_table.setVerticalHeaderLabels(header)
		self.mapping_table.setAcceptDrops(True)

		for i, field in enumerate(self.template_fields):
			item = QTableWidgetItem(field)
			self.mapping_table.setItem(i, 0, item)

	def custumize_gui(self):
		"""
		In the cutumize_gui() method, it is setting the window title, setting the geometry,
		and opening files for the template and data CSVs.
		"""
		#self.tableWidget_result.setHorizontalHeaderLabels(['Result'])
		self.comboBox_template.setInsertPolicy(QComboBox.InsertAtTop)
		self.comboBox_template.lineEdit().setPlaceholderText("Select an item...")
		#self.comboBox_template.setCurrentText("Select an item...")
		self.comboBox_template.addItems(self.CONVERSION)

		self.setCentralWidget(self.widget)

		self.statusbar.setSizeGripEnabled(False)

		self.statusbar.setStyleSheet("QStatusBar{border-top: 1px solid grey;}")


	def on_toolButton_load_pressed(self):
		self.add_mapping.setEnabled(True)
		# Open the data CSV file
		data_file, _ = QFileDialog.getOpenFileName(self, 'Open Data CSV', '', 'CSV files (*.csv)')
		if not data_file:
			self.show_error('No data file selected.')
			return
		self.transform_data(data_file,data_file)
		df = pd.read_csv(data_file, dtype = str)
		self.data_fields = df.columns.tolist()

		self.data_table.setDragEnabled(True)
		model = PandasModel(df)
		self.data_table.setModel(model)

	def on_add_mapping_pressed(self):
		#method is used to add a mapping between the template and the data fields
		template_index = self.template_table.currentRow()
		input_dialog = QInputDialog()
		data_field, okPressed = input_dialog.getItem(
			self,
			"Data Field",
			"Select Data Field:",
			self.data_fields,
			0,
			False
		)

		if okPressed:
			self.mapping[self.template_fields[template_index]] = data_field
			item = QTableWidgetItem(data_field)
			self.mapping_table.setItem(template_index, 1, item)
			self.convert_data.setEnabled(True)
			self.remove_mapping.setEnabled(True)

	def on_remove_mapping_pressed(self):
		#It  used to remove a mapping
		template_index = self.template_table.currentRow()
		del self.mapping[self.template_fields[template_index]]
		self.mapping_table.setItem(template_index, 1, QTableWidgetItem())

	def transform_data(self, file_path,output):
		with open(file_path, 'r') as f:
			reader = csv.reader(f)
			header = next(reader)
			col1_idx = header.index('anteriore')
			col2_idx = header.index('posteriore')
			col3_idx = header.index('contemporaneo')
			new_header = header + ['rapporti']
			rows = []
			for row in reader:
				col1_values = row[col1_idx].split('|')
				col2_values = row[col2_idx].split('|')
				col3_values = row[col3_idx].split('|')
				new_col = []
				for val in col1_values:

					if val:
						new_col.append(['copre', val])

				for val in col2_values:

					if val:
						new_col.append(['coperto da', val])
				for val in col3_values:

					if val:
						new_col.append(['si lega', val])
				row.append(new_col)
				rows.append(row)
		# with open(output, 'w', newline = '') as f:
		# 	writer = csv.writer(f)
		# 	writer.writerow(new_header)
		# 	for row in rows:
		# 		writer.writerow(row)
	def on_update_result_pressed(self):
		# ottieni l'indice delle righe selezionate
		selected_rows = [index.row() for index in self.tableWidget_result.selectionModel().selectedRows()]
		selected_columns = [index.column() for index in self.tableWidget_result.selectionModel().selectedColumns()]
		# use a QInputDialog to get user input
		user_input, ok_pressed = QInputDialog.getText(None, "Enter Data", "Enter a value:")

		if ok_pressed:


			# per ciascuna riga selezionata...
			for row in selected_rows:
				for column in selected_columns:
					if column==0:#aggiungere indice in sequenza
						a=self.add_numbers_in_sequence(int(user_input),row)###da modificare
						self.tableWidget_result.item(row, column).setText(str(a))###da modificare
					else:
						self.tableWidget_result.item(row, column).setText(user_input)
	def add_numbers_in_sequence(self,start_number, a_list):
		new_list = []
		current_number = start_number
		# loop through the list, adding to the sequence
		for i in range(a_list):
			new_list.append(current_number)
			current_number += 1
			print(new_list)
		return new_list
	def on_convert_data_pressed(self):

		if self.comboBox_template.currentText()=='':
			self.statusbar.showMessage('Waring! You need choose a template')
			pass
		if not self.data_fields:
			self.statusbar.showMessage('Waring! You need choose a data table')
			pass
		if self.comboBox_template.currentText()!='' and self.data_fields:

			output_file, _ = QFileDialog.getSaveFileName(self, 'Save Output CSV', '', 'CSV files (*.csv)')
			if not output_file:
				return
			output_fields = self.template_fields.copy()
			output_data = []
			for index, row in self.data_table.model()._data.iterrows():
				new_row = []
				for field in output_fields:
					if field in self.mapping:
						data_field = self.mapping[field]
						new_row.append(row[data_field])
					else:
						new_row.append('')
				output_data.append(new_row)
				#self.create_uuids(output_data)
			df = pd.DataFrame(output_data, columns=output_fields)
			df.to_csv(output_file, index=False)
			self.statusbar.showMessage('Output CSV saved successfully.')
			# open the CSV file and read the data
			with open(output_file) as csvfile:
				readCSV = csv.reader(csvfile,delimiter=',')
				#next(readCSV)
				row_count = 0
				rows=[]

				# loop through each row of the CSV file
				for row in readCSV:
					# get the number of columns in the row
					column_count = len(row)
					print(column_count)
					# add a new row to the QTableWidget object
					self.tableWidget_result.setRowCount(row_count + 1)
					self.tableWidget_result.setColumnCount(column_count)

					# loop through each column in the row
					for column in range(column_count):
						# create a new item and add it to the QTableWidget
						new_item = QTableWidgetItem(row[column])
						print(new_item)
						self.tableWidget_result.setItem(row_count, column, new_item)

					# increment the row count
					row_count += 1
					self.tableWidget_result.show()
			#self.tableWidget_result.show()
			#self.log_data.setText(data.to_string(index = False))
			self.out=output_file
	def on_save_data_pressed(self):
		with open(self.out, mode = 'w', newline = '') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			# loop through each row of the QTableWidget object
			for row in range(self.tableWidget_result.rowCount()):
				row_data = []
				# loop through each column in the row
				for column in range(self.tableWidget_result.columnCount()):
					# get the data for the current cell
					cell_data = self.tableWidget_result.item(row, column).text()
					# add the cell data to the row data list
					row_data.append(cell_data)
				# write the row data to the CSV file
				writer.writerow(row_data)

	def show_error(self, message):
		dialog = QMessageBox(self)
		dialog.setIcon(QMessageBox.Critical)
		dialog.setText(message)
		dialog.setWindowTitle('Error')
		dialog.setStandardButtons(QMessageBox.Ok)
		dialog.show()

class PandasModel(QAbstractTableModel):
	def __init__(self, data):
		QAbstractTableModel.__init__(self)
		self._data = data

	def rowCount(self, parent=None):
		return self._data.shape[0]

	def columnCount(self, parent=None):
		return self._data.shape[1]

	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():

			if role == Qt.DisplayRole:
				return str(self._data.iloc[index.row(), index.column()])

			column_count = self.columnCount()

			for column in range(0, column_count):

				if (index.column() == column and role == Qt.TextAlignmentRole):
					return Qt.AlignHCenter | Qt.AlignVCenter

		return None

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self._data.columns[section]
		return None

	def setData(self, index, value, role):
		if not index.isValid():
			return False

		if role != Qt.EditRole:
			return False

		row = index.row()

		if row < 0 or row >= self._data.shape[0]:
			return False

		column = index.column()

		if column < 0 or column >= self._data.shape[1]:
			return False

		self._data.iloc[row, column] = value
		self.dataChanged.emit(index, index)

		return True

	def flags(self, index):
		return Qt.ItemIsEnabled


if __name__ == '__main__':
	app = QApplication([])
	mapper = CSVMapper()
	mapper.show()
	app.exec_()