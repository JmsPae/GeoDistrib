from signal import raise_signal
import time
import fiona
import json
from fiona import Collection
from shapely.geometry import shape, Point

class SourceData:
    def __init__(self, dataDir: str, attributes: list[str]) -> None:
        self.data = fiona.open(dataDir)
        self.attributes = attributes
        
    data: fiona.Collection
    attributes: list[str]


class DestinationData:
    def __init__(self, dataDir: str, weight: str, outputDir: str, sourcesData: list[SourceData]):
        self.weight = weight
        self.data = fiona.open(dataDir)
        outputMeta = self.data.meta
        for source in sourcesData:
            for attrib in source.attributes:
                outputMeta['schema']['properties'][attrib] = source.data.meta['schema']['properties'][attrib]
        self.outputData = fiona.open(outputDir, 'w', **outputMeta)
        

    data: fiona.Collection
    outputData: fiona.Collection
    weight: str

def interpretPipeline(pipelineDir: str):
    f = open(pipelineDir)
    pipeline = json.load(f)
    f.close()

    sources: list[SourceData] = []
    destinations: list[DestinationData] = []

    try:
        distributeDict = pipeline['distribute']

        for src in distributeDict['sources']:
            sources.append(SourceData(src, distributeDict['sources'][src]['attributes']))

        for dest in distributeDict['destinations']:
            destinations.append(DestinationData(dest, distributeDict['destinations'][dest]['weight'], distributeDict['destinations'][dest]['output'], sources))
            

    except KeyError as e:
        print('Missing options in pipeline:', e)
    
    distribute(sources, destinations)

    # Cleaning up
    for src in sources:
        src.data.close()
    
    for dest in destinations:
        dest.data.close()
        dest.outputData.close()


def filter(sourceGeom, destFeature):
    destGeom = shape(destFeature['geometry'])
    return sourceGeom.contains(destGeom.centroid)

def distribute(sources: list[SourceData], destinations: list[DestinationData]):
    
    print('Processing...')
    startTime = time.time()


    for src in sources:
        for sourceFeature in src.data:
            sourceGeom = shape(sourceFeature['geometry'])

            for dest in destinations:
                #Filter destination features by intersection, then centroid
                destFeatureList = [destFeature for destFeature in dest.data.filter(mask=sourceFeature['geometry']) if filter(sourceGeom, destFeature) == True]
                
                sourceAttributes = []
                for attrib in src.attributes:
                    sourceAttributes.append(sourceFeature['properties'][attrib])

                weightSum = 0
                for destFeature in destFeatureList:
                    weightSum += destFeature['properties'][dest.weight]

                for destFeature in destFeatureList:
                    for i in range(len(sourceAttributes)):
                        destFeature['properties'][src.attributes[i]] = round(sourceAttributes[i] * (destFeature['properties'][dest.weight] / weightSum))

                dest.outputData.writerecords(destFeatureList);

    print('Done after', round(time.time() - startTime, 3), 'seconds')