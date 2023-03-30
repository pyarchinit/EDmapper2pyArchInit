# CSVMapper Class 
  
The following code defines a  CSVMapper  class which is a subclass of  QMainWindow . The purpose of this class is to map data from one CSV format to another using a template.  
  
The class has several methods that handle different operations such as loading templates, loading data, adding mappings, converting data, and more.  
  
## Program Flow 
  
The program starts by importing necessary libraries and modules, and defining the  QMainWindow  subclass  CSVMapper . It then defines various methods for the  CSVMapper  class and initializes the PyQt5 application. The class is instantiated, and the PyQt5 application is executed.  
  
## Key Methods 
  
Some of the key methods in the  CSVMapper  class are: 
  
-   __init__ : initializes the  CSVMapper  class, setting up the UI and connections  
-   customise_gui : customizes the UI elements, such as adding items to the combobox  
-   load_template : loads the selected template into the  template_table   
-   transform_data : transforms the data from the input CSV file based on the selected template  
-   on_convert_data_pressed : converts the data and saves the output as a CSV file  
-   on_save_data_pressed : saves the modified data in the  tableWidget_result  to an output CSV file  
  
## User Interaction 
  
The user can choose a template from the dropdown menu, load the data from a CSV file, map the fields as required, and then convert the data according to the chosen template. The program also provides functionalities like adding sequential index values, updating cell values manually, and searching and replacing cell values in the output table. Finally, the user can save the modified output data to a CSV file.
