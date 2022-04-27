import torch
import numpy as np
from .agent import ThorAgent
from utils.model_util import gpuify

from episodes.basic_episode import BasicEpisode
from models.model_io import ModelInput, ModelOutput


class RandomNavigationAgent(ThorAgent):
    def __init__(self, create_model, args, rank, scenes, targets, gpu_id):
        max_episode_length = args.max_episode_length
        hidden_state_sz = args.hidden_state_sz
        self.action_space = args.action_space
        from utils.class_finder import episode_class

        episode_constructor = episode_class(args.episode_type)
        episode = episode_constructor(args, gpu_id, args.strict_done)

        super(RandomNavigationAgent, self).__init__(
            create_model(args), args, rank, scenes, targets, episode, max_episode_length, gpu_id
        )
        self.hidden_state_sz = hidden_state_sz
        self.keep_ori_obs = args.keep_ori_obs

        self.glove = {}
        if 'SP' in self.model_name:
            with h5py.File('./data/thor_glove/glove_map300d.hdf5', 'r') as rf:
                for i in rf:
                    self.glove[i] = rf[i][:]

    """ A random navigation agent. """

    def eval_at_state(self, params=None):
        current_detection_feature = self.episode.current_detection_feature()
        current_detection_feature = self.select(current_detection_feature,self.episode.goal_embedding[:25])
        self.episode.environment.controller.select_bbox = current_detection_feature[self.targets.index(self.episode.target_object)][512:516]
        critic = torch.ones(1, 1)
        actor = torch.ones(1, self.action_space)
        critic = gpuify(critic, self.gpu_id)
        actor = gpuify(actor, self.gpu_id)
        return ModelInput(), ModelOutput(value=critic, logit=actor)

    def reset_hidden(self, volatile=False):
        pass

    def repackage_hidden(self, volatile=False):
        pass

    def preprocess_frame(self, frame):
        return None

    def state(self):
        return None

    def sync_with_shared(self, shared_model):
        return
    def select(self,group,att):
        result = np.zeros((len(self.targets),541))
        if group is not None:
            for object in group:
                data = group[object][()]
                if len(data) == 1:
                    result[self.targets.index(object)] = data[0]
                else:
                    result[self.targets.index(object)] = data[0]
                    dmin = np.linalg.norm(data[0][516:] - att)
                    for i in data:
                        d = np.linalg.norm(i[516:] - att)
                        if d < dmin:
                            result[self.targets.index(object)] = i
                            dmin = d
        return result