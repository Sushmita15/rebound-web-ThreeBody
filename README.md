Name: Sushmita Mandal

This project uses a restricted three body problem that allows the user to put an onject with negligible mass near two bodies with gravitational force. 
**REBOUND** API by Hanno Rein is used to create a simulation. 

Challenge: 

- the python script overrides the REBOUND feature to pause the simulation with line 40. fix: get rid of while loop and let rebound handle the simulation completely. 
- Every time I click “Launch Orbit”, I start a new thread and start a new REBOUND server on the same port (1234). fix: Reset the iframe before starting a new sim
- Backend was working correctly but the frontend simulation would not update. fix: let REBOUND control the whole simulation by not using a while loop and don't call integrate() manually. Flask is only used to input parameters.


Notes: 
I ran the following command: 
```
sushmitamandal@Sushmitas-MacBook-Pro rebound-web-ThreeBody % curl -X POST http://127.0.0.1:5001/update_sim \ -H "Content-Type: application/json" \ -d '{"x":0.8, "vy":0.5}'
```
- It showed me that the backend was running just fine. 