from flask import Flask, render_template, request
import rebound
import threading

app = Flask(__name__, template_folder='templates')

# Global variable to hold our simulation
sim = None

def run_rebound_server(x, vy):
    global sim

    if sim is not None:
        sim.stop_server()

    sim = rebound.Simulation()
    sim.integrator = "ias15"
    
    # Standard Restricted Three-Body Setup
    # Primary (Sun) - Make it huge
    sim.add(m=1.0, r=1.0, hash="Sun")
    sim.particles["Sun"].color = (1, 0.8, 0) # Use 0-1 scale instead of 0-255

    # Secondary (Planet) - Make it visible
    sim.add(m=0.01, a=1.0, r=0.05, hash="Planet")
    sim.particles["Planet"].color = (0, 0.5, 1)

    # Test Particle - Make it distinct
    sim.add(m=0, x=x, vy=vy, r=0.02, hash="Particle")
    sim.particles["Particle"].color = (1, 0, 0)
    
    sim.move_to_com()
    
    # This starts the visualization server on port 1234
    # 'pause=False' ensures it starts moving immediately
    sim.start_server(port=1234) 
    
    # Keep the simulation running
    while True:
        sim.integrate(sim.t + 0.05)

        # If the particle is 100 units away, it's 'ejected' - stop the loop
        if sim.particles[2].x > 100 or sim.particles[2].y > 100:
            print("Particle ejected! Stopping.")
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_sim', methods=['POST'])
def update_sim():
    data = request.json
    x = float(data.get('x'))
    vy = float(data.get('vy'))
    
    # Start the simulation in a background thread so it doesn't freeze the website
    thread = threading.Thread(target=run_rebound_server, args=(x, vy), daemon=True)
    thread.start()
    
    return {"status": "started"}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)