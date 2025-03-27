# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module contains the different parameters sets for each behavior. """

"""
主要定义汽车限速(max_speed)、与牵扯保持的安全时间(safety_time，基于ttc)，与牵扯最小安全距离(braking_distance)等安全相关参数
agressive的车相对normal的车速来说更快，跟车更近
"""
class Cautious(object):
    """Class for Cautious agent."""
    max_speed = 40
    speed_lim_dist = 6
    speed_decrease = 12
    safety_time = 3
    min_proximity_threshold = 12
    braking_distance = 6
    overtake_counter = -1
    tailgate_counter = 0


class Normal(object):
    """Class for Normal agent."""
    max_speed = 50
    speed_lim_dist = 3
    speed_decrease = 10
    safety_time = 3
    min_proximity_threshold = 10
    braking_distance = 5
    overtake_counter = 0
    tailgate_counter = 0


class Aggressive(object):
    """Class for Aggressive agent."""
    max_speed = 70
    speed_lim_dist = 1
    speed_decrease = 8
    safety_time = 3
    min_proximity_threshold = 8
    braking_distance = 4
    overtake_counter = 0
    tailgate_counter = -1
