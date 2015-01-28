import ROOT
import numpy

f = ROOT.TFile("egTriggerEff.root")
eff = f.Get("analyzer/crystal_tree")

f2 = ROOT.TFile("egTriggerRates.root")
rates = f2.Get("analyzer/crystal_tree")

def roc(bremlo, bremhi) :
  pts = 60
  groc = ROOT.TGraph(pts)
  ele_denom = eff.GetEntries("passed&&cluster_pt>10&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi))
  bkg_denom = rates.GetEntries("passed&&cluster_pt>10&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi))
  i = 0
  for deltaR in numpy.linspace(0.01,0.6,pts) :
    ele_num = eff.GetEntries("passed&&cluster_pt>10&&"+str(deltaR)+">trackDeltaR&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi))
    bkg_num = rates.GetEntries("passed&&cluster_pt>10&&"+str(deltaR)+">trackDeltaR&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi))
    groc.SetPoint(i, ele_num*1./ele_denom, bkg_num*1./bkg_denom)
    i+=1
  return groc

nobrem = roc(0.95, 1.1)
brem = roc(0.7, 0.95)
nobrem.Draw("acp")
brem.SetLineColor(ROOT.kRed)
brem.SetMarkerColor(ROOT.kRed)
brem.Draw("cp")
