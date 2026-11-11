"""
Relecture.py
------------------
Lecture du fichier texte DRAGON/DONJON format L_MULTICOMPO
et extraction des grandeurs neutroniques par pas de burnup.
 
Grandeurs extraites (par groupe d'énergie, 2 groupes ici) :
  NFTOT, NG, N2N, NTOT0, NUSIGF, TRANC,
  K-EFFECTIVE, K-INFINITY, B2 B1HOM
 
Usage :
  python Relecture.py
  -> affiche un résumé et génère les tracés matplotlib
  -> A changer : FILENAME
  -> A Tracer : SCALAR_KEYS 
"""
 
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
 
# ─────────────────────────────────────────────
# 1. PARAMÈTRES
# ─────────────────────────────────────────────
FILENAME = "EvoAssParamCb.x2m+MCPOMACRO.txt"
 
# Grandeurs scalaires (1 valeur par pas de burnup)
# SCALAR_KEYS = ["K-EFFECTIVE", "K-INFINITY", "B2  B1HOM"]
SCALAR_KEYS = ["K-EFFECTIVE", "K-INFINITY"]
 
# Grandeurs vectorielles (2 valeurs = groupe rapide + groupe thermique)
# VECTOR_KEYS = [
#    "NFTOT", "NG", "N2N", "N3N", "N4N", "NA", "NP",
#    "NTOT0", "NUSIGF", "TRANC", "NWT0", "STRD",
#    "CHI", "H-FACTOR", ]
VECTOR_KEYS = ["NFTOT", "NG", "N2N", "NUSIGF"]
 
# ─────────────────────────────────────────────
# 2. LECTURE ET PARSING
# ─────────────────────────────────────────────
def read_blocks(filename):
    """
    Lit le fichier et retourne la liste des blocs sous forme de dict.
    Chaque bloc correspond à un pas de burnup (un ensemble CALCULATIONS).
    """
 
    with open(filename, "r") as f:
        lines = f.readlines()
 
    # Récupération des valeurs de burnup (pval00000001)
    burnup_values = []
    for i, line in enumerate(lines):
        if "pval00000001" in line:
            j = i + 1
            vals = []
            while j < len(lines) and not lines[j].strip().startswith("->"):
                vals += [float(x) for x in lines[j].split()]
                j += 1
            burnup_values = vals
            break
 
    n_burnup = len(burnup_values)
    print(f"  Nombre de pas de burnup trouvés : {n_burnup}")
    print(f"  Burnup (MWj/t) : {burnup_values[:5]} ...")
 
    # Initialisation des conteneurs
    data = defaultdict(list)   # key -> liste de tableaux numpy (un par pas)
    current_key = None
    collect = False
    buffer = []
 
    # Compteurs pour repérer les blocs de calcul
    calc_step = -1  # incrémenté à chaque nouveau bloc CALCULATIONS
    in_calc = False
 
    # Ensemble des clés à extraire
    all_keys = set(SCALAR_KEYS) | set(VECTOR_KEYS)
 
    i = 0
    while i < len(lines):
        line = lines[i].strip()
 
        # Détection début bloc CALCULATIONS (niveau 4)
        if re.match(r"->.*<-", line):
            # Fin de collecte si en cours
            if collect and current_key and buffer:
                vals = np.array([float(x) for x in " ".join(buffer).split()])
                data[current_key].append(vals)
                buffer = []
                collect = False
                current_key = None
 
            # Détection du début d'un nouveau step de calcul :
            # le marqueur "->       5       0      99       0" indique un pas
            if re.search(r"->\s+5\s+0\s+99\s+0", line):
                in_calc = False
 
            i += 1
            continue
 
        # Détection d'une clé connue
        stripped = line.rstrip()
        if stripped in all_keys:
            # Fin de la collecte précédente
            if collect and current_key and buffer:
                vals = np.array([float(x) for x in " ".join(buffer).split()])
                data[current_key].append(vals)
                buffer = []
 
            current_key = stripped
            collect = True
            i += 1
            continue
 
        # Collecte des valeurs numériques
        if collect:
            # Ligne de métadonnées (->...<-)  déjà traitée plus haut
            # On ignore les lignes non numériques
            try:
                _ = [float(x) for x in line.split()]
                buffer.append(line)
            except ValueError:
                # Fin naturelle du bloc numérique : on sauvegarde
                if buffer and current_key:
                    vals = np.array([float(x) for x in " ".join(buffer).split()])
                    data[current_key].append(vals)
                    buffer = []
                collect = False
                current_key = None
 
        i += 1
 
    # Dernière collecte éventuelle
    if collect and current_key and buffer:
        vals = np.array([float(x) for x in " ".join(buffer).split()])
        data[current_key].append(vals)
 
    return burnup_values, dict(data)
 
 
