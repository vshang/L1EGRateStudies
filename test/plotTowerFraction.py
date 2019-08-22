from ROOT import *

#Select and load root files here
f_ggHTT = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_HiggsTauTau_testv2.root', '')
f_QCD = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_QCD_testv2.root', '')


#Set sameCanvas to True for all plots on same Canvas, False if you want seperate plots
sameCanvas = True

#Set number of histogram bins and maximum value of y axis here
nBins = 20
yMax = 0.2

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event trees
ggHTT_eventTree = f_ggHTT.Get('analyzer/tree')
QCD_eventTree = f_QCD.Get('analyzer/tree')


##Create tower E_T fraction distribution plots 
##-----------------------------------------------------------------------------------------------

# #Define ggHTT and QCD 3x3 tower histograms
# h_ggHTT_3x3 = TH1F('h_ggHTT_3x3', '3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_3x3 = TH1F('h_QCD_3x3', '3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD 1x3 tower histograms
# h_ggHTT_1x3 = TH1F('h_ggHTT_1x3', '1x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_1x3 = TH1F('h_QCD_1x3', '1x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD 3x1 tower histograms
# h_ggHTT_3x1 = TH1F('h_ggHTT_3x1', '3x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_3x1 = TH1F('h_QCD_3x1', '3x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD Cross tower histograms
# h_ggHTT_Cross = TH1F('h_ggHTT_Cross', 'Cross Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_Cross = TH1F('h_QCD_Cross', 'Cross Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD X tower histograms
# h_ggHTT_X = TH1F('h_ggHTT_X', 'X Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_X = TH1F('h_QCD_X', 'X Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD 1x1 tower histograms
# h_ggHTT_1x1 = TH1F('h_ggHTT_1x1', '1x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_1x1 = TH1F('h_QCD_1x1', '1x1 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD max1x1in3x3NoSeed tower histograms
# h_ggHTT_max1x1in3x3NoSeed = TH1F('h_ggHTT_max1x1in3x3NoSeed', 'max1x1in3x3NoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_max1x1in3x3NoSeed = TH1F('h_QCD_max1x1in3x3NoSeed', 'max1x1in3x3NoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD CrossNoSeed tower histograms
# h_ggHTT_CrossNoSeed = TH1F('h_ggHTT_CrossNoSeed', 'CrossNoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_CrossNoSeed = TH1F('h_QCD_CrossNoSeed', 'CrossNoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD XNoSeed tower histograms
# h_ggHTT_XNoSeed = TH1F('h_ggHTT_XNoSeed', 'XNoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_XNoSeed = TH1F('h_QCD_XNoSeed', 'XNoSeed Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

