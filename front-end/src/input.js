const node1 = {
    "files": {
        "955af05f3130ac5c70952a34a9aa710c9fbf812b": {
            "name": "127.0.0.1:3000",
            "value": "testing port 3000"
        },
        "1230123778434041": {
          "name": "is this a second file?",
          "value": "yes it is."
        }
    },
    "me": {
        "id": "955af05f3130ac5c70952a34a9aa710c9fbf812b",
        "ip": "127.0.0.1",
        "port": "3000"
    },
    "next": {
        "id": "b660cd6180a4629b8e5f3c7eaeedcddf07dd1b1d",
        "ip": "127.0.0.1",
        "port": "5000"
    },
    "previous": {
        "id": "caf8d9b85e7fa9a124cb44cb28ad5289faa44668",
        "ip": "127.0.0.1",
        "port": "4000"
    },
    "replicas": [
        {
            "caf8d9b85e7fa9a124cb44cb28ad5289faa44668": {
                "name": "127.0.0.1:4000",
                "value": "testing port 4000"
            }
        },
        {
            "b660cd6180a4629b8e5f3c7eaeedcddf07dd1b1d": {
                "name": "127.0.0.1:5000",
                "value": "testing port 5000"
            }
        }
    ]
};

const node2 = {
    "files": {
        "b660cd6180a4629b8e5f3c7eaeedcddf07dd1b1d": {
            "name": "127.0.0.1:5000",
            "value": "testing port 5000"
        }
    },
    "me": {
        "id": "b660cd6180a4629b8e5f3c7eaeedcddf07dd1b1d",
        "ip": "127.0.0.1",
        "port": "5000"
    },
    "next": {
        "id": "caf8d9b85e7fa9a124cb44cb28ad5289faa44668",
        "ip": "127.0.0.1",
        "port": "4000"
    },
    "previous": {
        "id": "955af05f3130ac5c70952a34a9aa710c9fbf812b",
        "ip": "127.0.0.1",
        "port": "3000"
    },
    "replicas": [
        {
            "955af05f3130ac5c70952a34a9aa710c9fbf812b": {
                "name": "127.0.0.1:3000",
                "value": "testing port 3000"
            }
        },
        {
            "caf8d9b85e7fa9a124cb44cb28ad5289faa44668": {
                "name": "127.0.0.1:4000",
                "value": "testing port 4000"
            }
        }
    ]
}

const nodes = [
  node1,
  node2,
];

export default nodes;
