import ROOT
from ROOT import gPad, gStyle

def createCDF(hist, invert = False) :
    for i in range( 0, hist.GetNbinsX()+1 ) :
        integral = hist.Integral(i, i, 0, hist.GetNbinsY()+1)
        if integral == 0 : continue
        for j in range( 0, hist.GetNbinsY()+1 ) :
            hist.SetBinContent(i, j, hist.GetBinContent(i, j)/integral)

        integral = 0
        for j in range( 1, hist.GetNbinsY()+2 ) :
            integral += hist.GetBinContent(i, j)
            #hist.SetBinContent(i, j, (invert)? 1-integral:integral)
            if invert : toSet = 1.-integral
            else : toSet = integral
            hist.SetBinContent(i, j, toSet)



def drawCDFs(c, rate, eff, variable, var_cuts, cut, max_) :
    prefix = c.GetName()
    var_name = c.GetTitle()
    cutFunction = ROOT.TF1(prefix+"_cut", cut, 0., 50.)
    c.Divide(2,1)

    c.cd(2)
    gPad.SetRightMargin(0.13)
    rate_cdf = ROOT.TH2F(prefix+"_rate_cdf", "BackgroundCluster pT"+var_name, 60, 0., 50., 50, 0., max_)
    #rate.Draw(variable+":raw_pt >> "+prefix+"_rate_cdf", var_cuts, "goff")
    rate.Draw(variable+":reco_pt >> "+prefix+"_rate_cdf", var_cuts, "goff")
    rate_cdf.GetYaxis().SetTitleOffset(1.4)
    rate_cdf.Draw("colz")
    cutFunction.Draw("lsame")

    c.cd(1)
    gPad.SetRightMargin(0.13)
    eff_cdf = ROOT.TH2F(prefix+"_eff_cdf", "Single Electron signalCluster pT"+var_name, 60, 0., 50., 50, 0., max_)
    #eff.Draw(variable+":raw_pt >> "+prefix+"_eff_cdf", var_cuts, "goff")
    eff.Draw(variable+":reco_pt >> "+prefix+"_eff_cdf", var_cuts, "goff")
    eff_cdf.GetYaxis().SetTitleOffset(1.4)
    eff_cdf.Draw("colz")
    cutFunction.Draw("lsame")

    c.Print("plots/"+c.GetName()+"_pdf.png")
    c.Clear()

    createCDF(rate_cdf, True)
    createCDF(eff_cdf)
    contours = [0., 0.5, 1-ROOT.TMath.exp(-1), 1-ROOT.TMath.exp(-2), 1-ROOT.TMath.exp(-3), 1-ROOT.TMath.exp(-4)]
    for i, contour in enumerate( contours ) :
        eff_cdf.SetContourLevel(i, contour)

    c.Divide(2,1)
    c.cd(1)
    gPad.SetRightMargin(0.13)
    eff_cdf.GetZaxis().SetTitle("Cumulative event fraction (<cut)")
    eff_cdf.Draw("colz")
    cutFunction.Draw("lsame")
    c.cd(2)
    gPad.SetRightMargin(0.13)
    rate_cdf.GetZaxis().SetTitle("Cumulative event fraction (>cut)")
    rate_cdf.Draw("colz")
    cutFunction.Draw("lsame")

    c.Print("plots/"+c.GetName()+"_cdf.png")
    c.Clear()



if __name__ == '__main__' :
    gStyle.SetOptStat(0)
    gStyle.SetTitleFont(42, "p")
    gStyle.SetTitleColor(1)
    gStyle.SetTitleTextColor(1)
    gStyle.SetTitleFillColor(10)
    gStyle.SetTitleFontSize(0.05)
    gStyle.SetTitleOffset(1.2, "XYZ")
    gStyle.SetTitleFont(42, "XYZ")
    gStyle.SetLabelFont(42, "XYZ")

    effFile = ROOT.TFile("egTriggerEff.root", "r")
    rateFile = ROOT.TFile("egTriggerRates.root", "r")
    eff = effFile.Get("analyzer/crystal_tree")
    rate = rateFile.Get("analyzer/crystal_tree")

    c = ROOT.TCanvas("canvas", "canvas", 1200, 600)

    c.SetName("hovere")
    c.SetTitle("H/E Value")
    # endcap: "22./x+0."
    drawCDFs(c, rate, eff, "cluster_hovere", "", "14/x+.05", 5)

    c.SetName("isolation")
    c.SetTitle("Isolation Value")
    # endcap: "64/x+0.1"
    drawCDFs(c, rate, eff, "cluster_iso", "", "40/x+0.1", 15)

    c.SetName("ptratio")
    c.SetTitle("Pt Ratio Value")
    # endcap: "0.18*(1-x/70)*(x<40)+.18*3/7*(x>40)"
    drawCDFs(c, rate, eff, "pt.5/(pt.1+pt.2)", "", "0.18*(1-x/100)*(x<30)+.18*.7*(x>30)", 0.3)


