from classes import  *
print("start")
helsingor = Highway(3, 110, 10)
freq = 2
step = 0

while True:
    step += 1
    if freq % step == 0:
        new_driver = Driver(1)
        new_coms = Coms(1, 1)
        new_car = Car(new_driver, new_coms)
        helsingor.lanes[0].cars.append(new_car)

