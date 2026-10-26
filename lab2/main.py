import sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit)

import rubles
import dollars
import euros

RUB_PER_USD = 80.5381
RUB_PER_EUR = 90.2429
USD_PER_EUR = 1.1205


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initial_width = 520
        self.initial_height = 320
        
        self.rub_model = rubles.RublesModel()
        self.dolar_model = dollars.DollarsModel()
        self.euro_model = euros.EurosModel()
        
        self.dolar_model._value = 1.0000
        self.rub_model._value = RUB_PER_USD
        self.euro_model._value = 1 / USD_PER_EUR
        
        self.lock_events = False
        
        self.init_ui()
        
    def init_ui(self):
        self.setGeometry(100, 100, self.initial_width, self.initial_height)
        self.setMinimumSize(240, 200)
        self.setWindowTitle("Конвертер валют (Сигналы-слоты)")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        central_widget.setLayout(self.main_layout)
        
        font = QFont()
        font.setPointSize(10)
        
        rx = QRegExp(r"^\d{0,7}(,\d{0,4})?$")
        validator = QRegExpValidator(rx)
        
        self.line_usd = self.create_input_row("Доллар (USD)", font, validator)
        self.line_usd.setText(f"{self.dolar_model.get_value():.4f}".replace('.', ','))
        
        self.line_rub = self.create_input_row("Рубль (RUB)", font, validator)
        self.line_rub.setText(f"{self.rub_model.get_value():.4f}".replace('.', ','))
        
        self.line_eur = self.create_input_row("Евро (EUR)", font, validator)
        self.line_eur.setText(f"{self.euro_model.get_value():.4f}".replace('.', ','))
        
        self.main_layout.addStretch()
        
        self.line_usd.textChanged.connect(self.on_usd_text_changed)
        self.line_rub.textChanged.connect(self.on_rub_text_changed)
        self.line_eur.textChanged.connect(self.on_eur_text_changed)
        
        self.dolar_model.valueChanged.connect(self.update_from_usd)
        self.rub_model.valueChanged.connect(self.update_from_rub)
        self.euro_model.valueChanged.connect(self.update_from_eur)

    def create_input_row(self, label_text, font, validator):
        row_layout = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setFont(font)
        label.setFixedWidth(120)
        
        line_edit = QLineEdit()
        line_edit.setFont(font)
        line_edit.setValidator(validator)
        line_edit.setMinimumSize(160, 30) 
        
        row_layout.addWidget(label)
        row_layout.addWidget(line_edit)
        
        self.main_layout.addLayout(row_layout)
        return line_edit

    def _parse_text(self, text):
        if not text: 
            return None
        try:
            return float(text.replace(',', '.'))
        except ValueError:
            return None

    def on_usd_text_changed(self, text):
        if self.lock_events: return
        val = self._parse_text(text)
        if val is not None:
            self.dolar_model.set_value(val)

    def on_rub_text_changed(self, text):
        if self.lock_events: return
        val = self._parse_text(text)
        if val is not None:
            self.rub_model.set_value(val)

    def on_eur_text_changed(self, text):
        if self.lock_events: return
        val = self._parse_text(text)
        if val is not None:
            self.euro_model.set_value(val)

    def update_from_usd(self, usd_val):
        self.lock_events = True
        try:
            rub_val = usd_val * RUB_PER_USD
            eur_val = usd_val / USD_PER_EUR
            
            self.line_rub.setText(f"{rub_val:.4f}".replace('.', ','))
            self.line_eur.setText(f"{eur_val:.4f}".replace('.', ','))
            
            self.rub_model._value = rub_val
            self.euro_model._value = eur_val
        finally:
            self.lock_events = False

    def update_from_rub(self, rub_val):
        self.lock_events = True
        try:
            usd_val = rub_val / RUB_PER_USD
            eur_val = rub_val / RUB_PER_EUR
            
            self.line_usd.setText(f"{usd_val:.4f}".replace('.', ','))
            self.line_eur.setText(f"{eur_val:.4f}".replace('.', ','))
            
            self.dolar_model._value = usd_val
            self.euro_model._value = eur_val
        finally:
            self.lock_events = False

    def update_from_eur(self, eur_val):
        self.lock_events = True
        try:
            usd_val = eur_val * USD_PER_EUR
            rub_val = eur_val * RUB_PER_EUR
            
            self.line_usd.setText(f"{usd_val:.4f}".replace('.', ','))
            self.line_rub.setText(f"{rub_val:.4f}".replace('.', ','))
            
            self.dolar_model._value = usd_val
            self.rub_model._value = rub_val
        finally:
            self.lock_events = False

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()