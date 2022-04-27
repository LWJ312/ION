from logging import RootLogger
import os
import h5py
import json
import shutil
import filecmp

from torch.multiprocessing import Manager
from tqdm import tqdm
from networkx.readwrite import json_graph


# loading the possible scenes
def loading_scene_list(args):
    scenes = []

    for i in range(4):
        if args.phase == 'train':
            for j in range(20):
                for k in range(1,6):
                    if i == 0:
                        scenes.append("FloorPlan" + str(j + 1) + '-' + str(k))
                    else:
                        scenes.append("FloorPlan" + str(i + 1) + '%02d' % (j + 1) + '-' + str(k))

        elif args.phase == 'eval':
            eval_scenes_list = []
            for j in range(10):
                for k in range(1,6):
                    if i == 0:
                        eval_scenes_list.append("FloorPlan" + str(j + 1) + '-' + str(k))
                    else:
                        eval_scenes_list.append("FloorPlan" + str(i + 1) + '%02d' % (j + 1 + 20) + '-' + str(k))
            scenes.append(eval_scenes_list)

    return scenes


# check scene data
def check_data(args):
    return
    root_dir = os.path.abspath("..")
    source_data_dir = os.path.join(root_dir, 'ION_dataset')
    # source_data_dir = os.path.expanduser('~/Data/AI2thor_offline_data_2.0.2/')
    scene_data_dir = args.data_dir
    if (os.path.exists(scene_data_dir) and os.listdir(scene_data_dir)
            and len(filecmp.dircmp(source_data_dir, scene_data_dir,
                                   ignore=['images.hdf5', 'metadata.json']).left_only) == 0):
        print('Scene Data Exists!')
    else:
        print('Start Copying Dataset to {} ...'.format(scene_data_dir))
        if os.path.exists(scene_data_dir):
            os.removedirs(scene_data_dir)
        shutil.copytree(source_data_dir, scene_data_dir,
                        ignore=shutil.ignore_patterns('images.hdf5', 'metadata.json', 'depth.json',
                                                      'instance_segmentation.json'))
        print('Copy Done!')
