# Implements the CSMA protocol for topology B
import random
from numpy import random as p

# Initialize transmission parameters
difs, sifs, ack, frame, cw_min, cw_max, sim_time = 2, 1, 2, 100, 4, 1024, 10
frame_rates = [100, 200, 300, 500, 700, 1000]

'''Takes as a parameter a contention window and returns a random integer in that window'''
def get_backoff_value(cw):
    return random.randint(0, cw-1)

'''Takes as a paramter a frame_rate and returns a list of intervals between frames. It is assumed
that frames arrive according to a poisson distribution'''
def get_frame_series(frame_rate):
    # Number of expected frames = frame rate * simulation time
    expected_frames = frame_rate * sim_time 
    # Expected number of slots between frames = total slots / expected frames
    slots_between = 1000000 // expected_frames

    sum = 0
    frame_series = []
    for i in range(expected_frames):
       sum += p.poisson(lam=slots_between)
       frame_series.append(sum)
    return frame_series

# Execute transmission algorithm for each frame rate
for frame_rate in frame_rates:
    # Initialize lists of a_frames and c_frames arrivals
    a_frames, c_frames = get_frame_series(frame_rate), get_frame_series(frame_rate)
    # Performance metrics are intialized to zero
    a_success, c_success, a_bo, c_bo, a_buffer, c_buffer, collisions, a_time, c_time = 0, 0, 0, 0, 0, 0, 0, 0, 0
    cw_a, cw_c = cw_min, cw_min
    a_arrival, c_arrival = 0, 0
    a_freeze, c_freeze = False, False

    # In a hidden terminal topology, A and C will transmit regardless of if the other station is actively
    # transmitting. Therefore, A and C will have individual 'time' variables as each station acts 
    # independently of the other. The transmission will end when one of these stations reaches the end 
    # of the simulation time.
    while a_time < 1000000 and c_time < 1000000:  
        # If a and c have no additional frames to send, end transmission
        if a_buffer == 0 and c_buffer == 0 and len(a_frames) == 0 and len(c_frames) == 0:
            break
        # If a's buffer is zero, move a's time to the next arrival of a packet
        if a_buffer == 0 and len(a_frames) > 0:
            a_time = a_frames[0]
            a_frames.pop(0)
            a_buffer += 1 # Increment a's buffer for new packet arrival
        # If c's buffer is zero, move a's time to the next arrival of a packet
        if c_buffer == 0 and len(c_frames) > 0:
            c_time = c_frames[0]
            c_frames.pop(0)
            c_buffer += 1
        # If a's buffer is nonempty, a will attempt to send a packet regardless of whether c is also
        # sending a packet. 
        if a_buffer > 0 and not a_freeze:
            a_bo = get_backoff_value(cw_a)
            # a_arrival stores time when frame transmission from a starts
            a_arrival = a_time + difs + a_bo
            a_time += difs + a_bo + frame + sifs + ack
        # If c's buffer is nonempty, c will attempt to send a packet regardless of whether a is also
        # sending a packet. 
        if c_buffer > 0 and not c_freeze:
            c_bo = get_backoff_value(cw_c)
            # c_arrival stores time when frame transmission from c starts
            c_arrival = c_time + difs + c_bo
            c_time += difs + c_bo + frame + sifs + ack
        # If C does not have a packet to send, A will transmit without contention
        if c_buffer == 0 and len(c_frames) == 0:
            # First unfreeze A if it is frozen
            if a_freeze == True:
                a_freeze = False
            # Then if a_buffer is greater than 0, A can transmit
            elif a_buffer > 0:
                a_success += 1
                a_buffer -= 1
                cw_a = cw_min
        # If A does not have a packet to send, C will transmit without contention
        elif a_buffer == 0 and len(a_frames) == 0:
            # First unfreeze C if it is frozen
            if c_freeze == True:
                c_freeze = False
            # Then if c_buffer is greater than 0, C can transmit
            elif c_buffer > 0:
                c_success += 1
                c_buffer -= 1
                cw_c = cw_min
        # If the difference between the arrival times of A and C is greater the the sum of 
        # the transmission time of a frame, sifs, and ack, one station will transmit successfully
        elif abs(a_arrival - c_arrival) >= (frame + sifs + ack):
            # If a_arrival < c_arrival, A will transmit successfully
            if a_arrival < c_arrival and a_buffer > 0:
                a_success += 1
                a_buffer -= 1
                cw_a = cw_min
                # Freeze varibales allow A's time to 'catch up' to C's time. In the case of a successful
                # transmission from A, it needs to be determined if the next frames sent from A will
                # collide with the current transmission from C.
                c_freeze = True
                a_freeze = False
            # If c_arrival < a_arrival, C will transmit successfully
            if c_arrival < a_arrival and c_buffer > 0:
                c_success += 1
                c_buffer -= 1
                cw_c = cw_min
                # Freeze station A and allow C to catch up to A's time.
                a_freeze = True
                c_freeze = False
        # Else a collision has occurred between A and C.
        else:
            collisions += 1 # Increment number of collisions
            # Update contention windows for A and C if they are not at their max values.
            if cw_a != cw_max:
                cw_a *= 2
            if cw_c != cw_max:
                cw_c *= 2
            # Unfreeze both stations
            c_freeze, a_freeze = False, False

        # Check if new frames from A have arrived during transmission
        cont = True
        while len(a_frames) > 0 and cont:
            if a_frames[0] <= a_time:
                a_frames.pop(0)
                a_buffer += 1
            else:
                cont = False
                
        # check if new frames from C have arrived during transmission
        cont = True
        while len(c_frames) > 0 and cont:
            if c_frames[0] <= c_time:
                c_frames.pop(0)
                c_buffer += 1
            else:
                cont = False
    # Print results of current Frame Rate:
    print(f"\nFrame Rate: {frame_rate} \n\tA Successes: {a_success}, C Successes: {c_success}, Collisions: {collisions}")