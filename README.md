Name: Sushmita Mandal

This project uses a restricted three body problem that allows the user to put an onject with negligible mass near two bodies with gravitational force. 
**REBOUND** API by Hanno Rein is used to create a simulation. 



Directions:
1. Prerequisites: 
Ensure you have Python 3.10+ installed. You will need the following libraries:REBOUND: The orbital mechanics engine.Flask: The web framework for the UI.Install them via terminal:Bashpip install rebound flask
2. Project Structure
app.py: The main Flask application and background physics thread.templates/index.html: The user interface for entering $x$ and $v_y$.physics_failures.db: 
 How to Run:
 Start the Server:Navigate to your project folder and run the Flask app:Bash
 ```
 python3 app.py
```
Open the Visualization:REBOUND starts a native visualizer. Open your browser to:http://localhost:1234

Open the Control Panel:In a new tab, open the Flask UI:http://127.0.0.1:5001/. Using the SimulatorEnter a starting X-coordinate (e.g., 0.8) and a Y-velocity (e.g., 1.5).Click Update Simulation.

3. Try x = 10 and y = 0.5 and see the Ejection 



Challenge: 

- the python script overrides the REBOUND feature to pause the simulation with line 40. fix: get rid of while loop and let rebound handle the simulation completely. 
- Every time I click “Launch Orbit”, I start a new thread and start a new REBOUND server on the same port (1234). fix: Reset the iframe before starting a new sim
- Backend was working correctly but the frontend simulation would not update. fix: let REBOUND control the whole simulation by not using a while loop and don't call integrate() manually. Flask is only used to input parameters.


Rules:

- Dont create simulation inside Flask.
- Flask only updates values

Notes: 
I ran the following command: 
```
curl -X POST http://127.0.0.1:5001/update_sim \ -H "Content-Type: application/json" \ -d '{"x":0.8, "vy":0.5}'
```
- It showed me that the backend was running just fine. 