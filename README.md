PY_ERROR 0.0.1
==============

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
[py-expression-eval] (https://github.com/AxiaCore/py-expression-eval)

To-Do
======

Bugfixing:<br><br>
Problems with constants like PI <br>
Problem with lambda as a variable (because of eval in sympify) <br>
Resolve py-expression-eval dependency<br><br>

Improvements:<br><br>
Add formula preview<br>
Add Gaussian correlation error propagation <br>
Stand-alone-versions for Linux (Debian-based) and Windows

