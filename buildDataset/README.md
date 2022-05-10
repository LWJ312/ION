## How to generate the ION dataset

> Note that this script only shows how our ION dataset is generated. 
>
> Re-run the script is not guaranteed to generate the totally same dataset as ours (even though each room could generate the same `specificSpawn.json` ), since the initialization operation in the modified simulator is in the random way, which would create different object layouts.

### 1. Modify the AI2THOR simulator

There're two ways to modify the ai2thor simulator:

* **(Recommend)** Download our modified ai2thor (version 2.4.0) from the link  [AI2THOR_Modified_Build](http://123.57.42.89/Dataset_ION/AI2THOR_Modified_Build.zip) and extract it into the folder `ION/buildDataset/AI2THOR_Modified_Build`

* Install Unity Editor and edit from the source code of ai2thor (we use the version 2.4.0) and make the following changes. (This way is not guaranteed to succeed at the first try, since some unreasonable crash within Unity may happen)

  > This operation aims to add the 'SpecificSpawn' operation into the ai2thor simulator, which is similar to the official "Initial Random Spawn" but can specify the object type (A) and different receptacle object types (B) with scale\color\texture settings.  
  >
  > When doing the 'SpecificSpawn', it attemps to randomly choose one object prefab of the specific object A  (using the ai2thor resources, different prefabs usually relate to different looks), set the specified scale and color and texture_name, and then randomly place it onto one specified receptacle object B (if there are many objects of the same B object type, just randomly select one).

  * The details about how to edit the Unity Editor (updating...)

### 2. Run the script to generate the ION dataset

* The (offline) ION dataset is (online) sampled from the AI2THOR simulator, which requires the `ai2thor version >= 2.4.0` since our modified AI2THOR is based on 2.4.0.

  ```bash
  conda create --name buildION python=3.6
  conda activate buildION
  pip install -r requirements_ION.txt
  ```

* Run the script.

  ```bash
  cd ION/buildDataset
  python generate_dataset.py
  ```

>  Every original rooms will be randomly initialized with 5 times, so that the ION dataset will include 600 rooms, which are named as FloorPlan1-1, FloorPlan1-2, ... FloorPlan1-5.

