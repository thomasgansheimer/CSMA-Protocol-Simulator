import random
from numpy import random as p

# Define transmission parameters for CSMA protocol
difs, sifs, ack, frame, cw_min, cw_max, slots_per_second = 2, 1, 2, 100, 4, 1024, 100000

'''Takes as a parameter a contention window and returns a random integer in that window'''
def get_backoff_value(cw):
    return random.randint(0, cw-1)

'''Takes as a paramter a frame_rate and returns a list of intervals between frames. It is assumed
that frames arrive according to a poisson distribution'''
def get_frame_series(frame_rate, sim_time):
    # Number of expected frames = frame rate * simulation time
    expected_frames = frame_rate * sim_time 
    # Expected number of slots between frames = total slots / expected frames
    slots_between = (slots_per_second * sim_time) // expected_frames

    sum = 0
    frame_series = []
    for i in range(expected_frames):
       sum += p.poisson(lam=slots_between)
       frame_series.append(sum)
    return frame_series