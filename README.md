# CSMA-Protocol-Simulator
A Python program that simulates the Carrier Sense Multiple Access protocol on two network topologies: hidden terminal and non-hidden terminal.

## CSMA
Carrier Sense Multiple Access (CSMA) is a wireless access protocol used to mediate the transmissions of wireless devies to an access point. The primary goal of CSMA is to maximize the throughput of each device by minimizing the number of collisions. A collision occurs when two or more devices attempt to transmit a packet at the same time. CSMA attempts to resolve this issue by requiring each device to sense the medium for a specified amount of time, called DIFS. After this time, if the medium is not being used, each device with a packet waiting in its buffer will choose a random back off value to determine when to start transmission. If a device's back off value expires, and the medium is still available, the device will transmit its packet. The access point acknowledges a successful transmission by sending an ACK back to the device.
<img src =images/csma_timing_diagram.png height=500>

## Non-Hidden Terminal Topology
In this network topology, both wireless devices are in the same collision domain. This means that each device can sense when the other is actively using the medium. In this topology, collisions occur when both devices choose the same back off value. This will cause each device to begin transmission at the same time, leading to a collision.

## Hidden Terminal Topology
In this network topology, the two wireless devices are in different collision domains, meaning that they cannot sense when the other device is using the medium. Collisions occur in a hidden terminal topology whenever one device begins transmission while the other is also transmitting. 

## Simulator Instructions
