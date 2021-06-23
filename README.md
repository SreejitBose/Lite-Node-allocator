# Lite-Node-allocator
A simple script to generate host file for IITK csews cluster which can be used in MPICH applications. 
The script uses uptime utility of Linux to determine the load of each node in the cluster and makes a list of nodes which are lightly loaded.



## Usage

```python
python3 lna.py <number of nodes> <number of cores per node>
```
## Output
The script creates a file named "host_file" which can be used in MPICH applications at time of execution of the binary, like below.
```bash
mpiexec –n <number of processes> -f host_file ./<binaryfile> 
