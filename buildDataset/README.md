## How to generate the ION dataset by yourself
### 1. Modify the AI2THOR simulator

There're two ways to modify the ai2thor simulator:

* **(Recommend)** Download our modified ai2thor (version 2.4.0) from the link  [AI2THOR_Modified_Build](https://drive.google.com/file/d/1hJiUMw6bySBlIMS_PGQD25iu8j3Gq063/view?usp=sharing) and extract it under the `ION/buildDataset/` folder.

* Install Unity Editor and edit from the source code of ai2thor (we use the version 2.4.0) and make the following changes. (This way is not guaranteed to succeed at the first try, since some unreasonable crash within Unity may happen)

  > This operation aims to add the 'SpecificSpawn' operation into the ai2thor simulator, which is similar to the official "Initial Random Spawn" but can specify the object type (A) and different receptacle object types (B) with scale\color\texture settings.  
  >
  > When doing the 'SpecificSpawn', it attemps to randomly choose one object prefab of the specific object A  (using the ai2thor resources, different prefabs usually relate to different looks), set the specified scale and color and texture_name, and then randomly place it onto one specified receptacle object B (if there are many objects of the same B object type, just randomly select one).

  * The details about how to edit the Unity Editor (updating...)

### 2. Run the script to generate our offline ION dataset!

```bash
cd ION/buildDataset
python generate_dataset.py
```

>  Every original rooms will be randomly initialized with 5 times, so that our ION dataset will include 600 rooms, which are named as FloorPlan1-1, FloorPlan1-2, ... FloorPlan1-5.
