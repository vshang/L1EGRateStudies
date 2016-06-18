import ROOT
from array import array



effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

#goodElec = ROOT.TFile('goodElec.root','RECREATE')
#tmpTree = eTree.CloneTree()
#goodElec.cd()
#tmpTree.Write()
#goodElec.Close()
#del tmpTree
#
#badElec = ROOT.TFile('badElec.root','RECREATE')
#tmpTree = eTree.CloneTree()
#badElec.cd()
#tmpTree.Write()
#badElec.Close()


#cut = "cluster_pt < 30 && cluster_pt > 10"
cut = "cluster_pt > 40"
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
