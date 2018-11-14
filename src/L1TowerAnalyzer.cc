//
// Original Author: Tyler Ruggles
// Created: Mon Nov 12 2018
//
//


#include "SimDataFormats/Track/interface/SimTrackContainer.h"
//#include "SimDataFormats/Vertex/interface/CoreSimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertex.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"

#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/HcalTowerAlgo/interface/HcalTrigTowerGeometry.h"
#include "Geometry/HcalTowerAlgo/interface/HcalGeometry.h"
#include <iostream>

#include "DataFormats/Phase2L1CaloTrig/interface/L1EGCrystalCluster.h"
#include "DataFormats/Phase2L1CaloTrig/interface/L1CaloJet.h"
#include "DataFormats/Phase2L1CaloTrig/interface/L1CaloTower.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/CaloTopology/interface/HcalTopology.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"

#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalSourcePositionData.h"

#include "Geometry/Records/interface/IdealGeometryRecord.h"

#include "TH1.h"
#include "TTree.h"


class L1TowerAnalyzer : public edm::EDAnalyzer {
    public:
        explicit L1TowerAnalyzer(const edm::ParameterSet&);

    private:
        virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

        //double EtminForStore;
        double HcalTpEtMin;
        double EcalTpEtMin;
        double puThreshold;
        double puThresholdEcal;
        double puThresholdHcal;
        double puThresholdL1eg;

        bool debug;
        edm::EDGetTokenT< std::vector< SimVertex > > simVertexToken_;
        edm::Handle< std::vector< SimVertex > > simVertexHandle;
        edm::EDGetTokenT< std::vector< TrackingVertex > > trackingVertexInitToken_;
        edm::Handle< std::vector< TrackingVertex > > trackingVertexInitHandle;

        edm::EDGetTokenT< L1CaloTowerCollection > l1TowerToken_;
        edm::Handle< L1CaloTowerCollection > l1CaloTowerHandle;

        edm::EDGetTokenT<l1slhc::L1EGCrystalClusterCollection> crystalClustersToken_;
        edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;
        l1slhc::L1EGCrystalClusterCollection crystalClusters;

        edm::ESHandle<CaloGeometry> caloGeometry_;
        const CaloSubdetectorGeometry * hbGeometry;
        edm::ESHandle<HcalTopology> hbTopology;
        const HcalTopology * hcTopology_;





        class simpleL1obj
        {
            public:
                bool stale = false; // Hits become stale once used in clustering algorithm to prevent overlap in clusters
                bool associated_with_tower = false; // L1EGs become associated with a tower to find highest ET total for seeding jets
                bool passesStandaloneWP = false; // Store whether any of the WPs are passed
                bool passesTrkMatchWP = false; // Store whether any of the WPs are passed
                reco::Candidate::PolarLorentzVector p4;

                void SetP4( double pt, double eta, double phi, double mass )
                {
                    this->p4.SetPt( pt );
                    this->p4.SetEta( eta );
                    this->p4.SetPhi( phi );
                    this->p4.SetM( mass );
                }
                inline float pt() const{return p4.pt();};
                inline float eta() const{return p4.eta();};
                inline float phi() const{return p4.phi();};
                inline float M() const{return p4.M();};
                inline reco::Candidate::PolarLorentzVector GetP4() const{return p4;};
        };
                


        class SimpleCaloHit
        {
            public:
                int tower_iEta = -99;
                int tower_iPhi = -99;
                float tower_eta = -99;
                float tower_phi = -99;
                float ecal_tower_et=0.;
                float hcal_tower_et=0.;
                float total_tower_et=0.;
                float total_tower_plus_L1EGs_et=0.;
                bool stale=false; // Hits become stale once used in clustering algorithm to prevent overlap in clusters
        };


        TH1D *NEvents;
        TH1D *nvtx;
        TH1D *nvtx_init;


        TH1D *total_hits;
        TH1D *total_hits_gtr_threshold;
        TH1D *total_hits_leq_threshold;
        TH1D *total_hits_et;
        TH1D *total_gtr_threshold_sum;
        TH1D *total_leq_threshold_sum;
        TH1D *total_et_sum;
        TH1D *ecal_hits;
        TH1D *ecal_hits_gtr_threshold;
        TH1D *ecal_hits_leq_threshold;
        TH1D *ecal_hits_et;
        TH1D *ecal_gtr_threshold_sum;
        TH1D *ecal_leq_threshold_sum;
        TH1D *ecal_et_sum;
        TH1D *hcal_hits;
        TH1D *hcal_hits_gtr_threshold;
        TH1D *hcal_hits_leq_threshold;
        TH1D *hcal_hits_et;
        TH1D *hcal_gtr_threshold_sum;
        TH1D *hcal_leq_threshold_sum;
        TH1D *hcal_et_sum;
        TH1D *l1eg_hits;
        TH1D *l1eg_hits_gtr_threshold;
        TH1D *l1eg_hits_leq_threshold;
        TH1D *l1eg_hits_et;
        TH1D *l1eg_gtr_threshold_sum;
        TH1D *l1eg_leq_threshold_sum;
        TH1D *l1eg_et_sum;
        TH1D *unc_hits;
        TH1D *unc_hits_gtr_threshold;
        TH1D *unc_hits_leq_threshold;
        TH1D *unc_hits_et;
        TH1D *unc_gtr_threshold_sum;
        TH1D *unc_leq_threshold_sum;
        TH1D *unc_et_sum;


