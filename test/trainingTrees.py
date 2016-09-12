import ROOT
from array import array



effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
cut = showerShapes
Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
cut += "*"+Isolation
tkMatched = "(trackDeltaR<.1)"
noTkMatched = "(trackDeltaR>.1)"
cut1 = cut+"*"+tkMatched
cut2 = cut+"*"+noTkMatched

cut = "cluster_pt > 10"
cut = cut2
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
