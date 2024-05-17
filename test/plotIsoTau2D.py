from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *
from array import array

#Select and load root files here
date = '04_04_2024'
file = 'output_round2_VBFHiggsTauTau_13_1X_calib3GeVmaxTT12jets'
#region = 'barrel'
region = 'endcap'

print('Opening Tfile...')
f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_14_0_0_pre3/20240404/' + file + '.root')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/isoTauStudies/CMSSW_14_0_0_pre3/' + date + '/' + file + '/'
checkDir( saveDirectory )


#Set number of histogram bins and maximum value of x and y axis here
nbinsx = 36
xMin = 20
xMax = 200
nbinsy = 100
yMin = 0.05
yMax = 5.05

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree = f.Get('analyzer/tree')

##Create 2D distribution plot of Iso Tau variable
##-----------------------------------------------------------------------------------------------

#Define histograms
print('file = ', file)
print('region = ', region)
print('Creating histograms...')
hist = TH2F('hist', file + ' ' + region + '; Tau p_{T}; (Jet p_{T} - Tau p_{T})/(Tau p_{T})', nbinsx, xMin, xMax, nbinsy, yMin, yMax)
hist_eff = TH1F('hist_eff', '; Tau p_{T}; (Jet p_{T} - Tau p_{T})/(Tau p_{T})', nbinsx, xMin, xMax)

#Fill histograms
print('Filling histograms...')
nEntries = eventTree.GetEntries()
for i in range(nEntries):
    eventTree.GetEntry(i)
    if region == 'barrel':
        if 'minBias' in file:
            passRegion = abs(eventTree.jetEta) < 1.4
        else:
            passRegion = abs(eventTree.genJet_eta) < 1.4
    elif region == 'endcap':
        if 'minBias' in file:
            passRegion = 1.6 < abs(eventTree.jetEta) < 2.6
        else:
            passRegion = 1.6 < abs(eventTree.genJet_eta) < 2.6
    if passRegion and eventTree.tauEt > 0:
        tau_pt = eventTree.tauEt
        jet_pt = eventTree.jetEt
        isoTauVariable = (jet_pt - tau_pt)/tau_pt
        #isoTauVariable = eventTree.tau_iso_et/eventTree.tauEt
        hist.Fill(tau_pt, isoTauVariable)

#Define 90% efficiency threshold
# for x in range(nbinsx):
#     if xMin + x*(xMax-xMin)/nbinsx < 100: #Only use Iso Tau variable for tauEt < 100 GeV
#         events_total = hist.Integral(x, x, 0, nbinsy)
#         # print 'x = ', x
#         # print 'events_total', events_total
#         for y in reversed(range(nbinsy)):
#             events_pass = hist.Integral(x, x, 0, y)
#             if events_pass > 0:
#                 eff = events_pass/events_total
#                 if eff >= 0.9:
#                     hist_eff.SetBinContent(x, (y+1)*(yMax-yMin)/nbinsy)
#                     # print '    y = ', y
#                     # print '    events_pass', events_pass
#                     # print '    eff = ', eff
# events_total100GeV = hist.Integral(16, 16, 0, nbinsy)
# for y in reversed(range(nbinsy)):
#     events_pass100GeV = hist.Integral(16, 16, 0, y)
#     if events_pass100GeV > 0:
#         eff100GeV = events_pass100GeV/events_total100GeV
#         if eff100GeV >= 0.9:
#             for x in range(16, nbinsx+1):
#                 hist_eff.SetBinContent(x, (y+1)*(yMax-yMin)/nbinsy)

