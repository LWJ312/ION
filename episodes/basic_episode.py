""" Contains the Episodes for Navigation. """
import random
import sys
from tkinter.messagebox import NO
import torch
import numpy as np
import math
from buildDataset.constants import GOAL_SUCCESS_REWARD, MOVE_AHEAD, SAMECLASS_INT,  STEP_PENALTY, ALL_GOALS_TEMP ,ALL_OBJS_TEMP,MODIFY_OBJS
from buildDataset.constants import DONE,TARGETS,REFERENCES,COLOR_ATT,MATERIAL_ATT,LINK
from buildDataset.environment import Environment

from utils.model_util import gpuify, toFloatTensor
from utils.action_util import get_actions
from utils.model_util import gpuify
from .episode import Episode


class BasicEpisode(Episode):
    """ Episode for Navigation. """

    def __init__(self, args, gpu_id, strict_done=False):
        super(BasicEpisode, self).__init__()
        self._env = None
        self.ep_area=[]
        self.dis2tar=None
        self.ob_cls = []
        self.success_foj= 0  # frequency of judge instances of the same class

        self.gpu_id = gpu_id
        self.strict_done = strict_done
        self.task_data = None
        self.task_data_cls =None
        self.glove_embedding = None
        self.actions = get_actions(args)
        self.done_count = 0
        self.duplicate_count = 0
        self.failed_action_count = 0
        self._last_action_embedding_idx = 0
        self.target_object = None
        self.prev_frame = None
        self.current_frame = None
        self.scene = None
        self.glove = np.load('./buildDataset/glove.npy')

        self.scene_states = []
        if args.eval:
            random.seed(args.seed)

        self._episode_times = 0
        self.seen_percentage = 0

        self.state_reps = []
        self.state_memory = []
        self.action_memory = []
        self.obs_reps = []

        self.episode_length = 0
        self.target_object_detected = False

        # tools
        self.states = []
        self.actions_record = []
        self.action_outputs = []
        self.detection_results = []

        # imitation learning
        self.imitation_learning = args.imitation_learning
        self.action_failed_il = False

        self.action_probs = []

        self.meta_learning = args.update_meta_network
        self.meta_predictions = []

        self.visual_infos = {}
        self.match_score = []
        self.indices_topk = []

    @property
    def environment(self):
        return self._env

    @property
    def actions_list(self):
        return [{"action": a} for a in self.actions]

    @property
    def episode_times(self):
        return self._episode_times

    @episode_times.setter
    def episode_times(self, times):
        self._episode_times = times

    def reset(self):
        self.done_count = 0
        self.duplicate_count = 0
        self._env.back_to_start()

    def state_for_agent(self):
        return self.environment.current_frame

    def current_detection_feature(self):
        return self.environment.current_detection_feature
        
    def current_cls_masks(self):
        return self.environment.current_cls_masks

    def current_depth(self):
        return self.environment.current_depth

    def current_agent_position(self):
        """ Get the current position of the agent in the scene. """
        return self.environment.current_agent_position

    def step(self, action_as_int):

        action = self.actions_list[action_as_int]

        if action["action"] != DONE:
            self.environment.step(action)
        else:
            self.done_count += 1

        reward, terminal, action_was_successful = self.judge(action)
        return reward, terminal, action_was_successful
        
    def get_dis(self, pos, id_):
        goals = self.environment.controller.metadata[id_]
        pos = pos.split('|')
        ds = []
        for goal in goals:
            goal = goal.split('|')[:2]
            d = math.sqrt((float(pos[0]) - float(goal[0]))**2 + (float(pos[1]) - float(goal[1]))**2)
            ds.append(d)
        return float(sum(ds))/len(ds)

    def judge(self, action):
        """ Judge the last event. """
        reward = STEP_PENALTY
        # Thresholding replaced with simple look up for efficiency.
        if self.environment.controller.state in self.scene_states:
            if action["action"] != DONE:
                if self.environment.last_action_success:
                    self.duplicate_count += 1
                else:
                    self.failed_action_count += 1
        else:
            self.scene_states.append(self.environment.controller.state)
        if (action["action"] == MOVE_AHEAD) and self.environment.last_action_success:
            self.move_count+=1
        pos = '|'.join(str(self.environment.controller.state).split('|')[:2])
        if pos not in self.ep_area:
            self.ep_area.append(pos)

        for id_ in self.task_data_cls:
            if self.environment.object_is_visible(id_):
                self.ob_cls.append(id_)
        
        mean_distances = []
        for id_ in self.task_data:
            mean_dis = self.get_dis(pos, id_)
            mean_distances.append(mean_dis)
        self.dis2tar = min(mean_distances)
        done = False
        if action["action"] == DONE:

            for id_ in self.task_data:
                if self.environment.cls_success(id_.split('|')[0]):
                    reward = SAMECLASS_INT
                    break

            action_was_successful = False
            for id_ in self.task_data:
                if self.environment.object_is_visible(id_):
                    reward = GOAL_SUCCESS_REWARD
                    done = True
                    action_was_successful = True
                    self.success_foj = len(self.ob_cls)
                    break
        else:
            action_was_successful = self.environment.last_action_success

        return reward, done, action_was_successful

    # Set the target index.
    @property
    def target_object_index(self):
        """ Return the index which corresponds to the target object. """
        return self._target_object_index

    @target_object_index.setter
    def target_object_index(self, target_object_index):
        """ Set the target object by specifying the index. """
        self._target_object_index = gpuify(
            torch.LongTensor([target_object_index]), self.gpu_id
        )

    def get_goal_embedding(self,task):
        color_onehot = np.zeros(len(COLOR_ATT))
        material_onehot = np.zeros(len(MATERIAL_ATT))
        colors = task[1].split('-')
        materials = task[2].split('-')
        if materials == ['']:
            materials = []
        for color in colors:
            color_onehot[COLOR_ATT.index(color)] = 1.0
        for material in materials:
            material_onehot[MATERIAL_ATT.index(material)] = 1.0
        link_glove=self.glove[LINK.index(task[3])]
        reference_glove=self.glove[REFERENCES.index(task[4])+4]
        goal_embedding = np.concatenate((color_onehot,material_onehot))
        glove_embedding = np.concatenate((link_glove,reference_glove))

        return goal_embedding,glove_embedding


    def _new_episode(self, args, scenes, targets):
        """ New navigation episode. """
        scene = random.choice(scenes)
        self.scene = scene

        if self._env is None:
            self._env = Environment(
                offline_data_dir=args.data_dir,
                use_offline_controller=True,
                grid_size=0.25,
                detection_feature_file_name=args.detection_feature_file_name,
                images_file_name=args.images_file_name,
                visible_object_map_file_name=args.visible_map_file_name,
                local_executable_path=args.local_executable_path,
                optimal_action_file_name=args.optimal_action_file_name,
            )
            self._env.start(scene)
        else:
            self._env.reset(scene)


        # Randomize the start location.
        self._env.randomize_agent_location()

        self.task_data = []
        self.task_data_cls = []

        objects = self._env.all_objects()

        intersection = []
        for obj in objects:
            if obj.split("|")[0] in ALL_GOALS_TEMP:
                if obj.split("|")[-1] in ALL_OBJS_TEMP:
                    origin = obj.split('|')
                    if origin[0] in MODIFY_OBJS.keys():
                        origin[0] = MODIFY_OBJS[origin[0]]
                    if origin[-1] in MODIFY_OBJS.keys():
                        origin[-1] = MODIFY_OBJS[origin[-1]]
                    new = '|'.join(str(i) for i in origin)
                    intersection.append(new)
        idx = random.randint(0, len(intersection) - 1)
        task = intersection[idx].split("|")
        goal_object_type = task[0]
        self.target_object = goal_object_type
        self.goal_embedding,self.glove_embedding = self.get_goal_embedding(task)

        for id_ in objects:
            first = id_.split("|")[0]
            last = id_.split("|")[-1]
            if first in MODIFY_OBJS.keys():
                first = MODIFY_OBJS[first]
            if last in MODIFY_OBJS.keys():
                last = MODIFY_OBJS[last]
            if (task[0]==first):
                self.task_data_cls.append(id_)
            if (task[0]==first) and (task[1]==id_.split("|")[1]) and \
                    (task[2]==id_.split("|")[2]) and(task[3]==id_.split("|")[3]) and (task[4]==last):
                self.task_data.append(id_)
        if args.verbose:
            print("Scene", scene, "Navigating towards:", task)

    def new_episode(self, args, scenes, targets):
        self.move_count= 0
        self.ep_area=[]
        self.dis2tar=None
        self.ob_cls = []
        self.success_foj = 0
        
        self.done_count = 0
        self.duplicate_count = 0
        self.failed_action_count = 0
        self.episode_length = 0
        self.prev_frame = None
        self.current_frame = None
        self.scene_states = []

        self.state_reps = []
        self.state_memory = []
        self.action_memory = []

        self.target_object_detected = False

        self.episode_times += 1

        self.states = []
        self.actions_record = []
        self.action_outputs = []
        self.detection_results = []
        self.obs_reps = []

        self.action_failed_il = False

        self.action_probs = []
        self.meta_predictions = []
        self.visual_infos = {}
        self.match_score = []
        self.indices_topk = []

        self._new_episode(args, scenes, targets)
