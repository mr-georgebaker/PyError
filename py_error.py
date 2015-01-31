try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import ttk
import sympy as sp
from sympy.abc import *
from py_expression_eval import Parser

from constants import REPLACE_DIC, OPTIONS

parser = Parser()

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
            formula_raw_2 = self.formula.get().replace('pi', 'PI')
            self.formula_1 = parser.parse(formula_raw)
            self.formula_2 = sp.sympify(formula_raw)
            self.variables = self.formula_1.variables()
            self.update_UI(self.variables)
        except AttributeError:
            self.formula.insert(0, "Something went wrong")
        

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
        self.checkbox = []
        self.checkbox_value = []
        self.checkbox_trace = []
        self.nice_greek = [REPLACE_DIC.get(item,item) for item in self.variables]
        for i in range(len(variables)):
            self.entry_val.append(ttk.Entry(self))
            self.entry_val[i].grid(row=i+3, column=1)
            self.entry_unc.append(ttk.Entry(self))
            self.entry_unc[i].grid(row=i+3, column=2)
            self.label.append(tk.Label(self, text=self.nice_greek[i]))
            self.label[i].grid(row=i+3, column=0)
            self.label_val = tk.Label(self, text='Value')
            self.label_val.grid(row=2, column=1)
            self.label_unc = tk.Label(self, text='Uncertainty')
            self.label_unc.grid(row=2, column=2)
            self.checkbox_value.append(tk.StringVar(self))
            self.checkbox.append(tk.OptionMenu(self, self.checkbox_value[i],
                                               *OPTIONS.keys()))
            self.checkbox[i].grid(row=i+3, column=3)
            self.checkbox_trace.append(self.checkbox_value[i].trace('w',
                                                                    self.insert_constants))

    def insert_constants(self, *args):
        for i in range(len(self.checkbox_value)):
            try:
                if self.entry_val[i].get():
                    pass
                else:
                    self.entry_val[i].insert(0, '')
                    self.entry_unc[i].insert(0, '')
                    value_unc = OPTIONS[self.checkbox_value[i].get()]
                    self.entry_val[i].insert(0, value_unc[0])
                    self.entry_unc[i].insert(0, value_unc[1])
            except KeyError:
                pass
                                    
            
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
