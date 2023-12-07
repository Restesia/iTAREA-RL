import gym
from gym import spaces
import numpy as np


class NFVEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, Nodes=[], Task=[]):
        #self.size = size  # The size of the square grid
        #self.window_size = 512  # The size of the PyGame window

        # He utilizado la estructura de Task como 
        self.observation_space = spaces.Dict(
            {
                "CPU": int,
                "RAM": int,
                "User": int,
                "MinimTrans": int,
                "Compatibility": spaces.Discrete(2),
                "PReq": spaces.Dict({}),
                "Transmit": spaces.Dict({}),
                "loc": spaces.Text(10),
                "Type": spaces.Text(10),
                "DReq": spaces.Discrete(5),
                "TaskName": spaces.Text(10) 
            }
        )

        # Tenemos una posible acción por cada nodo
        self.action_space = spaces.Discrete(len(Nodes))

        """
        Esta sescción define el espacio de acción 
        """
        action_dict = dict()
        it = 0

        for x in Nodes:
            action_dict[it] = x
            it = it +1
            
        self._action_to_direction = action_dict

        """
        Esta sección es un tema de la renderización, dado que no estoy interesado en renderizar nada no debería importarme. 
        No sé si es posible eliminarlo, ya lo investigaré
        """

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        Lo mismo de antes
        """
        self.window = None
        self.clock = None


prueba = NFVEnv(Nodes = [1], Task= [])
print(prueba.observation_space.sample())