2026/11/15
- Ajout du fichier EvoAssParamTfDmod.x2m pour faire une boucle en Tf et Dmod
- Ajout de la procédure  MixFuelCellD.c2m appelée par EvoAssParamTfDmod.x2m
  Note : la procédure s'inspire de la proc MixFuellCell du TP1 qui utilise
  le module INFO. 
- En sortie le fichier EvoAssParamTfDmod.x2m+MCPOMACROTFuel.txt donne une
  tabulation en BU (26 pas), Tfuel (3 pas) et Dmod (2 pas) soit 156 points.
  Preuve : `grep -i effective EvoAssParamTfDmod.x2m+MCPOMACROTFuel.txt | wc -l`
