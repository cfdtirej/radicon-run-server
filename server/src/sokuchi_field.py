import math
# フィールド座標
# xa = 3
# ya = 18

def field_sokuchi(xa,ya):
    # ポールの位置（測地系直交座標）
    pole_x1 = 32303.41695	
    pole_y1 = -46486.44926
    pole_x2 = 32283.39407	
    pole_y2 = -46457.075
    pole_x3 = 32267.68525	
    pole_y3 = -46473.79497


    pole_x1_x2 = pole_y1 - pole_y2
    pole_y1_y2 = pole_x1 - pole_x2
    # digree = pole_x1_x2 / pole_y1_y2
    differ_radian = math.atan2(pole_y1_y2,pole_x1_x2) + math.atan2(ya,xa)

    length = math.sqrt(xa**2 + ya**2)

    xb = length * math.cos(differ_radian)
    yb = length * math.sin(differ_radian)

    xc = pole_y2 + xb
    yc = pole_x2 + yb

    return xc, yc


def sokuchi_field(X,Y):
    pole_x1 = 32303.41695	
    pole_y1 = -46486.44926
    pole_x2 = 32283.39407	
    pole_y2 = -46457.075
    pole_x3 = 32267.68525	
    pole_y3 = -46473.79497

    a = X - pole_x2
    b = Y - pole_y2

    pole_x1_x2 = pole_y1 - pole_y2
    pole_y1_y2 = pole_x1 - pole_x2
    
    differ_pole = math.atan2(pole_y1_y2,pole_x1_x2)
    differ_pole_digerr = math.degrees(differ_pole)
    differ = math.atan2(a, b)
    if differ <= 0:
        differ_digree = 360 + math.degrees(differ)
    else:
        differ_digree = math.degrees(differ)
    length = math.sqrt(a**2 + b**2)

    c = math.radians(differ_digree - differ_pole_digerr)
    d = length * math.cos(c)
    e = length * math.sin(c)

    return d, e