# ─────────────────────────────────────────────
# 3. MISE EN FORME NUMPY
# ─────────────────────────────────────────────
def build_arrays(burnup_values, raw_data):
    """
    Construit des tableaux numpy 2D :
      - shape (n_burnup,)       pour les scalaires
      - shape (n_burnup, n_grp) pour les vecteurs groupes
    """
    n = len(burnup_values)
    arrays = {}
    burnup = np.array(burnup_values)
 
    for key, list_of_arrays in raw_data.items():
        arr = np.array(list_of_arrays)  # shape (n_occurrences, n_vals)
 
        # Garder seulement les n premiers (un par burnup)
        arr = arr[:n]
 
        if arr.shape[1] == 1:
            arrays[key] = arr[:, 0]          # (n,)
        else:
            arrays[key] = arr                # (n, n_grp)
 
    return burnup, arrays
 
 
# ─────────────────────────────────────────────
# 4. AFFICHAGE RÉSUMÉ
# ─────────────────────────────────────────────
def print_summary(burnup, arrays):
    print("\n" + "="*60)
    print("RÉSUMÉ DES DONNÉES EXTRAITES")
    print("="*60)
    print(f"{'Clé':<20} {'Shape':>12}  {'Min':>14}  {'Max':>14}")
    print("-"*60)
    for key, arr in sorted(arrays.items()):
        print(f"{key:<20} {str(arr.shape):>12}  {arr.min():>14.4e}  {arr.max():>14.4e}")
    print("="*60)
 
 
