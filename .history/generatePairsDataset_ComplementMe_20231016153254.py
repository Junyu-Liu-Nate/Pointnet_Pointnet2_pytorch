import os
import numpy as np
import random

from generateWholeFeatures import computeWholeFeature
from fileIO import read_features_from_txt, create_initial_txt, add_pair_to_existing_txt, read_features_from_txt_shapenet

BASE_DATA_PATH = "/Users/liujunyu/Data/Research/BVC/ITSS/"

def generatePairsDataset(outputPath):
    #%% Load pre-generated pfh features for whole shapes - candidates
    ### Load all ShapeNet v2 whole shape features
    whole_feature_path = os.path.join(DATA_BASE_PATH, "dataset", "ShapeNetv2_Wholes_100", "airplane")
    selectedNamePath = os.path.join(DATA_BASE_PATH, "dataset", "ComplementMe", "components", "Airplane", "component_all_md5s.txt")
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
