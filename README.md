# CMPE 273 Week 1 Lab
## Author of this project: Hei Lam (014751503)

## Objective
The goal of this lab is to experience the core characteristics of a distributed system by building a small but real system locally.

This lab demonstrates:

- Independent services running as separate processes
- Communication over a network
- Failure propagation across service boundaries
- Basic logging and graceful error handling

Although both services run on the same machine, they behave as independent distributed components.


## System Overview

This system consists of two services:

### Service A (Provider)
- Runs independently on its own port
- Exposes a simple HTTP API
- Responds to requests from other services
- Logs incoming requests

### Service B (Consumer)
- Runs independently on its own port
- Exposes its own HTTP API
- Calls Service A over the network
- Handles failures gracefully when Service A is unavailable or slow