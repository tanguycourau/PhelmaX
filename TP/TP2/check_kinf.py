# -*-coding:utf-8 -*-
"""Analyse d'un fichier compo
Ordre des calculs dans le fichier EvoAssParamDmodTf.x2m+ :
on fait eux boucles imbriquées en faisant varier le BU et la Tfuel
- La première avec Dmod = 0.7
- La seconde avec Dmod = 1.0
grep -i -E '\$|infinite'  EvoAssParamDmodTf.x2m+ > kinf.out



Construction de la compo
grep -i infinity -A1 EvoAssParamDmodTf.x2m+MCPOMACRODmodTFuel.txt  | grep -v INF > kinf.txt
P1 : bu
P2 : Dmod
P3 : Tfuel
"""

import numpy as np
import pandas as pd
# param 1
bu = np.array([
    0.00000000E+00, 8.99999008E+01, 1.79999786E+02, 3.59999573E+02, 7.19999268E+02, 
    1.07999890E+03, 1.43999829E+03, 1.79999768E+03, 3.59999438E+03, 5.39999072E+03, 
    7.19998633E+03, 8.99998145E+03, 1.07999756E+04, 1.43999697E+04, 1.79999609E+04, 
    2.15999512E+04, 2.51999453E+04, 3.05999336E+04, 3.59999219E+04, 4.13999180E+04, 
    4.67999219E+04, 5.21999180E+04, 5.75999219E+04, 6.47999258E+04, 7.19999297E+04, 
    7.91999375E+04])
# param 2
dmod = np.array([0.7, 1.0])
# param 3
tfuel = np.array([3.00000000E+02, 9.00000000E+02, 1.50000000E+03])
filename = 'kinf.txt'
kinf = np.loadtxt(filename)
cols = pd.MultiIndex.from_product(
     [dmod, tfuel],
     names=["Dmod", "Tfuel"])
df = pd.DataFrame(kinf.reshape(-1, 26).T, columns=cols)
df.index=bu/36
df.index.name='time'
print(df)
