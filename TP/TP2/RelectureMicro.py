# -*-coding:utf-8 -*-
"""
parse_mcpomicro.py
------------------
Lecture du fichier texte DRAGON/DONJON format L_MULTICOMPO (micro)
et extraction des densités de noyaux par isotope vs burnup.

Les densités sont lues dans le bloc ISOTOPESDENS, dont l'ordre
suit la liste ISOTOPESUSED (lue une seule fois en début de fichier).

Usage :
  python parse_mcpomicro.py
"""

import re
import numpy as np
import matplotlib.pyplot as plt
import csv

# ─────────────────────────────────────────────
# PARAMÈTRES UTILISATEUR
# ─────────────────────────────────────────────
FILENAME = "EvoCellPas2temps.x2m+MCPOMICRO.txt"

# Groupes d'isotopes à tracer (les noms doivent correspondre exactement
# à ceux lus dans ISOTOPESUSED).  Modifier à volonté.
PLOT_GROUPS = {
    "Uranium"   : ["U234", "U235", "U236", "U238"],
    "Neptunium" : ["Np237", "Np238", "Np239"],
    "Plutonium" : ["Pu238", "Pu239", "Pu240", "Pu241", "Pu242"],
    "Américium" : ["Am241", "Am242", "Am242m", "Am243"],
    "Curium"    : ["Cm242", "Cm243", "Cm244", "Cm245", "Cm246"],
}

# ─────────────────────────────────────────────
# 1. LECTURE DU FICHIER
# ─────────────────────────────────────────────
def parse_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    # --- Burnup values (pval00000001) ---
    burnup = []
    for i, line in enumerate(lines):
        if "pval00000001" in line:
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("->"):
                burnup += [float(x) for x in lines[j].split()]
                j += 1
            break
    burnup = np.array(burnup)
    n_bu = len(burnup)
    print(f"  Pas de burnup : {n_bu}  ({burnup[0]:.0f} → {burnup[-1]:.0f} MWj/t)")

    # --- Liste ordonnée des isotopes (ISOTOPESUSED, première occurrence) ---
    isotope_list = []
    for i, line in enumerate(lines):
        if "ISOTOPESUSED" in line:
            # Sauter les lignes de métadonnées (entiers)
            j = i + 1
            raw_chars = ""
            while j <len(lines) and not lines[j].strip().startswith("->"):
                tok = lines[j].strip("\n")
                try:
                    [int(x) for x in tok.split()]
                    j += 1
                    continue
                except ValueError:
                    pass
                # Lignes de noms d'isotopes (peuvent être collées)
                raw_chars += f"{tok:<80}"
                j += 1
                # print(raw_chars)
            for start in range (0, len(raw_chars), 12):
                name = raw_chars[start:start + 12].strip()
                if name and not name.startswith("->"):
                    isotope_list.append(name)
            break

    # Filtrer les noms parasites (souvent *MAC*RES ou vides)
    isotope_list = [n for n in isotope_list if n]
    print(f"  Isotopes trouvés ({len(isotope_list)}) : {isotope_list}")

    n_iso = len(isotope_list)

    # --- Extraction des ISOTOPESDENS (une occurrence par burnup step) ---
    # On cherche tous les blocs ISOTOPESDENS
    densities_raw = []   # liste de tableaux numpy, un par step burnup

    i = 0
    while i < len(lines):
        if "ISOTOPESDENS" in lines[i] and not lines[i].strip().startswith("->"):
            # La ligne suivante contient les valeurs
            j = i + 1
            vals = []
            # print("OK")
            while j < len(lines) and not lines[j].strip().startswith("->"):
                try:
                    vals += [float(x) for x in lines[j].split()]
                    # print(vals)
                except ValueError:
                    pass
                j += 1
            if len(vals) == n_iso:
                densities_raw.append(np.array(vals))
            i = j
            continue
        i += 1

    print(f"  Occurrences ISOTOPESDENS trouvées : {len(densities_raw)}")

    # Garder uniquement les n_bu premiers (un par burnup)
    densities_raw = densities_raw[:n_bu]

    # Construction du tableau 2D  (n_bu, n_iso)
    dens = np.vstack(densities_raw)   # shape (n_bu, n_iso)

    return burnup, isotope_list, dens


# ─────────────────────────────────────────────
# 2. ACCÈS PAR NOM D'ISOTOPE
# ─────────────────────────────────────────────
def get_density(iso_name, isotope_list, dens):
    """Retourne le vecteur de densité (n_bu,) pour un isotope donné."""
    try:
        idx = isotope_list.index(iso_name)
        return dens[:, idx]
    except ValueError:
        return None


