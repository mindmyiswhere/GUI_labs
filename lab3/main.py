import sys
import os
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog,
                             QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
                             QMessageBox, QLabel, QHeaderView)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Лабораторная работа 3: PyQt + SQL')
        self.resize(900, 600)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')

        set_conn_act = QAction('Set connection', self)
        set_conn_act.triggered.connect(self.set_connection)
        file_menu.addAction(set_conn_act)

        close_conn_act = QAction('Close connection', self)
        close_conn_act.triggered.connect(self.close_connection)
        file_menu.addAction(close_conn_act)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        controls_layout = QHBoxLayout()
        
        self.combo = QComboBox()
        self.combo.addItem('Выберите колонку...')
        self.combo.addItems(['name', 'type', 'tbl_name', 'sql']) 
        self.combo.currentTextChanged.connect(self.on_combo_change)

        self.bt1 = QPushButton('Запрос 1 (Tab 2)')
        self.bt1.clicked.connect(self.on_bt1)
        
        self.bt2 = QPushButton('Запрос 2 (Tab 4)')
        self.bt2.clicked.connect(self.on_bt2)
        
        self.bt3 = QPushButton('Запрос 3 (Tab 5)')
        self.bt3.clicked.connect(self.on_bt3)

        controls_layout.addWidget(QLabel('Колонка:'))
        controls_layout.addWidget(self.combo)
        controls_layout.addWidget(self.bt1)
        controls_layout.addWidget(self.bt2)
        controls_layout.addWidget(self.bt3)
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tabs.addTab(self.tab1, "Tab 1 (sqlite_master)")
        self.tabs.addTab(self.tab2, "Tab 2 (bt1)")
        self.tabs.addTab(self.tab3, "Tab 3 (Combo)")
        self.tabs.addTab(self.tab4, "Tab 4 (bt2)")
        self.tabs.addTab(self.tab5, "Tab 5 (bt3)")

        self.table1 = self.setup_table(self.tab1)
        self.table2 = self.setup_table(self.tab2)
        self.table3 = self.setup_table(self.tab3)
        self.table4 = self.setup_table(self.tab4)
        self.table5 = self.setup_table(self.tab5)

        main_layout.addWidget(self.tabs)

        self.set_controls_enabled(False)

    def setup_table(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        table = QTableWidget()
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return table

    def set_controls_enabled(self, enabled):
        self.combo.setEnabled(enabled)
        self.bt1.setEnabled(enabled)
        self.bt2.setEnabled(enabled)
        self.bt3.setEnabled(enabled)

    def execute_and_fill(self, table_widget, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            col_names = [description[0] for description in cursor.description]

            table_widget.setRowCount(len(rows))
            table_widget.setColumnCount(len(col_names))
            table_widget.setHorizontalHeaderLabels(col_names)

            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data) if cell_data is not None else "NULL")
                    table_widget.setItem(row_idx, col_idx, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка SQL", str(e))

    def set_connection(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Выберите базу данных', '', 
            'SQLite DB (*.db *.sqlite);;All Files (*)'
        )
        if file_path:
            try:
                self.conn = sqlite3.connect(file_path)
                self.set_controls_enabled(True)
                self.execute_and_fill(self.table1, "SELECT * FROM sqlite_master")
                self.tabs.setCurrentIndex(0)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка подключения", str(e))

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        
        self.set_controls_enabled(False)
        
        for table in [self.table1, self.table2, self.table3, self.table4, self.table5]:
            table.setRowCount(0)
            table.setColumnCount(0)

    def on_bt1(self):
        self.execute_and_fill(self.table2, "SELECT name FROM sqlite_master")
        self.tabs.setCurrentIndex(1)

    def on_combo_change(self, text):
        if text and text != 'Выберите колонку...' and self.conn:
            query = f"SELECT {text} FROM sqlite_master"
            self.execute_and_fill(self.table3, query)
            self.tabs.setCurrentIndex(2)

    def on_bt2(self):
        query = "SELECT name, type FROM sqlite_master WHERE type='table'"
        self.execute_and_fill(self.table4, query)
        self.tabs.setCurrentIndex(3)

    def on_bt3(self):
        query = "SELECT name, sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
        self.execute_and_fill(self.table5, query)
        self.tabs.setCurrentIndex(4)


def create_test_db():
    lab_dir = 'lab3'
    if not os.path.exists(lab_dir):
        os.makedirs(lab_dir)
    
    db_path = os.path.join(lab_dir, 'test_lab3.db')
    
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        c.execute("INSERT INTO students (name, age) VALUES ('Иван', 20)")
        c.execute("INSERT INTO students (name, age) VALUES ('Мария', 22)")
        conn.commit()
        conn.close()

if __name__ == '__main__':
    create_test_db()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())