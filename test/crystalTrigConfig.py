import json
from collections import OrderedDict

iPhiTot = 360
iEtaTot = 170

def makeMapping( phiNum, etaNum ) :
    print "Making crystal mapping with %i Phi Divisions and %i Eta Divisions" % (phiNum, etaNum)
    print "Current settings:"
    print " -- iPhiTotal:",iPhiTot
    print " -- iEtaTotal:",iEtaTot
    
    #rMap = regionNumbering( phiNum, etaNum )

    iPhiPer = int(iPhiTot/phiNum)
    iEtaPer = int(iEtaTot/etaNum)
    print "iPhiPer:",iPhiPer
    print "iEtaPer:",iEtaPer
    rCount = 1
    rMap = OrderedDict() # map to hold region numbers

    tMap = OrderedDict()
    # loop over all iEta and iPhi in detector
    # there is no iEta == 0 in detector
    oneSidedEtaTot = iEtaTot/2
    for iEta in range( -1*oneSidedEtaTot, oneSidedEtaTot+1 ) :
        if iEta == 0 : continue 
        for iPhi in range( 1, iPhiTot+1 ) :
            #reg = (int((iPhi-1)/iPhiPer), int(iEta/iEtaPer))
            #elif iEta < 0 :
            #    reg = (int((iPhi-1)/iPhiPer), int(iEta/iEtaPer))
            #elif iEta > 0 :
            #    reg = (int((iPhi-1)/iPhiPer), int((iEta-1)/iEtaPer))
            if etaNum == 1 :
                if iEta < 0 :
                    reg = (int((iPhi-1)/iPhiPer), int(iEta/iEtaPer)+1) 
                    # +1 deals with integer division rounding down
                    # it makes sure that all eta give same value of "0"
                elif iEta > 0 :
                    reg = (int((iPhi-1)/iPhiPer), int((iEta-1)/iEtaPer))
            if iEta < 0 :
                reg = (int((iPhi-1)/iPhiPer), int(iEta/iEtaPer))
            elif iEta > 0 :
                reg = (int((iPhi-1)/iPhiPer), int((iEta-1)/iEtaPer))

            # Build our region mapping if not already present
            if reg not in rMap.keys() :
                rMap[reg] = rCount
                rCount += 1

            # Assign a region to each iEta,iPhi
            #tMap[(iEta,iPhi)] = rMap[reg]
            tMap["(%i, %i)" % (iEta,iPhi)] = rMap[reg]

    print rMap

    return tMap
    


def printJson( jDict ) :
    with open('map36.json', 'w') as outFile :
        json.dump( jDict, outFile, indent=2 )
        outFile.close()

if __name__ == '__main__' :
    phi = 1 # defaul setting
    eta = 1
    phi = 24 # first recommended config
    eta = 1
    phi = 18 # second test config
    eta = 2
    tMap = makeMapping( phi, eta )

    for iEta in range( -1*iEtaTot/2, iEtaTot/2+1 ) :
        if iEta == 0 : continue 
        line = []
        for iPhi in range( 1, iPhiTot+1 ) :
            line.append( tMap["(%i, %i)" % (iEta,iPhi)] )
        print "iEta:",iEta,line

    printJson( tMap )


