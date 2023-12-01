"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


# I'm using a class here to make the formula in the actual functions a lot neater
class Brevet_Speed:
    def __init__(self, start_distance, end_distance, min_speed, max_speed):
        self.start_distance = start_distance
        self.end_distance = end_distance
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.gap = self.end_distance - self.start_distance


# make a list of brevet speeds
speeds = [
    Brevet_Speed(0, 200, 15, 34),
    Brevet_Speed(200, 400, 15, 32),
    Brevet_Speed(400, 600, 15, 30),
    Brevet_Speed(600, 1000, 11.428, 28),
    Brevet_Speed(1000, 1300, 13.333, 26),
]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600,
          or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if control_dist_km == 0:
        return brevet_start_time

    # case of the last brevet
    if control_dist_km >= brevet_dist_km:
        control_dist_km = brevet_dist_km

    dist_remaining = control_dist_km
    for speed in speeds:
        if dist_remaining > speed.gap:
            dist_remaining -= speed.gap
            brevet_start_time = brevet_start_time.shift(
                minutes=round((speed.gap / speed.max_speed) * 60)
            )
        else:
            brevet_start_time = brevet_start_time.shift(
                minutes=round((dist_remaining / speed.max_speed) * 60)
            )
            break

    return brevet_start_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    # Table { distance(km): time limit (mins) }
    final_limits = {200: 810, 300: 1200, 400: 1620, 600: 2400, 1000: 4500}

    if control_dist_km == 0:
        return brevet_start_time.shift(minutes=60)

    # case of the last brevet
    if control_dist_km >= brevet_dist_km:
        return brevet_start_time.shift(minutes=final_limits[brevet_dist_km])

    # special case for close brevets
    if control_dist_km <= 60:
        return brevet_start_time.shift(
            minutes=round(((control_dist_km / 20) * 60) + 60)
        )

    dist_remaining = control_dist_km
    for speed in speeds:
        if dist_remaining > speed.gap:
            dist_remaining -= speed.gap
            brevet_start_time = brevet_start_time.shift(
                minutes=round((speed.gap / speed.min_speed) * 60)
            )
        else:
            brevet_start_time = brevet_start_time.shift(
                minutes=round((dist_remaining / speed.min_speed) * 60)
            )
            break

    return brevet_start_time
