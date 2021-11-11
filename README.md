# MBSE-traffic-simulation

Simple traffic simulator.


## Creating simple simulation
```python
from sim import Scheduler

highway_length = 1             # in kilometers
num_of_lanes = 4               # number of lanes
average_drivers_mood = 0.85    # how propable it is that driver will not perform any action
sim_time = 20                  # in minutes
inflow = 10                    # cars per minute
speed_limit = 60               # kilemeters per hour

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit,
                        step_time = 1)

results, results_dict1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)
scheduler.safe_to_file("sim1")
```

## Visualizing output

```python
from animation import createAnimation

createAnimation(
    [results_dict1],                # results from simulation - multiple can provided for compering simulations
    animation_speed= 20,            # animation speed
    reduce_data = 1,                # howmuch reduce the data, usefull in large datasets
    highway_length=highway_length,  # length in kilometers
    num_of_lanes=[num_of_lanes]     
    )

```

## Results

**Basecases**

![basecase](/static/basecase.gif)

**Other**

![testcase](/static/testcase.gif)

