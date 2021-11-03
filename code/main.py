from HiddenTerminal import CSMA_hidden_terminal
from NonHiddenTerminal import CSMA_non_hidden_terminal

'''Requests and returns a frame rate from the user.'''
def get_frame_rate():
    print()
    while True:
        try:
            frame_rate = int(input("Enter a frame rate (>= 100 and <= 1000): "))
            if frame_rate >= 100 and frame_rate <= 1000:
                return frame_rate
            print("\tMust be between 100 and 1000!")
        except ValueError:
            print("\tMust be an integer!")

'''Requests and returnsa simulation time from the user'''
def get_sim_time():
    print()
    while True:
        try:
            sim_time = int(input("Enter a simulation time in seconds (>= 1 and <= 10): "))
            if sim_time >= 1 and sim_time <= 10:
                return sim_time
            print("\tMust be between 1 and 10!")
        except ValueError:
            print("\tMust be an integer!")

print("/***************************************************************\\")
print("/                                                               \\")
print("/                         CSMA Simulator                        \\")
print("/                                                               \\")
print("/***************************************************************\\")

frame_rate = get_frame_rate()
sim_time = get_sim_time()

a_success_non_hidden, c_success_non_hidden, collisions_non_hidden = CSMA_non_hidden_terminal(frame_rate, sim_time)
a_success_hidden, c_success_hidden, collisions_hidden = CSMA_hidden_terminal(frame_rate, sim_time)

print(f"\n{sim_time} second simulation results for {frame_rate} frames/sec frame rate:")
print("/********************* Non-Hidden Terminal *********************\\")
print(f"\tDevice A Successes: {a_success_non_hidden}")
print(f"\tDevice C Successes: {c_success_non_hidden}")
print(f"\tCollisions:         {collisions_non_hidden}")
print("/*********************** Hidden Terminal ***********************\\")
print(f"\tDevice A Successes: {a_success_hidden}")
print(f"\tDevice C Successes: {c_success_hidden}")
print(f"\tCollisions:         {collisions_hidden}")