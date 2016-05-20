import ROOT
import numpy

f = ROOT.TFile("egTriggerEff.root")
eff = f.Get("analyzer/crystal_tree")

f2 = ROOT.TFile("egTriggerRates.root")
rates = f2.Get("analyzer/crystal_tree")

def roc(def_cut, var, lo, hi) :
  pts = 60
  groc = ROOT.TGraph(pts)
  i = 0
  ele_denom = eff.GetEntries(def_cut)
  bkg_denom = rates.GetEntries(def_cut)
  for val in numpy.linspace(lo,hi,pts) :
    ele_num = eff.GetEntries(def_cut+"&&"+str(val)+">"+var)
    bkg_num = rates.GetEntries(def_cut+"&&"+str(val)+">"+var)
    groc.SetPoint(i, ele_num*1./ele_denom, bkg_num*1./bkg_denom)
    i+=1
  groc.SetTitle("ROC Curve")
  return groc

def dRroc(bremlo, bremhi) :
  graph = roc("passed&&cluster_pt>10&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi), "deltaR", 0.01, 0.6)
  graph.SetTitle("#DeltaR")
  return graph

def trackIsoroc(bremlo, bremhi) :
  graph = roc("passed&&cluster_pt>10&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi), "trackIsoConePtSum", 0.01, 20)
  graph.SetTitle("Track Isolation")
  return graph

def trackIsoCountroc(bremlo, bremhi) :
  graph = roc("passed&&cluster_pt>10&&bremStrength>"+str(bremlo)+"&&bremStrength<="+str(bremhi), "trackIsoConeTrackCount", 0.01, 20)
  graph.SetTitle("Nearby track count")
  return graph

def drawBremNoBrem(rocFunction) :
  mg = ROOT.TMultiGraph("roc", "ROC curves")
  nobrem = rocFunction(0.95, 1.1)
  brem = rocFunction(0.7, 0.95)
  brem.SetFillColor(ROOT.kWhite)
  brem.SetTitle(brem.GetTitle()+" w/brem")
  nobrem.SetTitle(nobrem.GetTitle()+" no brem")
  nobrem.SetFillColor(ROOT.kWhite)
  mg.Add(nobrem)
  brem.SetLineColor(ROOT.kRed)
  brem.SetMarkerColor(ROOT.kRed)
  mg.Add(brem)
  mg.Draw("acp")
  mg.GetXaxis().SetTitle("Single electron efficiency")
  mg.GetYaxis().SetTitle("minBias acceptance")
  ROOT.gPad.Update()
  return mg

c = ROOT.TCanvas('c','c',600,600)
mg = drawBremNoBrem(trackIsoroc)

leg = ROOT.gPad.BuildLegend(0.15,0.7,0.6,0.88)
leg.SetFillColor(ROOT.kWhite)
leg.SetLineColor(ROOT.kWhite)
ROOT.gPad.Update()
c.Print('plots/'+'roc'+'.png')
