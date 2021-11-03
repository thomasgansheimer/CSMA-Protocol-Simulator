# Implements the CSMA protocol for topology A
import random
from numpy import random as p

# Initialize values for transmission parameters
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

# Iterate through each frame_rate in frame_rates and perform transmission algorithm
for frame_rate in frame_rates:
    a_frames, c_frames = get_frame_series(frame_rate), get_frame_series(frame_rate)
    # Performance metrics are initialized to zero 
    a_success, c_success, collisions, a_bo, c_bo, a_buffer, c_buffer, time = 0, 0, 0, 0, 0, 0, 0, 0
    # Contention window is set to its minimum value
    cw = cw_min

    # Transmission occurs while time has not exceeded total number of slots available
    while time < 1000000:
        # If no additional frames exist in buffers or frame lists, end transmission
        if a_buffer == 0 and c_buffer == 0 and len(a_frames) == 0 and len(c_frames) == 0:
            break
        # If no frames are waiting at A or C
        if a_buffer == 0 and c_buffer == 0:
            # A is empty, then time advances to next C frame
            if len(a_frames) == 0:
                time = c_frames[0]
                c_frames.pop(0)
                c_buffer += 1
            # C is empty, then time advances to next A frame
            elif len(c_frames) == 0:
                time = a_frames[0]
                a_frames.pop(0)
                a_buffer += 1
            # A's next frame arrives before C's next frame, time advances to A's
            # next frame
            elif a_frames[0] < c_frames[0]:
                time = a_frames[0]
                a_frames.pop(0)
                a_buffer += 1
            # C's next frame arrives before A's next frame, time advances to C's 
            # next frame
            elif c_frames[0] < a_frames[0]:
                time = c_frames[0]
                c_frames.pop(0)
                c_buffer += 1
            # A's and C's next frame arrive at the same time, time advances to A's
            # and C's next frame
            else:
                time = a_frames[0]
                a_frames.pop(0)
                c_frames.pop(0)
                a_buffer += 1
                c_buffer += 1
        # If both stations have a frame waiting in the buffer, both stations will contend for
        # transmission
        elif a_buffer >= 1 and c_buffer >= 1:
            time += difs # Both stations wait DIFS time
            if a_bo == 0: # Assign new back off values if A and/or C has reached 0
                a_bo = get_backoff_value(cw)
            if c_bo == 0:
                c_bo = get_backoff_value(cw)

            if a_bo < c_bo: # A wins contention
                a_success += 1 # Add 1 to successes
                a_buffer -= 1 # Subtract 1 from buffer
                c_bo -= a_bo # Update C back off 
                time += a_bo + frame + sifs + ack # Add time of transmission
                a_bo = 0 # Update A back off to zero
                cw = cw_min # cw is reset to cw_min on successful transmission
            elif c_bo < a_bo: # C wins contention
                c_success += 1 # Add 1 to successes
                c_buffer -= 1 # Subtract 1 from buffer
                a_bo -= c_bo # Update A back off
                time += c_bo + frame + sifs + ack # Add time of transmission
                c_bo = 0 # Update C back off to zero
                cw = cw_min # cw is reset to cw_min on successful transmission
            else: # A and C chose same back off value, leads to collision
                collisions += 1 # Add 1 to collisions
                time += a_bo + frame + sifs + ack # Add time of transmission
                a_bo, c_bo = 0, 0 # Update both A and C back offs to 0
                if cw != cw_max: # If cw has not reached max value, double it
                    cw *= 2
        # A has a frame waiting in buffer but C does not
        elif a_buffer >= 1:
            if a_bo == 0: # update A's back off value
                a_bo = get_backoff_value(cw)
            time += difs + a_bo # A waits difs time and adds back off value
            # If C has no more frames to send or C's next frame arrives after A's transmission, A will
            # win contention and transmit
            if len(c_frames) == 0 or c_frames[0] > (time - difs):
                a_success += 1 # Update A's successes
                a_buffer -= 1 # Remove sent frame from buffer
                time += frame + sifs + ack # Update transmission time
                a_bo = 0 # Reset back off value to 0
                cw = cw_min # Reset contention window to min
            # Else, a frame from C arrives with a chance to contend with A
            else:
                c_buffer += 1
                c_arrival = c_frames.pop(0)
                if c_bo == 0: # Update back off value for C
                    c_bo = get_backoff_value(cw)
                # C frame completes difs and back off before A, so C wins contention
                if (c_arrival + difs + c_bo) < time:
                    c_success += 1
                    c_buffer -= 1
                    a_bo = time - (c_arrival + difs + c_bo) # Update A's back off counter
                    # Time is updated to match C's transmission time
                    time = c_arrival + difs + c_bo + frame + sifs + ack
                    c_bo = 0
                    cw = cw_min
                # C frame completes difs and back off after A, so A winds contention
                elif (c_arrival + difs + c_bo) > time:
                    a_success += 1
                    a_buffer -= 1
                    c_bo = (c_arrival + difs + c_bo) - time # update C's back off counter
                    # Add rest of transmission time of A
                    time += frame + sifs + ack
                    a_bo = 0
                    cw = cw_min
                # A and C complete difs and back off at the same time, leading to a collision
                else:
                    collisions += 1
                    time += frame + sifs + ack
                    a_bo, c_bo = 0, 0
                    if cw != cw_max: # If cw has not reached max value, double it
                        cw *= 2
        # C has a frame waiting in buffer but A does not
        # protocol repeats steps above when A had a frame waiting in buffer but C did not
        elif c_buffer >= 1:
            if c_bo == 0:
                c_bo = get_backoff_value(cw)
            time += difs + c_bo
            if len(a_frames) == 0 or a_frames[0] > (time - difs):
                c_success += 1
                c_buffer -= 1
                time += frame + sifs + ack
                c_bo = 0
                cw = cw_min
            else:
                a_buffer += 1
                a_arrival = a_frames.pop(0)
                if a_bo == 0:
                    a_bo = get_backoff_value(cw)
                if (a_arrival + difs + a_bo) < time:
                    a_success += 1
                    a_buffer -= 1
                    c_bo = time - (a_arrival + difs + a_bo)
                    time = a_arrival + difs + a_bo + frame + sifs + ack
                    a_bo = 0
                    cw = cw_min
                elif (a_arrival + difs + a_bo) > time:
                    c_success += 1
                    c_buffer -= 1
                    a_bo = (a_arrival + difs + a_bo) - time
                    time += frame + sifs + ack
                    c_bo = 0
                    cw = cw_min
                else:
                    collisions += 1
                    time += frame + sifs + ack
                    a_bo, c_bo = 0, 0
                    if cw != cw_max: 
                        cw *= 2
        
        # Check if new frames from A have arrived during transmission
        cont = True
        while len(a_frames) > 0 and cont:
            if a_frames[0] <= time:
                a_frames.pop(0)
                a_buffer += 1
            else:
                cont = False
            
        # Check if new frames from C have arrived during transmission
        cont = True
        while len(c_frames) > 0 and cont:
            if c_frames[0] <= time:
                c_frames.pop(0)
                c_buffer += 1
            else:
                cont = False
    # Print results for Frame Rate
    print(f"\nFrame Rate: {frame_rate} \n\tA Successes: {a_success}, C Successes: {c_success}, Collisions: {collisions}")