import ROOT
from array import array



effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

cut = "cluster_pt > 10"
#cut = "(0.000889811 + 0.0078119*TMath::Exp(-0.19245*cluster_pt)) < abs(trackRInv)"
trainingTrees = ROOT.TFile('trainingTrees.root','RECREATE')
#ETree = eTree.CloneTree( cut )
ETree = eTree.CopyTree( cut )
ETree.SetName('signal')

#RTree = rTree.CloneTree( cut)
RTree = rTree.CopyTree( cut )
RTree.SetName('background')

trainingTrees.cd()

ETree.Write()
RTree.Write()
trainingTrees.Close()
