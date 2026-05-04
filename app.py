from flask import Flask, render_template, request
import rebound
import threading
import time

app = Flask(__name__, template_folder='templates')

# -------------------------
# CREATE SIMULATION ONCE
# -------------------------
sim = rebound.Simulation()
sim.integrator = "ias15"

sim.collision = "direct"
sim.collision_resolve = "merge"

sim.add(m=1.0)
sim.add(m=0.01, a=1.0)
sim.add(m=0, x=0.8, vy=0.5)


sim.move_to_com()


sim.collision = "direct"
sim.collision_resolve = "merge"


sim.start_server(port=1234)
print("REBOUND running at http://127.0.0.1:1234") 

def run_sim():
    while True:
        sim.integrate(sim.t + 0.1)
        
        time.sleep(0.01)
        print("t =", sim.t, "Particle 2 position:", sim.particles[2].x, sim.particles[2].y)
        if sim.particles[2].x > 10 or sim.particles[2].y > 10 or sim.t > 300:
            print("Particle ejected! Stopping.")
            break

threading.Thread(target=run_sim, daemon=True).start()


# -------------------------
# FLASK
# -------------------------


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_sim', methods=['POST'])
def update_sim():
    data = request.json
    x = float(data.get('x'))
    vy = float(data.get('vy'))
    sim.t = 0  
    print("Updating particle")
    print("t =", sim.t)

    sim.particles[2].x = x
    sim.particles[2].vy = vy

    return {"status": "updated"}


if __name__ == '__main__':
    app.run(port=5001, debug=True, use_reloader=False)