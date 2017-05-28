


# File to store the most current cuts instead of having them defined in
# each python file

def getCutMap() :
    cutMap = {
    '90x500MeV' : {
        'showerShape' : '(0.943562 + 0.0520763*TMath::Exp(-0.0443794*cluster_pt)<(e2x5/e5x5))',
        'isolation' : '((0.849167 + (-0.00799425)*cluster_pt) > cluster_iso)',
        #'isolation' : '((0.214497 + 1.20357*TMath::Exp(-0.0129899*cluster_pt))>cluster_iso)',
        'trackMatch' : '(trackDeltaR < 0.05)',
        'photonTag' : '(e2x2/e2x5 > 0.95)',
    },
    '90x250MeV' : {
        'showerShape' : '(0.939843 + 0.108017*TMath::Exp(-0.106255*cluster_pt)<(e2x5/e5x5))',
        'isolation' : '((-0.266481 + 1.48726*TMath::Exp(-0.0129899*cluster_pt))>cluster_iso)',
    },
    '62x' : {
        'showerShape' : '(-0.896501 + 0.181135*TMath::Exp(-0.0696926*cluster_pt)>(-1)*(e2x5/e5x5))',
        'isolation' : '((1.0614 + 5.65869*TMath::Exp(-0.0646173*cluster_pt))>cluster_iso)',
    }, # 62x
    } # end map
    return cutMap
