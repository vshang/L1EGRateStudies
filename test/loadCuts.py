


# File to store the most current cuts instead of having them defined in
# each python file

def getCutMap() :
    cutMap = {
    '90x500MeV' : {
        'showerShape' : '(-0.944982 + -0.0638548*TMath::Exp(-0.0623697*cluster_pt)>(-1)*(e2x5/e5x5))',
        'isolation' : '((0.772083 + (-0.00664368)*cluster_pt) > cluster_iso)',
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
