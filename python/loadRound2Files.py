import FWCore.ParameterSet.Config as cms
import os

# For processing samples in two rounds, this loads edm files from round1 into
# the round 2 cfg
def getSampleFiles( name ) :

    fileNames = cms.untracked.vstring()
    print(os.getenv('CMSSW_BASE')+'/src/L1Trigger/L1EGRateStudies/test/Round2Files/'+name+'.txt')
    file = open(os.getenv('CMSSW_BASE')+'/src/L1Trigger/L1EGRateStudies/test/Round2Files/'+name+'.txt')
    for line in file :
        line = line.strip()
        fileNames.append( 'file:'+line )    
    print("\n\nTarget Files:",name)
    print("Loaded Files:")
    print(fileNames)
    print("\n\n")
    return fileNames


