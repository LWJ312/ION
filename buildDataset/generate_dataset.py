from ai2thor.controller import Controller
from Ai2thor_graph import generate_graph
from Ai2thor_visible import generate_visible_info
from multiprocessing import Pool
import os
import json
import cv2
import random
import torchvision
import torch.nn as nn
from constants import * 

def controller_init_(scene_name='FloorPlan1'):
    build_path = os.path.join(project_path, "buildDataset/AI2THOR_Modified_Build/build.x86_64")
    c = Controller(local_executable_path=build_path,scene=scene_name)
    c.step(dict(action='Initialize', gridSize=0.25, degrees=45))
    return c

def getAllScenes():
    scenes=[]
    #ithor
    type = [0,200,300,400]
    for t in type:
        for i in range(1,31):
            scene="FloorPlan" + str(t+i)
            scenes.append(scene)
    #robotthor
    # for i in range(1,13):
    #     for j in range(1,6):
    #         scene='FloorPlan_Train'+str(i)+'_'+str(j)
    #         scenes.append(scene)
    # for i in range(1,4):
    #     for j in range(1,6):
    #         scene='FloorPlan_Val'+str(i)+'_'+str(j)
    #         scenes.append(scene)
    return scenes

def diyObjsFromScene(scene, init_ObjTypes, seed):
    random.seed(seed)
    scene_id = int(scene.split('FloorPlan')[-1])
    scene_type = 'kitchen'*(scene_id<=30) + 'livingRoom'*(scene_id>=201 and scene_id<=230) + 'bedroom'*(scene_id>=301 and scene_id<=330) + 'bathroom'*(scene_id>=401 and scene_id<=430)
    multiInstance_ObjTypes = MULTI_INSTANCE[scene_type]
    candidate_ObjTypes = list(set(init_ObjTypes).intersection(set(multiInstance_ObjTypes)))
    # print(len(candidate_ObjTypes))
    candidate_ObjTypes.sort()
    if scene_id % 100 <= 20:
        if len(candidate_ObjTypes) > NUM_DIY_OBJTYPEs_SCENE_TRAIN:
            diy_ObjTypes = random.sample(candidate_ObjTypes, NUM_DIY_OBJTYPEs_SCENE_TRAIN)
        else:
            diy_ObjTypes = candidate_ObjTypes
    else:
        if len(candidate_ObjTypes) > NUM_DIY_OBJTYPEs_SCENE_TEST:
            diy_ObjTypes = random.sample(candidate_ObjTypes, NUM_DIY_OBJTYPEs_SCENE_TEST)
        else:
            diy_ObjTypes = candidate_ObjTypes
    # print(diy_ObjTypes)

    diy_objs_recep = []
    diy_objs_others = []
    for objType in diy_ObjTypes:
        diy_obj = {'objectType': objType}
        repType = []
        scale = []
        texture = []
        color = []

        candidate_RepObjTypes = list(set(init_ObjTypes).intersection(set(OBJ_TO_RECEP[objType])))
        candidate_RepObjTypes.sort()
        # thoughts for bathroom 
        if scene_id % 100 <= 20:
            copy_times = min(len(candidate_RepObjTypes), NUM_MAX_SPAWNTIMES_TRAIN[len(candidate_RepObjTypes)>1])
        else:
            copy_times = min(len(candidate_RepObjTypes), NUM_MAX_SPAWNTIMES_TEST[len(candidate_RepObjTypes)>1])
        for count in range(copy_times):
            rep = random.choices(candidate_RepObjTypes)[0]
            repType.append(rep)
            scale.append([1.0, 1.0, 1.0])
            texture.append(None)
            color_prob = random.random()
            if objType in PREFABS_IN_MULTI_INSTANCE:
                if color_prob <= PROBABILITY_DIY_COLOR_PREFABS:
                    color.append(*random.choices(OBJ_TO_COLOR[objType]))
                else:
                    color.append(None)
            else:
                if color_prob <= PROBABILITY_DIY_COLOR_SINGLE:
                    color.append(*random.choices(OBJ_TO_COLOR[objType]))
                else:
                    color.append(None)
            
        diy_obj['RepType'] = repType
        diy_obj['Scale'] = scale
        diy_obj['Texture'] = texture
        diy_obj['Color'] = color

        if objType in RECEP_IN_MULTI_INSTANCE:
            diy_objs_recep.append(diy_obj)
        else:
            diy_objs_others.append(diy_obj)
    
    return diy_objs_recep, diy_objs_others

