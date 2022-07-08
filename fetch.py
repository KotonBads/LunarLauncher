import requests


params = {
    "hwid": "0",
    "os": "linux",
    "arch": "x64",
    "version": "1.8",
    "branch": "master",
    "launch_type": "OFFLINE",
    "classifier": "optifine",
}

res = requests.post("https://api.lunarclientprod.com/launcher/launch", json=params).json()
