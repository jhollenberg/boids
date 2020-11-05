import random
import math

m1 = 10
m2 = m1**3
v1 = 0
v2 = round(random.uniform(-2, 0), 4)


def quadratic(a, b, c):
    ans1 = round(-(-b + math.sqrt(b ** 2 - (4 * a * c)))/(2 * a), 4)
    ans2 = round(-(-b - math.sqrt(b ** 2 - (4 * a * c)))/(2 * a), 4)
    if ans1 in (v1, v2):
        return ans2
    elif ans2 in (v1, v24):
        return ans1
    else:
        print("problem")
        return


def collide():
    a = m1 * m2 + m2**2
    b = 2 * m2**2 * v2 + 2 * m2 * v1
    c = v1**2 + m2**2 * v2**2 + 2 * v1 * m2 * v2 - m1**2 * v1**2 - m1 * m2 * v2**2
    new_v1 = quadratic(a, b, c)
    new_v2 = v1 + v2 - new_v1
    return new_v1, new_v2


v1, v2 = collide()