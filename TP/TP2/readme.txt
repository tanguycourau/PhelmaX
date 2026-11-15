2026/11/15
- Ajout du fichier EvoAssParamDmodTf.x2m pour faire une boucle en Tf et Dmod
- Ajout de la procédure  MixFuelCellD.c2m appelée par EvoAssParamTfDmod.x2m
  Note : la procédure s'inspire de la proc MixFuellCell du TP1 qui utilise
  le module INFO. 
- En sortie le fichier EvoAssParamDmodTf.x2m+MCPOMACRODmodTFuel.txt donne une
  tabulation en BU (26 pas), Tfuel (3 pas) et Dmod (2 pas) soit 156 points.
  Preuve : `grep -i infinity EvoAssParamDmodTf.x2m+MCPOMACRODmodTFuel.txt | wc -l`



Analyse du fichier résultat : EvoAssParamTfDmod.x2m+MCPOMACRODmodTFuel.txt 
 - PARKEY : burnup                 Dmod            T-FUEL 
 - PVAL   : #1/26 [0.0 79200.]     #2/2 [0.7 1.0]  #3/3 [300. 900. 1500.]    


Fichier kinf :
grep -i infinity -A1 EvoAssParamDmodTf.x2m+MCPOMACRODmodTFuel.txt  | grep -v INF > kinf.txt
