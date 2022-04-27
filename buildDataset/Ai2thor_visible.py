from utils import getColor, getMaterial, getReference, draw_anchor
from constants import ALL_GOALS_TEMP
import json
import sys
import pickle
import numpy as np
import torch 
import cv2
import h5py
import os

#sys.setrecursionlimit(2000)

def generate_visible_info(save_dir, c, model, positions):
    hdf_dict={}   # pos_str: [feature]
    masks_dict={} # pos_str: [class_masks feature]
    bbox = {}     # pos_str: [category|color|material|bbox, category|color|material|bbox, ...]
    ins_visible_map = {}  # goal(category|color|material|reference): [pos_str|bbox, pos|str+bbox]
    nav_visible_map = {}  # goal(category|color|material|reference): [pos_str, pos_str]
    cate_visible_map = {} # goal(category only): [pos_str|bbox, pos_str|bbox, ...]

    count = 0
    for pos in positions:
        c.step(action='Teleport', **pos)
        for i in range(8):
            event = c.step(dict(action='RotateLeft',
                                degrees=45,
                                gridSize=0.25))

            for lookDown_Up in range(2):
                if lookDown_Up == 1:
                    event = c.step(dict(action='LookDown',
                                degrees=30,
                                gridSize=0.25))

                current_bboxes = event.instance_detections2D
                rot = int(event.metadata['agent']['rotation']['y'] + 0.5)
                if rot ==360:
                    rot =0
                pos_str = str('%.2f' % pos['x']) + '|' + str('%.2f' % pos['z']) + '|' \
                        + str(rot) + '|' + str(int(event.metadata['agent']['cameraHorizon'] + 0.5))
                
                image=np.array(cv2.resize(event.cv2img,(224,224)))
                t_image=torch.from_numpy(image.transpose((2,0,1))).float().div(255).unsqueeze(0)
                feature = model(t_image.cuda()).detach().cpu().numpy()
                hdf_dict[pos_str]=feature

                img = event.cv2img
                count = count + 1

                save_feature = np.zeros((len(ALL_GOALS_TEMP),7, 7))
                class_masks = event.class_masks
                for k in class_masks:
                    if k in ALL_GOALS_TEMP:
                        down_mask = np.zeros((7,7))
                        for i in range(300):
                            for j in range(300):
                                x = int(i*6.99/300)
                                y = int(j*6.99/300)
                                down_mask[x][y] += class_masks[k][i][j]*0.001
                        save_feature[ALL_GOALS_TEMP.index(k)] = down_mask
                masks_dict[pos_str] = save_feature

                for obj in event.metadata['objects']:
                    if obj['visible'] and obj['distance']<1.5 and obj['objectId'] in current_bboxes.keys():
                        objId = obj['objectId']

                        obj_type = obj['objectType']
                        obj_color = getColor(obj)         # list
                        obj_material = getMaterial(obj)   # list
                        obj_relation_ObjType = getReference(obj, event.metadata['objects']) # list

                        if pos_str not in bbox.keys():
                            bbox[pos_str] =[]
                        obj_bbox = list(current_bboxes[objId])
                        gt = pos_str + '|' + '-'.join(str(i) for i in obj_bbox)

                        obj_bbox_str = str(obj_type)+'|'+'-'.join(str(color) for color in obj_color) +'|' + '-'.join(str(material) for material in obj_material) +'|' +'-'.join(str(x) for x in obj_bbox) 
                        bbox[pos_str].append(obj_bbox_str)
                        # img = draw_anchor(img, *obj_bbox, obj['objectType'])

                        if obj_type not in cate_visible_map.keys():
                            cate_visible_map[obj_type] = []
                        cate_visible_map[obj_type].append(gt)

                        for relation_ObjType in obj_relation_ObjType:
                            goal = str(obj_type) + '|' + '-'.join(str(color) for color in obj_color) +'|' + '-'.join(str(material) for material in obj_material) + '|' +str(relation_ObjType)
                            if goal not in ins_visible_map.keys():
                                ins_visible_map[goal] = []
                            ins_visible_map[goal].append(gt)
                            if goal not in nav_visible_map.keys():
                                nav_visible_map[goal] = []
                            nav_visible_map[goal].append(pos_str)

                # img_dir = save_dir + '/pic'
                # if not os.path.exists(img_dir):
                #     os.makedirs(img_dir)
                # cv2.imwrite(img_dir+'/{:0>6d}.jpg'.format(count), img)

                if lookDown_Up == 1:
                    event = c.step(dict(action='LookUp',
                                        degrees=30,
                                        gridSize=0.25))

    # resnet18_featuremap.hdf5
    with h5py.File(save_dir+'/resnet18_featuremap.hdf5','w') as f:
        for k,v in hdf_dict.items():
            f.create_dataset(k,data=v)

    # class_masks.hdf5
    with h5py.File(save_dir+'/class_masks.hdf5','w') as f:
        for k,v in masks_dict.items():
            f.create_dataset(k,data=v)

    # bbox.json
    with open(save_dir+'/bbox.json','w') as wf:
        # pickle.dump(bbox,wf)
        json.dump(bbox, wf)  
    
    # LABEL Ground Truth
    # ins_visible_location-bbox.json
    with open(save_dir+'/ins_visible_location_bbox.json', 'w') as wf:
        json.dump(ins_visible_map, wf)
    # nav_visible_location.json
    with open(save_dir+'/nav_visible_location.json', 'w') as wf:
        json.dump(nav_visible_map, wf)
    # cate_visible_location-bbox.json
    with open(save_dir+'/cate_visible_location_bbox.json', 'w') as wf:
        json.dump(cate_visible_map, wf)   
    
    
