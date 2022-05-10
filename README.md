# ION: Instance-level Object Navigation

> Weijie Li, Xinhang Song, Yubing Bai, Sixian Zhang, Shuqiang Jiang. 29th ACM International Conference on Multimedia (ACM Multimedia 2021), Chengdu, China, October 20-24, 2021.

ION (Instance-level Object Navigation) is a task which requires the agent to find the specific target, given the instance-level descriptions *<category, color, material, reference>*. The ION dataset is built for this task based on the AI2THOR simulator.

[ACMMM 2021 Paper](https://dl.acm.org/doi/pdf/10.1145/3474085.3475575) | [Website](http://123.57.42.89/Dataset_ION/home.html)

## Setup

1. **Clone this  repository and go into this project**

```bash
git clone https://github.com/LWJ312/ION.git
cd ION
```

2. **Setup the conda environment and install other dependencies**

```bash
conda create --name objnav python=3.6
conda activate objnav
pip install -r requirements.txt
```

3. Prepare the **ION datase**t. 

   * Download from the link [ION_dataset (~63G) ](http://123.57.42.89/Dataset_ION/ION_dataset.zip), and extract into the `ION/ION_dataset` folder. Note that the whole dataset is offline sampled, including 600 rooms. The whole decompressed dataset is about **140 G.**
   * The right ION_dataset folder should look like:

   ```
    ION_dataset/ 
       └── FloorPlan1-1/
       │   ├── TopView.jpg
       │   ├── allObject.json
       │   ├── grid.json
       │   ├── graph.json
       │   ├── bbox.json
       │   ├── specificSpawn.json
       │   ├── resnet18_featuremap.hdf5
       │   ├── detect_att.hdf5
       │   ├── class_masks.hdf5
       │   ├── ins_visible_location_bbox.json
       │   ├── nav_visible_location.json
       │   └── cate_visible_location_bbox.json
       ├── ...
       ├── FloorPlan1-5/
       │   ├── ...
       ├── FloorPlan2-1/
       │   ├── ...
       └── ...
   ```



## Our method

### Train

* Base model

```bash
python main.py --title BaseModel --model BaseModel --workers 12 --gpu-ids 0
```

* IRG model

```bash
python main.py --title IRGModel --model IRGModel --workers 12 --gpu-ids 0
```

* IRGSemMap model

```bash
python main.py --title IRGSemMap --model IRGSemMap --workers 12 --gpu-ids 0
```

### Evaluation

* Base model

```bash
# Instance-Localization metric
python full_eval.py --title BaseModel --model BaseModel --results-json Base_IL.json --gpu-ids 0 --select
# Instance-Navigation metric
python full_eval.py --title BaseModel --model BaseModel --results-json Base_IN.json --gpu-ids 0 
# Category-Localization metric
python full_eval.py --title BaseModel --model BaseModel --results-json Base_CL.json --gpu-ids 0 --catelv --select
```

* IRG model

```bash
# Instance-Localization metric
python full_eval.py --title IRGModel --model IRGModel --results-json IRG_IL.json --gpu-ids 0 --select
# Instance-Navigation metric
python full_eval.py --title IRGModel --model IRGModel --results-json IRG_IN.json --gpu-ids 0 
# Category-Localization metric
python full_eval.py --title IRGModel --model IRGModel --results-json IRG_CL.json --gpu-ids 0 --catelv --select
```

* IRGSemMap model

```bash
# Instance-Localization metric
python full_eval.py --title IRGSemMap --model IRGSemMap --results-json IRGSemMap_IL.json --gpu-ids 0 --select
# Instance-Navigation metric
python full_eval.py --title IRGSemMap --model IRGSemMap --results-json IRGSemMap_IN.json --gpu-ids 0
# Category-Localization metric
python full_eval.py --title IRGSemMap --model IRGSemMap --results-json IRGSemMap_CL.json --gpu-ids 0 --catelv --select
```

-----------

## Cite

If you use ION in your research, please cite the following:

```
@inproceedings{DBLP:conf/mm/LiSBZJ21,
  author    = {Weijie Li and
               Xinhang Song and
               Yubing Bai and
               Sixian Zhang and
               Shuqiang Jiang},
  editor    = {Heng Tao Shen and
               Yueting Zhuang and
               John R. Smith and
               Yang Yang and
               Pablo Cesar and
               Florian Metze and
               Balakrishnan Prabhakaran},
  title     = {{ION:} Instance-level Object Navigation},
  booktitle = {{MM} '21: {ACM} Multimedia Conference, Virtual Event, China, October
               20 - 24, 2021},
  pages     = {4343--4352},
  publisher = {{ACM}},
  year      = {2021},
  url       = {https://doi.org/10.1145/3474085.3475575},
  doi       = {10.1145/3474085.3475575},
  timestamp = {Wed, 20 Oct 2021 12:40:01 +0200},
  biburl    = {https://dblp.org/rec/conf/mm/LiSBZJ21.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```











