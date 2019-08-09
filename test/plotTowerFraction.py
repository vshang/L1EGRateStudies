from ROOT import *

#Select and load root files here
f_ggHTT = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_HiggsTauTau_testv1.root', '')
f_QCD = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_QCD_testv1.root', '')


#Set sameCanvas to True for all plots on same Canvas, False if you want seperate plots
sameCanvas = True

#Set number of histogram bins and maximum value of y axis here
nBins = 20
yMax = 0.2

#Remove stats box from histograms
gStyle.SetOptStat(0)

#Get event trees
ggHTT_eventTree = f_ggHTT.Get('analyzer/tree')
QCD_eventTree = f_QCD.Get('analyzer/tree')


##Create tower E_T fraction distribution plots 
##-----------------------------------------------------------------------------------------------

#Define ggHTT and QCD 3x3 tower histograms
h_ggHTT_3x3 = TH1F('h_ggHTT_3x3', '3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_3x3 = TH1F('h_QCD_3x3', '3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD 1x3 tower histograms
h_ggHTT_1x3 = TH1F('h_ggHTT_1x3', '1x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_1x3 = TH1F('h_QCD_1x3', '1x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD 3x1 tower histograms
h_ggHTT_3x1 = TH1F('h_ggHTT_3x1', '3x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_3x1 = TH1F('h_QCD_3x1', '3x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD Cross tower histograms
h_ggHTT_Cross = TH1F('h_ggHTT_Cross', 'Cross Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_Cross = TH1F('h_QCD_Cross', 'Cross Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD X tower histograms
h_ggHTT_X = TH1F('h_ggHTT_X', 'X Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_X = TH1F('h_QCD_X', 'X Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Fill ggHTT histograms
nEntries_ggHTT = ggHTT_eventTree.GetEntries()
for i in range(nEntries_ggHTT):
    ggHTT_eventTree.GetEntry(i)
    if ggHTT_eventTree.total_3x3 >= 0:
        h_ggHTT_3x3.Fill(ggHTT_eventTree.total_3x3/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_1x3 >= 0:
        h_ggHTT_1x3.Fill(ggHTT_eventTree.total_1x3/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_3x1 >= 0:
        h_ggHTT_3x1.Fill(ggHTT_eventTree.total_3x1/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_Cross >= 0:
        h_ggHTT_Cross.Fill(ggHTT_eventTree.total_Cross/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_X >= 0:
        h_ggHTT_X.Fill(ggHTT_eventTree.total_X/float(ggHTT_eventTree.total_3x5))

#Fill QCD histograms
nEntries_QCD = QCD_eventTree.GetEntries()
for i in range(nEntries_QCD):
    QCD_eventTree.GetEntry(i)
    if QCD_eventTree.total_3x3 >= 0:
        h_QCD_3x3.Fill(QCD_eventTree.total_3x3/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_1x3 >= 0:
        h_QCD_1x3.Fill(QCD_eventTree.total_1x3/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_3x1 >= 0:
        h_QCD_3x1.Fill(QCD_eventTree.total_3x1/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_Cross >= 0:
        h_QCD_Cross.Fill(QCD_eventTree.total_Cross/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_X >= 0:
        h_QCD_X.Fill(QCD_eventTree.total_X/float(QCD_eventTree.total_3x5))

#Normalize ggHTT histograms to unit area
h_ggHTT_3x3.Scale(1/h_ggHTT_3x3.Integral())
h_ggHTT_1x3.Scale(1/h_ggHTT_1x3.Integral())
h_ggHTT_3x1.Scale(1/h_ggHTT_3x1.Integral())
h_ggHTT_Cross.Scale(1/h_ggHTT_Cross.Integral())
h_ggHTT_X.Scale(1/h_ggHTT_X.Integral())

#Normalize QCT histograms to unit area
h_QCD_3x3.Scale(1/h_QCD_3x3.Integral())
h_QCD_1x3.Scale(1/h_QCD_1x3.Integral())
h_QCD_3x1.Scale(1/h_QCD_3x1.Integral())
h_QCD_Cross.Scale(1/h_QCD_Cross.Integral())
h_QCD_X.Scale(1/h_QCD_X.Integral())

#Draw 3x3 tower E_T fraction distribution plots 
if sameCanvas:
    c = TCanvas('c', 'Tower energy fraction distributions')
    c.Divide(3,2)
    c.cd(1)
else:
    c_3x3 = TCanvas('c_3x3', '3x3 Tower energy fraction distribution')
h_ggHTT_3x3.Draw('hist')
h_QCD_3x3.Draw('hist same')
#Set ggHTT_3x3 histogram options
h_ggHTT_3x3.SetLineColor(kRed)
h_ggHTT_3x3.SetLineWidth(3)
h_ggHTT_3x3.SetMinimum(0)
h_ggHTT_3x3.SetMaximum(yMax)
#Set QCD_3x3 histogram options
h_QCD_3x3.SetLineColor(kBlue)
h_QCD_3x3.SetLineWidth(3)
h_QCD_3x3.SetMinimum(0)
h_QCD_3x3.SetMaximum(yMax)
#Add legend
legend_3x3 = TLegend(0.46, 0.73, 0.75, 0.87)
legend_3x3.AddEntry(h_ggHTT_3x3, 'ggHTT, 3x3', 'l')
legend_3x3.AddEntry(h_QCD_3x3, 'QCD, 3x3', 'l')
legend_3x3.Draw('same')
legend_3x3.SetBorderSize(0)

#Draw 1x3 tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(2)
else:
    c_1x3 = TCanvas('c_1x3', '1x3 Tower energy fraction distribution')
h_ggHTT_1x3.Draw('hist')
h_QCD_1x3.Draw('hist same')
#Set ggHTT_1x3 histogram options
h_ggHTT_1x3.SetLineColor(kRed)
h_ggHTT_1x3.SetLineWidth(3)
h_ggHTT_1x3.SetMinimum(0)
h_ggHTT_1x3.SetMaximum(yMax)
#Set QCD_1x3 histogram options
h_QCD_1x3.SetLineColor(kBlue)
h_QCD_1x3.SetLineWidth(3)
h_QCD_1x3.SetMinimum(0)
h_QCD_1x3.SetMaximum(yMax)
#Add legend
legend_1x3 = TLegend(0.46, 0.73, 0.75, 0.87)
legend_1x3.AddEntry(h_ggHTT_1x3, 'ggHTT, 1x3', 'l')
legend_1x3.AddEntry(h_QCD_1x3, 'QCD, 1x3', 'l')
legend_1x3.Draw('same')
legend_1x3.SetBorderSize(0)

#Draw 3x1 tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(3)
else:
    c_3x1 = TCanvas('c_3x1', '3x1 Tower energy fraction distribution')
h_ggHTT_3x1.Draw('hist')
h_QCD_3x1.Draw('hist same')
#Set ggHTT_3x1 histogram options
h_ggHTT_3x1.SetLineColor(kRed)
h_ggHTT_3x1.SetLineWidth(3)
h_ggHTT_3x1.SetMinimum(0)
h_ggHTT_3x1.SetMaximum(yMax)
#Set QCD_3x1 histogram options
h_QCD_3x1.SetLineColor(kBlue)
h_QCD_3x1.SetLineWidth(3)
h_QCD_3x1.SetMinimum(0)
h_QCD_3x1.SetMaximum(yMax)
#Add legend
legend_3x1 = TLegend(0.46, 0.73, 0.75, 0.87)
legend_3x1.AddEntry(h_ggHTT_3x1, 'ggHTT, 3x1', 'l')
legend_3x1.AddEntry(h_QCD_3x1, 'QCD, 3x1', 'l')
legend_3x1.Draw('same')
legend_3x1.SetBorderSize(0)

#Draw Cross tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(4)
else:
    c_Cross = TCanvas('c_Cross', 'Cross Tower energy fraction distribution')
h_ggHTT_Cross.Draw('hist')
h_QCD_Cross.Draw('hist same')
#Set ggHTT_Cross histogram options
h_ggHTT_Cross.SetLineColor(kRed)
h_ggHTT_Cross.SetLineWidth(3)
h_ggHTT_Cross.SetMinimum(0)
h_ggHTT_Cross.SetMaximum(yMax)
#Set QCD_Cross histogram options
h_QCD_Cross.SetLineColor(kBlue)
h_QCD_Cross.SetLineWidth(3)
h_QCD_Cross.SetMinimum(0)
h_QCD_Cross.SetMaximum(yMax)
#Add legend
legend_Cross = TLegend(0.46, 0.73, 0.75, 0.87)
legend_Cross.AddEntry(h_ggHTT_Cross, 'ggHTT, Cross', 'l')
legend_Cross.AddEntry(h_QCD_Cross, 'QCD, Cross', 'l')
legend_Cross.Draw('same')
legend_Cross.SetBorderSize(0)

#Draw X tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(5)
else:
    c_X = TCanvas('c_X', 'X Tower energy fraction distribution')
h_ggHTT_X.Draw('hist')
h_QCD_X.Draw('hist same')
#Set ggHTT_X histogram options
h_ggHTT_X.SetLineColor(kRed)
h_ggHTT_X.SetLineWidth(3)
h_ggHTT_X.SetMinimum(0)
h_ggHTT_X.SetMaximum(yMax)
#Set QCD_X histogram options
h_QCD_X.SetLineColor(kBlue)
h_QCD_X.SetLineWidth(3)
h_QCD_X.SetMinimum(0)
h_QCD_X.SetMaximum(yMax)
#Add legend
legend_X = TLegend(0.46, 0.73, 0.75, 0.87)
legend_X.AddEntry(h_ggHTT_X, 'ggHTT, X', 'l')
legend_X.AddEntry(h_QCD_X, 'QCD, X', 'l')
legend_X.Draw('same')
legend_X.SetBorderSize(0)
