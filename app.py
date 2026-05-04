from flask import Flask, render_template, request
import rebound
import time
import threading

sim = None
app = Flask(__name__, template_folder='templates')

def create_sim(x, vy):
    sim = rebound.Simulation()
    sim.integrator = "ias15"

    sim.collision = "direct"
    sim.collision_resolve = "merge"

    sim.add(m=1.0)
    sim.add(m=0.01, a=1.0)
    sim.add(m=0, x=x, vy=vy)

    sim.move_to_com()
    sim.start_server(port=1234)

    return sim



def run_simulation():
    while True:
        sim.integrate(sim.t + 0.01)
        time.sleep(0.01)


threading.Thread(target=run_simulation, daemon=True).start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_sim', methods=['POST'])
def update_sim():
    global sim

    data = request.json
    x = float(data.get('x'))
    vy = float(data.get('vy'))

    print("Restarting simulation with new parameters")

    # stop old simulation
    if sim is not None:
        sim.stop_server()
    sim = create_sim(x, vy)

    return {"status": "restarted"}


if __name__ == '__main__':
    app.run(port=5001, debug=True, use_reloader=False)