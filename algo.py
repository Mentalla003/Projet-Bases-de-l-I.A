import math

# ---- vitesse du bateau (formule du sujet) ----
def vitesse(alpha, y):
    if y < 4000:
        return 10 - (120 - alpha) ** 2 / 1000
    return 8 - (120 - alpha) ** 2 / 1250

# ---- temps d'une branche : le bateau monte de y_debut à y_fin avec l'angle alpha ----
def temps_branche(y_debut, y_fin, alpha):
    cos_a = math.cos(math.radians(alpha))
    montee_bas = max(0, min(y_fin, 4000) - y_debut)   # partie sous y = 4000
    montee_haut = (y_fin - y_debut) - montee_bas      # partie au-dessus de y = 4000
    dist_bas = montee_bas / cos_a                     # d = dy / cos(alpha)
    dist_haut = montee_haut / cos_a
    return dist_bas / vitesse(alpha, 0) + dist_haut / vitesse(alpha, 4000)   # t = d / V

# ---- temps total pour un angle alpha1 et un virement à la hauteur yt ----
def temps_total(alpha1, yt):
    xt = yt * math.tan(math.radians(alpha1))                 # position x du virement
    alpha2 = math.degrees(math.atan(xt / (5000 - yt)))       # angle de la 2e branche
    if alpha2 <= 20:
        return None                                          # pas possible (vitesse nulle)
    return temps_branche(0, yt, alpha1) + 10 + temps_branche(yt, 5000, alpha2)

# ---- TABLEAU : on change les angles et les hauteurs de virement ----
angles = [30, 40, 45, 50, 53, 54, 55, 60, 70]
hauteurs = [1000, 2000, 2500, 3000, 4000]

print("Temps total (en secondes)")
print("alpha1 \\ yt |" + "".join("%9d" % h for h in hauteurs))
print("-" * (13 + 9 * len(hauteurs)))
meilleur = (999999, 0, 0)
for a in angles:
    ligne = "%8d°    |" % a
    for h in hauteurs:
        t = temps_total(a, h)
        if t is None:
            ligne += "%9s" % "-"
        else:
            ligne += "%9.0f" % t
            if t < meilleur[0]:
                meilleur = (t, a, h)
    print(ligne)

print("\nMeilleur du tableau : %.0f s avec alpha1 = %d° et yt = %d m" % meilleur)