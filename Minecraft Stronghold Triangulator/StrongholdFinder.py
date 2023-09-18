import math

def main():
    # Coords and angle for 1st throw
    p1 = tuple(map(float, input("Position 1: ").split(" ")))
    a1 = float(input("Angle 1: "))
    
    # Coords and angle for 2nd throw
    p2 = tuple(map(float, input("Position 2: ").split(" ")))
    a2 = float(input("Angle 2: "))
    
    # Gradient of each throw for linear line
    m1 = math.tan(a1 * math.pi / 180 - math.pi/2)
    m2 = math.tan(a2 * math.pi / 180 - math.pi/2)
    
    # Y intercept for each linear line
    c1 = p1[1] - m1 * p1[0]
    c2 = p2[1] - m2 * p2[0]
    
    # Stronghold coords prediction, distance prediction and nether coords prediction 
    stronghold = (round((c1 - c2) / (m2 - m1)), round((c1 * m2 - c2 * m1) / (m2 - m1)))
    distance = round(math.sqrt(((stronghold[0] - p1[0]) ** 2) + ((stronghold[1] - p1[1]) ** 2)))
    nether = (round(stronghold[0] / 8), round(stronghold[1] / 8))
    
    print(f"\n\n\nStronghold is near: X = {stronghold[0]}, Z= {stronghold[1]}")
    print(f"\nDistance: {distance}m")
    print(f"\nNether portal coordinates: X = {nether[0]}, Z = {nether[1]}\n")

if __name__ == "__main__":
    main()