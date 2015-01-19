try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import sympy as sp
from sympy.abc import *
from py_expression_eval import Parser

parser = Parser()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

    def init_UI(self):
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.bottomframe = tk.Frame(self)
        self.bottomframe.pack(side='bottom')

        self.vars = {}

        self.title('Fehlerrechnung')
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='Usage', command=self.instruction)

        self.formula = tk.Entry(self.frame, width=80)
        self.formula.pack(side='left', fill='x')

        self.analyze_button = tk.Button(self.frame, text='Analyze Formula',
                                        command=self.analyze_formula)
        self.analyze_button.pack(side='left')

    def analyze_formula(self):
        """ Analyzes the formula with sympy and py_expression_eval """
        formula_raw = self.formula.get()
        formula_1 = parser.parse(formula_raw)
        formula_2 = sp.sympify(formula_raw)
        variables = formula_1.variables()
        self.update_UI(variables)
        self.differentiate(formula_2, variables)

    def differentiate(self, formula, variables):
        """ Differentiates the formula with respect to all variables """
        diff = []
        for element in variables:
            sym = sp.sympify(element)
            differ = sp.diff(formula, sym)
            diff.append(differ)

    def update_UI(self, variables):
        self.init_UI()
        for i in range(len(variables)):
            self.vars[i] = tk.StringVar()
            self.entry = ttk.Entry(self.bottomframe, textvariable=self.vars[i])
            self.entry.pack(side='bottom', fill='x')

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
