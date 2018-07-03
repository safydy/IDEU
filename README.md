### Product Information

Exploration Interactive de Liaison de Variable  

### How to Run

- Jupyter Notebook with Python (2.7 or 3.5).
- The Jupyter Notebook server has been set up and is running on the machine that you have access. You should be able to clone the Azure-TDSP-Utilities repository to a directory on that machine. 
- `jupyterhub` or `jupyter lab`

### Python Modules 
The Python modules that are used in IDEAR are as follows. If your Jupyter Notebook server is running on Anaconda Python (2.7 or 3.5), most of the needed modules have been installed when you install Anaconda Python, with a few exceptions. However, if you are using [Azure Data Science Virtual Machines (DSVM)](https://azure.microsoft.com/en-us/marketplace/partners/microsoft-ads/standard-data-science-vm/), all modules are installed. 
 
- pandas
- numpy
- os
- [collections*](https://docs.python.org/2/library/collections.html)
- matplotlib
- [io*](https://docs.python.org/2/library/io.html)
- sys
- operator
- nbformat
- IPython
- ipywidgets
- scipy
- statsmodels
- [errno*](https://docs.python.org/2/library/errno.html)
- seaborn
- string
- functools

*Not included in Anaconda Python

Microsoft Data Analyst Team also defined some functions on top of libraries: 

- ReportMagics.py
- ConfUtility.py
- ReportGeneration.py
- UniVarAnalytics.py
- MultiVarAnalytics.py
