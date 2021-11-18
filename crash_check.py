def collide(a, b, use_f=False):
    if use_f:
        left_a, bottom_a, right_a, top_a = a.get_fbb()
    else:
        left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_direction(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    delta_a_x = right_a - left_a
    delta_a_y = top_a - bottom_a
    gradient_a = delta_a_y / delta_a_x
    # 중점이 b의 밖에 있는 경우
    if a.x > right_b and top_b + gradient_a * (a.x - right_b) >= a.y >= bottom_b - gradient_a * (a.x - right_b):
        return 6
    elif a.x < left_b and top_b + gradient_a * (left_b - a.x) >= a.y >= bottom_b - gradient_a * (left_b - a.x):
        return 4
    elif a.y > top_b:   # and a.y > top_b + gradient_a * (a.x - right_b) and a.y > top_b + gradient_a * (left_b - a.x):
        return 8        # elif니까 위의 코드는 필요 없을듯?
    else:
        return 2
    # elif a.y < bottom_b:
    #     return 2
    # 중점이 b의 안에 있는 경우
    # else:
    #     return 5
