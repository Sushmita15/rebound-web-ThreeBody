import rebound
sim = rebound.Simulation()
sim.add(m=1)
sim.start_server(port=1234)

import time
while True:
    time.sleep(1)