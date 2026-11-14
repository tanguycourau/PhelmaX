## Verification des densites
# Lecture du fichier Cell.x2m+ (2eme sortie du module lib)
 
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
print(f'fractions massiques U5 et U8:  {wgt_U5:.3f} {wgt_U8:.3f}')


# Melange 6
n_H1H2O   = 4.8093E-02
n_O16H2O  = 2.4047E-02 
n_B10     = 5.1856E-06
n_B11     = 2.0873E-05 

NA = 0.602214 # Avogadro en 10E24

## Fractions massiques
den = (n_H1H2O*m_H1H2O+n_O16H2O*m_O16H2O+n_B10*m_B10+n_B11*m_B11)
wgt_H1H2O = 100*n_H1H2O * m_H1H2O / den
wgt_O16H2O = 100*n_O16H2O * m_O16H2O / den
wgt_B10 = 100*n_B10 * m_B10 / den
wgt_B11 = 100*n_B11 * m_B11 / den

print(f'fractions massiques H1, O16, B10, B11:  {wgt_H1H2O:.5e} {wgt_O16H2O:.5e} {wgt_B10:.5e} {wgt_B11:.5e}')

print(f'densite = {den/NA}')





## Calcul des propriétés de l'eau

## H2O densite densmod
## Ajout  de bore avec une Cb exprimée en ppm

# densmod, Cb = 0.7, 1000.
# densmod = densmod (1+ Cb*1.Oe-6)


ppmB = 650.0
pct_B10, pct_B11 = 0.1990 , 0.8010
m_Bore =  pct_B10 * m_B10 + pct_B11 * m_B11  

m_mod = (m_H1H2O *2 + m_O16H2O)*(1+ppmB*1.0e-6)
m_H2O = (m_H1H2O *2 + m_O16H2O)
w_H2O = m_H2O/(m_mod)
w_Bnat = 1-w_H2O

print(f'w_Bnat/w_H2O (ppm): {w_Bnat/w_H2O*1.0e6}')
w_H   = 2*m_H1H2O/m_H2O
w_O   = m_O16H2O/m_H2O
w_B10 =  pct_B10* m_B10 / m_Bore
w_B11 =  pct_B11* m_B11 / m_Bore

print(f'fractions massiques H, O, B10 et B11:  {w_H2O*w_H} {w_H2O*w_O} {w_Bnat*w_B10} {w_Bnat*w_B11}')

print(f'somme des fractions {w_H2O*w_H+ w_H2O*w_O+w_Bnat*w_B10+w_Bnat*w_B11}')
