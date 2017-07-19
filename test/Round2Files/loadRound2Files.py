import FWCore.ParameterSet.Config as cms


def getSampleFiles( name ) :

    fileNames = cms.untracked.vstring()
    file = open('Round2Files/'+name+'.txt')
    for line in file :
        line = line.strip()
        fileNames.append( 'file:'+line )    
    print "\n\nTarget Files:",name
    print "Loaded Files:"
    print fileNames
    print "\n\n"
    return fileNames


if '__main__' in __name__ :
    getSampleFiles( 'singleElectron_20170716top20' )
