![icon](http://georgebaker.lima-city.de/lib/exe/fetch.php?media=icon.ico)     PyError 0.0.3
==============

Project Homepage: [PyError](http://georgebaker.lima-city.de/doku.php?id=start) <br>
Author: mr-georgebaker<br>
Email: georgebaker1@hotmail.com

Parses an entered formula and calculates the value as well as the uncertainty according to Gaussian error propagation.

Install
=======
1) Install needed python libraries (see below)<br>
2) git clone https://github.com/mr-georgebaker/py_error <br>
3) change to the new directory <br>
4) chmod +x py_error.py

Needed Python Libraries
=======================

[Sympy] (http://www.sympy.org/en/index.html) <br>
[py-expression-eval] (https://github.com/AxiaCore/py-expression-eval) <br>
[PIL](https://pypi.python.org/pypi/Pillow/2.2.1) <br>
[Requests](https://pypi.python.org/pypi/Pillow/2.2.1)

To-Do
======

Bugfixing:<br><br>
Problem with lambda as a variable (because of eval in sympify) <br>
Resolve py-expression-eval dependency<br><br>

Improvements:<br><br>

Add Gaussian correlation error propagation <br>