def sample_one_scene(scene, randomSeed):
    c = controller_init_(scene)
    gridSize=c.last_action['gridSize']
    
    resnet18 = torchvision.models.resnet18(pretrained=True)
    modules = list(resnet18.children())[:-2]
    model = nn.Sequential(*modules)
    model.cuda()

    scene_dir = dataset_dir + '/' + scene
    initObjTypes = []    
    objs = c.last_event.metadata['objects']
    for obj in objs:
        if obj['objectType'] not in initObjTypes:
            initObjTypes.append(obj['objectType'])
    # print('InitObjTypes: ', len(initObjTypes), initObjTypes)

    # Every scene will diy 5 times
    for sub in range(1, num_sub_scenes+1):
        c.reset(scene)
        c.step(dict(action='Initialize',
                gridSize=0.25,
                degrees=45,
                renderObjectImage=True,
                renderClassSegmentation=True))
        save_dir = scene_dir + '-'+ str(sub)
        print('---Sampling {}'.format(save_dir))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # diy scene
        objsToSpawn_recep, objsToSpawn_others = diyObjsFromScene(scene, initObjTypes, randomSeed+sub)
        # specificSpawn.json
        objsToSpawn_filePath = save_dir + '/specificSpawn.json'
        spawnContent = [{'seed': randomSeed+sub}]
        spawnContent = spawnContent + objsToSpawn_recep + objsToSpawn_others
        with open(objsToSpawn_filePath, 'w') as f:
            json.dump(spawnContent, f, indent=4)
        
        # print(objsToSpawn_recep)
        if len(objsToSpawn_recep):
            c.step(action='SpecificSpawn',
                randomSeed=randomSeed+sub,
                placeStationary=True,
                numPlacementAttempts= NUM_PLACEMENT_ATTEMPTS,
                numObjToRepOfType = objsToSpawn_recep
            )
            # print(c.last_event.metadata['lastActionSuccess'])

        c.step(action='SpecificSpawn',
                randomSeed=randomSeed+sub,
                placeStationary=True,
                numPlacementAttempts= NUM_PLACEMENT_ATTEMPTS,
                numObjToRepOfType = objsToSpawn_others
        )
        # print(c.last_event.metadata['lastActionSuccess'])
        # allObject.json
        allObject = c.last_event.metadata['objects']
        with open(save_dir + '/allObject.json', 'w') as wf:
            json.dump(allObject, wf)

        # SAMPLE offline_data and label GT
        # grid.json
        event = c.step(action="GetReachablePositions")
        positions = event.metadata['reachablePositions']
        with open(save_dir + '/grid.json', 'w') as wf:
            json.dump(positions, wf)
        
        # graph.json
        generate_graph(save_dir, gridSize, positions)
        # resnet18_featuremap.hdf5
        # class_masks.hdf5
        # bbox.json
        # ins/nav/cate_visible.json
        generate_visible_info(save_dir, c, model, positions)
    
        # Top-Down image
        event = c.step('ToggleMapView')
        img = event.cv2img
        cv2.imwrite(save_dir +'/TopView.jpg', img)
    
    c.stop()


if __name__ == '__main__':
    randomSeed = 1024
    num_sub_scenes = 5
    project_path = os.path.abspath('..')
    dataset_dir = os.path.join(project_path, 'ION_dataset')
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)

    # scenes=getAllScenes()[:30]
    scenes= ['FloorPlan401']
    
    # pool = Pool(processes=2)
    # for i, scene in enumerate(scenes):
    #     id = int(scene.split('FloorPlan')[-1])
    #     pool.apply_async(func=sample_one_scene, args=(scene, randomSeed+num_sub_scenes*(id-1)))

    # pool.close()
    # pool.join()


    id = int(scenes[0].split('FloorPlan')[-1])
    sample_one_scene(scenes[0], randomSeed+num_sub_scenes*(id-1))
        
        
        




            


         