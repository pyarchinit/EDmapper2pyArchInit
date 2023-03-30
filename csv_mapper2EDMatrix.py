"""
This is a Python GUI application that allows users to convert CSV files
into a uniform format. It uses Qt to create a GUI window and displays two tables,
one with template fields and the other with the data fields. Users are then able
to map the data fields to the corresponding template fields, and click on the 'Convert'
button to generate a new, uniform CSV file.
Additionally, this application also provides a way to generate
unique UUID values for each data row and also provide mapping to concepts from a JSON file.
"""
from time import sleep
try:
    import pyi_splash
except:
    pass
else:
	sleep(5)
	pyi_splash.close()

from PyQt5.QtCore import (QAbstractTableModel,
						  Qt)
from PyQt5.QtWidgets import (QDialog,
							 QFileDialog,
							 QInputDialog,
							 QTableWidgetItem,
							 QTableWidget,
							 QMainWindow,
							 QApplication,
							 QComboBox,
							 QMessageBox,
							 QLineEdit,
							 QPushButton,
							 QHBoxLayout,
							 QVBoxLayout,
							 QLabel)
from PyQt5.uic import loadUiType
from PyQt5 import QtCore
import os
import csv
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
		self.index_tab.setEnabled(False)
		self.update_result.setEnabled(False)
		self.find_replace.setEnabled(False)
		self.save_data.setEnabled(False)
		self.out=''



	def on_find_replace_pressed(self):
		self.replace_cell_values()
	def replace_cell_values(self):
		# Ottiene la colonna selezionata dall'utente
		selected_column = self.tableWidget_result.currentColumn()
		# Ottiene il testo di ricerca dalla finestra di input
		search_text, ok = QInputDialog.getText(self, 'Find and replace', 'insert text:')
		if ok:
			# Ottiene il valore di sostituzione dalla finestra di input
			replace_text, ok = QInputDialog.getText(self, 'Find and replace',
													'Insert a value:')
			if ok:
				# Scorre le righe della colonna selezionata e cerca corrispondenze per la stringa di ricerca
				for row in range(self.tableWidget_result.rowCount()):
					item = self.tableWidget_result.item(row, selected_column)
					if item is not None and search_text in item.text():
						# Sostituisce il valore della cella con il valore di sostituzione
						self.tableWidget_result.setItem(row, selected_column, QTableWidgetItem(replace_text))
					#else:
						#self.show_info('No data found')
					#break
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
		try:
			self.transform_data(data_file,data_file)
		except:
			pass
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

	def on_auto_mapping_pressed(self):
		#funziona solo per il template Extended matrix
		#indce della lista del template
		template_index = [3,5,29,76,18]
		#lista dei campi del template ED
		data_field = ["nome us","descrizione","tipo","epoca","rapporti"]
		#iterazione e unione delle due liste
		for i, e in zip(data_field,template_index):
			self.mapping[self.template_fields[e]] = i
			item = QTableWidgetItem(i)
			self.mapping_table.setItem(e, 1, item)

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
				col1_values = row[col1_idx].split(',')
				col2_values = row[col2_idx].split(',')
				col3_values = row[col3_idx].split(',')
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

		with open(output, 'w', newline = '') as f:
		 	writer = csv.writer(f)
		 	writer.writerow(new_header)
		 	for row in rows:
		 		writer.writerow(row)
		self.data_table.removeColumn(new_header)
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
					if column==0:
						self.show_info('Use Add index for this column')
						break
					else:
						self.tableWidget_result.item(row, column).setText(user_input)
			#if column == 0:  # aggiungere indice in sequenza alla prima colonna

	def on_index_tab_pressed(self):
		self.add_sequence_to_selected_rows()

	def add_sequence_to_selected_rows(self):
		"""
		Aggiunge numeri in sequenza alle righe selezionate di una QTableWidget a partire da un input.
		"""
		dialog = self.AddSequenceDialog(self.tableWidget_result)
		input_num = dialog.exec_()
		if input_num is None:
			return
		selected_rows = [index.row() for index in self.tableWidget_result.selectedIndexes() if index.column() == 0]
		if not selected_rows:
			return
		last_index = max(selected_rows)
		for i in range(last_index + 1, self.tableWidget_result.rowCount()):
			if i not in selected_rows:
				break
			input_num += 1
		for row in selected_rows:
			self.tableWidget_result.setItem(row, 0, QTableWidgetItem(str(input_num)))
			input_num += 1
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
				header=next(readCSV)
				row_count = 0

				# loop su ogni riga del csv
				for row in readCSV:
					# lunghezza del numero di colonne
					column_count = len(row)
					print(column_count)
					# add a new row to the QTableWidget object
					self.tableWidget_result.setRowCount(row_count + 1)
					self.tableWidget_result.setColumnCount(column_count)
					self.tableWidget_result.setHorizontalHeaderLabels(header)
					# loop through each column in the row
					for column in range(column_count):
						# create a new item and add it to the QTableWidget
						new_item = QTableWidgetItem(row[column])
						print(new_item)
						self.tableWidget_result.setItem(row_count, column, new_item)

					# increment the row count
					row_count += 1
					self.tableWidget_result.show()
			#Si abilitano le funzioni per la tableWidget_result
			self.out=output_file
			self.index_tab.setEnabled(True)
			self.update_result.setEnabled(True)
			self.find_replace.setEnabled(True)
			self.save_data.setEnabled(True)

	def on_save_data_pressed(self):
		with open(self.out, mode = 'w', newline = '') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			# Scrive l'intestazione della tabella
			headers = []
			for column in range(self.tableWidget_result.columnCount()):
				headers.append(self.tableWidget_result.horizontalHeaderItem(column).text())
			writer.writerow(headers)
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
			self.show_info('Saved successfully')

	def show_error(self, message):
		dialog = QMessageBox(self)
		dialog.setIcon(QMessageBox.Critical)
		dialog.setText(message)
		dialog.setWindowTitle('Error')
		dialog.setStandardButtons(QMessageBox.Ok)
		dialog.show()

	def show_info(self, message):
		dialog = QMessageBox(self)
		dialog.setIcon(QMessageBox.Information)
		dialog.setText(message)
		dialog.setWindowTitle('Info')
		dialog.setStandardButtons(QMessageBox.Ok)
		dialog.show()
	class AddSequenceDialog(QDialog):
		def __init__(self, table_widget: QTableWidget):
			super().__init__()
			self.table_widget = table_widget
			self.input_num = None
			self.input_edit = QLineEdit()
			ok_button = QPushButton('Ok')
			ok_button.clicked.connect(self.accept)
			cancel_button = QPushButton('Cancel')
			cancel_button.clicked.connect(self.reject)
			button_layout = QHBoxLayout()
			button_layout.addWidget(ok_button)
			button_layout.addWidget(cancel_button)
			layout = QVBoxLayout()
			layout.addWidget(QLabel('Enter starting number: '))
			layout.addWidget(self.input_edit)
			layout.addLayout(button_layout)
			self.setLayout(layout)

		def exec_(self):
			super().exec_()
			try:
				self.input_num = int(self.input_edit.text())
			except ValueError:
				self.input_num = None
			return self.input_num
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