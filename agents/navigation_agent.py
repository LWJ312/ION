import torch
import numpy as np
import h5py

from utils.model_util import gpuify, toFloatTensor
from models.model_io import ModelInput

from .agent import ThorAgent


class NavigationAgent(ThorAgent):
    """ A navigation agent who learns with pretrained embeddings. """

    def __init__(self, create_model, args, rank, scenes, targets, gpu_id):
        max_episode_length = args.max_episode_length
        hidden_state_sz = args.hidden_state_sz
        self.action_space = args.action_space
        from utils.class_finder import episode_class

        episode_constructor = episode_class(args.episode_type)
        episode = episode_constructor(args, gpu_id, args.strict_done)

        super(NavigationAgent, self).__init__(
            create_model(args), args, rank, scenes, targets, episode, max_episode_length, gpu_id
        )
        self.hidden_state_sz = hidden_state_sz
        self.keep_ori_obs = args.keep_ori_obs

        self.glove = {}
        if 'SP' in self.model_name:
            with h5py.File('./data/thor_glove/glove_map300d.hdf5', 'r') as rf:
                for i in rf:
                    self.glove[i] = rf[i][:]

    def eval_at_state(self, model_options):
        model_input = ModelInput()

        # model inputs
        if self.episode.current_frame is None:
            model_input.state = self.state()
        else:
            model_input.state = self.episode.current_frame

        model_input.hidden = self.hidden

        # Instance Mask
        target_embedding_array = np.zeros((len(self.targets), 25)) 
        # ablation
        # for i in range(len(target_embedding_array)):
        #     target_embedding_array[i] = self.episode.goal_embedding
        target_embedding_array[self.targets.index(self.episode.target_object)] = self.episode.goal_embedding
        if self.episode.current_cls_masks() is None:
            current_cls_masks = np.zeros((29,7,7))
        else:
            current_cls_masks = self.episode.current_cls_masks()[()]
        # current_cls_masks = np.zeros((29,7,7))
        current_detection_feature = self.episode.current_detection_feature()
        # Instance Selection
        current_detection_feature = self.select(current_detection_feature, self.episode.goal_embedding[:25])
        # Instance Relation Graph (IRG)
        self.episode.environment.controller.select_bbox = current_detection_feature[self.targets.index(self.episode.target_object)][512:516]
        self.episode.detection_results.append(
            list(current_detection_feature[self.targets.index(self.episode.target_object), 512:]))
        rate = np.random.random()
        if rate > 0.5 :
            current_detection_feature=np.zeros((len(self.targets), 541))

        target_embedding = {'cur_appear': current_detection_feature[:, :512],
                            'cur_info': current_detection_feature[:, 512:],
                            'indicator': target_embedding_array,
                            'glove': self.episode.glove_embedding,
                            'masks':current_cls_masks}
        target_embedding['cur_appear'] = toFloatTensor(target_embedding['cur_appear'], self.gpu_id)
        target_embedding['cur_info'] = toFloatTensor(target_embedding['cur_info'], self.gpu_id)
        target_embedding['indicator'] = toFloatTensor(target_embedding['indicator'], self.gpu_id)
        target_embedding['glove'] = toFloatTensor(target_embedding['glove'], self.gpu_id)
        target_embedding['masks'] = toFloatTensor(target_embedding['masks'], self.gpu_id)
        model_input.target_class_embedding = target_embedding

        model_input.action_probs = self.last_action_probs

        if 'Memory' in self.model_name:
            state_length = self.hidden_state_sz

            if len(self.episode.state_reps) == 0:
                model_input.states_rep = torch.zeros(1, state_length)
            else:
                model_input.states_rep = torch.stack(self.episode.state_reps)

            dim_obs = 512
            if len(self.episode.obs_reps) == 0:
                model_input.obs_reps = torch.zeros(1, dim_obs)
            else:
                model_input.obs_reps = torch.stack(self.episode.obs_reps)

            if len(self.episode.state_memory) == 0:
                model_input.states_memory = torch.zeros(1, state_length)
            else:
                model_input.states_memory = torch.stack(self.episode.state_memory)

            if len(self.episode.action_memory) == 0:
                model_input.action_memory = torch.zeros(1, 6)
            else:
                model_input.action_memory = torch.stack(self.episode.action_memory)

            model_input.states_rep = toFloatTensor(model_input.states_rep, self.gpu_id)
            model_input.states_memory = toFloatTensor(model_input.states_memory, self.gpu_id)
            model_input.action_memory = toFloatTensor(model_input.action_memory, self.gpu_id)
            model_input.obs_reps = toFloatTensor(model_input.obs_reps, self.gpu_id)

        return model_input, self.model.forward(model_input, model_options)

    def preprocess_frame(self, frame):
        """ Preprocess the current frame for input into the model. """
        state = torch.Tensor(frame)
        return gpuify(state, self.gpu_id)

    def reset_hidden(self):
        with torch.cuda.device(self.gpu_id):
            self.hidden = (
                torch.zeros(2, 1, self.hidden_state_sz).cuda(),
                torch.zeros(2, 1, self.hidden_state_sz).cuda(),
            )

        self.last_action_probs = gpuify(
            torch.zeros((1, self.action_space)), self.gpu_id
        )

    def repackage_hidden(self):
        self.hidden = (self.hidden[0].detach(), self.hidden[1].detach())
        self.last_action_probs = self.last_action_probs.detach()

    def state(self):
        return self.preprocess_frame(self.episode.state_for_agent())

    def exit(self):
        pass

    # Instance Selection
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
                # result[self.targets.index(object)] = data[0] #no select
        return result