# #Define ggHTT and QCD max2x2in3x3 tower histograms
# h_ggHTT_max2x2in3x3 = TH1F('h_ggHTT_max2x2in3x3', 'max2x2in3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
# h_QCD_max2x2in3x3 = TH1F('h_QCD_max2x2in3x3', 'max2x2in3x3 Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max2inCross_0LessThreshold tower histograms
h_ggHTT_max2inCross_0LessThreshold = TH1F('h_ggHTT_max2inCross_0LessThreshold', 'max2inCross_0LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max2inCross_0LessThreshold = TH1F('h_QCD_max2inCross_0LessThreshold', 'max2inCross_0LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max2inCross_1LessThreshold tower histograms
h_ggHTT_max2inCross_1LessThreshold = TH1F('h_ggHTT_max2inCross_1LessThreshold', 'max2inCross_1LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max2inCross_1LessThreshold = TH1F('h_QCD_max2inCross_1LessThreshold', 'max2inCross_1LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max2inCross_2LessThreshold tower histograms
h_ggHTT_max2inCross_2LessThreshold = TH1F('h_ggHTT_max2inCross_2LessThreshold', 'max2inCross_2LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max2inCross_2LessThreshold = TH1F('h_QCD_max2inCross_2LessThreshold', 'max2inCross_2LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max3inCross_0LessThreshold tower histograms
h_ggHTT_max3inCross_0LessThreshold = TH1F('h_ggHTT_max3inCross_0LessThreshold', 'max3inCross_0LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max3inCross_0LessThreshold = TH1F('h_QCD_max3inCross_0LessThreshold', 'max3inCross_0LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max3inCross_1LessThreshold tower histograms
h_ggHTT_max3inCross_1LessThreshold = TH1F('h_ggHTT_max3inCross_1LessThreshold', 'max3inCross_1LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max3inCross_1LessThreshold = TH1F('h_QCD_max3inCross_1LessThreshold', 'max3inCross_1LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)

#Define ggHTT and QCD max3inCross_2LessThreshold tower histograms
h_ggHTT_max3inCross_2LessThreshold = TH1F('h_ggHTT_max3inCross_2LessThreshold', 'max3inCross_2LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)
h_QCD_max3inCross_2LessThreshold = TH1F('h_QCD_max3inCross_2LessThreshold', 'max3inCross_2LessThreshold Tower Energy fraction distribution; fraction of total 3x5 tower E_{T}; Number of tau jets (normalized)', nBins, 0, 1)


#Fill ggHTT histograms
nEntries_ggHTT = ggHTT_eventTree.GetEntries()
for i in range(nEntries_ggHTT):
    ggHTT_eventTree.GetEntry(i)

    # if ggHTT_eventTree.total_3x3 >= 0:
    #     h_ggHTT_3x3.Fill(ggHTT_eventTree.total_3x3/float(ggHTT_eventTree.total_3x5))
    # if ggHTT_eventTree.total_1x3 >= 0:
    #     h_ggHTT_1x3.Fill(ggHTT_eventTree.total_1x3/float(ggHTT_eventTree.total_3x5))
    # if ggHTT_eventTree.total_3x1 >= 0:
    #     h_ggHTT_3x1.Fill(ggHTT_eventTree.total_3x1/float(ggHTT_eventTree.total_3x5))
    # if ggHTT_eventTree.total_Cross >= 0:
    #     h_ggHTT_Cross.Fill(ggHTT_eventTree.total_Cross/float(ggHTT_eventTree.total_3x5))
    # if ggHTT_eventTree.total_X >= 0:
    #     h_ggHTT_X.Fill(ggHTT_eventTree.total_X/float(ggHTT_eventTree.total_3x5))

    # if ggHTT_eventTree.total_3x5 >= 0:
    #     h_ggHTT_1x1.Fill(ggHTT_eventTree.total_seed/float(ggHTT_eventTree.total_3x5))
    # ggHTT_total_max1x1in3x3NoSeed = max(ggHTT_eventTree.total_21, ggHTT_eventTree.total_22, ggHTT_eventTree.total_23, ggHTT_eventTree.total_31, ggHTT_eventTree.total_33, ggHTT_eventTree.total_41, ggHTT_eventTree.total_42, ggHTT_eventTree.total_43)
    # if ggHTT_eventTree.total_3x5 >= 0:
    #      h_ggHTT_max1x1in3x3NoSeed.Fill(ggHTT_total_max1x1in3x3NoSeed/float(ggHTT_eventTree.total_3x5))
    # ggHTT_total_CrossNoSeed = max(ggHTT_eventTree.total_22, ggHTT_eventTree.total_31, ggHTT_eventTree.total_33, ggHTT_eventTree.total_42)
    # if ggHTT_eventTree.total_3x5 >= 0:
    #      h_ggHTT_CrossNoSeed.Fill(ggHTT_total_CrossNoSeed/float(ggHTT_eventTree.total_3x5))
    # ggHTT_total_XNoSeed = max(ggHTT_eventTree.total_21, ggHTT_eventTree.total_23, ggHTT_eventTree.total_41, ggHTT_eventTree.total_43)
    # if ggHTT_eventTree.total_3x5 >= 0:
    #      h_ggHTT_XNoSeed.Fill(ggHTT_total_XNoSeed/float(ggHTT_eventTree.total_3x5))
    # ggHTT_total_2x2a = ggHTT_eventTree.total_21 + ggHTT_eventTree.total_22 + ggHTT_eventTree.total_31 + ggHTT_eventTree.total_seed
    # ggHTT_total_2x2b = ggHTT_eventTree.total_22 + ggHTT_eventTree.total_23 + ggHTT_eventTree.total_seed + ggHTT_eventTree.total_33
    # ggHTT_total_2x2c = ggHTT_eventTree.total_31 + ggHTT_eventTree.total_seed + ggHTT_eventTree.total_41 + ggHTT_eventTree.total_42
    # ggHTT_total_2x2d = ggHTT_eventTree.total_seed + ggHTT_eventTree.total_33 + ggHTT_eventTree.total_42 + ggHTT_eventTree.total_43
    # ggHTT_total_max2x2in3x3 = max(ggHTT_total_2x2a, ggHTT_total_2x2b, ggHTT_total_2x2c, ggHTT_total_2x2d)
    # if ggHTT_eventTree.total_3x5 >= 0:
    #      h_ggHTT_max2x2in3x3.Fill(ggHTT_total_max2x2in3x3/float(ggHTT_eventTree.total_3x5))

    ggHTT_CrossTowerList = [ggHTT_eventTree.total_seed, ggHTT_eventTree.total_22, ggHTT_eventTree.total_31, ggHTT_eventTree.total_33, ggHTT_eventTree.total_42]
    ggHTT_CrossTowerList.sort(reverse=True)
    ggHTT_sortedTowers = ggHTT_CrossTowerList
    ggHTT_total_max2inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1]
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
        h_ggHTT_max2inCross_0LessThreshold.Fill(ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
        h_ggHTT_max2inCross_1LessThreshold.Fill(ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
        h_ggHTT_max2inCross_2LessThreshold.Fill(ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5))
    ggHTT_total_max3inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1] + ggHTT_sortedTowers[2]
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
        h_ggHTT_max3inCross_0LessThreshold.Fill(ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
        h_ggHTT_max3inCross_1LessThreshold.Fill(ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5))
    if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
        h_ggHTT_max3inCross_2LessThreshold.Fill(ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5))

#Fill QCD histograms
nEntries_QCD = QCD_eventTree.GetEntries()
for i in range(nEntries_QCD):
    QCD_eventTree.GetEntry(i)

    # if QCD_eventTree.total_3x3 >= 0:
    #     h_QCD_3x3.Fill(QCD_eventTree.total_3x3/float(QCD_eventTree.total_3x5))
    # if QCD_eventTree.total_1x3 >= 0:
    #     h_QCD_1x3.Fill(QCD_eventTree.total_1x3/float(QCD_eventTree.total_3x5))
    # if QCD_eventTree.total_3x1 >= 0:
    #     h_QCD_3x1.Fill(QCD_eventTree.total_3x1/float(QCD_eventTree.total_3x5))
    # if QCD_eventTree.total_Cross >= 0:
    #     h_QCD_Cross.Fill(QCD_eventTree.total_Cross/float(QCD_eventTree.total_3x5))
    # if QCD_eventTree.total_X >= 0:
    #     h_QCD_X.Fill(QCD_eventTree.total_X/float(QCD_eventTree.total_3x5))

    # if QCD_eventTree.total_3x5 >= 0:
    #     h_QCD_1x1.Fill(QCD_eventTree.total_seed/float(QCD_eventTree.total_3x5))
    # QCD_total_max1x1in3x3NoSeed = max(QCD_eventTree.total_21, QCD_eventTree.total_22, QCD_eventTree.total_23, QCD_eventTree.total_31, QCD_eventTree.total_33, QCD_eventTree.total_41, QCD_eventTree.total_42, QCD_eventTree.total_43)
    # if QCD_eventTree.total_3x5 >= 0:
    #      h_QCD_max1x1in3x3NoSeed.Fill(QCD_total_max1x1in3x3NoSeed/float(QCD_eventTree.total_3x5))
    # QCD_total_CrossNoSeed = max(QCD_eventTree.total_22, QCD_eventTree.total_31, QCD_eventTree.total_33, QCD_eventTree.total_42)
    # if QCD_eventTree.total_3x5 >= 0:
    #      h_QCD_CrossNoSeed.Fill(QCD_total_CrossNoSeed/float(QCD_eventTree.total_3x5))
    # QCD_total_XNoSeed = max(QCD_eventTree.total_21, QCD_eventTree.total_23, QCD_eventTree.total_41, QCD_eventTree.total_43)
    # if QCD_eventTree.total_3x5 >= 0:
    #      h_QCD_XNoSeed.Fill(QCD_total_XNoSeed/float(QCD_eventTree.total_3x5))
    # QCD_total_2x2a = QCD_eventTree.total_21 + QCD_eventTree.total_22 + QCD_eventTree.total_31 + QCD_eventTree.total_seed
    # QCD_total_2x2b = QCD_eventTree.total_22 + QCD_eventTree.total_23 + QCD_eventTree.total_seed + QCD_eventTree.total_33
    # QCD_total_2x2c = QCD_eventTree.total_31 + QCD_eventTree.total_seed + QCD_eventTree.total_41 + QCD_eventTree.total_42
    # QCD_total_2x2d = QCD_eventTree.total_seed + QCD_eventTree.total_33 + QCD_eventTree.total_42 + QCD_eventTree.total_43
    # QCD_total_max2x2in3x3 = max(QCD_total_2x2a, QCD_total_2x2b, QCD_total_2x2c, QCD_total_2x2d)
    # if QCD_eventTree.total_3x5 >= 0:
    #      h_QCD_max2x2in3x3.Fill(QCD_total_max2x2in3x3/float(QCD_eventTree.total_3x5))

    QCD_CrossTowerList = [QCD_eventTree.total_seed, QCD_eventTree.total_22, QCD_eventTree.total_31, QCD_eventTree.total_33, QCD_eventTree.total_42]
    QCD_CrossTowerList.sort(reverse=True)
    QCD_sortedTowers = QCD_CrossTowerList
    QCD_total_max2inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1]
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
        h_QCD_max2inCross_0LessThreshold.Fill(QCD_total_max2inCross/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
        h_QCD_max2inCross_1LessThreshold.Fill(QCD_total_max2inCross/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
        h_QCD_max2inCross_2LessThreshold.Fill(QCD_total_max2inCross/float(QCD_eventTree.total_3x5))
    QCD_total_max3inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1] + QCD_sortedTowers[2]
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
        h_QCD_max3inCross_0LessThreshold.Fill(QCD_total_max3inCross/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
        h_QCD_max3inCross_1LessThreshold.Fill(QCD_total_max3inCross/float(QCD_eventTree.total_3x5))
    if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
        h_QCD_max3inCross_2LessThreshold.Fill(QCD_total_max3inCross/float(QCD_eventTree.total_3x5))

#Normalize ggHTT histograms to unit area
# h_ggHTT_3x3.Scale(1/h_ggHTT_3x3.Integral())
# h_ggHTT_1x3.Scale(1/h_ggHTT_1x3.Integral())
# h_ggHTT_3x1.Scale(1/h_ggHTT_3x1.Integral())
# h_ggHTT_Cross.Scale(1/h_ggHTT_Cross.Integral())
# h_ggHTT_X.Scale(1/h_ggHTT_X.Integral())

# h_ggHTT_1x1.Scale(1/h_ggHTT_1x1.Integral())
# h_ggHTT_max1x1in3x3NoSeed.Scale(1/h_ggHTT_max1x1in3x3NoSeed.Integral())
# h_ggHTT_CrossNoSeed.Scale(1/h_ggHTT_CrossNoSeed.Integral())
# h_ggHTT_XNoSeed.Scale(1/h_ggHTT_XNoSeed.Integral())
# h_ggHTT_max2x2in3x3.Scale(1/h_ggHTT_max2x2in3x3.Integral())

h_ggHTT_max2inCross_0LessThreshold.Scale(1/h_ggHTT_max2inCross_0LessThreshold.Integral())
h_ggHTT_max2inCross_1LessThreshold.Scale(1/h_ggHTT_max2inCross_1LessThreshold.Integral())
h_ggHTT_max2inCross_2LessThreshold.Scale(1/h_ggHTT_max2inCross_2LessThreshold.Integral())
h_ggHTT_max3inCross_0LessThreshold.Scale(1/h_ggHTT_max3inCross_0LessThreshold.Integral())
h_ggHTT_max3inCross_1LessThreshold.Scale(1/h_ggHTT_max3inCross_1LessThreshold.Integral())
h_ggHTT_max3inCross_2LessThreshold.Scale(1/h_ggHTT_max3inCross_2LessThreshold.Integral())

#Normalize QCT histograms to unit area
# h_QCD_3x3.Scale(1/h_QCD_3x3.Integral())
# h_QCD_1x3.Scale(1/h_QCD_1x3.Integral())
# h_QCD_3x1.Scale(1/h_QCD_3x1.Integral())
# h_QCD_Cross.Scale(1/h_QCD_Cross.Integral())
# h_QCD_X.Scale(1/h_QCD_X.Integral())

# h_QCD_1x1.Scale(1/h_QCD_1x1.Integral())
# h_QCD_max1x1in3x3NoSeed.Scale(1/h_QCD_max1x1in3x3NoSeed.Integral())
# h_QCD_CrossNoSeed.Scale(1/h_QCD_CrossNoSeed.Integral())
# h_QCD_XNoSeed.Scale(1/h_QCD_XNoSeed.Integral())
# h_QCD_max2x2in3x3.Scale(1/h_QCD_max2x2in3x3.Integral())

h_QCD_max2inCross_0LessThreshold.Scale(1/h_QCD_max2inCross_0LessThreshold.Integral())
h_QCD_max2inCross_1LessThreshold.Scale(1/h_QCD_max2inCross_1LessThreshold.Integral())
h_QCD_max2inCross_2LessThreshold.Scale(1/h_QCD_max2inCross_2LessThreshold.Integral())
h_QCD_max3inCross_0LessThreshold.Scale(1/h_QCD_max3inCross_0LessThreshold.Integral())
h_QCD_max3inCross_1LessThreshold.Scale(1/h_QCD_max3inCross_1LessThreshold.Integral())
h_QCD_max3inCross_2LessThreshold.Scale(1/h_QCD_max3inCross_2LessThreshold.Integral())

#Draw max2inCross_0LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c = TCanvas('c', 'Tower energy fraction distributions')
    c.Divide(3,2)
    c.cd(1)
else:
    #c_3x3 = TCanvas('c_3x3', '3x3 Tower energy fraction distribution')
    #c_1x1 = TCanvas('c_1x1', '1x1 Tower energy fraction distribution')
    c_max2inCross_0LessThreshold = TCanvas('c_max2inCross_0LessThreshold', 'max2inCross_0LessThreshold Tower energy fraction distribution')
# h_ggHTT_3x3.Draw('hist')
# h_QCD_3x3.Draw('hist same')
# #Set ggHTT_3x3 histogram options
# h_ggHTT_3x3.SetLineColor(kRed)
# h_ggHTT_3x3.SetLineWidth(1)
# h_ggHTT_3x3.SetMinimum(0)
# h_ggHTT_3x3.SetMaximum(yMax)
# #Set QCD_3x3 histogram options
# h_QCD_3x3.SetLineColor(kBlue)
# h_QCD_3x3.SetLineWidth(1)
# h_QCD_3x3.SetMinimum(0)
# h_QCD_3x3.SetMaximum(yMax)
# #Add legend
# legend_3x3 = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_3x3.AddEntry(h_ggHTT_3x3, 'ggHTT, 3x3', 'l')
# legend_3x3.AddEntry(h_QCD_3x3, 'QCD, 3x3', 'l')
# legend_3x3.Draw('same')
# legend_3x3.SetBorderSize(0)
h_ggHTT_max2inCross_0LessThreshold.Draw('hist')
h_QCD_max2inCross_0LessThreshold.Draw('hist same')
#Set ggHTT_max2inCross_0LessThreshold histogram options
h_ggHTT_max2inCross_0LessThreshold.SetLineColor(kRed)
h_ggHTT_max2inCross_0LessThreshold.SetLineWidth(1)
h_ggHTT_max2inCross_0LessThreshold.SetMinimum(0)
h_ggHTT_max2inCross_0LessThreshold.SetMaximum(yMax)
#Set QCD_max2inCross_0LessThreshold histogram options
h_QCD_max2inCross_0LessThreshold.SetLineColor(kBlue)
h_QCD_max2inCross_0LessThreshold.SetLineWidth(1)
h_QCD_max2inCross_0LessThreshold.SetMinimum(0)
h_QCD_max2inCross_0LessThreshold.SetMaximum(yMax)
#Add legend
legend_max2inCross_0LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max2inCross_0LessThreshold.AddEntry(h_ggHTT_max2inCross_0LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max2inCross_0LessThreshold.GetEntries()), 'l')
legend_max2inCross_0LessThreshold.AddEntry(h_QCD_max2inCross_0LessThreshold, 'QCD, entries = ' + str(h_QCD_max2inCross_0LessThreshold.GetEntries()), 'l')
legend_max2inCross_0LessThreshold.Draw('same')
legend_max2inCross_0LessThreshold.SetBorderSize(0)

#Draw max2inCross_1LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(2)
else:
    #c_1x3 = TCanvas('c_1x3', '1x3 Tower energy fraction distribution')
    #c_max1x1in3x3NoSeed = TCanvas('c_max1x1in3x3NoSeed', 'max1x1in3x3NoSeed Tower energy fraction distribution')
    c_max2inCross_1LessThreshold = TCanvas('c_max2inCross_1LessThreshold', 'max2inCross_1LessThreshold Tower energy fraction distribution')
# h_ggHTT_1x3.Draw('hist')
# h_QCD_1x3.Draw('hist same')
# #Set ggHTT_1x3 histogram options
# h_ggHTT_1x3.SetLineColor(kRed)
# h_ggHTT_1x3.SetLineWidth(1)
# h_ggHTT_1x3.SetMinimum(0)
# h_ggHTT_1x3.SetMaximum(yMax)
# #Set QCD_1x3 histogram options
# h_QCD_1x3.SetLineColor(kBlue)
# h_QCD_1x3.SetLineWidth(1)
# h_QCD_1x3.SetMinimum(0)
# h_QCD_1x3.SetMaximum(yMax)
# #Add legend
# legend_1x3 = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_1x3.AddEntry(h_ggHTT_1x3, 'ggHTT, 1x3', 'l')
# legend_1x3.AddEntry(h_QCD_1x3, 'QCD, 1x3', 'l')
# legend_1x3.Draw('same')
# legend_1x3.SetBorderSize(0)
h_ggHTT_max2inCross_1LessThreshold.Draw('hist')
h_QCD_max2inCross_1LessThreshold.Draw('hist same')
#Set ggHTT_max2inCross_1LessThreshold histogram options
h_ggHTT_max2inCross_1LessThreshold.SetLineColor(kRed)
h_ggHTT_max2inCross_1LessThreshold.SetLineWidth(1)
h_ggHTT_max2inCross_1LessThreshold.SetMinimum(0)
h_ggHTT_max2inCross_1LessThreshold.SetMaximum(yMax)
#Set QCD_max2inCross_1LessThreshold histogram options
h_QCD_max2inCross_1LessThreshold.SetLineColor(kBlue)
h_QCD_max2inCross_1LessThreshold.SetLineWidth(1)
h_QCD_max2inCross_1LessThreshold.SetMinimum(0)
h_QCD_max2inCross_1LessThreshold.SetMaximum(yMax)
#Add legend
legend_max2inCross_1LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max2inCross_1LessThreshold.AddEntry(h_ggHTT_max2inCross_1LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max2inCross_1LessThreshold.GetEntries()), 'l')
legend_max2inCross_1LessThreshold.AddEntry(h_QCD_max2inCross_1LessThreshold, 'QCD, entries = ' + str(h_QCD_max2inCross_1LessThreshold.GetEntries()), 'l')
legend_max2inCross_1LessThreshold.Draw('same')
legend_max2inCross_1LessThreshold.SetBorderSize(0)

#Draw max2inCross_2LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(3)
else:
    #c_3x1 = TCanvas('c_3x1', '3x1 Tower energy fraction distribution')
    c_max2inCross_2LessThreshold = TCanvas('c_max2inCross_2LessThreshold', 'max2inCross_2LessThreshold Tower energy fraction distribution')
# h_ggHTT_3x1.Draw('hist')
# h_QCD_3x1.Draw('hist same')
# #Set ggHTT_3x1 histogram options
# h_ggHTT_3x1.SetLineColor(kRed)
# h_ggHTT_3x1.SetLineWidth(1)
# h_ggHTT_3x1.SetMinimum(0)
# h_ggHTT_3x1.SetMaximum(yMax)
# #Set QCD_3x1 histogram options
# h_QCD_3x1.SetLineColor(kBlue)
# h_QCD_3x1.SetLineWidth(1)
# h_QCD_3x1.SetMinimum(0)
# h_QCD_3x1.SetMaximum(yMax)
# #Add legend
# legend_3x1 = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_3x1.AddEntry(h_ggHTT_3x1, 'ggHTT, 3x1', 'l')
# legend_3x1.AddEntry(h_QCD_3x1, 'QCD, 3x1', 'l')
# legend_3x1.Draw('same')
# legend_3x1.SetBorderSize(0)
h_ggHTT_max2inCross_2LessThreshold.Draw('hist')
h_QCD_max2inCross_2LessThreshold.Draw('hist same')
#Set ggHTT_max2inCross_2LessThreshold histogram options
h_ggHTT_max2inCross_2LessThreshold.SetLineColor(kRed)
h_ggHTT_max2inCross_2LessThreshold.SetLineWidth(1)
h_ggHTT_max2inCross_2LessThreshold.SetMinimum(0)
h_ggHTT_max2inCross_2LessThreshold.SetMaximum(yMax)
#Set QCD_max2inCross_2LessThreshold histogram options
h_QCD_max2inCross_2LessThreshold.SetLineColor(kBlue)
h_QCD_max2inCross_2LessThreshold.SetLineWidth(1)
h_QCD_max2inCross_2LessThreshold.SetMinimum(0)
h_QCD_max2inCross_2LessThreshold.SetMaximum(yMax)
#Add legend
legend_max2inCross_2LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max2inCross_2LessThreshold.AddEntry(h_ggHTT_max2inCross_2LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max2inCross_2LessThreshold.GetEntries()), 'l')
legend_max2inCross_2LessThreshold.AddEntry(h_QCD_max2inCross_2LessThreshold, 'QCD, entries = ' + str(h_QCD_max2inCross_2LessThreshold.GetEntries()), 'l')
legend_max2inCross_2LessThreshold.Draw('same')
legend_max2inCross_2LessThreshold.SetBorderSize(0)

#Draw max3inCross_0LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(4)
else:
    #c_Cross = TCanvas('c_Cross', 'Cross Tower energy fraction distribution')
    c_max3inCross_0LessThreshold = TCanvas('c_max3inCross_0LessThreshold', 'max3inCross_0LessThreshold Tower energy fraction distribution')
# h_ggHTT_Cross.Draw('hist')
# h_QCD_Cross.Draw('hist same')
# #Set ggHTT_Cross histogram options
# h_ggHTT_Cross.SetLineColor(kRed)
# h_ggHTT_Cross.SetLineWidth(1)
# h_ggHTT_Cross.SetMinimum(0)
# h_ggHTT_Cross.SetMaximum(yMax)
# #Set QCD_Cross histogram options
# h_QCD_Cross.SetLineColor(kBlue)
# h_QCD_Cross.SetLineWidth(1)
# h_QCD_Cross.SetMinimum(0)
# h_QCD_Cross.SetMaximum(yMax)
# #Add legend
# legend_Cross = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_Cross.AddEntry(h_ggHTT_Cross, 'ggHTT, Cross', 'l')
# legend_Cross.AddEntry(h_QCD_Cross, 'QCD, Cross', 'l')
# legend_Cross.Draw('same')
# legend_Cross.SetBorderSize(0)
h_ggHTT_max3inCross_0LessThreshold.Draw('hist')
h_QCD_max3inCross_0LessThreshold.Draw('hist same')
#Set ggHTT_max3inCross_0LessThreshold histogram options
h_ggHTT_max3inCross_0LessThreshold.SetLineColor(kRed)
h_ggHTT_max3inCross_0LessThreshold.SetLineWidth(1)
h_ggHTT_max3inCross_0LessThreshold.SetMinimum(0)
#h_ggHTT_max3inCross_0LessThreshold.SetMaximum(yMax)
h_ggHTT_max3inCross_0LessThreshold.SetMaximum(0.6)
#Set QCD_max3inCross_0LessThreshold histogram options
h_QCD_max3inCross_0LessThreshold.SetLineColor(kBlue)
h_QCD_max3inCross_0LessThreshold.SetLineWidth(1)
h_QCD_max3inCross_0LessThreshold.SetMinimum(0)
h_QCD_max3inCross_0LessThreshold.SetMaximum(yMax)
#Add legend
legend_max3inCross_0LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max3inCross_0LessThreshold.AddEntry(h_ggHTT_max3inCross_0LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max3inCross_0LessThreshold.GetEntries()), 'l')
legend_max3inCross_0LessThreshold.AddEntry(h_QCD_max3inCross_0LessThreshold, 'QCD, entries = ' + str(h_QCD_max3inCross_0LessThreshold.GetEntries()), 'l')
legend_max3inCross_0LessThreshold.Draw('same')
legend_max3inCross_0LessThreshold.SetBorderSize(0)