        TTree * hit_tree;
        struct {
            double run;
            double lumi;
            double event;
            int nvtx;
            int nvtx_init;
            // N Tower totals
            int i_total_hits;
            int i_total_hits_gtr_threshold;
            int i_total_hits_leq_threshold;
            int i_ecal_hits;
            int i_ecal_hits_er1to3;
            int i_ecal_hits_er4to6;
            int i_ecal_hits_er7to9;
            int i_ecal_hits_er10to12;
            int i_ecal_hits_er13to15;
            int i_ecal_hits_er16to18;
            int i_ecal_hits_gtr_threshold;
            int i_ecal_hits_leq_threshold;
            int i_hcal_hits;
            int i_hcal_hits_er1to3;
            int i_hcal_hits_er4to6;
            int i_hcal_hits_er7to9;
            int i_hcal_hits_er10to12;
            int i_hcal_hits_er13to15;
            int i_hcal_hits_er16to18;
            int i_hcal_hits_gtr_threshold;
            int i_hcal_hits_leq_threshold;
            int i_l1eg_hits;
            int i_l1eg_hits_gtr_threshold;
            int i_l1eg_hits_leq_threshold;
            int i_unc_hits;
            int i_unc_hits_gtr_threshold;
            int i_unc_hits_leq_threshold;
            // ET totals
            float f_total_hits;
            float f_total_hits_gtr_threshold;
            float f_total_hits_leq_threshold;
            float f_ecal_hits;
            float f_ecal_hits_er1to3;
            float f_ecal_hits_er4to6;
            float f_ecal_hits_er7to9;
            float f_ecal_hits_er10to12;
            float f_ecal_hits_er13to15;
            float f_ecal_hits_er16to18;
            float f_ecal_hits_gtr_threshold;
            float f_ecal_hits_leq_threshold;
            float f_hcal_hits;
            float f_hcal_hits_er1to3;
            float f_hcal_hits_er4to6;
            float f_hcal_hits_er7to9;
            float f_hcal_hits_er10to12;
            float f_hcal_hits_er13to15;
            float f_hcal_hits_er16to18;
            float f_hcal_hits_gtr_threshold;
            float f_hcal_hits_leq_threshold;
            float f_l1eg_hits;
            float f_l1eg_hits_gtr_threshold;
            float f_l1eg_hits_leq_threshold;
            float f_unc_hits;
            float f_unc_hits_gtr_threshold;
            float f_unc_hits_leq_threshold;
        } treeinfo;

};

