from flask import Flask, render_template, request
import rebound

app = Flask(__name__, template_folder='templates')

sim = rebound.Simulation()
sim.integrator = "ias15"

print("Creating REBOUND system...")

sim.add(m=1.0)
sim.add(m=0.01, a=1.0)
sim.add(m=0, x=0.8, vy=0.5)

sim.move_to_com()

sim.start_server(port=1234)
print("🚀 REBOUND running at http://127.0.0.1:1234")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_sim', methods=['POST'])
def update_sim():
    data = request.json
    x = float(data.get('x'))
    vy = float(data.get('vy'))

    print("Updating particle")

    sim.particles[2].x = x
    sim.particles[2].vy = vy

    return {"status": "updated"}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)