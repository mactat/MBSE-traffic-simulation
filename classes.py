

class Driver:
    def __init__(self, reaction_time, lane_change_behavior=None, exit_behavior=None, breaking_behavior=None):
        self.reaction_time = reaction_time
        self.lane_change_behavior = lane_change_behavior
        self.exit_behavior = exit_behavior
        self.breaking_behavior = breaking_behavior


class Coms:
    def __init__(self, radius, delay):
        self.range = radius
        self.delay = delay


class Car(Driver, Coms):
    def __init__(self, acc, breaking, coms_available=False):
        self.acc = acc
        self.breaking = breaking
        self.coms_available = coms_available


class Lane:
    def __init__(self, no):
        self.no = no
        self.cars = []


class Highway:
    def __init__(self, no_lanes, speed_limit, length):
        self.lanes = []
        for i in range(no_lanes):
            self.lanes.append(Lane(i))
        self.speed_limit = speed_limit
        self.length = length

