from random import randint

def captcha_challenge():
    x = [randint(0, 50) for i in range(3)]
    p1 = f"{x[0]} + {x[1]} + {x[2]} = "
    p2 = str(sum(x))
    return p1, p2

