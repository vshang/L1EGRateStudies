import ROOT


def getKeysOfClass( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys


def loadObjectsMatchingPattern( file_, dir_, keys, matchString ) :
    hists = []
    parts = matchString.split('*')
    #for p in parts : print p
    for key in keys :
        allSuccess = True
        for part in parts :
            if not part in key.GetName() :
                allSuccess = False
        if allSuccess :
            #print "append"
            hists.append( file_.Get( dir_ + '/' + key.GetName() ) )
            #hists.append( file_.GetObject( key.GetName(), key.GetClassName() ) )
            #print hists[-1]
    return hists



def makeNewCutTrees( ifileName, ofileName, cut ) :
    effFile = ROOT.TFile( ifileName, 'r' )
    #rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    eTree = effFile.Get("analyzer/crystal_tree")
    #rTree = rateFile.Get("analyzer/crystal_tree")
    
    newEffFile = ROOT.TFile(ofileName,'RECREATE')
    ETree = eTree.CopyTree( cut )
    ETree.SetName('events')
    print "Post Cut - New tree has %i events" % ETree.GetEntries()
    newEffFile.cd()
    ETree.Write()
    newEffFile.Close()




if __name__ == '__main__' :
    f = ROOT.TFile('egTriggerEff.root','r')
    dir_ = 'analyzer'
    keys = getKeysOfClass( f, dir_, 'TH1F' )
    for key in keys :
        print key, key.GetName(), key.GetClassName()

    hists = loadObjectsMatchingPattern( f, dir_, keys, "*_efficiency*_pt" )
    for h in hists :
        print h
