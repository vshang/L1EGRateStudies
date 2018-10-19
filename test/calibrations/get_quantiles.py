import ROOT
ROOT.gROOT.SetBatch(True)

f = ROOT.TFile('/data/truggles/phaseII_qcd_20180925_v1-condor_jets/qcd.root','r')

t = f.Get('analyzer/tree')

#h = ROOT.TH1D('h','h',10000,0,10)
h = ROOT.TH1D('h','h',41,0,1.025)

t.Draw( '(ecal_L1EG_jet_pt + ecal_pt)/jet_pt >> h', 'jet_pt >= 0')

total = h.Integral()

c = ROOT.TCanvas('c','c',600,400)
h.Draw()
c.SaveAs('quant.png')

cum = 0
index = 1
for b in range( h.GetXaxis().GetNbins() ) :
    cum += h.GetBinContent( b )
    #if b > 20 : break
    if cum * 10 > total :
        print index, b, h.GetBinCenter(b), cum
        cum = 0
        index += 1
        
