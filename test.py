import pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
data = pd.read_csv('aluminium dataset.csv')
data.groupby('bauxite (kg)')['aluminium (kg)'].aggregate(['mean','median']).plot.bar()
plt.show()
