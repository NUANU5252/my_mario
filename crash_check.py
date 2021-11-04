
def collision_check(x1, y1, x2, y2, x3, y3, x4, y4):
    direction_of_collision = 0
    #   직사각형 1(1,2)가 5 에 있을때 직사각형 2(3,4) 의 위치
    #   7   8   9
    #   4   5   6
    #   1   2   3
    #   0 : 충돌하지 않음
    #   5 : 오류 -- 오브젝트의 속도가 너무 빠르니까 조정 필요
    delta_x1 = x2 - x1
    delta_y1 = y2 - y1
    center_of_rect_1_x = x1 + delta_x1 / 2
    center_of_rect_1_y = y1 + delta_y1 / 2

    delta_x2 = x4 - x3
    delta_y2 = y4 - y3
    center_of_rect_2_x = x3 + delta_x2/2
    center_of_rect_2_y = y3 + delta_y2/2
    if(x1 < center_of_rect_2_x & center_of_rect_2_x < x2):
        if (y1 < center_of_rect_2_y & center_of_rect_2_y < y2):
            return 5

    if x1 < x3 & x3 < x2:
        if center_of_rect_2_x >= x2:
            if (center_of_rect_2_y - y2)/(center_of_rect_2_x - x2) > delta_y2 / delta_x2:
                return 8
            elif(center_of_rect_2_y - y2)/(center_of_rect_2_x - x2) < -(delta_y2 / delta_x2):
                return 2
            else:
                return 6
        elif center_of_rect_2_x <= x1:
            pass # 불가능하다
    if x1 < x4 & x4 < x2:
        if center_of_rect_2_x >= x2:
            if (center_of_rect_2_y - y2)/(center_of_rect_2_x - x2) > delta_y2 / delta_x2:
                return 8
            elif(center_of_rect_2_y - y2)/(center_of_rect_2_x - x2) < -(delta_y2 / delta_x2):
                return 2
            else:
                return 6
        elif center_of_rect_2_x <= x1:
            pass
    else:
        return 0


if __name__ == '__main__':
  pass