# ─────────────────────────────────────────────
# 3. AFFICHAGE RÉSUMÉ
# ─────────────────────────────────────────────
def print_summary(burnup, isotope_list, dens):
    bu_gwd = burnup / 1000.0
    print("\n" + "="*70)
    print(f"{'Isotope':<14} {'Densité BU=0':>16}  {'Densité BU_max':>16}  {'Max':>16}")
    print("-"*70)
    for k, iso in enumerate(isotope_list):
        d = dens[:, k]
        print(f"{iso:<14} {d[0]:>16.4e}  {d[-1]:>16.4e}  {d.max():>16.4e}")
    print("="*70)


# ─────────────────────────────────────────────
# 4. TRACÉS
# ─────────────────────────────────────────────
# Palette de couleurs distinctes
COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]

def plot_group(group_name, iso_names, burnup, isotope_list, dens, logy=True):
    """Trace les densités d'un groupe d'isotopes sur un même graphe."""
    bu_gwd = burnup / 1000.0
    fig, ax = plt.subplots(figsize=(8, 5))

    found = 0
    for k, iso in enumerate(iso_names):
        d = get_density(iso, isotope_list, dens)
        if d is None:
            print(f"  [WARNING] Isotope '{iso}' non trouvé dans la liste.")
            continue
        # Eviter les vecteurs nuls (semilogy interdit les zéros)
        if logy:
            mask = d > 0
            if mask.sum() > 1:
                ax.semilogy(bu_gwd[mask], d[mask], "o-", lw=1.5,
                            color=COLORS[k % len(COLORS)], label=iso)
            else:
                ax.semilogy(bu_gwd, d + 1e-30, "o-", lw=1.5,
                            color=COLORS[k % len(COLORS)], label=iso, alpha=0.3)
        else:
            ax.plot(bu_gwd, d, "o-", lw=1.5,
                    color=COLORS[k % len(COLORS)], label=iso)
        found += 1

    ax.set_xlabel("Burnup (GWj/t)", fontsize=12)
    ax.set_ylabel("Densité de noyaux (atomes/barn·cm)", fontsize=12)
    ax.set_title(f"Évolution des densités — {group_name}", fontsize=13)
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()

    fname = f"densites_{group_name.lower().replace(' ', '_')}.png"
    plt.savefig(fname, dpi=150)
    plt.show()
    print(f"  -> Sauvegardé : {fname}")


def plot_all_groups(burnup, isotope_list, dens):
    for group_name, iso_names in PLOT_GROUPS.items():
        plot_group(group_name, iso_names, burnup, isotope_list, dens, logy=True)
"""
    # Panneau résumé : tous les actinides sur 1 figure multi-sous-graphes
    groups = list(PLOT_GROUPS.items())
    n = len(groups)
    bu_gwd = burnup / 1000.0
    fig, axes = plt.subplots(1, n, figsize=(4.5 * n, 4.5))
    for ax, (gname, iso_names) in zip(axes, groups):
        for k, iso in enumerate(iso_names):
            d = get_density(iso, isotope_list, dens)
            if d is None:
                continue
            mask = d > 0
            if mask.sum() > 1:
                ax.semilogy(bu_gwd[mask], d[mask], "o-", lw=1.2,
                            color=COLORS[k % len(COLORS)], label=iso)
        ax.set_title(gname, fontsize=10)
        ax.set_xlabel("BU (GWj/t)", fontsize=9)
        ax.legend(fontsize=7, ncol=1)
        ax.grid(True, ls="--", alpha=0.4)
    axes[0].set_ylabel("Densité (at/barn·cm)", fontsize=9)
    plt.suptitle("Évolution des densités de noyaux vs Burnup", fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig("densites_panel_complet.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("  -> Sauvegardé : densites_panel_complet.png")
"""

# ─────────────────────────────────────────────
# 5. EXPORT CSV
# ─────────────────────────────────────────────
def export_csv(burnup, isotope_list, dens, filename="densites_isotopes.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["burnup_MWj_t"] + isotope_list
        writer.writerow(header)
        for i, bu in enumerate(burnup):
            row = [bu] + list(dens[i, :])
            writer.writerow(row)
    print(f"  -> CSV exporté : {filename}")


# ─────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\nLecture de : {FILENAME}")
    burnup, isotope_list, dens = parse_file(FILENAME)

    print_summary(burnup, isotope_list, dens)

    # Accès direct — exemples
    print("\nExemple d'accès direct aux tableaux numpy :")
    for iso in ["U235", "Pu239", "Pu241"]:
        d = get_density(iso, isotope_list, dens)
        if d is not None:
            print(f"  {iso:8s} : {d}")

    # Tracés
    print("\nGénération des tracés ...")
    plot_all_groups(burnup, isotope_list, dens)

    # Export
    # export_csv(burnup, isotope_list, dens)

    print("\nTerminé.")
