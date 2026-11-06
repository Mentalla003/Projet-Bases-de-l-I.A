import math

angles = [30, 40, 50, 60, 70]
positions = [2000, 2500, 3000, 3500]

for a1 in angles:
   for y in positions:

       # Calcul de l'angle après le virement
       a2 = math.degrees(math.atan(y * math.tan(math.radians(a1)) / (5000-y)))

       # Calcul des distances
       distance1 = y / math.cos(math.radians(a1))
       distance2 = (4000-y) / math.cos(math.radians(a2))
       distance3 = 1000 / math.cos(math.radians(a2))

       # Calcul des vitesses
       V1 = 10 - (120-a1)**2 / 1000
       V2 = 10 - (120-a2)**2 / 1000
       V3 = 8 - (120-a2)**2 / 1250

       # Calcul du temps total
       temps = distance1/V1 + distance2/V2 + distance3/V3 + 10

       print("Angle de départ :", a1)
       print("Coordonnée en y du point de virement :", y, "m")
       minutes = int(temps // 60)
       secondes = int(temps % 60)

       print(f"Temps total : {minutes} min {secondes} s")
       print("--------------------------")
