from PyQt6.QtWidgets import QMenu, QMessageBox, QToolBar, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QDockWidget, QTableWidgetItem, QWidget, QApplication, QTableWidget, QMainWindow,QLabel,QLineEdit
import sys
import sqlite3
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.conn=sqlite3.connect("products.db")
        self.create_table()
        self.initUI()
    def load_data(self):
        cursor=self.conn.cursor() # cursor is a type of pointer that points the database and helps to access the database, u can execute certain sql commands with cursor ...cursor.execute is used to store the actual command and they must be in caps
        cursor.execute("SELECT * FROM PRODUCT")  # PRODUCT is the table name 
        products=cursor.fetchall()
        self.table_widget.setRowCount(len(products))
        
        for row, product in enumerate(products):
            for col,value in enumerate(product):
               item=QTableWidgetItem(str(value))
               self.table_widget.setItem(row,col,item)

                
            

        
       
    def create_table(self):
        cursor=self.conn.cursor() # cursor is a type of pointer that points the database and helps to access the database, u can execute certain sql commands with cursor ...cursor.execute is used to store the actual command and they must be in caps
        cursor.execute("""  
                CREATE TABLE IF NOT EXISTS PRODUCT(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT,
              price INTEGER,
              description TEXT
            );

           """)
        self.conn.commit()   # in order to commit the above changes this command is used


    def initUI(self):
        self.setGeometry(0, 0, 700, 500)
       
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)


        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["ID","Name", "Price", "Description"])

        self.setCentralWidget(central_widget)
        self.load_data()

        self.name_edit=QLineEdit(self)  # Qline likhne ki jagah banayega 
        self.price_edit=QLineEdit(self)
        self.description_edit=QLineEdit(self)

        layout .addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        
        layout .addWidget(QLabel("Price:"))
        layout.addWidget(self.price_edit)
        
        layout .addWidget(QLabel("Description:"))
        layout.addWidget(self.description_edit)

        add_button=QPushButton("Add Product",self)
        add_button.clicked.connect(self.add_product)

        del_button= QPushButton("Delete Product",self)
        del_button.clicked.connect(self.del_product)
        update_button=QPushButton("Update Product",self)
        update_button.clicked.connect(self.update_product)


        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(update_button)
         
    def update_product(self):
        current_row=self.table_widget.currentRow()
        if current_row<0 or current_row>=self.table_widget.rowCount():
            return QMessageBox.warning(self,"No Row Selected")
        name=self.name_edit.text().strip()
        price=self.price_edit.text().strip() 
        description=self.description_edit.text().strip()
        product_id=int(self.table_widget.item(current_row,0).text() ) 
        cursor=self.conn.cursor()
        cursor.execute("UPDATE PRODUCT SET name=? , price=?, description=? WHERE id=?",(name,price, description,product_id))   # ? represents something and fo filling the something value we used a tuple 
        self.conn.commit()
        self.load_data()  

        
        

    def del_product(self):
        current_row=self.table_widget.currentRow() # this will give the selected row 
        if current_row<0 or current_row>=self.table_widget.rowCount():
            return QMessageBox.warning(self,"No Row Selected")
        product_id=int(self.table_widget.item(current_row,0).text() ) 
        button=QMessageBox.question(self,"Delete Product","Do you want to delete this product?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)     
        if button ==QMessageBox.StandardButton.Yes:
            cursor=self.conn.cursor()
            cursor.execute("DELETE FROM PRODUCT WHERE id=?",(product_id,)) # here coma is there becoz python will think its a tuple and ? has to be  replaced with tuple 
            self.conn.commit()
            self.load_data()  


    

    def add_product(self):
        name=self.name_edit.text().strip()
        price=self.price_edit.text().strip() 
        description=self.description_edit.text().strip()
         # adding new product to the database
        
        
        
        self.name_edit.clear()  # clear the name edit field when the info is entered above
        self.price_edit.clear()
        self.description_edit.clear()    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
