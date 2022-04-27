# train
NUM_DIY_OBJTYPEs_SCENE_TRAIN = 5
NUM_MAX_SPAWNTIMES_TRAIN = [2, 5]
# test
NUM_DIY_OBJTYPEs_SCENE_TEST = 7
NUM_MAX_SPAWNTIMES_TEST = [1, 3]
NUM_PLACEMENT_ATTEMPTS = 100
PROBABILITY_DIY_COLOR_PREFABS = 0.4  
PROBABILITY_DIY_COLOR_SINGLE = 0.6

SINGLE_INSTANCE = {
    'kitchen': ['StoveBurner', 'Sink', 'Microwave', 'Toaster', 'Fridge', 'CoffeeMachine', 'LightSwitch'],
    'livingRoom': ['Television', 'LightSwitch'],
    'bedroom': ['Television', 'LightSwitch'],
    'bathroom': ['Sink', 'LightSwitch'],
}

# Some appearance-similar classes will be modified into one class (according to the following MODIFY_OBJS), e.g., FloorLamp and DeskLamp -> Lamp
MULTI_INSTANCE = {
    'kitchen': ['SoapBottle', 'Pan', 'Plate', 'Pot', 'GarbageCan', 'Bowl', 'Chair', 'Apple', 'DishSponge', 'PaperTowelRoll'],
    'livingRoom': ['Chair', 'FloorLamp', 'Box', 'Laptop', 'GarbageCan', 'Pillow', 'RemoteControl', 'DeskLamp', 'Plate', 'Book', 'CellPhone', 'Bowl', 'TissueBox'],
    'bedroom': ['Chair', 'Pillow', 'DeskLamp', 'Book', 'Laptop', 'CellPhone', 'GarbageCan', 'AlarmClock', 'Bowl', 'Box', 'RemoteControl', 'Cloth', 'TissueBox'],
    'bathroom': ['PaperTowelRoll', 'ToiletPaper', 'SoapBottle', 'GarbageCan', 'Cloth', 'SoapBar', 'DishSponge', 'TissueBox']
}

MODIFY_OBJS = {
    'ToiletPaper': 'PaperTowelRoll',
    'DeskLamp': 'Lamp',
    'FloorLamp': 'Lamp',
    'CoffeeTable': 'Table',
    'DiningTable': 'Table',
    'SideTable': 'Table',
    'BathtubBasin': 'Bathtub',
    'SinkBasin': 'Sink',
    'Ottoman': 'ArmChair',
}

RECEP_IN_MULTI_INSTANCE= ['Bowl', 'Box', 'Chair', 'GarbageCan', 'Pan', 'Plate', 'Pot']

