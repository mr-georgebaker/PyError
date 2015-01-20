try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import ttk
import sympy as sp
from sympy.abc import *
from py_expression_eval import Parser

from constants import REPLACE_DIC

parser = Parser()
sp.init_printing()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Fehlerrechnung')

        self.formula = ttk.Entry(self)
        self.formula.grid(row=0, column=0)

        self.analyze_button = ttk.Button(self, text='Analyze Formula',
                                        command=self.analyze_formula)
        self.analyze_button.grid(row=0, column=1)

        self.calculate_button = ttk.Button(self, text='Calculate',
                                          command=self.calculate_value)
        self.calculate_button.grid(row=0, column=2)

    def analyze_formula(self):
        """ Parses the formula using sympy and py_expression_eval """
        try:
            formula_raw = self.formula.get()
            self.formula_1 = parser.parse(formula_raw)
            self.formula_2 = sp.sympify(formula_raw)
            self.variables = self.formula_1.variables()
            self.update_UI(self.variables)
        except Exception:
            self.formula.insert(0, "Please use a different formula")

    def update_UI(self, variables):
        """ Adds to the UI entry-fields for values and uncertainties"""
        try:
            for i in range(len(self.entry_val)):
                self.entry_val[i].destroy()
                self.entry_unc[i].destroy()
                self.label[i].destroy()
        except AttributeError:
            pass
        self.entry_val = []
        self.entry_unc = []
        self.label = []
        self.nice_greek = [REPLACE_DIC.get(item,item) for item in self.variables]
        for i in range(len(variables)):
            self.entry_val.append(ttk.Entry(self))
            self.entry_val[i].grid(row=i+2, column=1)
            self.entry_unc.append(ttk.Entry(self))
            self.entry_unc[i].grid(row=i+2, column=2)
            self.label.append(tk.Label(self, text=self.nice_greek[i]))
            self.label[i].grid(row=i+2, column=0)
            self.label_val = tk.Label(self, text='Value')
            self.label_val.grid(row=1, column=1)
            self.label_unc = tk.Label(self, text='Uncertainty')
            self.label_unc.grid(row=1, column=2)

    def calculate_value(self):
        """ Calculates the solution """
        self.dic_value = {}
        try:
            self.differentiate(self.formula_2, self.variables)
            for i in range(len(self.variables)):
                self.dic_value.update({self.variables[i]:self.entry_val[i].get()})
            self.solution = self.formula_2.evalf(5, subs=self.dic_value)
            self.calculate_error()
            self.present_solution()
        except AttributeError:
            pass

    def calculate_error(self):
        """ Calculates the error according to Gaussian error propagation"""
        self.error = 0
        for i in range(len(self.diff_list)):
            value_diff = self.diff_list[i].evalf(subs=self.dic_value)
            value_diff *= float(self.entry_unc[i].get())
            value_diff = value_diff**2
            self.error += value_diff
        self.error = sp.N(sp.sqrt(self.error), 3)
        
    def differentiate(self, formula, variables):
        """ Differentiates the formula with respect to all variables """
        self.diff_list = []
        for element in variables:
            sym = sp.sympify(element)
            differ = sp.diff(formula, sym)
            self.diff_list.append(differ)
            
    def present_solution(self):
        """ Presents the solution in a canvas """
        solution_final = str(self.solution) + " +/- " + str(self.error)
        self.canvas = tk.Canvas(self, width=200, height=50)
        self.canvas.grid(row=100, column=1)
        canvas_id = self.canvas.create_text(10,10, anchor='nw')
        self.canvas.itemconfig(canvas_id, text=solution_final)

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
