import math
#this is a routine for angular stealthy-shmealthy FOV behaviour.

def is_point_in_sector(from_x, from_y, look_x, look_y, target_x, target_y, sector_angle):
    half_of_sector_angle = (sector_angle / 2) * math.pi / 180
    centered_x, centered_y = target_x - from_x, target_y - from_y
    looking_angle = math.atan2(look_y, look_x)
    taget_angle = math.atan2(centered_y, centered_x)
    if centered_x < 0 and centered_y < 0 and look_y >= 0:
        taget_angle += 2 * math.pi
    if looking_angle - half_of_sector_angle <= taget_angle <= looking_angle + half_of_sector_angle:
        return True
    return False