# ─────────────────────────────────────────────
# 5. TRACÉS
# ─────────────────────────────────────────────
def plot_all(burnup, arrays):
    bu = burnup / 1000.0  # conversion MWj/t -> GWj/t pour l'affichage
 
    # --- K-EFFECTIVE et K-INFINITY ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, key in zip(axes, ["K-EFFECTIVE", "K-INFINITY"]):
        if key in arrays:
            ax.plot(bu, arrays[key], "o-", lw=1.5)
            ax.set_xlabel("Burnup (GWj/t)")
            ax.set_ylabel(key)
            ax.set_title(key)
            ax.grid(True, ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("keff_kinf.png", dpi=150)
    plt.show()
    print("  -> Sauvegardé : keff_kinf.png")

    # --- Sections efficaces NFTOT, NG, N2N par groupe ---
    for key in ["NFTOT", "NG", "N2N"] :
        if key not in arrays:
            continue
        arr = arrays[key]
        if arr.ndim == 1:
            continue
        n_grp = arr.shape[1]
        fig, ax = plt.subplots(figsize=(7, 4))
        for g in range(n_grp):
            label = f"Groupe {g+1} ({'rapide' if g == 0 else 'thermique'})"
            ax.semilogy(bu, arr[:, g], "o-", lw=1.5, label=label)
        ax.set_xlabel("Burnup (GWj/t)")
        ax.set_ylabel(f"{key} (cm⁻¹)")
        ax.set_title(f"Section efficace {key} vs Burnup")
        ax.legend()
        ax.grid(True, ls="--", alpha=0.5)
        plt.tight_layout()
        fname = f"{key.lower()}_vs_burnup.png"
        plt.savefig(fname, dpi=150)
        plt.show()
        print(f"  -> Sauvegardé : {fname}")
"""
    # --- B2 ---
    if "B2  B1HOM" in arrays:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(bu, arrays["B2  B1HOM"], "o-", lw=1.5, color="darkgreen")
        ax.axhline(0, color="k", lw=0.8, ls="--")
        ax.set_xlabel("Burnup (GWj/t)")
        ax.set_ylabel("B² (cm⁻²)")
        ax.set_title("Laplacien critique B² vs Burnup")
        ax.grid(True, ls="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("b2_vs_burnup.png", dpi=150)
        plt.show()
        print("  -> Sauvegardé : b2_vs_burnup.png")
 
    # --- Panneau multi-grandeurs (groupe thermique) ---
    keys_panel = [k for k in ["NFTOT", "NG", "NUSIGF", "STRD"] if k in arrays
                  and arrays[k].ndim == 2]
    if keys_panel:
        n_plots = len(keys_panel)
        fig, axes = plt.subplots(1, n_plots, figsize=(4 * n_plots, 4))
        if n_plots == 1:
            axes = [axes]
        for ax, key in zip(axes, keys_panel):
            ax.semilogy(bu, arrays[key][:, 1], "s-", lw=1.5, color="tomato",
                        label="Thermique")
            ax.semilogy(bu, arrays[key][:, 0], "o-", lw=1.5, color="steelblue",
                        label="Rapide")
            ax.set_xlabel("Burnup (GWj/t)")
            ax.set_ylabel(key)
            ax.set_title(key)
            ax.legend(fontsize=8)
            ax.grid(True, ls="--", alpha=0.5)
        plt.suptitle("Sections efficaces macroscopiques vs Burnup", y=1.02)
        plt.tight_layout()
        plt.savefig("panel_xs_vs_burnup.png", dpi=150, bbox_inches="tight")
        plt.show()
        print("  -> Sauvegardé : panel_xs_vs_burnup.png")
 """
 
# ─────────────────────────────────────────────
# 6. EXPORT CSV (optionnel)
# ─────────────────────────────────────────────
def export_csv(burnup, arrays, filename="resultats_mcpo.csv"):
    """
    Exporte toutes les données dans un fichier CSV.
    Les grandeurs vectorielles sont séparées par groupe (_G1, _G2 ...).
    """
    import csv
    header = ["burnup_MWj_t"]
    rows_data = [burnup]
 
    for key in sorted(arrays.keys()):
        arr = arrays[key]
        if arr.ndim == 1:
            header.append(key)
            rows_data.append(arr)
        else:
            for g in range(arr.shape[1]):
                header.append(f"{key}_G{g+1}")
                rows_data.append(arr[:, g])
 
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(burnup)):
            writer.writerow([col[i] for col in rows_data])
 
    print(f"  -> CSV exporté : {filename}")
 
 
# ─────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\nLecture du fichier : {FILENAME}")
    burnup_vals, raw = read_blocks(FILENAME)
 
    burnup, arrays = build_arrays(burnup_vals, raw)
 
    print_summary(burnup, arrays)
 
    # Accès direct aux tableaux numpy — exemples :
    print("\nExemples d'accès direct :")
    if "K-INFINITY" in arrays:
        print(f"  K-INFINITY  (shape={arrays['K-INFINITY'].shape}) :")
        print(f"    {arrays['K-INFINITY']}")
    if "NFTOT" in arrays:
        print(f"  NFTOT       (shape={arrays['NFTOT'].shape}) :")
        print(f"    Groupe rapide    : {arrays['NFTOT'][:, 0]}")
        print(f"    Groupe thermique : {arrays['NFTOT'][:, 1]}")
 
    # Tracés
    print("\nGénération des tracés ...")
    plot_all(burnup, arrays)
 
    # Export CSV
    # export_csv(burnup, arrays)
 
    print("\nTerminé.")