#Define efficiency curve for previous Iso Tau performance
#20 GeV: 40%, 25 GeV: 45%, 30 GeV: 50%, 35 GeV: 60%, 40 GeV: 70%, 45 GeV: 75%, 50 GeV: 80%, 55 GeV: 85%, 60 GeV: 90%, 70 GeV: 95%, 80 GeV: 96%
print('Computing efficiency curve for Iso Tau performance...')
events_total20 = hist.Integral(1, 1, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass20 = hist.Integral(1, 1, 0, y)
    if events_pass20 > 10:
        eff20 = events_pass20/events_total20
        #if eff20 >= 0.45:
        if eff20 >= 0.60:
            hist_eff.SetBinContent(1, (y+1)*(yMax-yMin)/nbinsy)

events_total25 = hist.Integral(2, 2, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass25 = hist.Integral(2, 2, 0, y)
    if events_pass25 > 0:
        eff25 = events_pass25/events_total25
        #if eff25 >= 0.50:
        if eff25 >= 0.60:
            hist_eff.SetBinContent(2, (y+1)*(yMax-yMin)/nbinsy)

events_total30 = hist.Integral(3, 3, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass30 = hist.Integral(3, 3, 0, y)
    if events_pass30 > 0:
        eff30 = events_pass30/events_total30
        #if eff30 >= 0.60:
        if eff30 >= 0.65:
            hist_eff.SetBinContent(3, (y+1)*(yMax-yMin)/nbinsy)

events_total35 = hist.Integral(4, 4, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass35 = hist.Integral(4, 4, 0, y)
    if events_pass35 > 0:
        eff35 = events_pass35/events_total35
        #if eff35 >= 0.70:
        if eff35 >= 0.75:
            hist_eff.SetBinContent(4, (y+1)*(yMax-yMin)/nbinsy)

events_total40 = hist.Integral(5, 5, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass40 = hist.Integral(5, 5, 0, y)
    if events_pass40 > 0:
        eff40 = events_pass40/events_total40
        #if eff40 >= 0.75:
        if eff40 >= 0.80:
            hist_eff.SetBinContent(5, (y+1)*(yMax-yMin)/nbinsy)

events_total45 = hist.Integral(6, 6, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass45 = hist.Integral(6, 6, 0, y)
    if events_pass45 > 0:
        eff45 = events_pass45/events_total45
        #if eff45 >= 0.80:
        if eff45 >= 0.85:
            hist_eff.SetBinContent(6, (y+1)*(yMax-yMin)/nbinsy)

events_total50 = hist.Integral(7, 7, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass50 = hist.Integral(7, 7, 0, y)
    if events_pass50 > 0:
        eff50 = events_pass50/events_total50
        #if eff50 >= 0.85:
        if eff50 >= 0.90:
            hist_eff.SetBinContent(7, (y+1)*(yMax-yMin)/nbinsy)

events_total55 = hist.Integral(8, 8, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass55 = hist.Integral(8, 8, 0, y)
    if events_pass55 > 0:
        eff55 = events_pass55/events_total55
        #if eff55 >= 0.90:
        if eff55 >= 0.93:
            hist_eff.SetBinContent(8, (y+1)*(yMax-yMin)/nbinsy)

events_total60 = hist.Integral(9, 10, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass60 = hist.Integral(9, 10, 0, y)
    if events_pass60 > 0:
        eff60 = events_pass60/events_total60
        #if eff60 >= 0.93:
        if eff60 >= 0.95:
            hist_eff.SetBinContent(9, (y+1)*(yMax-yMin)/nbinsy)
            hist_eff.SetBinContent(10, (y+1)*(yMax-yMin)/nbinsy)

events_total70 = hist.Integral(11, 12, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass70 = hist.Integral(11, 12, 0, y)
    if events_pass70 > 0:
        eff70 = events_pass70/events_total70
        #if eff70 >= 0.95:
        if eff70 >= 0.97:
            hist_eff.SetBinContent(11, (y+1)*(yMax-yMin)/nbinsy)
            hist_eff.SetBinContent(12, (y+1)*(yMax-yMin)/nbinsy)

events_total80 = hist.Integral(13, 16, 0, nbinsy)
for y in reversed(range(nbinsy)):
    events_pass80 = hist.Integral(13, 16, 0, y)
    if events_pass80 > 0:
        eff80 = events_pass80/events_total80
        #if eff80 >= 0.97:
        if eff80 >= 0.98:
            for i in range(13, nbinsx+1):
                hist_eff.SetBinContent(i, (y+1)*(yMax-yMin)/nbinsy)

#Define efficiency curve Tgraph
graph_eff = TGraph(hist_eff)
        
#Define Iso Tau threshold cut as function of Tau pT
f1Barrel = TF1( 'isoTauBarrel', '([0] + [1]*TMath::Exp(-[2]*x))', 20, 200)
f1Barrel.SetParName( 0, "y rise" )
f1Barrel.SetParName( 1, "scale" )
f1Barrel.SetParName( 2, "decay" )
f1Barrel.SetParameter( 0, 0.30 )
f1Barrel.SetParameter( 1, 0.31 )
f1Barrel.SetParameter( 2, 0.040 )
f1Barrel.SetMinimum(yMin)
f1Barrel.SetMaximum(yMax)
    
f1HGCal = TF1( 'isoTauHGCal', '([0] + [1]*TMath::Exp(-[2]*x))', 20, 200)
f1HGCal.SetParName( 0, "y rise" )
f1HGCal.SetParName( 1, "scale" )
f1HGCal.SetParName( 2, "decay" )
f1HGCal.SetParameter( 0, 0.34 )
f1HGCal.SetParameter( 1, 0.35 )
f1HGCal.SetParameter( 2, 0.051 )
f1HGCal.SetMinimum(yMin)
f1HGCal.SetMaximum(yMax)

#Define new Iso Tau threshold function to fit for barrel
f1Barrel_new = TF1( 'newIsoTauBarrel', '([0] + [1]*TMath::Exp(-[2]*x))', 20, 200)
f1Barrel_new.SetParName( 0, "y rise" )
f1Barrel_new.SetParName( 1, "scale" )
f1Barrel_new.SetParName( 2, "decay" )
f1Barrel_new.SetParameter( 0, 0.30 )
f1Barrel_new.SetParameter( 1, 0.50 )
f1Barrel_new.SetParameter( 2, 0.052 )
f1Barrel_new.SetMinimum(yMin)
f1Barrel_new.SetMaximum(yMax)

if region == 'barrel':
    #Fit new Iso Tau threshold function for barrel
    print('Fitting new Iso Tau threshold function...')
    hist_eff.Fit('newIsoTauBarrel')
    print('old y rise: ', f1Barrel.GetParameter("y rise"))
    print('old scale: ', f1Barrel.GetParameter("scale"))
    print('old decay: ', f1Barrel.GetParameter("decay"))
    print('new y rise: ', f1Barrel_new.GetParameter("y rise"))
    print('new scale: ', f1Barrel_new.GetParameter("scale"))
    print('new decay: ', f1Barrel_new.GetParameter("decay"))

#Define new Iso Tau threshold function to fit for endcap
f1HGCal_new = TF1( 'newIsoTauHGCal', '([0] + [1]*TMath::Exp(-[2]*x))', 20, 200)
f1HGCal_new.SetParName( 0, "y rise" )
f1HGCal_new.SetParName( 1, "scale" )
f1HGCal_new.SetParName( 2, "decay" )
f1HGCal_new.SetParameter( 0, 0.93 )
f1HGCal_new.SetParameter( 1, 0.51 )
f1HGCal_new.SetParameter( 2, 0.025 )
f1HGCal_new.SetMinimum(yMin)
f1HGCal_new.SetMaximum(yMax)

if region == 'endcap':
    #Fit new Iso Tau threshold function for endcap
    print('Fitting new Iso Tau threshold function...')
    hist_eff.Fit('newIsoTauHGCal')
    print('old y rise: ', f1HGCal.GetParameter("y rise"))
    print('old scale: ', f1HGCal.GetParameter("scale"))
    print('old decay: ', f1HGCal.GetParameter("decay"))
    print('new y rise: ', f1HGCal_new.GetParameter("y rise"))
    print('new scale: ', f1HGCal_new.GetParameter("scale"))
    print('new decay: ', f1HGCal_new.GetParameter("decay"))

#Draw histograms
print('Drawing histograms...')
canvas = TCanvas('canvas', 'Tau Relative Isolation Variable')
hist.Draw('Colz')
graph_eff.Draw('same')
if region == 'barrel':
    f1Barrel.Draw('same')
    f1Barrel_new.Draw('same')
elif region =='endcap':
    f1HGCal.Draw('same')
    f1HGCal_new.Draw('same')
#Set histogram settings
graph_eff.SetLineColor(kBlack)
graph_eff.SetLineWidth(3)
if region == 'barrel':
    f1Barrel_new.SetLineColor(kBlue)
elif region == 'endcap':
    f1HGCal_new.SetLineColor(kBlue)
canvas.SetLogy(1)
canvas.SetLogz(1)
#Add legend
legend = TLegend(0.52, 0.57, 0.82, 0.87)
legend.AddEntry(graph_eff, 'Run-II IsoTau efficiency', 'l')
if region == 'barrel':
    legend.AddEntry(f1Barrel, 'Old IsoTau threshold curve', 'l')
    legend.AddEntry(f1Barrel_new, 'New IsoTau threshold curve', 'l')
elif region == 'endcap':
    legend.AddEntry(f1HGCal, 'Old IsoTau threshold curve', 'l')
    legend.AddEntry(f1HGCal_new, 'New IsoTau threshold curve', 'l')
legend.Draw('same')
legend.SetBorderSize(0)
#Save histogram
print('Saving histogram...')
canvas.SaveAs(saveDirectory+'isoTauVariable2D_' + file + '_' + region + '.png')
print('Saved histogram')
