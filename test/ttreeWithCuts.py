import ROOT


def ttreeWithCuts( oldFile, oldTreePath, fOutName='ttreeWithCut.root', cut='' ) :
    f = ROOT.TFile( oldFile, 'r' )
    t = f.Get(oldTreePath)
    print "Num Events in initial TTree:",t.GetEntries()
    
    fOut = ROOT.TFile(fOutName,'RECREATE')
    tOut = t.CopyTree( cut )
    print "Num events in new TTree:",tOut.GetEntries()

    fOut.cd()
    
    # Make same directory path
    info = oldTreePath.split('/')
    info.pop() # Get rid of TTree name
    newPath = '/'.join( info )
    fOut.mkdir( newPath )
    fOut.cd( newPath )
    print "New path: %s/%s" % (newPath, tOut.GetName() )

    tOut.Write()
    fOut.Close()



if __name__ == '__main__' :
    oldFile = '/afs/cern.ch/user/v/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/testR2sample_Victor/output_round2_testSampleHTauTauv1.root'
    oldTreePath = 'analyzer/tree'
    fOutName = '/afs/cern.ch/user/v/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/testR2sample_Victor/output_round2_testSampleHTauTauv1_withCuts.root'
    cut = '(calibPtHH > 15 || stage2tau_pt_calibration3 > 15)'
    ttreeWithCuts( oldFile, oldTreePath, fOutName, cut )