OBJ_TO_RECEP = {
    'AlarmClock': ['Box', 'Dresser', 'Desk', 'SideTable', 'DiningTable', 'TVStand', 'CoffeeTable', 'CounterTop', 'Shelf'],
    'Apple': ['Pot', 'Pan', 'Bowl', 'Plate', 'SinkBasin', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'Desk', 'CounterTop', 'GarbageCan', 'Dresser'],
    'Book': ['Chair', 'Sofa', 'ArmChair', 'Box', 'Ottoman', 'Dresser', 'Desk', 'Bed', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf'],
    'Bowl': ['Chair', 'Dresser', 'Desk', 'SinkBasin','DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf'],
    'Box': ['Floor', 'Sofa', 'ArmChair', 'Dresser', 'Desk', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'Ottoman'],
    'CellPhone': ['Chair', 'Sofa', 'ArmChair', 'Box', 'Ottoman', 'Dresser', 'Desk', 'Bed', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'Safe'],
    'Chair': ['Floor'],
    'Cloth': ['Floor', 'Sofa', 'ArmChair', 'Box', 'Ottoman', 'Dresser', 'LaundryHamper', 'Desk', 'Toilet', 'BathtubBasin', 'Bathtub', 'SinkBasin', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'DeskLamp': ['CoffeeTable', 'DiningTable', 'SideTable', 'Desk', 'Shelf', 'Dresser'],
    'FloorLamp': ['Floor'],
    'DishSponge': ['Pot', 'Pan', 'Bowl', 'Plate', 'Box', 'Toilet', 'BathtubBasin', 'Bathtub', 'SinkBasin',  'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'GarbageCan': ['Floor'],
    'Laptop':['Chair', 'Sofa', 'ArmChair', 'Ottoman', 'Dresser', 'Desk', 'Bed', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop'],
    'Pan': ['DiningTable', 'CounterTop', 'TVStand', 'CoffeeTable', 'SideTable', 'SinkBasin','StoveBurner'],
    'PaperTowelRoll': ['Dresser', 'Desk', 'Toilet', 'ToiletPaperHanger', 'Bathtub','DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'ToiletPaper': ['Dresser', 'Desk', 'Toilet', 'ToiletPaperHanger', 'Bathtub','DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'Pillow': ['Floor', 'Sofa', 'ArmChair', 'Ottoman', 'Bed'],
    'Plate': ['Chair', 'Dresser', 'Desk', 'SinkBasin','DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf'],
    'Pot': ['Chair', 'StoveBurner', 'SinkBasin', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf'],
    'RemoteControl': ['Sofa', 'ArmChair', 'Box', 'Ottoman', 'Dresser', 'Desk', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf'],
    'SoapBar': ['Toilet', 'Bathtub', 'BathtubBasin', 'SinkBasin', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'SoapBottle': ['Dresser', 'Desk', 'Toilet',  'Bathtub', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf', 'GarbageCan'],
    'TissueBox': ['Box', 'Dresser', 'Desk', 'Toilet', 'DiningTable', 'TVStand', 'CoffeeTable', 'SideTable', 'CounterTop', 'Shelf','GarbageCan'],
} 

PREFABS_IN_MULTI_INSTANCE = ['AlarmClock','Apple','Book','Bowl','Box','CellPhone','Cloth','DeskLamp','FloorLamp','GarbageCan','Pan','Pillow','Plate','Pot','SoapBottle']

IN_RELATION_OBJS = ['Sink', 'Microwave', 'Toaster', 'Fridge', 'CoffeeMachine','Bowl', 'Box', 'GarbageCan', 'Pot']

# 31 categories of Goal（following MODIFY_OBJS to union some classes，and get 29 categories at last）
ALL_GOALS_TEMP = set()
for k, v in SINGLE_INSTANCE.items():
    for obj in v:
        ALL_GOALS_TEMP.add(obj)
for k, v in MULTI_INSTANCE.items():
    for obj in v:
        ALL_GOALS_TEMP.add(obj)
ALL_GOALS_TEMP = list(ALL_GOALS_TEMP)

# 29 categories Goal
TARGETS = ['Laptop', 'Lamp', 'AlarmClock', 'PaperTowelRoll', 'Book', 'CoffeeMachine', 'GarbageCan',
           'Apple', 'Plate', 'RemoteControl', 'Box', 'SoapBar', 'Bowl', 'LightSwitch', 'SoapBottle',
           'Chair', 'Cloth', 'DishSponge', 'Pan', 'Pillow', 'Sink', 'StoveBurner', 'TissueBox',
           'Toaster', 'CellPhone', 'Pot', 'Fridge', 'Television', 'Microwave']

# 51 categories of objects (including Goal and reference object) 
# (following MODIFY_OBJS to union some classes, and get 44 categoreis at last)
ALL_OBJS_TEMP = set(ALL_GOALS_TEMP)
for k, v in OBJ_TO_RECEP.items():
    for obj in v:
        ALL_OBJS_TEMP.add(obj)
ALL_OBJS_TEMP = list(ALL_OBJS_TEMP)

# 44 categories
REFERENCES = ['Sofa', 'RemoteControl', 'Toaster', 'Pillow', 'Lamp', 'Chair', 'SoapBar', 'Pan',
              'Dresser', 'Box', 'Safe', 'Bathtub', 'ToiletPaperHanger', 'LightSwitch', 'Shelf',
              'Floor', 'Desk', 'SoapBottle', 'TVStand', 'DishSponge', 'Table', 'Toilet', 'Television',
              'Bowl', 'PaperTowelRoll', 'ArmChair', 'AlarmClock', 'CoffeeMachine', 'Bed', 'Apple',
              'CounterTop', 'Pot', 'Sink', 'Cloth', 'Laptop', 'CellPhone', 'Microwave', 'GarbageCan',
              'LaundryHamper', 'Fridge', 'Plate', 'Book', 'StoveBurner', 'TissueBox']
COLOR_ATT=['black','gray','white','red','orange','yellow','green','cyan','blue','purple']
MATERIAL_ATT=['Metal','Wood','Plastic','Glass','Ceramic','Stone',
              'Fabric','Rubber','Food','Paper','Wax','Soap','Sponge','Organic','Leather']
LINK=['hold','on','in','near']

ALL_COLORS = [
    [0.0, 0.0, 0.0], #0
    [0.5, 0.5, 0.5], #1
    [1.0, 1.0, 1.0], #2
    [1.0, 0.0, 0.0], #3
    [1.0, 0.647, 0], #4
    [1.0, 1.0, 0],   #5
    [0, 1.0, 0],     #6
    [0, 1.0, 1.0],   #7
    [0, 0, 1.0],     #8
    [0.545, 0, 1.0]  #9
]

OBJ_TO_COLOR = {
    'AlarmClock': ALL_COLORS,
    'Apple': [ALL_COLORS[i] for i in [3,4,5,6,0]],
    'Book': ALL_COLORS,
    'Bowl': ALL_COLORS,
    'Box': ALL_COLORS,
    'CellPhone': [ALL_COLORS[i] for i in [0,1,3,4,5,6,7,8,9]],
    'Chair': ALL_COLORS,
    'Cloth': ALL_COLORS,
    'DeskLamp': ALL_COLORS,
    'FloorLamp': ALL_COLORS,
    'DishSponge':  [ALL_COLORS[i] for i in [0,1,3,4,5,6,7,8,9]],
    'GarbageCan': ALL_COLORS,
    'Laptop':  [ALL_COLORS[i] for i in [0,1,2]],
    'Pan': ALL_COLORS,
    'PaperTowelRoll':[ALL_COLORS[2]],
    'ToiletPaper': [ALL_COLORS[2]],
    'Pillow': ALL_COLORS,
    'Plate': ALL_COLORS,
    'Pot': [ALL_COLORS[i] for i in [0,1,3,4,5,6,7,8,9]],
    'RemoteControl': [ALL_COLORS[i] for i in [0,1,2]],
    'SoapBar': ALL_COLORS,
    'SoapBottle': ALL_COLORS,
    'TissueBox':  ALL_COLORS,
}

MOVE_AHEAD = 'MoveAhead'
ROTATE_LEFT = 'RotateLeft'
ROTATE_RIGHT = 'RotateRight'
LOOK_UP = 'LookUp'
LOOK_DOWN = 'LookDown'
DONE = 'Done'

# navigation rewards
DONE_ACTION_INT = 5
SAMECLASS_INT = 1
GOAL_SUCCESS_REWARD = 5
STEP_PENALTY = -0.01

# wandering rewards
DUPLICATE_STATE = -0.01
UNSEEN_STATE = 0.1

if __name__ == '__main__':
    print(ALL_GOALS_TEMP)
    print(len(ALL_GOALS_TEMP))
    print(ALL_OBJS_TEMP)
    print(len(ALL_OBJS_TEMP))