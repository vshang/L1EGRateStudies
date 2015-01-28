import ROOT
f = ROOT.TFile("egTriggerEff.root")
eff = f.Get("analyzer/crystal_tree")

f2 = ROOT.TFile("egTriggerRates.root")
rates = f2.Get("analyzer/crystal_tree")

