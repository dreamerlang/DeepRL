import jpype
import json
import numpy as np
import uuid
from gym import spaces
import random

jpype.startJVM(classpath=['./jars/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:
    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()

    def get_observation(self):
        obs = self._env.getObs()
        obs_json=json.loads(str(obs))

