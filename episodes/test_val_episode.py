""" Contains the Episodes for Navigation. """
from ast import arg
from buildDataset.environment import Environment
from buildDataset.offline_controller_with_small_rotation import ThorAgentState
from buildDataset.constants import GOAL_SUCCESS_REWARD, STEP_PENALTY, ALL_GOALS_TEMP ,ALL_OBJS_TEMP,MODIFY_OBJS
from buildDataset.constants import DONE,TARGETS,REFERENCES,COLOR_ATT,MATERIAL_ATT,LINK
from utils.model_util import gpuify
from .basic_episode import BasicEpisode
import pickle
import random
from buildDataset.utils import num_to_name


class TestValEpisode(BasicEpisode):
    """ Episode for Navigation. """

    def __init__(self, args, gpu_id, strict_done=False):
        super(TestValEpisode, self).__init__(args, gpu_id, strict_done)
        self.file = None
        self.all_data = None
        self.all_data_enumerator = 0

        self.model_update = False

    def _new_episode(self, args, episode):
        """ New navigation episode. """
        scene = episode["scene"]
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
            )
            self._env.start(scene)
        else:
            self._env.reset(scene)
        self.environment.controller.select = args.select
        objects = self._env.all_objects()
        
        y = 0.9009995
        x, z, hor, rot = episode['state'].split('|')
        self.environment.controller.state = ThorAgentState(float(x), float(y), float(z), float(hor), float(rot))
        self.task_data=[]
        self.task_data_cls = []

        task = episode['task_data'][0].split("|")
        for id_ in objects:
            first = id_.split("|")[0]
            last = id_.split("|")[-1]
            if first in MODIFY_OBJS.keys():
                first = MODIFY_OBJS[first]
            if last in MODIFY_OBJS.keys():
                last = MODIFY_OBJS[last]
            if (task[0] == first):
                self.task_data_cls.append(id_)
                if args.catelv:
                    self.task_data.append(id_)
                elif (task[0]==first) and (task[1]==id_.split("|")[1]) and \
                    (task[2]==id_.split("|")[2]) and(task[3]==id_.split("|")[3]) and (task[4]==last):
                    self.task_data.append(id_)
        self.target_object = episode['goal_object_type']
        self.goal_embedding, self.glove_embedding = self.get_goal_embedding(episode['task_data'][0].split('|'))

        if args.verbose:
            print('Scene', scene, 'Navigating towards:', self.target_object)

        return True

    def new_episode(self, args, scenes, targets):
        self.move_count= 0
        self.ep_area=[]
        self.dis2tar=None
        self.ob_cls = []
        self.done_count = 0
        self.duplicate_count = 0
        self.failed_action_count = 0
        self.prev_frame = None
        self.current_frame = None
        self.scene_states = []

        self.state_reps = []
        self.state_memory = []
        self.action_memory = []

        self.states = []
        self.actions_record = []
        self.action_outputs = []
        self.detection_results = []
        self.obs_reps = []

        self.target_object_detected = False

        self.action_failed_il = False

        self.model_update = False

        self.action_probs = []
        self.meta_predictions = []
        self.visual_infos = {}
        self.match_score = []
        self.indices_topk = []

        if self.file is None:
            sample_scene = scenes[0]
            scene_num = sample_scene.split('-')[0][9:]
            scene_num = int(scene_num)
            scene_type = num_to_name(scene_num)
            task_type = args.test_or_val
            self.file = open(
                "./test_val_split/" + scene_type + "_" + task_type + ".pkl", "rb"
            )
            self.all_data = pickle.load(self.file)
            self.file.close()
            self.all_data_enumerator = 0
            # random.shuffle(self.all_data)

        episode = self.all_data[self.all_data_enumerator]
        self.all_data_enumerator += 1
        self._new_episode(args, episode)
