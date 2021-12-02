[![Build Status](https://dev.azure.com/s202609/Other/_apis/build/status/MBSE-traffic-simulation?branchName=master)](https://dev.azure.com/s202609/Other/_build/latest?definitionId=9&branchName=master)
# MBSE-traffic-simulation

Simple traffic simulator.
## Quickstart
```python
git clone git@github.com:mactat/MBSE-traffic-simulation.git
cd ./MBSE-traffic-simulation/
pip3 install -r requirements.txt
cd ./src

# For example with animation
python3 example.py

# For headless
cd ../tests
python3 ../src/headless.py < "input1.txt" 

```

## Creating simple simulation
```python
from sim import Scheduler

highway_length =          1    # in kilometers
num_of_lanes =            4    # number of lanes
average_drivers_mood =    0.85 # how propable it is that driver will not perform any action
sim_time =                20   # in minutes
inflow =                  10   # cars per minute
speed_limit =             60   # in kilometers per hour
propotion_of_autonomous = 0.5  # propotion of autonomous cars
proportion_of_trucks =    0.1  # proportion of trucks 

scheduler = Scheduler(
                        average_drivers_mood =      average_drivers_mood ,
                        num_of_lanes =              num_of_lanes, 
                        highway_length =            highway_length, 
                        speed_limit =               speed_limit,
                        propotion_of_trucks =       propotion_of_trucks,
                        proportion of autonomous =  propotion_of_trucks,
                        step_time = 1)

results, results_dict, average_speed = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)
```

## Reusing scheduler object


```python
scheduler.num_of_lanes = 3
scheduler.average_drivers_mood = 0.97
scheduler.reset()
results, results_dict, average_speed = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

```
## Exporting data

**Exporting only data**

After simulation data can be safed in form f a json file:

```python
scheduler.safe_results_to_file("results")
```

**Exporting whole scheduler**

Scheduler can be aslo exported and imported(both data and parameters of an objects)

```python
scheduler.safe_to_file("sheduler.pkl")
```

**Importing scheduler**
```python
scheduler1 = Scheduler.load_from_file("test.pkl")
```

## Visualizing output

```python
from animation import createAnimation

createAnimation(
    results_list = [results_dict1],            # results from simulation - multiple can provided for compering simulations
    animation_speed= 20,                       # animation speed
    reduce_data = 1,                           # how much reduce the data, usefull in large datasets
    highway_length=highway_length,             # length in kilometers
    num_of_lanes=[num_of_lanes],
    names = ["Simple test"] ,                  # if not provided default
    export_gif_path = "../static/testcase.gif" # if not provided, animation will be shown in the form of plot
    )
```
**Note: All parameters provided to animation are arrays, so it is possible to visualize multiple simulation in one animation.**
## Results
As a results simulator is evaluating number of cars which were able to pass the highway:

```
Animation time: 23.90/24.0s Real time: 3.98/4.00min
Results: 13/60
```

## Functions of the simulator

**Basecases(overtaking, changing lanes)**

![basecase](/static/basecase.gif)

**Basic simulation**

![testcase](/static/testcase.gif)

**Changing speed of simulation**

![testcase](/static/speed.gif)

**Changing number of lanes**

![testcase](/static/num_of_lanes.gif)

**Comparing different simulations**

![testcase](/static/multiple.gif)

**Simulation with autonomous cars**

```
Results without autonomous: 35/160
Results with only autonomous: 140/160
Results with 50/50: 74/160
```

![testcase](/static/autonomous.gif)

```
Animation time: 179.00/180.0s Real time: 2.98/3.00min
Results without autonomous vehicles:
Flow: 38/120 vehicles passed the highway.
Average speed: 23.3/110 km/h.

Results with only autonomous vehicles:
Flow: 147/120 vehicles passed the highway.
Average speed: 109.5/110 km/h.

Results with 50/50 autonomous vehicles:
Flow: 120/120 vehicles passed the highway.
Average speed: 81.5/110 km/h.
```

![testcase](/static/autonomous2.gif)


**Simulation with autonomous cars and plots**

![testcase](/static/autonomous_with_plots.gif)




