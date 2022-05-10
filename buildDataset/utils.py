import colorsys
import numpy as np
import cv2
import random
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from constants import IN_RELATION_OBJS
else:
    # uses current package visibility
    from .constants import IN_RELATION_OBJS

COLOR_ATT = ['black', 'gray', 'white', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

COLOR_MODIFY = {
    'Apple': {
        'Apple1_AlbedoTransparency1 (UnityEngine.Texture2D)': ['red'],
        'Apple1_AlbedoTransparency3 (UnityEngine.Texture2D)': ['red'],
        'Apple1_AlbedoTransparency4 (UnityEngine.Texture2D)': ['red'],
        'Apple1_AlbedoTransparency5 (UnityEngine.Texture2D)': ['red'],
        'Apple1_AlbedoTransparency6 (UnityEngine.Texture2D)': ['red'],
        'Apple2_AlbedoTransparency1 (UnityEngine.Texture2D)': ['red'],
        'Apple2_AlbedoTransparency2 (UnityEngine.Texture2D)': ['red'],
        'Apple1_AlbedoTransparency2 (UnityEngine.Texture2D)': ['green'],
        'Apple1_AlbedoTransparency7 (UnityEngine.Texture2D)': ['green'],
        'Apple1_AlbedoTransparency8 (UnityEngine.Texture2D)': ['green'],
        'Apple2_AlbedoTransparency3 (UnityEngine.Texture2D)': ['yellow'],
        'ArmChair1_CouchFrameMat_MetallicSmoothness (UnityEngine.Texture2D)': ['black'],
    },
    'Pot': {
        'Copper_AlbedoTransparency (UnityEngine.Texture2D)': ['orange'],
    },
    'DishSponge':{
        'SpongeGreenYellow (UnityEngine.Texture2D)': ['green','yellow'],
    },
    'CellPhone':{
        'Cellphone_1A_AlbedoTransparency (UnityEngine.Texture2D)': ['white','black'],
        'Cellphone_1B_AlbedoTransparency (UnityEngine.Texture2D)': ['white','black'],
        'Cellphone_2B_AlbedoTransparency (UnityEngine.Texture2D)': ['white','black'],
        'Cellphone_4A_AlbedoTransparency (UnityEngine.Texture2D)': ['white','black'],
        'Cellphone_2A_AlbedoTransparency (UnityEngine.Texture2D)': ['black'],
        'Cellphone_3A_AlbedoTransparency (UnityEngine.Texture2D)': ['black'],
        'Cellphone_3B_AlbedoTransparency (UnityEngine.Texture2D)': ['blue','black'],
        'Cellphone_4B_AlbedoTransparency (UnityEngine.Texture2D)': ['red','black'],
    }
}

def getColor(obj):
    if obj['RGBA']['x']==1.0 and obj['RGBA']['y']==1.0 and obj['RGBA']['z']==1.0 and obj['objectType'] in COLOR_MODIFY.keys() and obj['texture_filename'] != '':
        return COLOR_MODIFY[obj['objectType']][obj['texture_filename']]
    rgb = obj['RGBA']
    h, s, v = colorsys.rgb_to_hsv(rgb['x'], rgb['y'], rgb['z'])
    color_att = hsv2color(int(h * 180), int(s * 255), int(v * 255))
    return color_att

def hsv2color(h, s, v):
    hlist = [list(range(0, 180 + 1)), list(range(0, 180 + 1)), list(range(0, 180 + 1)),
                list(range(0, 10 + 1)) + list(range(156, 180 + 1)),
                list(range(11, 25 + 1)), list(range(26, 34 + 1)), list(range(35, 77 + 1)), list(range(78, 99 + 1)),
                list(range(100, 124 + 1)), list(range(125, 155 + 1))]
    slist = [list(range(0, 255 + 1)), list(range(0, 43 + 1)), list(range(0, 43 + 1)), list(range(43, 255 + 1)),
                list(range(43, 255 + 1)), list(range(43, 255 + 1)), list(range(43, 255 + 1)), list(range(43, 255 + 1)),
                list(range(43, 255 + 1)), list(range(43, 255 + 1))]
    vlist = [list(range(0, 46 + 1)), list(range(46, 220 + 1)), list(range(221, 255 + 1)), list(range(46, 255 + 1)),
                list(range(46, 255 + 1)), list(range(46, 255 + 1)), list(range(46, 255 + 1)), list(range(46, 255 + 1)),
                list(range(46, 255 + 1)), list(range(46, 255 + 1))]
    h_idx = []
    s_idx = []
    v_idx = []
    color_list = []
    for id, color in enumerate(hlist):
        if h in color:
            h_idx.append(id)
    for id, color in enumerate(slist):
        if s in color:
            s_idx.append(id)
    for id, color in enumerate(vlist):
        if v in color:
            v_idx.append(id)
    for i in range(10):
        if (i in h_idx) and (i in s_idx) and (i in v_idx):
            # result = np.zeros(10)
            # result[i] += 1
            color_list.append(COLOR_ATT[i])
    return color_list

def getMaterial(obj):
    material = []
    if obj['salientMaterials'] is not None:
        material = material + obj['salientMaterials']
    return material

def getReference(obj, metadata):
    recep_ObjId = obj['receptacleObjectIds']
    parentRecep_ObjId = obj['parentReceptacles']
    neighbor_ObjId = obj['neighborObjectIDs']
    relation_ObjType = []

    if recep_ObjId is not None and len(recep_ObjId) > 0:
        for objId in recep_ObjId:
            relation_type = 'hold'+'|'+ objId.split('|')[0]
            relation_ObjType.append(relation_type)
    if parentRecep_ObjId is not None and len(parentRecep_ObjId) > 0:
        for objId in parentRecep_ObjId:
            type_ = objId.split('|')[0]
            if type_ == 'Floor' and len(parentRecep_ObjId) > 1:
                continue
            else:
                bbox1 = obj['axisAlignedBoundingBox']['cornerPoints'][-1]+obj['axisAlignedBoundingBox']['cornerPoints'][0]
                for otherObj in metadata:
                    if otherObj['objectId'] == objId:
                        bbox2 = otherObj['axisAlignedBoundingBox']['cornerPoints'][-1]+otherObj['axisAlignedBoundingBox']['cornerPoints'][0]
                if bbox1 and bbox2:
                    if isBboxContained(bbox1, bbox2) and type_ in IN_RELATION_OBJS:
                        relation_type = 'in'+'|'+ type_
                    else:
                        relation_type = 'on'+'|'+ type_
                    relation_ObjType.append(relation_type)
    if neighbor_ObjId is not None and len(neighbor_ObjId) > 0:
        for objId in neighbor_ObjId:
            if (recep_ObjId is not None and objId in recep_ObjId) or (parentRecep_ObjId is not None and objId in parentRecep_ObjId):
                continue
            else:
                relation_type = 'near'+'|'+ objId.split('|')[0]
                relation_ObjType.append(relation_type)   
    return relation_ObjType             


def isBboxContained(box1, box2):
    '''
        box [x1,y1,z1,x2,y2,z2]   
    '''
    area1 = (box1[3]-box1[0])*(box1[4]-box1[1])*(box1[5]-box1[2])
    area2 = (box2[3]-box2[0])*(box2[4]-box2[1])*(box2[5]-box2[2])
    area_sum = area1 + area2

    #calculate the overlap area, set the intersection bbox as [x1,y1,z1,x2,y2,z2]
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    z1 = max(box1[2], box2[2])
    x2 = min(box1[3], box2[3])
    y2 = min(box1[4], box2[4])
    z2 = min(box1[5], box2[5])
    if x1 >= x2 or y1 >= y2 or z1 >= z2:
        return False
    else:
        inter_area = (x2-x1)*(y2-y1)*(z2-z1)

    # Original IOU should return inter_area/(area_sum-inter_area)
    # if coverRatio (smaller one) > 0.5, then 'in' else 'on'
    if (inter_area/min(area1,area2)) > 0.5:
        return True

def color_choose():
    colors = [(102, 102, 255),
              (102, 255, 204),
              (204, 51, 255),
              (255, 114, 86),
              (255, 193, 37),
              (0, 153, 51),
              (238, 58, 140),
              (255, 106, 106),
              (164, 211, 238)]
    id = random.randint(0, len(colors)-1)
    return colors[id]


def draw_anchor(img, x, y, x_end, y_end, phrase):
    zeros = np.zeros((img.shape), dtype=np.uint8)
    color = color_choose()
    mask = cv2.rectangle(zeros, (x, y-15), (x_end, y), color, thickness=-1)
    new_img = cv2.addWeighted(img, 1, mask, 0.4, 0)
    new_img = cv2.rectangle(new_img, (x, y), (x_end, y_end), color, thickness=2)
    new_img = cv2.putText(new_img, phrase, (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 0, 0), 1)
    return new_img

def name_to_num(name):
    return ["kitchen", "living_room", "bedroom", "bathroom"].index(name)


def num_to_name(num):
    return ["kitchen", "", "living_room", "bedroom", "bathroom"][int(num / 100)]


if __name__=='__main__':
    # bbox1 = [-2.01954937,0.043677628,2.06741, -1.90500116, 0.171541914, 2.1819582]
    # bbox2 = [-2.103387,2.38418579e-07,1.77712607,-1.76361442,0.500411034,2.28087544] 
    bbox1 = [-0.231173187,1.78846443,-2.63570786, -0.11662513,1.91632879,-2.52115965,]
    bbox2 = [ -0.539615154,1.6890142,-2.70501041, 0.06675327,2.04253745,-2.3161478,]

    iou = isBboxContained()(bbox1,bbox2)
    print(iou)
