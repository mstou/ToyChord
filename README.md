# ToyChord

Toychord is an implementation of Chord distributed hash table in Python.

## Installation

To install all dependencies run

```bash
pip3 install -r requirements.txt
```
## Node Deployment

To deploy a node as bootstrap run:
```bash
python3 node.py 5000 bootstrap
```

To deploy a node to listen at port <port> run:
```bash 
python3 node.py <port>
```
For example 
```bash
python3 node.py 3000 
```

## Local Testing
You can use the functions in `local_testing.py` or run:
```bash
python local_testing.py
```
 to deploy some servers at different ports on the same machine and test.

 
 To run the unit tests, simply run
 ```bash
 pytest
 ```
 in the root directory.