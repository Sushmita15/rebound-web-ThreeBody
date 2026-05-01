import rebound

def run_restricted_3body(user_x, user_vy):
    sim = rebound.Simulation()
    sim.integrator = "ias15" # High precision
    
    # 1. Add the "Primary" (e.g., The Sun)
    sim.add(m=1.0)
    
    # 2. Add the "Secondary" (e.g., Jupiter) 
    # We place it at x=1.0 in a circular orbit (vy = sqrt(G*M/r))
    sim.add(m=0.01, x=1.0, vy=1.0) 
    
    # 3. Add YOUR Particle (The "Restricted" one)
    # This is the one the user controls from the website
    sim.add(m=0, x=user_x, vy=user_vy)
    
    sim.move_to_com() # Keep simulation centered
    
    path_x = []
    path_y = []
    
    # Run for 20 orbital periods
    for t in range(200):
        sim.integrate(t * 0.1)
        test_particle = sim.particles[2] # The massless one
        path_x.append(test_particle.x)
        path_y.append(test_particle.y)
        
    return {"x_coords": path_x, "y_coords": path_y}