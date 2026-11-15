# -*-coding:utf-8 -*-
"""Contrôle des densités calculées par Dragon en sortie de Cell.x2m+
l'obejctif est de recalculer les densités massiques à partir des densités atomiques fournies en sortie du module EDI
"""
 
## Sortie du module info  fichier Cell.x2m+ 
m_H1H2O, m_O16, m_U5, m_U8, m_B10, m_B11 = 1.007828e+00, 1.599491e+01, 2.350441e+02,  2.380508e+02, 1.001294e+01, 1.100928e+01
m_O16H2O = m_O16

print('Analyse des densités atomiques')
# Melange 1 ficher Cell.x2m+
n_U5 =  7.6337E-04
n_U8 =  2.2438E-02
n_O16 =  4.6403E-02

## Fractions massiques ficher Cell.x2m+
wgt_U5 = 100*n_U5 * m_U5 / (n_U5*m_U5+n_U8*m_U8)
wgt_U8 = 100*n_U8 * m_U8 / (n_U5*m_U5+n_U8*m_U8)

w_U5 = 100*n_U5 * m_U5 / (n_U5*m_U5+n_U8*m_U8+n_O16*m_O16)
w_U8 = 100*n_U8 * m_U8 / (n_U5*m_U5+n_U8*m_U8+n_O16*m_O16)
w_O16 = 100*n_O16 * m_O16 / (n_U5*m_U5+n_U8*m_U8+n_O16*m_O16)

print(f'fractions massiques recaculées U5 et U8:  {wgt_U5:.3f} {wgt_U8:.3f}')
print(f'fractions massiques recaculées U5, U8, U16:  {w_U5:.3f} {w_U8:.3f} {w_O16:.3f}')
print('faction massique du module info w_U5 w_U8 w_O16 : 2.864854e+00  8.528450e+01  1.185064e+01')

print('Fin de traitement du mélange 1 : Fuel')

# Melange 6
n_H1H2O   = 4.8093E-02
n_O16H2O  = 2.4047E-02 
n_B10     = 5.1856E-06
n_B11     = 2.0873E-05 

NA = 0.602214 # Avogadro en 10E24

## Fractions massiques
den = (n_H1H2O*m_H1H2O+n_O16H2O*m_O16H2O+n_B10*m_B10+n_B11*m_B11)
wgt_H1H2O = n_H1H2O * m_H1H2O / den
wgt_O16H2O = n_O16H2O * m_O16H2O / den
wgt_B10 = n_B10 * m_B10 / den
wgt_B11 = n_B11 * m_B11 / den

print(f'fractions massiques recalculées H1, O16, B10, B11:  {wgt_H1H2O:.5e} {wgt_O16H2O:.5e} {wgt_B10:.5e} {wgt_B11:.5e}')

print(f'densite = {den/NA}')
print('Données Cell.xm2+ : w_H2O w_Bore 9.993500e-01 6.500483e-04')
print('Données Cell.xm2+ : w_HH2O w_OH2O w_B10H2O w_B11H2O 1.118424e-01 8.875076e-01 1.198103e-04 5.302380e-04 ')

print('Fin de traitement du mélange 6 : Modérateur')


## Calcul des propriétés de l'eau analogue à la procédure MixFuelCell.c2m
## H2O densite densmod
##Ajout  de bore avec une Cb exprimée en ppm
## densmod, Cb = 0.7, 1000.
## densmod = densmod (1+ Cb*1.Oe-6) proposition de correction de densité en fonction de la Cb

# ppmb = 650.0e-06
# pct_B10, pct_B11 = 0.1990 , 0.8010
# m_Bore =  pct_B10 * m_B10 + pct_B11 * m_B11  

# alpha = ppmb/(1-ppmb) # alpha = m_Bore/m_H2O = ppmb/(1-ppmb)
# m_mod = (m_H1H2O *2 + m_O16H2O)*(1+alpha)
# m_H2O = (m_H1H2O *2 + m_O16H2O)
# w_H2O = m_H2O/m_mod ## 1/(1+alpha)
# w_Bnat = 1-w_H2O ## alpha/(1+alpha)

# print(f'w_Bnat/w_H2O (ppm): {w_Bnat/w_H2O*1.0e6}')
# w_H   = 2*m_H1H2O/m_H2O
# w_O   = m_O16H2O/m_H2O
# w_B10 =  pct_B10* m_B10 / m_Bore
# w_B11 =  pct_B11* m_B11 / m_Bore

# print(f'fractions massiques H, O, B10 et B11:  {w_H2O*w_H*100} {w_H2O*w_O*100} {w_Bnat*w_B10*100} {w_Bnat*w_B11*100}')
# print(f'somme des fractions {100*(w_H2O*w_H+ w_H2O*w_O+w_Bnat*w_B10+w_Bnat*w_B11)}')


