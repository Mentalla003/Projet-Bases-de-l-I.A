import math
import random

# ----------------------------------------------------------------------------
# Paramètres du problème
# ----------------------------------------------------------------------------
Y_ARRIVEE = 5000.0
Y_SEUIL = 4000.0          # au-delà, vent plus faible
T_VIREMENT = 10.0         # pénalité de virement (s)
ALPHA_MIN, ALPHA_MAX = 20.0, 89.0
Y_V_MIN, Y_V_MAX = 1.0, 4999.0
COUT_INFINI = 1e9


# ----------------------------------------------------------------------------
# Modèle physique
# ----------------------------------------------------------------------------
def vitesse(alpha: float, fort: bool) -> float:
    """Vitesse (m/s) selon l'angle alpha (deg) ; fort=True si y < 4000."""
    if alpha <= 20:
        return 0.0
    if fort:
        return -((120 - alpha) ** 2) / 1000 + 10
    return -((120 - alpha) ** 2) / 1250 + 8


def temps_branche(alpha: float, y_a: float, y_b: float) -> float:
    """Temps pour aller de y_a à y_b (y_a < y_b) à angle alpha constant."""
    v_fort = vitesse(alpha, True)
    v_faible = vitesse(alpha, False)
    dy_fort = max(0.0, min(y_b, Y_SEUIL) - y_a)
    dy_faible = max(0.0, y_b - max(y_a, Y_SEUIL))
    c = math.cos(math.radians(alpha))
    t = 0.0
    if dy_fort > 0:
        if v_fort <= 0:
            return COUT_INFINI
        t += dy_fort / c / v_fort
    if dy_faible > 0:
        if v_faible <= 0:
            return COUT_INFINI
        t += dy_faible / c / v_faible
    return t


def calcule_cout_vecteur(alpha: float, y_v: float):
    """Retourne (arrive: bool, cout: float, alpha2: float)."""
    x_v = y_v * math.tan(math.radians(alpha))
    reste = Y_ARRIVEE - y_v
    alpha2 = math.degrees(math.atan2(x_v, reste))

    t1 = temps_branche(alpha, 0.0, y_v)
    t2 = temps_branche(alpha2, y_v, Y_ARRIVEE)
    if t1 >= COUT_INFINI or t2 >= COUT_INFINI:
        return (False, COUT_INFINI, alpha2)
    return (True, t1 + T_VIREMENT + t2, alpha2)


# ----------------------------------------------------------------------------
# Algorithme génétique
# ----------------------------------------------------------------------------
def borne(v):
    alpha, y_v = v
    return (min(max(alpha, ALPHA_MIN), ALPHA_MAX),
            min(max(y_v, Y_V_MIN), Y_V_MAX))


def creer_individu():
    return (random.uniform(ALPHA_MIN, ALPHA_MAX),
            random.uniform(Y_V_MIN, Y_V_MAX))


def evaluer(v):
    return calcule_cout_vecteur(*v)[1]


def mutation(v, amplitude):
    """Modifie UNE des deux propriétés (au hasard) de +-amplitude (relatif)."""
    alpha, y_v = v
    facteur = 1 + random.uniform(-amplitude, amplitude)
    if random.random() < 0.5:
        alpha *= facteur
    else:
        y_v *= facteur
    return borne((alpha, y_v))


def croisement(v1, v2):
    """Direction de l'un, position de virement de l'autre."""
    return borne((v1[0], v2[1])) if random.random() < 0.5 else borne((v2[0], v1[1]))


def algo_genetique(n=1000, n_survivants=100, n_iter=50,
                   amp_init=0.03, decroissance=True,
                   part_croisement=0.5, verbose=True):
    population = [creer_individu() for _ in range(n)]
    historique = []

    for it in range(n_iter):
        population.sort(key=evaluer)
        meilleur = population[0]
        historique.append(evaluer(meilleur))
        if verbose and (it % 5 == 0 or it == n_iter - 1):
            print(f"Itération {it:3d} | meilleur : alpha={meilleur[0]:.2f}°, "
                  f"y_v={meilleur[1]:.1f} m, temps={historique[-1]:.2f} s")

        survivants = population[:n_survivants]
        amp = amp_init * (1 - it / n_iter) + 0.001 if decroissance else amp_init

        population = list(survivants)
        while len(population) < n:
            if random.random() < part_croisement and n_survivants >= 2:
                p1, p2 = random.sample(survivants, 2)
                population.append(croisement(p1, p2))
            else:
                population.append(mutation(random.choice(survivants), amp))

    population.sort(key=evaluer)
    return population[0], historique


def afficher_resultat(v):
    alpha, y_v = v
    _, cout, alpha2 = calcule_cout_vecteur(alpha, y_v)
    x_v = y_v * math.tan(math.radians(alpha))
    print("\n=== Meilleure solution ===")
    print(f"Angle 1re branche : {alpha:.2f}°")
    print(f"Point de virement : x = {x_v:.1f} m, y = {y_v:.1f} m")
    print(f"Angle 2e branche  : {alpha2:.2f}°")
    print(f"Temps total       : {cout:.2f} s ({cout / 60:.2f} min)")


def sauver_csv(historique, nom="convergence_voilier.csv"):
    """Sauvegarde la convergence dans un CSV (ouvrable dans Excel pour tracer la courbe)."""
    with open(nom, "w", encoding="utf-8") as f:
        f.write("iteration;meilleur_temps_s\n")
        for i, t in enumerate(historique):
            f.write(f"{i};{t:.4f}\n")
    print(f"Convergence sauvegardée dans {nom}")


# ----------------------------------------------------------------------------
# Expériences (partie « Amélioration » du TP)
# ----------------------------------------------------------------------------
def experiences(n_essais=10):
    print("\n=== Impact du nombre de survivants et de la décroissance ===")
    for surv in (5, 10, 25, 50):
        for decr in (False, True):
            res = []
            for _ in range(n_essais):
                _, h = algo_genetique(n=100, n_survivants=surv, n_iter=15,
                                      decroissance=decr, verbose=False)
                res.append(h[-1])
            print(f"survivants={surv:3d} | décroissance={decr!s:5} | "
                  f"temps moyen={sum(res)/len(res):.3f} s | min={min(res):.3f} s")


if __name__ == "__main__":
    random.seed(42)
    meilleur, hist = algo_genetique()
    afficher_resultat(meilleur)
    sauver_csv(hist)
    experiences()