#Draw max3inCross_1LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(5)
else:
    #c_X = TCanvas('c_X', 'X Tower energy fraction distribution')
    c_max3inCross_1LessThreshold = TCanvas('c_max3inCross_1LessThreshold', 'max3inCross_1LessThreshold Tower energy fraction distribution')
# h_ggHTT_X.Draw('hist')
# h_QCD_X.Draw('hist same')
# #Set ggHTT_X histogram options
# h_ggHTT_X.SetLineColor(kRed)
# h_ggHTT_X.SetLineWidth(1)
# h_ggHTT_X.SetMinimum(0)
# h_ggHTT_X.SetMaximum(yMax)
# #Set QCD_X histogram options
# h_QCD_X.SetLineColor(kBlue)
# h_QCD_X.SetLineWidth(1)
# h_QCD_X.SetMinimum(0)
# h_QCD_X.SetMaximum(yMax)
# #Add legend
# legend_X = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_X.AddEntry(h_ggHTT_X, 'ggHTT, X', 'l')
# legend_X.AddEntry(h_QCD_X, 'QCD, X', 'l')
# legend_X.Draw('same')
# legend_X.SetBorderSize(0)
h_ggHTT_max3inCross_1LessThreshold.Draw('hist')
h_QCD_max3inCross_1LessThreshold.Draw('hist same')
#Set ggHTT_max3inCross_1LessThreshold histogram options
h_ggHTT_max3inCross_1LessThreshold.SetLineColor(kRed)
h_ggHTT_max3inCross_1LessThreshold.SetLineWidth(1)
h_ggHTT_max3inCross_1LessThreshold.SetMinimum(0)
h_ggHTT_max3inCross_1LessThreshold.SetMaximum(yMax)
#Set QCD_max3inCross_1LessThreshold histogram options
h_QCD_max3inCross_1LessThreshold.SetLineColor(kBlue)
h_QCD_max3inCross_1LessThreshold.SetLineWidth(1)
h_QCD_max3inCross_1LessThreshold.SetMinimum(0)
h_QCD_max3inCross_1LessThreshold.SetMaximum(yMax)
#Add legend
legend_max3inCross_1LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max3inCross_1LessThreshold.AddEntry(h_ggHTT_max3inCross_1LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max3inCross_1LessThreshold.GetEntries()), 'l')
legend_max3inCross_1LessThreshold.AddEntry(h_QCD_max3inCross_1LessThreshold, 'QCD, entries = ' + str(h_QCD_max3inCross_1LessThreshold.GetEntries()), 'l')
legend_max3inCross_1LessThreshold.Draw('same')
legend_max3inCross_1LessThreshold.SetBorderSize(0)

