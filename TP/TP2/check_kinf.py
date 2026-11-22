# -*-coding:utf-8 -*-
"""Analyse d'un fichier compo
Ordre des calculs dans le fichier EvoAssParamDmodTf.x2m+ :
on fait des boucles imbriquées en faisant varier : BU, Tfuel, Dmod, CB 
grep -i -E '\$|infinite'  EvoAssParamCbDmodTf.x2m+ > kinf.out



Construction de la compo
grep -i infinity -A1 EvoAssParamCbDmodTf.x2m+MCPOMACROCbDmodTFuel.txt  | grep -v INF | grep -v '\-\-' > kinf.txt
pval1 : bu
pval2 : T-FUEL
pval3 : Dmod
pval4 CB
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pval 1: cf  EvoAssParamCbDmodTf.x2m+MCPOMACROCbDmodTFuel.txt
bu = np.array([
    0.00000000E+00, 8.99999008E+01, 1.79999786E+02, 3.59999573E+02, 7.19999268E+02, 
    1.07999890E+03, 1.43999829E+03, 1.79999768E+03, 3.59999438E+03, 5.39999072E+03, 
    7.19998633E+03, 8.99998145E+03, 1.07999756E+04, 1.43999697E+04, 1.79999609E+04, 
    2.15999512E+04, 2.51999453E+04, 3.05999336E+04, 3.59999219E+04, 4.13999180E+04, 
    4.67999219E+04, 5.21999180E+04, 5.75999219E+04, 6.47999258E+04, 7.19999297E+04, 
    7.91999375E+04])
# pval 2
tfuel = np.array([3.00000000E+02, 9.00000000E+02, 1.50000000E+03])
# pval 3
dmod = np.array([0.7, 1.0])
# pval 4
cb =np.array([0.0, 1200.0, 2400.0])

filename = 'kinf.txt'
kinf = np.loadtxt(filename)

cols = pd.MultiIndex.from_product(
     [tfuel, dmod, cb],
     names=['Tfuel', 'Dmod', 'Cb'])
df = pd.DataFrame(kinf.reshape(-1, 26).T, columns=cols)
df.insert(0, 'Bu', bu.round())
df.insert(0, 'Time', (bu/36).round())


print(df.columns)
print(df)

#             Tfuel 
# df[['Time', 1500]]
#     Tfuel Dmod  Cb
# df[(1500, 0.7, 1200)]
# Tf
# df[900]



df.drop(['Time'], axis=1).plot(x='Bu', grid='True', title='kinfinite')
plt.legend()
plt.show()
