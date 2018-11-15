import ROOT
from ROOT import gStyle, gROOT
import L1Trigger.L1EGRateStudies.trigHelpers

def drawHeatmaps() :
   gStyle.SetOptStat(0)
   c = ROOT.TCanvas()
	
   heatmapfile = ROOT.TFile("egTriggerEff.root")

   keys = trigHelpers.getKeysOfClass(heatmapfile, "L1EGCrystalsHeatMap", "TH2F")
   heatmaps = trigHelpers.loadObjectsMatchingPattern(heatmapfile, "L1EGCrystalsHeatMap", keys, "evt*")

   for heatmap in heatmaps :
      c.Clear()
      heatmap.Draw("colz")
      c.Print("plots/"+heatmap.GetName()+".png")


if __name__ == '__main__' :
    ROOT.gROOT.SetBatch(True)
    drawHeatmaps()



