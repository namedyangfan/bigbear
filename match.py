import pandas as pd 
import datetime as dt
import os

def readWellNames (file_path, index_col = None):
    data = pd.read_csv(file_path, index_col = index_col)
    return( data)

def mergeReginalDfWithBoxDf (lookUpTableDf, boxModelDf, regionalDf):
    assert 'concentration' in boxModelDf.columns
    assert 'rain_olf' in regionalDf.columns
    assert 'Box' in lookUpTableDf.columns
    assert 'Regional' in lookUpTableDf.columns

    mergedBoxLookUpDf = pd.merge(lookUpTableDf,boxModelDf[['node','concentration']], how='left', left_on='Box', right_on='node')
    mergedBoxLookUpDf.rename(columns={'node':'boxNode'}, inplace=True)
    mergedBoxLookUpDfReginal = pd.merge(regionalDf,mergedBoxLookUpDf[['Regional','concentration']], how='left', left_on='node', right_on='Regional')
    mergedBoxLookUpDfReginal['concentration'].fillna(mergedBoxLookUpDfReginal['rain_olf'], inplace = True)
    return mergedBoxLookUpDfReginal[['node', 'concentration']]

def mergeReginalWithBox (lookUpTableDf, regionalDf, boxModelDir, boxModelFileName):
    boxModelPath =  os.path.join(boxModelDir, boxModelFileName)
    boxModel = readWellNames(boxModelPath)
    mergedDf = mergeReginalDfWithBoxDf (lookUpTableDf, boxModel, regionalDf)
    mergedFileName = "merged.{}".format(boxModelFileName)
    mergedDf.to_csv(mergedFileName, index=False)

def main():
    lookUpTablePath = './Concentration_node_lookup.csv'
    boxModelFilePath = './'
    boxModelFileName = 'MLWCo.concentration.00017.csv'
    regionalPath = './MLWCo.concentration.00000.csv'

    lookUpTable = readWellNames(lookUpTablePath,index_col = "Index")
    regional = readWellNames(regionalPath)
    mergeReginalWithBox(lookUpTableDf= lookUpTable, regionalDf = regional, boxModelDir = boxModelFilePath, boxModelFileName = boxModelFileName)
  
if __name__== "__main__":
  main()
