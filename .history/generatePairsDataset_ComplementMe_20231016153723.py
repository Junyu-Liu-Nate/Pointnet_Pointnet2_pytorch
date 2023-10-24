import os
import numpy as np
import random

from generateWholeFeatures import computeWholeFeature
from fileIO import readWholePointnetFeatures_ShapeNet, readSelectedMD5s

BASE_DATA_PATH = "/Users/liujunyu/Data/Research/BVC/ITSS/"

def generatePairsDataset(outputPath):
    #%% Load pre-generated features for whole shapes
    ### Load ShapeNet v2 ComplementMe portion whole shape features
    whole_feature_path = os.path.join(BASE_DATA_PATH, "dataset", "ShapeNetv2_Wholes_100", "airplane")
    selectedNamePath = os.path.join(BASE_DATA_PATH, "dataset", "ComplementMe", "components", "Airplane", "component_all_md5s.txt")
    selectedWholeNames = readSelectedMD5s(selectedNamePath)

    wholeFeaturesDict = readWholePointnetFeatures_ShapeNet(whole_feature_path, selectedWholeNames)
    wholeNames = list(wholeFeaturesDict.keys())
    wholeFeatures = list(wholeFeaturesDict.values())
    print("Finish loading features for ShapeNet whole shapes.")

    #%% ComplementMe Dataset
    dataset = os.path.join(BASE_DATA_PATH, "dataset", "ComplementMe")
    datasetType = "parts"
    category = "Airplane"
    dataType = "part_all_centered_point_clouds"
    featureDataPath = os.path.join(dataset, datasetType, category, dataType)

    instanceNames = [d for d in os.listdir(featureDataPath) if os.path.isdir(os.path.join(featureDataPath, d))]

    for instanceName in instanceNames:
        instanceFolder = os.path.join(featureDataPath, instanceName)
        partNames = [f for f in os.listdir(instanceFolder) if os.path.isfile(os.path.join(instanceFolder, f))]

        for partName in partNames:
            partFeature = np.load(os.path.join(instanceFolder, partName))

            posShapeIdxs = [shapeName]
            num_neighbor = 1
            negShapeIdxs = find_negative_pointnet_neighors(exact_feature, all_pointnet_features, num_neighbor)
            print(f"    Positive index: {posShapeIdxs} (remember to +1 when finding files)")
            print(f"    Negative index: {negShapeIdxs} (remember to +1 when finding files)")

            for posShapeIdx in posShapeIdxs:
                #TODO: Need to modify the read fucntion when loading in training
                pair = {
                    'id': str(pos_pair_counter),
                    'label': True,
                    'part': partFeature,
                    'whole': str(posShapeIdx)
                }
                add_pair_to_existing_txt(outputPath, pair)
                pos_pair_counter += 1
            for negShapeIdx in negShapeIdxs:
                pair = {
                    'id': str(neg_pair_counter),
                    'label': False,
                    'part': partFeature,
                    'whole': str(negShapeIdx)
                }
                add_pair_to_existing_txt(outputPath, pair)
                neg_pair_counter += 1
