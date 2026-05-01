from flask import Flask, render_template, request
import rebound
import threading

app = Flask(__name__, template_folder='templates')

# Global variable to hold our simulation
sim = None

def run_rebound_server(x, vy):
    global sim
    sim = rebound.Simulation()
    sim.integrator = "ias15"
    
    # Standard Restricted Three-Body Setup
    sim.add(m=1.0) # Primary
    sim.add(m=0.01, a=1.0) # Secondary
    sim.add(m=0, x=x, vy=vy) # The User's Particle
    
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