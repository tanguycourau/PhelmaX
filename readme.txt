Travail réalisé dans le cadre de la nouvelle mouture du cours à partir de 2026

Sce : Directory Source : données de Xavier
Shells : Quelques script à partager
Tst : Tests réalisés à partir d'adapation des données sources de Xavier


- Install dragon Version 5.1 : https://merlin.polymtl.ca/version5.htm
  tagged version 5.1.0	tgz	2025/09/07 (initial release)

- Autre solution via l'AEN en utilisant git-lfs :
  + git clone https://git.oecd-nea.org/dragon/5.1.git
  + git clone https://git.oecd-nea.org/dragon/libraries.git
  +  git lfs pull -I l_endian/draglibendfb7r1SHEM295_v5p1.gz  



- Compilation à l'aide de la commande make dans les répertoires Dragon et Donjon
- Le code se trouve dans le répertoire : /home/tanguy/Codes/Version5.1
- Téléchargement de la Librarie https://merlin.polymtl.ca/libraries_v5p1.htm
- Libraire EndfB7 - Shem295 positionnée sous : /home/tanguy/DragonLib/draglibendfb7r1SHEM295_v5p1

- Adapatation de rundragon pour pointer vers les bibliothèques


