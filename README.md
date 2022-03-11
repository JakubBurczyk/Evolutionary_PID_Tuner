# Evolutiuonal algorithm PID controller tuner

## Dependencies:
### Software:
* __Matlab and simuliunk__ - tested with version 2021b.
* __Matlab Python engine__ - install manual and refference can be found [__here__](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html).
* __Python 3.9__ - as of Matlab 2021b it is the highest supported python version for Matlab Python engine, can be downloaded [here](https://www.python.org/downloads/release/python-3910/).

### Python packages:


# Concept:
* __General approach__ - possibility to use multiple evolutionary algorithms such as artificial bee colony __(ABC)__ *(default)*
* __Simulink integration__ - simulate closed control loop via Matlab Python engine and Simulink model including a PID controller and plant object
* __Multithreading__ - each agent is assigned a different thread, algorithm iteration completes when all agents finish their simulation
