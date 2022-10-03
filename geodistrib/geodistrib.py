import json
import fiona
from fiona import Collection
from shapely.geometry import shape, Point

def filter(sourceGeom, destFeature):
    destGeom = shape(destFeature['geometry'])
    return sourceGeom.contains(destGeom.centroid)

def distribute(sourceData: Collection, destData: Collection, attribute: str, weight: str, outputDir: str):
    # Copy metadata from the original destination file to the output
    outputMeta = destData.meta
    outputMeta['schema']['properties'][attribute] = sourceData.meta['schema']['properties'][attribute]
    output = fiona.open(outputDir, 'w', **outputMeta)
    
    for sourceFeature in sourceData:
        sourceGeom = shape(sourceFeature['geometry'])

        #Filter destination features by intersection, then centroid
        destFeatureList = [destFeature for destFeature in destData.filter(mask=sourceFeature['geometry']) if filter(sourceGeom, destFeature) == True]
        
        
        numFeatures = len(destFeatureList)  
        sourceAttribute = sourceFeature['properties'][attribute]

        weightSum = 0
        for destFeature in destFeatureList:
            weightSum += destFeature['properties'][weight]

        for destFeature in destFeatureList:
            destFeature['properties'][attribute] = round(sourceAttribute * (destFeature['properties'][weight] / weightSum))

        output.writerecords(destFeatureList);

        print("Processed", numFeatures)

    output.flush()
    output.close()