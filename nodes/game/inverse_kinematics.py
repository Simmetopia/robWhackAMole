import math


def invkin(x, y, z):
    """
    Python implementation af invers kinematik for crustcrawler-robotten.
    Input: x,y og z positioner
    Output: vinkler for hvert led: q1,q2,q3,q4
    """
    d1 = 165  # hoejden fra bordplade til 2. led.
    a1 = 0  # forskydningen langs y-aksen mellem 1. og 2. led.
    a2 = 170  # afstanden mellem 2. og 3. led.
    d4 = 230  # afstanden fra 3. led og ud til griberens gribepunkts inkl. 4. led.

    q1 = math.atan2(y, x)
    r2 = (x - a1 * math.cos(q1)) ** 2 + (y - a1 * math.sin(q1)) ** 2
    s = (z - d1)
    D = (r2 + s ** 2 - a2 ** 2 - d4 ** 2) / (2 * a2 * d4)
    q3 = math.atan2(-math.sqrt(1 - D ** 2), D)
    q2 = math.atan2(s, math.sqrt(r2)) - math.atan2(d4 * math.sin(q3), a2 + d4 * math.cos(q3)) - math.pi / 2
    q4 = 0  # Der tages ikke hoejde for griberens rotation i denne opgave.

    return q1, q2, q3, q4
