import dubins

q0 = (-50, 50, 0)
q1 = (0, 0, 0)
turning_radius = 1.0
step_size = 0.5

path = dubins.shortest_path(q0, q1, turning_radius)
configurations, _ = path.sample_many(step_size)