#Draw max3inCross_2LessThreshold tower E_T fraction distribution plots 
if sameCanvas:
    c.cd(6)
else:
    #c_X = TCanvas('c_X', 'X Tower energy fraction distribution')
    c_max3inCross_2LessThreshold = TCanvas('c_max3inCross_2LessThreshold', 'max3inCross_2LessThreshold Tower energy fraction distribution')
# h_ggHTT_X.Draw('hist')
# h_QCD_X.Draw('hist same')
# #Set ggHTT_X histogram options
# h_ggHTT_X.SetLineColor(kRed)
# h_ggHTT_X.SetLineWidth(1)
# h_ggHTT_X.SetMinimum(0)
# h_ggHTT_X.SetMaximum(yMax)
# #Set QCD_X histogram options
# h_QCD_X.SetLineColor(kBlue)
# h_QCD_X.SetLineWidth(1)
# h_QCD_X.SetMinimum(0)
# h_QCD_X.SetMaximum(yMax)
# #Add legend
# legend_X = TLegend(0.46, 0.73, 0.75, 0.87)
# legend_X.AddEntry(h_ggHTT_X, 'ggHTT, X', 'l')
# legend_X.AddEntry(h_QCD_X, 'QCD, X', 'l')
# legend_X.Draw('same')
# legend_X.SetBorderSize(0)
h_ggHTT_max3inCross_2LessThreshold.Draw('hist')
h_QCD_max3inCross_2LessThreshold.Draw('hist same')
#Set ggHTT_max3inCross_2LessThreshold histogram options
h_ggHTT_max3inCross_2LessThreshold.SetLineColor(kRed)
h_ggHTT_max3inCross_2LessThreshold.SetLineWidth(1)
h_ggHTT_max3inCross_2LessThreshold.SetMinimum(0)
h_ggHTT_max3inCross_2LessThreshold.SetMaximum(yMax)
#Set QCD_max3inCross_2LessThreshold histogram options
h_QCD_max3inCross_2LessThreshold.SetLineColor(kBlue)
h_QCD_max3inCross_2LessThreshold.SetLineWidth(1)
h_QCD_max3inCross_2LessThreshold.SetMinimum(0)
h_QCD_max3inCross_2LessThreshold.SetMaximum(yMax)
#Add legend
legend_max3inCross_2LessThreshold = TLegend(0.46, 0.73, 0.75, 0.87)
legend_max3inCross_2LessThreshold.AddEntry(h_ggHTT_max3inCross_2LessThreshold, 'ggHTT, entries = ' + str(h_ggHTT_max3inCross_2LessThreshold.GetEntries()), 'l')
legend_max3inCross_2LessThreshold.AddEntry(h_QCD_max3inCross_2LessThreshold, 'QCD, entries = ' + str(h_QCD_max3inCross_2LessThreshold.GetEntries()), 'l')
legend_max3inCross_2LessThreshold.Draw('same')
legend_max3inCross_2LessThreshold.SetBorderSize(0)