L1TowerAnalyzer::L1TowerAnalyzer(const edm::ParameterSet& iConfig) :
    //EtminForStore(iConfig.getParameter<double>("EtminForStore")),
    HcalTpEtMin(iConfig.getParameter<double>("HcalTpEtMin")), // Should default to 0 MeV
    EcalTpEtMin(iConfig.getParameter<double>("EcalTpEtMin")), // Should default to 0 MeV
    puThreshold(iConfig.getParameter<double>("puThreshold")), // Should default to 5.0 GeV
    puThresholdEcal(iConfig.getParameter<double>("puThresholdEcal")), // Should default to 5.0 GeV
    puThresholdHcal(iConfig.getParameter<double>("puThresholdHcal")), // Should default to 5.0 GeV
    puThresholdL1eg(iConfig.getParameter<double>("puThresholdL1eg")), // Should default to 5.0 GeV
    debug(iConfig.getParameter<bool>("debug")),
    simVertexToken_(consumes< std::vector< SimVertex > >(iConfig.getParameter<edm::InputTag>("vertexTag"))),
    trackingVertexInitToken_(consumes< std::vector< TrackingVertex > >(iConfig.getParameter<edm::InputTag>("trackingVertexInitTag"))),
    l1TowerToken_(consumes< L1CaloTowerCollection >(iConfig.getParameter<edm::InputTag>("l1CaloTowers"))),
    crystalClustersToken_(consumes<l1slhc::L1EGCrystalClusterCollection>(iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag")))

{
    //now do what ever initialization is needed
 
    edm::Service<TFileService> fs;
    NEvents = fs->make<TH1D>("NEvents" , "NEvents" , 1 , -0.5 , 0.5 );
    nvtx = fs->make<TH1D>("nvtx" , "nvtx" , 400 , 0 , 800 );
    nvtx_init = fs->make<TH1D>("nvtx_init" , "nvtx_init" , 300 , 0 , 300 );


    int total_max = 2000;
    int total_n_bins = 200;
    int et_total_max = 3000;
    int et_total_n_bins = 300;
    total_hits = fs->make<TH1D>("total_hits" , "total_hits" , total_n_bins , 0 , total_max );
    total_hits_gtr_threshold = fs->make<TH1D>("total_hits_gtr_threshold" , "total_hits_gtr_threshold" , 250 , 0 , 250 );
    total_hits_leq_threshold = fs->make<TH1D>("total_hits_leq_threshold" , "total_hits_leq_threshold" , total_n_bins , 0 , total_max );
    total_hits_et = fs->make<TH1D>("total_hits_et" , "total_hits_et" , 300 , 0 , 150 );
    total_gtr_threshold_sum = fs->make<TH1D>("total_gtr_threshold_sum" , "total_gtr_threshold_sum" , et_total_n_bins, 0, et_total_max );
    total_leq_threshold_sum = fs->make<TH1D>("total_leq_threshold_sum" , "total_leq_threshold_sum" , et_total_n_bins , 0 , et_total_max );
    total_et_sum = fs->make<TH1D>("total_et_sum" , "total_et_sum" , et_total_n_bins , 0 , et_total_max );

    ecal_hits = fs->make<TH1D>("ecal_hits" , "ecal_hits" , total_n_bins , 0 , total_max );
    ecal_hits_gtr_threshold = fs->make<TH1D>("ecal_hits_gtr_threshold" , "ecal_hits_gtr_threshold" , 50 , 0 , 50 );
    ecal_hits_leq_threshold = fs->make<TH1D>("ecal_hits_leq_threshold" , "ecal_hits_leq_threshold" , total_n_bins , 0 , total_max );
    ecal_hits_et = fs->make<TH1D>("ecal_hits_et" , "ecal_hits_et" , 100 , 0 , 100 );
    ecal_gtr_threshold_sum = fs->make<TH1D>("ecal_gtr_threshold_sum" , "ecal_gtr_threshold_sum" , et_total_n_bins, 0, 100 );
    ecal_leq_threshold_sum = fs->make<TH1D>("ecal_leq_threshold_sum" , "ecal_leq_threshold_sum" , et_total_n_bins , 0 , et_total_max );
    ecal_et_sum = fs->make<TH1D>("ecal_et_sum" , "ecal_et_sum" , et_total_n_bins , 0 , et_total_max );

    hcal_hits = fs->make<TH1D>("hcal_hits" , "hcal_hits" , total_n_bins , 0 , total_max );
    hcal_hits_gtr_threshold = fs->make<TH1D>("hcal_hits_gtr_threshold" , "hcal_hits_gtr_threshold" , 250 , 0 , 250 );
    hcal_hits_leq_threshold = fs->make<TH1D>("hcal_hits_leq_threshold" , "hcal_hits_leq_threshold" , total_n_bins , 0 , total_max );
    hcal_hits_et = fs->make<TH1D>("hcal_hits_et" , "hcal_hits_et" , 300 , 0 , 150 );
    hcal_gtr_threshold_sum = fs->make<TH1D>("hcal_gtr_threshold_sum" , "hcal_gtr_threshold_sum" , et_total_n_bins, 0, et_total_max );
    hcal_leq_threshold_sum = fs->make<TH1D>("hcal_leq_threshold_sum" , "hcal_leq_threshold_sum" , et_total_n_bins , 0 , et_total_max );
    hcal_et_sum = fs->make<TH1D>("hcal_et_sum" , "hcal_et_sum" , et_total_n_bins , 0 , et_total_max );

    l1eg_hits = fs->make<TH1D>("l1eg_hits" , "l1eg_hits" , total_n_bins , 0 , total_max );
    l1eg_hits_gtr_threshold = fs->make<TH1D>("l1eg_hits_gtr_threshold" , "l1eg_hits_gtr_threshold" , 250 , 0 , 250 );
    l1eg_hits_leq_threshold = fs->make<TH1D>("l1eg_hits_leq_threshold" , "l1eg_hits_leq_threshold" , total_n_bins , 0 , total_max );
    l1eg_hits_et = fs->make<TH1D>("l1eg_hits_et" , "l1eg_hits_et" , 300 , 0 , 300 );
    l1eg_gtr_threshold_sum = fs->make<TH1D>("l1eg_gtr_threshold_sum" , "l1eg_gtr_threshold_sum" , et_total_n_bins, 0, et_total_max );
    l1eg_leq_threshold_sum = fs->make<TH1D>("l1eg_leq_threshold_sum" , "l1eg_leq_threshold_sum" , et_total_n_bins , 0 , et_total_max );
    l1eg_et_sum = fs->make<TH1D>("l1eg_et_sum" , "l1eg_et_sum" , et_total_n_bins , 0 , et_total_max );

    unc_hits = fs->make<TH1D>("unc_hits" , "unc_hits" , total_n_bins , 0 , total_max );
    unc_hits_gtr_threshold = fs->make<TH1D>("unc_hits_gtr_threshold" , "unc_hits_gtr_threshold" , 250 , 0 , 250 );
    unc_hits_leq_threshold = fs->make<TH1D>("unc_hits_leq_threshold" , "unc_hits_leq_threshold" , total_n_bins , 0 , total_max );
    unc_hits_et = fs->make<TH1D>("unc_hits_et" , "unc_hits_et" , 300 , 0 , 150 );
    unc_gtr_threshold_sum = fs->make<TH1D>("unc_gtr_threshold_sum" , "unc_gtr_threshold_sum" , et_total_n_bins, 0, et_total_max );
    unc_leq_threshold_sum = fs->make<TH1D>("unc_leq_threshold_sum" , "unc_leq_threshold_sum" , et_total_n_bins , 0 , et_total_max );
    unc_et_sum = fs->make<TH1D>("unc_et_sum" , "unc_et_sum" , et_total_n_bins , 0 , et_total_max );



    // Make TTree too
    hit_tree = fs->make<TTree>("hit_tree","hit_tree");
    hit_tree->Branch("run", &treeinfo.run);
    hit_tree->Branch("lumi", &treeinfo.lumi);
    hit_tree->Branch("event", &treeinfo.event);
    hit_tree->Branch("nvtx", &treeinfo.nvtx);
    hit_tree->Branch("nvtx_init", &treeinfo.nvtx_init);
    // N Tower totals
    hit_tree->Branch("i_total_hits",                &treeinfo.i_total_hits);
    hit_tree->Branch("i_total_hits_gtr_threshold",  &treeinfo.i_total_hits_gtr_threshold);
    hit_tree->Branch("i_total_hits_leq_threshold",  &treeinfo.i_total_hits_leq_threshold);
    hit_tree->Branch("i_ecal_hits",                 &treeinfo.i_ecal_hits);
    hit_tree->Branch("i_ecal_hits_er1to3",          &treeinfo.i_ecal_hits_er1to3);
    hit_tree->Branch("i_ecal_hits_er4to6",          &treeinfo.i_ecal_hits_er4to6);
    hit_tree->Branch("i_ecal_hits_er7to9",          &treeinfo.i_ecal_hits_er7to9);
    hit_tree->Branch("i_ecal_hits_er10to12",        &treeinfo.i_ecal_hits_er10to12);
    hit_tree->Branch("i_ecal_hits_er13to15",        &treeinfo.i_ecal_hits_er13to15);
    hit_tree->Branch("i_ecal_hits_er16to18",        &treeinfo.i_ecal_hits_er16to18);
    hit_tree->Branch("i_ecal_hits_gtr_threshold",   &treeinfo.i_ecal_hits_gtr_threshold);
    hit_tree->Branch("i_ecal_hits_leq_threshold",   &treeinfo.i_ecal_hits_leq_threshold);
    hit_tree->Branch("i_hcal_hits",                 &treeinfo.i_hcal_hits);
    hit_tree->Branch("i_hcal_hits_er1to3",          &treeinfo.i_hcal_hits_er1to3);
    hit_tree->Branch("i_hcal_hits_er4to6",          &treeinfo.i_hcal_hits_er4to6);
    hit_tree->Branch("i_hcal_hits_er7to9",          &treeinfo.i_hcal_hits_er7to9);
    hit_tree->Branch("i_hcal_hits_er10to12",        &treeinfo.i_hcal_hits_er10to12);
    hit_tree->Branch("i_hcal_hits_er13to15",        &treeinfo.i_hcal_hits_er13to15);
    hit_tree->Branch("i_hcal_hits_er16to18",        &treeinfo.i_hcal_hits_er16to18);
    hit_tree->Branch("i_hcal_hits_gtr_threshold",   &treeinfo.i_hcal_hits_gtr_threshold);
    hit_tree->Branch("i_hcal_hits_leq_threshold",   &treeinfo.i_hcal_hits_leq_threshold);
    hit_tree->Branch("i_l1eg_hits",                 &treeinfo.i_l1eg_hits);
    hit_tree->Branch("i_l1eg_hits_gtr_threshold",   &treeinfo.i_l1eg_hits_gtr_threshold);
    hit_tree->Branch("i_l1eg_hits_leq_threshold",   &treeinfo.i_l1eg_hits_leq_threshold);
    hit_tree->Branch("i_unc_hits",                  &treeinfo.i_unc_hits);
    hit_tree->Branch("i_unc_hits_gtr_threshold",    &treeinfo.i_unc_hits_gtr_threshold);
    hit_tree->Branch("i_unc_hits_leq_threshold",    &treeinfo.i_unc_hits_leq_threshold);
    // ET totals
    hit_tree->Branch("f_total_hits",                &treeinfo.f_total_hits);
    hit_tree->Branch("f_total_hits_gtr_threshold",  &treeinfo.f_total_hits_gtr_threshold);
    hit_tree->Branch("f_total_hits_leq_threshold",  &treeinfo.f_total_hits_leq_threshold);
    hit_tree->Branch("f_ecal_hits",                 &treeinfo.f_ecal_hits);
    hit_tree->Branch("f_ecal_hits_er1to3",          &treeinfo.f_ecal_hits_er1to3);
    hit_tree->Branch("f_ecal_hits_er4to6",          &treeinfo.f_ecal_hits_er4to6);
    hit_tree->Branch("f_ecal_hits_er7to9",          &treeinfo.f_ecal_hits_er7to9);
    hit_tree->Branch("f_ecal_hits_er10to12",        &treeinfo.f_ecal_hits_er10to12);
    hit_tree->Branch("f_ecal_hits_er13to15",        &treeinfo.f_ecal_hits_er13to15);
    hit_tree->Branch("f_ecal_hits_er16to18",        &treeinfo.f_ecal_hits_er16to18);
    hit_tree->Branch("f_ecal_hits_gtr_threshold",   &treeinfo.f_ecal_hits_gtr_threshold);
    hit_tree->Branch("f_ecal_hits_leq_threshold",   &treeinfo.f_ecal_hits_leq_threshold);
    hit_tree->Branch("f_hcal_hits",                 &treeinfo.f_hcal_hits);
    hit_tree->Branch("f_hcal_hits_er1to3",          &treeinfo.f_hcal_hits_er1to3);
    hit_tree->Branch("f_hcal_hits_er4to6",          &treeinfo.f_hcal_hits_er4to6);
    hit_tree->Branch("f_hcal_hits_er7to9",          &treeinfo.f_hcal_hits_er7to9);
    hit_tree->Branch("f_hcal_hits_er10to12",        &treeinfo.f_hcal_hits_er10to12);
    hit_tree->Branch("f_hcal_hits_er13to15",        &treeinfo.f_hcal_hits_er13to15);
    hit_tree->Branch("f_hcal_hits_er16to18",        &treeinfo.f_hcal_hits_er16to18);
    hit_tree->Branch("f_hcal_hits_gtr_threshold",   &treeinfo.f_hcal_hits_gtr_threshold);
    hit_tree->Branch("f_hcal_hits_leq_threshold",   &treeinfo.f_hcal_hits_leq_threshold);
    hit_tree->Branch("f_l1eg_hits",                 &treeinfo.f_l1eg_hits);
    hit_tree->Branch("f_l1eg_hits_gtr_threshold",   &treeinfo.f_l1eg_hits_gtr_threshold);
    hit_tree->Branch("f_l1eg_hits_leq_threshold",   &treeinfo.f_l1eg_hits_leq_threshold);
    hit_tree->Branch("f_unc_hits",                  &treeinfo.f_unc_hits);
    hit_tree->Branch("f_unc_hits_gtr_threshold",    &treeinfo.f_unc_hits_gtr_threshold);
    hit_tree->Branch("f_unc_hits_leq_threshold",    &treeinfo.f_unc_hits_leq_threshold);

}

void L1TowerAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

    // Reset TTree to zeros
    // N Tower totals
    treeinfo.i_total_hits = 0;
    treeinfo.i_total_hits_gtr_threshold = 0;
    treeinfo.i_total_hits_leq_threshold = 0;
    treeinfo.i_ecal_hits = 0;
    treeinfo.i_ecal_hits_er1to3 = 0;
    treeinfo.i_ecal_hits_er4to6 = 0;
    treeinfo.i_ecal_hits_er7to9 = 0;
    treeinfo.i_ecal_hits_er10to12 = 0;
    treeinfo.i_ecal_hits_er13to15 = 0;
    treeinfo.i_ecal_hits_er16to18 = 0;
    treeinfo.i_ecal_hits_gtr_threshold = 0;
    treeinfo.i_ecal_hits_leq_threshold = 0;
    treeinfo.i_hcal_hits = 0;
    treeinfo.i_hcal_hits_er1to3 = 0;
    treeinfo.i_hcal_hits_er4to6 = 0;
    treeinfo.i_hcal_hits_er7to9 = 0;
    treeinfo.i_hcal_hits_er10to12 = 0;
    treeinfo.i_hcal_hits_er13to15 = 0;
    treeinfo.i_hcal_hits_er16to18 = 0;
    treeinfo.i_hcal_hits_gtr_threshold = 0;
    treeinfo.i_hcal_hits_leq_threshold = 0;
    treeinfo.i_l1eg_hits = 0;
    treeinfo.i_l1eg_hits_gtr_threshold = 0;
    treeinfo.i_l1eg_hits_leq_threshold = 0;
    treeinfo.i_unc_hits = 0;
    treeinfo.i_unc_hits_gtr_threshold = 0;
    treeinfo.i_unc_hits_leq_threshold = 0;
    // ET totals
    treeinfo.f_total_hits = 0;
    treeinfo.f_total_hits_gtr_threshold = 0;
    treeinfo.f_total_hits_leq_threshold = 0;
    treeinfo.f_ecal_hits = 0;
    treeinfo.f_ecal_hits_er1to3 = 0;
    treeinfo.f_ecal_hits_er4to6 = 0;
    treeinfo.f_ecal_hits_er7to9 = 0;
    treeinfo.f_ecal_hits_er10to12 = 0;
    treeinfo.f_ecal_hits_er13to15 = 0;
    treeinfo.f_ecal_hits_er16to18 = 0;
    treeinfo.f_ecal_hits_gtr_threshold = 0;
    treeinfo.f_ecal_hits_leq_threshold = 0;
    treeinfo.f_hcal_hits = 0;
    treeinfo.f_hcal_hits_er1to3 = 0;
    treeinfo.f_hcal_hits_er4to6 = 0;
    treeinfo.f_hcal_hits_er7to9 = 0;
    treeinfo.f_hcal_hits_er10to12 = 0;
    treeinfo.f_hcal_hits_er13to15 = 0;
    treeinfo.f_hcal_hits_er16to18 = 0;
    treeinfo.f_hcal_hits_gtr_threshold = 0;
    treeinfo.f_hcal_hits_leq_threshold = 0;
    treeinfo.f_l1eg_hits = 0;
    treeinfo.f_l1eg_hits_gtr_threshold = 0;
    treeinfo.f_l1eg_hits_leq_threshold = 0;
    treeinfo.f_unc_hits = 0;
    treeinfo.f_unc_hits_gtr_threshold = 0;
    treeinfo.f_unc_hits_leq_threshold = 0;

    treeinfo.run = iEvent.eventAuxiliary().run();
    treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
    treeinfo.event = iEvent.eventAuxiliary().event();

    // Get calo geometry info split by subdetector
    iSetup.get<CaloGeometryRecord>().get(caloGeometry_);
    hbGeometry = caloGeometry_->getSubdetectorGeometry(DetId::Hcal, HcalBarrel);
    iSetup.get<HcalRecNumberingRecord>().get(hbTopology);
    hcTopology_ = hbTopology.product();
    HcalTrigTowerGeometry theTrigTowerGeometry(hcTopology_);
    iEvent.getByToken(crystalClustersToken_,crystalClustersHandle);
    crystalClusters = (*crystalClustersHandle.product());

    NEvents->Fill( 0. );
    // nvtx
    iEvent.getByToken(simVertexToken_,simVertexHandle);
    treeinfo.nvtx = 0;
    for (auto& vert : *simVertexHandle.product())
    {
        //std::cout << i_nvtx << "  eventId().bunchCrossing(): " << vert.eventId().bunchCrossing() << "    parentIndex(): " << vert.parentIndex() << "   processType: " << vert.processType() << std::endl;
        if(vert.eventId().bunchCrossing() != 0) continue;
        treeinfo.nvtx++;
    }
    nvtx->Fill( treeinfo.nvtx );
    
    iEvent.getByToken(trackingVertexInitToken_,trackingVertexInitHandle);
    treeinfo.nvtx_init = 0;
    for (auto& vert : *trackingVertexInitHandle.product())
    {
        //std::cout << i_nvtx << "  eventId().bunchCrossing(): " << vert.eventId().bunchCrossing() << "    parentIndex(): " << vert.parentIndex() << "   processType: " << vert.processType() << std::endl;
        if(vert.eventId().bunchCrossing() != 0) continue;
        treeinfo.nvtx_init++;
    }
    nvtx_init->Fill( treeinfo.nvtx_init );
    
    // Load the ECAL+HCAL tower sums coming from L1EGammaCrystalsEmulatorProducer.cc
    std::vector< SimpleCaloHit > l1CaloTowers;
    
    iEvent.getByToken(l1TowerToken_,l1CaloTowerHandle);
    for (auto& hit : *l1CaloTowerHandle.product())
    {

        SimpleCaloHit l1Hit;
        l1Hit.ecal_tower_et  = hit.ecal_tower_et;
        l1Hit.hcal_tower_et  = hit.hcal_tower_et;
        // Add min ET thresholds for tower ET
        if (l1Hit.ecal_tower_et < EcalTpEtMin) l1Hit.ecal_tower_et = 0.0;
        if (l1Hit.hcal_tower_et < HcalTpEtMin) l1Hit.hcal_tower_et = 0.0;
        l1Hit.total_tower_et  = l1Hit.ecal_tower_et + l1Hit.hcal_tower_et;
        l1Hit.tower_iEta  = hit.tower_iEta;
        l1Hit.tower_iPhi  = hit.tower_iPhi;
        l1Hit.tower_eta  = hit.tower_eta;
        l1Hit.tower_phi  = hit.tower_phi;
        l1CaloTowers.push_back( l1Hit );
        if (debug) printf("Tower iEta %i iPhi %i eta %f phi %f ecal_et %f hcal_et_sum %f total_et %f\n", (int)l1Hit.tower_iEta, (int)l1Hit.tower_iPhi, l1Hit.tower_eta, l1Hit.tower_phi, l1Hit.ecal_tower_et, l1Hit.hcal_tower_et, l1Hit.total_tower_et);
    }


    // Make simple L1objects from the L1EG input collection with marker for 'stale'
    // FIXME could later add quality criteria here to help differentiate likely
    // photons/electrons vs. pions. This could be helpful for L1CaloJets
    std::vector< simpleL1obj > crystalClustersVect;
    for (auto EGammaCand : crystalClusters)
    {
        simpleL1obj l1egObj;
        l1egObj.SetP4(EGammaCand.pt(), EGammaCand.eta(), EGammaCand.phi(), 0.);
        l1egObj.passesStandaloneWP = EGammaCand.standaloneWP();
        l1egObj.passesTrkMatchWP = EGammaCand.looseL1TkMatchWP();
        crystalClustersVect.push_back( l1egObj );
        if (debug) printf("L1EG added from emulator: eta %f phi %f pt %f\n", l1egObj.eta(), l1egObj.phi(), l1egObj.pt());
    }

    // Sorting is unnecessary as we're matching to already built HCAL Jets
    // but it is interesting to know highest pt L1EG, so sort either way
    // Sort clusters so we can always pick highest pt cluster to begin with in our jet clustering
    std::sort(begin(crystalClustersVect), end(crystalClustersVect), [](const simpleL1obj& a,
            simpleL1obj& b){return a.pt() > b.pt();});

    // Match the L1EGs to their associated tower to calculate a TOTAL energy associated
    // with a tower: "total_tower_plus_L1EGs_et".  This can be attributed to multiple
    // L1EGs. Once an L1EG is associated with a tower, mark them as such so they are not
    // double counted for some reason, use "associated_with_tower".
    // This associate will be semi-crude, with barrel geometry, a tower is
    // 0.087 wide, associate them if they are within dEta/dPhi 0.0435.

    for (auto &l1CaloTower : l1CaloTowers)
    {

        l1CaloTower.total_tower_plus_L1EGs_et = l1CaloTower.total_tower_et; // Set to total before finding associated L1EGs

        int j = 0;
        for (auto &l1eg : crystalClustersVect)
        {

            if (l1eg.associated_with_tower) continue;

            // Could be done very cleanly with iEta/iPhi if we had this from the L1EGs...
            float d_eta = l1CaloTower.tower_eta - l1eg.eta();
            float d_phi = reco::deltaPhi( l1CaloTower.tower_phi, l1eg.phi() );

            if ( fabs( d_eta ) > 0.0435 || fabs( d_phi ) > 0.0435 ) continue;

            j++;
            l1CaloTower.total_tower_plus_L1EGs_et += l1eg.pt();
            if (debug) printf(" - %i L1EG associated with tower: dEta %f dPhi %f L1EG pT %f\n", j, d_eta, d_phi, l1eg.pt());

            l1eg.associated_with_tower = true;

        }

        // Update n_totals and ET sums
        if(l1CaloTower.total_tower_plus_L1EGs_et > 0.) 
        {
            treeinfo.i_total_hits++;
            total_hits_et->Fill( l1CaloTower.total_tower_plus_L1EGs_et );
            treeinfo.f_total_hits += l1CaloTower.total_tower_plus_L1EGs_et;
            if(l1CaloTower.total_tower_plus_L1EGs_et > puThreshold)
            {
                treeinfo.i_total_hits_gtr_threshold++;
                treeinfo.f_total_hits_gtr_threshold += l1CaloTower.total_tower_plus_L1EGs_et;
            }
            if(l1CaloTower.total_tower_plus_L1EGs_et <= puThreshold) 
            {
                treeinfo.i_total_hits_leq_threshold++;
                treeinfo.f_total_hits_leq_threshold += l1CaloTower.total_tower_plus_L1EGs_et;
            }
        }

        if(l1CaloTower.ecal_tower_et > 0.) 
        {
            treeinfo.i_ecal_hits++;
            ecal_hits_et->Fill( l1CaloTower.ecal_tower_et );
            treeinfo.f_ecal_hits += l1CaloTower.ecal_tower_et;
            if(l1CaloTower.ecal_tower_et > puThresholdEcal) 
            {
                treeinfo.i_ecal_hits_gtr_threshold++;
                treeinfo.f_ecal_hits_gtr_threshold += l1CaloTower.ecal_tower_et;
            }
            if(l1CaloTower.ecal_tower_et <= puThresholdEcal) 
            {
                treeinfo.i_ecal_hits_leq_threshold++;
                treeinfo.f_ecal_hits_leq_threshold += l1CaloTower.ecal_tower_et;
            }
            
            //if( l1CaloTower.ecal_tower_et <= puThresholdEcal) 
            //    treeinfo.i_ecal_hits_er1to3++;
            //    treeinfo.i_ecal_hits_er4to6++;
            //    treeinfo.i_ecal_hits_er7to9++;
            //    treeinfo.i_ecal_hits_er10to12++;
            //    treeinfo.i_ecal_hits_er13to15++;
            //    treeinfo.i_ecal_hits_er16to18++;
        }

        if(l1CaloTower.hcal_tower_et > 0.) 
        {
            treeinfo.i_hcal_hits++;
            hcal_hits_et->Fill( l1CaloTower.hcal_tower_et );
            treeinfo.f_hcal_hits += l1CaloTower.hcal_tower_et;
            if(l1CaloTower.hcal_tower_et > puThresholdHcal) 
            {
                treeinfo.i_hcal_hits_gtr_threshold++;
                treeinfo.f_hcal_hits_gtr_threshold += l1CaloTower.hcal_tower_et;
            }
            if(l1CaloTower.hcal_tower_et <= puThresholdHcal)
            {
                treeinfo.i_hcal_hits_leq_threshold++;
                treeinfo.f_hcal_hits_leq_threshold += l1CaloTower.hcal_tower_et;
            }
        }

        if(( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et) > 0.) 
        {
            treeinfo.i_l1eg_hits++;
            l1eg_hits_et->Fill( ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et) );
            treeinfo.f_l1eg_hits += ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et);
            if( ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et) > puThresholdL1eg) 
            {
                treeinfo.i_l1eg_hits_gtr_threshold++;
                treeinfo.f_l1eg_hits_gtr_threshold += ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et);
            }
            if( ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et) <= puThresholdL1eg) 
            {
                treeinfo.i_l1eg_hits_leq_threshold++;
                treeinfo.f_l1eg_hits_leq_threshold += ( l1CaloTower.total_tower_plus_L1EGs_et - l1CaloTower.total_tower_et);
            }
        }

        if((l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et) > 0.) 
        {
            treeinfo.i_unc_hits++;
            unc_hits_et->Fill( (l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et) );
            treeinfo.f_unc_hits += (l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et);
            if((l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et) > puThreshold) 
            {
                treeinfo.i_unc_hits_gtr_threshold++;
                treeinfo.f_unc_hits_gtr_threshold += (l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et);
            }
            if((l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et) <= puThreshold)
            {
                treeinfo.i_unc_hits_leq_threshold++;
                treeinfo.f_unc_hits_leq_threshold += (l1CaloTower.ecal_tower_et + l1CaloTower.hcal_tower_et);
            }
        }

    }

    // Fill n_total hists
    total_hits->Fill(               treeinfo.i_total_hits );
    total_hits_gtr_threshold->Fill( treeinfo.i_total_hits_gtr_threshold );
    total_hits_leq_threshold->Fill( treeinfo.i_total_hits_leq_threshold );
    ecal_hits->Fill(                treeinfo.i_ecal_hits );
    ecal_hits_gtr_threshold->Fill(  treeinfo.i_ecal_hits_gtr_threshold );
    ecal_hits_leq_threshold->Fill(  treeinfo.i_ecal_hits_leq_threshold );
    hcal_hits->Fill(                treeinfo.i_hcal_hits );
    hcal_hits_gtr_threshold->Fill(  treeinfo.i_hcal_hits_gtr_threshold );
    hcal_hits_leq_threshold->Fill(  treeinfo.i_hcal_hits_leq_threshold );
    l1eg_hits->Fill(                treeinfo.i_l1eg_hits );
    l1eg_hits_gtr_threshold->Fill(  treeinfo.i_l1eg_hits_gtr_threshold );
    l1eg_hits_leq_threshold->Fill(  treeinfo.i_l1eg_hits_leq_threshold );
    unc_hits->Fill(                 treeinfo.i_unc_hits );
    unc_hits_gtr_threshold->Fill(   treeinfo.i_unc_hits_gtr_threshold );
    unc_hits_leq_threshold->Fill(   treeinfo.i_unc_hits_leq_threshold );

    // Fill ET sums
    total_et_sum->Fill(               treeinfo.f_total_hits );
    total_gtr_threshold_sum->Fill( treeinfo.f_total_hits_gtr_threshold );
    total_leq_threshold_sum->Fill( treeinfo.f_total_hits_leq_threshold );
    ecal_et_sum->Fill(                treeinfo.f_ecal_hits );
    ecal_gtr_threshold_sum->Fill(  treeinfo.f_ecal_hits_gtr_threshold );
    ecal_leq_threshold_sum->Fill(  treeinfo.f_ecal_hits_leq_threshold );
    hcal_et_sum->Fill(                treeinfo.f_hcal_hits );
    hcal_gtr_threshold_sum->Fill(  treeinfo.f_hcal_hits_gtr_threshold );
    hcal_leq_threshold_sum->Fill(  treeinfo.f_hcal_hits_leq_threshold );
    l1eg_et_sum->Fill(                treeinfo.f_l1eg_hits );
    l1eg_gtr_threshold_sum->Fill(  treeinfo.f_l1eg_hits_gtr_threshold );
    l1eg_leq_threshold_sum->Fill(  treeinfo.f_l1eg_hits_leq_threshold );
    unc_et_sum->Fill(                 treeinfo.f_unc_hits );
    unc_gtr_threshold_sum->Fill(   treeinfo.f_unc_hits_gtr_threshold );
    unc_leq_threshold_sum->Fill(   treeinfo.f_unc_hits_leq_threshold );

    hit_tree->Fill();
}



DEFINE_FWK_MODULE(L1TowerAnalyzer);
