# ToyChord

Toychord is an implementation of Chord distributed hash table in Python.

## Installation

To install all dependencies, make sure you are using python 3 (preferably inside a virtual environment) and run

```bash
python -m install -r requirements.txt
```
## Node Deployment

To deploy a node to listen at port <port> run:
```bash
python3 node.py --port <port>
```
For example
```bash
python3 node.py --port 3000
```
To specify the number of replicas use the `-k` argument.
If you are running nodes locally in one machine, pass the `--local` argument.
If you want to deploy a bootstrap node, add the `--boostrap` argument.

Example command to deploy a non-boostrap node running locally, listening to port 3000
and joining a ToyChord network with k = 3:

```
python3 node.py --port 3000 -k 3 --local
```
If you want to deploy a boostrap node locally, listening to 5000:

```
python3 node.py --port 5000 -k 3 --local --bootstrap
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

 ## Front end deployment to heroku (for the owner of the Heroku app)

You need to run 
```
heroku git:remote -a toychord
git subtree push --prefix front-end heroku main
```
in project root level.