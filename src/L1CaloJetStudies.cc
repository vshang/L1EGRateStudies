// -*- C++ -*-
//
// Package:     L1CaloJetStudies
// Class:        L1CaloJetStudies
// 
/**\class L1CaloJetStudies L1CaloJetStudies.cc L1Trigger/L1EGRateStudies/src/L1CaloJetStudies.cc

 Description: [one line class summary]

 Implementation:
      [Notes on implementation]
*/
//
// Original Author:  Tyler Ruggles
//            Created:  Sept 2, 2018
// $Id$
//
//


// system include files
#include <memory>
#include <array>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TTree.h"
#include "TMath.h"

// Gen
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

#include "DataFormats/Phase2L1CaloTrig/interface/L1CaloJet.h"
#include "DataFormats/Phase2L1CaloTrig/src/classes.h"

#include "FastSimulation/BaseParticlePropagator/interface/BaseParticlePropagator.h"

#include "FastSimulation/Particle/interface/RawParticle.h"

// Stage2
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"


//
// class declaration
//
class L1CaloJetStudies : public edm::EDAnalyzer {
    typedef BXVector<l1t::Jet> JetBxCollection;
    typedef std::vector<l1t::Jet> JetCollection;
    typedef std::vector<reco::GenJet> GenJetCollection;
    typedef BXVector<l1t::Tau> TauBxCollection;
    typedef std::vector<l1t::Tau> TauCollection;

    public:
        explicit L1CaloJetStudies(const edm::ParameterSet&);
        ~L1CaloJetStudies();

        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


    private:
        virtual void beginJob() ;
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob() ;

        virtual void beginRun(edm::Run const&, edm::EventSetup const&);

        // -- user functions
        void integrateDown(TH1F *);
        void fill_tree(const l1slhc::L1CaloJet& caloJet);
        void fill_tree_null();
        
        // ----------member data ---------------------------
        bool doRate;
        bool debug;
        
        double genMatchDeltaRcut;
        double genMatchRelPtcut;
        

        edm::EDGetTokenT<l1slhc::L1CaloJetsCollection> caloJetsToken_;
        l1slhc::L1CaloJetsCollection caloJets;
        edm::Handle<l1slhc::L1CaloJetsCollection> caloJetsHandle;        

        //edm::EDGetTokenT<reco::GenParticleCollection> genCollectionToken_;
        //reco::GenParticleCollection genParticles;
        //edm::Handle<reco::GenParticleCollection> genParticleHandle;

        edm::EDGetTokenT<std::vector<reco::GenJet>> genJetsToken_;
        std::vector<reco::GenJet> genJets;
        edm::Handle<std::vector<reco::GenJet>> genJetsHandle;

        edm::EDGetTokenT<std::vector<reco::GenJet>> genHadronicTausToken_;
        edm::Handle<std::vector<reco::GenJet>> genHTaus;

        // Stage2 Digis
        edm::EDGetTokenT<BXVector<l1t::Jet> > stage2JetToken_;
        edm::Handle<BXVector<l1t::Jet>> stage2JetHandle;
        edm::EDGetTokenT<BXVector<l1t::Tau> > stage2TauToken_;
        edm::Handle<BXVector<l1t::Tau>> stage2TauHandle;

        edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;
        edm::Handle<std::vector<PileupSummaryInfo>> puInfo;

        // Efficiency hists
        TH1F * nEvents;
        TH1F * eff_all_denom_pt;
        TH1F * eff_all_num_pt;
        TH1F * eff_all_num_stage2jet_pt;
        TH1F * eff_all_denom_eta;
        TH1F * eff_all_num_eta;
        TH1F * eff_all_num_stage2jet_eta;

        TH1F * eff_barrel_denom_pt;
        TH1F * eff_barrel_num_pt;
        TH1F * eff_barrel_num_stage2jet_pt;
        TH1F * eff_barrel_denom_eta;
        TH1F * eff_barrel_num_eta;
        TH1F * eff_barrel_num_stage2jet_eta;

        TH1F * nTruePUHist;
        TH1F * totalET;
        TH1F * nTT;
        TH1F * phase2_rate_all_hist;
        TH1F * stage2_rate_all_hist;
        TH1F * phase2_rate_barrel_hist;
        TH1F * stage2_rate_barrel_hist;
                
        // Crystal pt stuff
        TTree * tree;
        struct {
            double run;
            double lumi;
            double event;
            float nTruePU;
            float iPhi_ET_rings_ecal;
            float iPhi_ET_rings_l1eg;
            float iPhi_ET_rings_hcal;
            float iPhi_ET_rings_total;
            float iPhi_nTowers_rings_ecal;
            float iPhi_nTowers_rings_l1eg;
            float iPhi_nTowers_rings_hcal;
            float iPhi_nTowers_rings_total;
            float total_et;
            float total_nTowers;
            float ecal_pt;
            float ecal_eta;
            float ecal_phi;
            float ecal_mass;
            float ecal_energy;
            float ecal_L1EG_jet_pt;
            float ecal_L1EG_jet_eta;
            float ecal_L1EG_jet_phi;
            float ecal_L1EG_jet_mass;
            float ecal_L1EG_jet_energy;
            float hcal_pt;
            float hcal_calibration;
            float hcal_pt_calibration;
            float hcal_eta;
            float hcal_phi;
            float hcal_mass;
            float hcal_energy;
            float jet_pt;
            float jet_pt_calibration;
            float transition_calibration;
            float jet_eta;
            float jet_phi;
            float jet_mass;
            float jet_energy;
            float ecal_PU_pt;
            float ecal_L1EG_jet_PU_pt;
            float hcal_PU_pt;
            float ecal_PU_cor_pt;
            float ecal_L1EG_jet_PU_cor_pt;
            float hcal_PU_cor_pt;
            float jet_PU_cor_pt;
            float hovere;
            float hcal_3x3;
            float hcal_5x5;
            float hcal_7x7;
            float hcal_2x2_1;
            float hcal_2x2_2;
            float hcal_2x2_3;
            float hcal_2x2_4;
            float seed_pt;
            float seed_iEta;
            float seed_iPhi;
            float seed_eta;
            float seed_phi;
            float seed_energy;
            float hcal_nHits;
            float ecal_leading_pt;
            float ecal_leading_eta;
            float ecal_leading_phi;
            float ecal_leading_energy;
            float ecal_dR0p05;
            float ecal_dR0p075;
            float ecal_dR0p1;
            float ecal_dR0p125;
            float ecal_dR0p15;
            float ecal_dR0p2;
            float ecal_dR0p3;
            float ecal_dR0p4;
            float ecal_dR0p1_leading;
            float ecal_nL1EGs;
            float ecal_nL1EGs_standalone;
            float ecal_nL1EGs_trkMatch;
            float deltaR_ecal_vs_jet;
            float deltaR_hcal_vs_jet;
            float deltaR_L1EGjet_vs_jet;
            float deltaR_hcal_vs_seed;
            float deltaR_ecal_vs_hcal;
            float deltaR_ecal_vs_seed;
            float deltaR_ecal_lead_vs_jet;
            float deltaR_ecal_lead_vs_ecal;
            float deltaR;
            float deltaPhi;
            float deltaEta;
            float genJet_pt;
            float genJet_eta;
            float genJet_phi;
            float genJet_energy;
            float genJet_mass;
            float genJet_charge;
            float genTau_pt;
            float genTau_eta;
            float genTau_phi;
            float genTau_energy;
            float genTau_mass;
            float genTau_charge;
            float stage2jet_pt;
            float stage2jet_eta;
            float stage2jet_phi;
            float stage2jet_energy;
            float stage2jet_mass;
            float stage2jet_charge;
            float stage2jet_puEt;
            float stage2jet_deltaRGen;
            float stage2tau_pt;
            float stage2tau_eta;
            float stage2tau_phi;
            float stage2tau_energy;
            float stage2tau_mass;
            float stage2tau_charge;
            float stage2tau_hasEM;
            float stage2tau_isMerged;
            float stage2tau_isoEt;
            float stage2tau_nTT;
            float stage2tau_rawEt;
            float stage2tau_isoBit;
            float stage2tau_deltaRGen;
        } treeinfo;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
L1CaloJetStudies::L1CaloJetStudies(const edm::ParameterSet& iConfig) :
    doRate(iConfig.getUntrackedParameter<bool>("doRate", false)),
    debug(iConfig.getUntrackedParameter<bool>("debug", false)),
    genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.3)),
    genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
    caloJetsToken_(consumes<l1slhc::L1CaloJetsCollection>(iConfig.getParameter<edm::InputTag>("L1CaloJetsInputTag"))),
    genJetsToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genJets"))),
    genHadronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genHadronicTauSrc"))),
    stage2JetToken_(consumes<BXVector<l1t::Jet>>(iConfig.getParameter<edm::InputTag>("Stage2JetTag"))),
    stage2TauToken_(consumes<BXVector<l1t::Tau>>(iConfig.getParameter<edm::InputTag>("Stage2TauTag"))),
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc")))
{

    edm::Service<TFileService> fs;

    nEvents = fs->make<TH1F>("nEvents", "nEvents", 1, 0.5, 1.5);
    eff_all_denom_pt = fs->make<TH1F>("eff_all_denom_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_all_num_pt = fs->make<TH1F>("eff_all_num_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_all_num_stage2jet_pt = fs->make<TH1F>("eff_all_num_stage2jet_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_all_denom_eta = fs->make<TH1F>("eff_all_denom_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);
    eff_all_num_eta = fs->make<TH1F>("eff_all_num_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);
    eff_all_num_stage2jet_eta = fs->make<TH1F>("eff_all_num_stage2jet_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);

    eff_barrel_denom_pt = fs->make<TH1F>("eff_barrel_denom_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_num_pt = fs->make<TH1F>("eff_barrel_num_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_num_stage2jet_pt = fs->make<TH1F>("eff_barrel_num_stage2jet_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_denom_eta = fs->make<TH1F>("eff_barrel_denom_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);
    eff_barrel_num_eta = fs->make<TH1F>("eff_barrel_num_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);
    eff_barrel_num_stage2jet_eta = fs->make<TH1F>("eff_barrel_num_stage2jet_eta", "Gen. eta;Gen. #eta; Counts", 70, -3.5, 3.5);

    nTruePUHist = fs->make<TH1F>("nTruePUHist", "nTrue PU", 250, 0, 250);
    totalET = fs->make<TH1F>("totalET", "Total ET", 500, 0, 5000);
    nTT = fs->make<TH1F>("nTT", "nTT", 500, 0, 5000);
    phase2_rate_all_hist = fs->make<TH1F>("phase2_rate_all_hist", "phase2_rate_all_hist", 500, 0, 500);
    stage2_rate_all_hist = fs->make<TH1F>("stage2_rate_all_hist", "stage2_rate_all_hist", 500, 0, 500);
    phase2_rate_barrel_hist = fs->make<TH1F>("phase2_rate_barrel_hist", "phase2_rate_barrel_hist", 500, 0, 500);
    stage2_rate_barrel_hist = fs->make<TH1F>("stage2_rate_barrel_hist", "stage2_rate_barrel_hist", 500, 0, 500);

    tree = fs->make<TTree>("tree", "CaloJet values");
    tree->Branch("run", &treeinfo.run);
    tree->Branch("lumi", &treeinfo.lumi);
    tree->Branch("event", &treeinfo.event);
    tree->Branch("nTruePU", &treeinfo.nTruePU);
    tree->Branch("ecal_PU_pt", &treeinfo.ecal_PU_pt);
    tree->Branch("ecal_L1EG_jet_PU_pt", &treeinfo.ecal_L1EG_jet_PU_pt);
    tree->Branch("hcal_PU_pt", &treeinfo.hcal_PU_pt);
    tree->Branch("ecal_PU_cor_pt", &treeinfo.ecal_PU_cor_pt);
    tree->Branch("ecal_L1EG_jet_PU_cor_pt", &treeinfo.ecal_L1EG_jet_PU_cor_pt);
    tree->Branch("hcal_PU_cor_pt", &treeinfo.hcal_PU_cor_pt);
    tree->Branch("jet_PU_cor_pt", &treeinfo.jet_PU_cor_pt);
    tree->Branch("iPhi_ET_rings_ecal", &treeinfo.iPhi_ET_rings_ecal);
    tree->Branch("iPhi_ET_rings_l1eg", &treeinfo.iPhi_ET_rings_l1eg);
    tree->Branch("iPhi_ET_rings_hcal", &treeinfo.iPhi_ET_rings_hcal);
    tree->Branch("iPhi_ET_rings_total", &treeinfo.iPhi_ET_rings_total);
    tree->Branch("iPhi_nTowers_rings_ecal", &treeinfo.iPhi_nTowers_rings_ecal);
    tree->Branch("iPhi_nTowers_rings_l1eg", &treeinfo.iPhi_nTowers_rings_l1eg);
    tree->Branch("iPhi_nTowers_rings_hcal", &treeinfo.iPhi_nTowers_rings_hcal);
    tree->Branch("iPhi_nTowers_rings_total", &treeinfo.iPhi_nTowers_rings_total);
    tree->Branch("total_et", &treeinfo.total_et);
    tree->Branch("total_nTowers", &treeinfo.total_nTowers);
    tree->Branch("ecal_pt", &treeinfo.ecal_pt);
    tree->Branch("ecal_eta", &treeinfo.ecal_eta);
    tree->Branch("ecal_phi", &treeinfo.ecal_phi);
    tree->Branch("ecal_mass", &treeinfo.ecal_mass);
    tree->Branch("ecal_energy", &treeinfo.ecal_energy);
    tree->Branch("ecal_L1EG_jet_pt", &treeinfo.ecal_L1EG_jet_pt);
    tree->Branch("ecal_L1EG_jet_eta", &treeinfo.ecal_L1EG_jet_eta);
    tree->Branch("ecal_L1EG_jet_phi", &treeinfo.ecal_L1EG_jet_phi);
    tree->Branch("ecal_L1EG_jet_mass", &treeinfo.ecal_L1EG_jet_mass);
    tree->Branch("ecal_L1EG_jet_energy", &treeinfo.ecal_L1EG_jet_energy);
    tree->Branch("hcal_pt", &treeinfo.hcal_pt);
    tree->Branch("hcal_calibration", &treeinfo.hcal_calibration);
    tree->Branch("hcal_pt_calibration", &treeinfo.hcal_pt_calibration);
    tree->Branch("hcal_eta", &treeinfo.hcal_eta);
    tree->Branch("hcal_phi", &treeinfo.hcal_phi);
    tree->Branch("hcal_mass", &treeinfo.hcal_mass);
    tree->Branch("hcal_energy", &treeinfo.hcal_energy);
    tree->Branch("jet_pt", &treeinfo.jet_pt);
    tree->Branch("jet_pt_calibration", &treeinfo.jet_pt_calibration);
    tree->Branch("transition_calibration", &treeinfo.transition_calibration);
    tree->Branch("jet_eta", &treeinfo.jet_eta);
    tree->Branch("jet_phi", &treeinfo.jet_phi);
    tree->Branch("jet_mass", &treeinfo.jet_mass);
    tree->Branch("jet_energy", &treeinfo.jet_energy);
    tree->Branch("hovere", &treeinfo.hovere);
    tree->Branch("hcal_3x3", &treeinfo.hcal_3x3);
    tree->Branch("hcal_5x5", &treeinfo.hcal_5x5);
    tree->Branch("hcal_7x7", &treeinfo.hcal_7x7);
    tree->Branch("hcal_2x2_1", &treeinfo.hcal_2x2_1);
    tree->Branch("hcal_2x2_2", &treeinfo.hcal_2x2_2);
    tree->Branch("hcal_2x2_3", &treeinfo.hcal_2x2_3);
    tree->Branch("hcal_2x2_4", &treeinfo.hcal_2x2_4);
    tree->Branch("seed_pt", &treeinfo.seed_pt);
    tree->Branch("seed_iEta", &treeinfo.seed_iEta);
    tree->Branch("seed_iPhi", &treeinfo.seed_iPhi);
    tree->Branch("seed_eta", &treeinfo.seed_eta);
    tree->Branch("seed_phi", &treeinfo.seed_phi);
    tree->Branch("seed_energy", &treeinfo.seed_energy);
    tree->Branch("hcal_nHits", &treeinfo.hcal_nHits);
    tree->Branch("ecal_leading_pt", &treeinfo.ecal_leading_pt);
    tree->Branch("ecal_leading_eta", &treeinfo.ecal_leading_eta);
    tree->Branch("ecal_leading_phi", &treeinfo.ecal_leading_phi);
    tree->Branch("ecal_leading_energy", &treeinfo.ecal_leading_energy);
    tree->Branch("ecal_dR0p05", &treeinfo.ecal_dR0p05);
    tree->Branch("ecal_dR0p075", &treeinfo.ecal_dR0p075);
    tree->Branch("ecal_dR0p1", &treeinfo.ecal_dR0p1);
    tree->Branch("ecal_dR0p125", &treeinfo.ecal_dR0p125);
    tree->Branch("ecal_dR0p15", &treeinfo.ecal_dR0p15);
    tree->Branch("ecal_dR0p2", &treeinfo.ecal_dR0p2);
    tree->Branch("ecal_dR0p3", &treeinfo.ecal_dR0p3);
    tree->Branch("ecal_dR0p4", &treeinfo.ecal_dR0p4);
    tree->Branch("ecal_dR0p1_leading", &treeinfo.ecal_dR0p1_leading);
    tree->Branch("ecal_nL1EGs", &treeinfo.ecal_nL1EGs);
    tree->Branch("ecal_nL1EGs_standalone", &treeinfo.ecal_nL1EGs_standalone);
    tree->Branch("ecal_nL1EGs_trkMatch", &treeinfo.ecal_nL1EGs_trkMatch);
    tree->Branch("deltaR_ecal_vs_jet", &treeinfo.deltaR_ecal_vs_jet);
    tree->Branch("deltaR_hcal_vs_jet", &treeinfo.deltaR_hcal_vs_jet);
    tree->Branch("deltaR_L1EGjet_vs_jet", &treeinfo.deltaR_L1EGjet_vs_jet);
    tree->Branch("deltaR_hcal_vs_seed", &treeinfo.deltaR_hcal_vs_seed);
    tree->Branch("deltaR_ecal_vs_hcal", &treeinfo.deltaR_ecal_vs_hcal);
    tree->Branch("deltaR_ecal_vs_seed", &treeinfo.deltaR_ecal_vs_seed);
    tree->Branch("deltaR_ecal_lead_vs_jet", &treeinfo.deltaR_ecal_lead_vs_jet);
    tree->Branch("deltaR_ecal_lead_vs_ecal", &treeinfo.deltaR_ecal_lead_vs_ecal);
    // Gen
    tree->Branch("deltaR_gen", &treeinfo.deltaR);
    tree->Branch("deltaPhi_gen", &treeinfo.deltaPhi);
    tree->Branch("deltaEta_gen", &treeinfo.deltaEta);
    tree->Branch("genJet_pt", &treeinfo.genJet_pt);
    tree->Branch("genJet_eta", &treeinfo.genJet_eta);
    tree->Branch("genJet_phi", &treeinfo.genJet_phi);
    tree->Branch("genJet_energy", &treeinfo.genJet_energy);
    tree->Branch("genJet_mass", &treeinfo.genJet_mass);
    tree->Branch("genJet_charge", &treeinfo.genJet_charge);
    tree->Branch("genTau_pt", &treeinfo.genTau_pt);
    tree->Branch("genTau_eta", &treeinfo.genTau_eta);
    tree->Branch("genTau_phi", &treeinfo.genTau_phi);
    tree->Branch("genTau_energy", &treeinfo.genTau_energy);
    tree->Branch("genTau_mass", &treeinfo.genTau_mass);
    tree->Branch("genTau_charge", &treeinfo.genTau_charge);
    // Stage-2
    tree->Branch("stage2jet_pt", &treeinfo.stage2jet_pt);
    tree->Branch("stage2jet_eta", &treeinfo.stage2jet_eta);
    tree->Branch("stage2jet_phi", &treeinfo.stage2jet_phi);
    tree->Branch("stage2jet_energy", &treeinfo.stage2jet_energy);
    tree->Branch("stage2jet_mass", &treeinfo.stage2jet_mass);
    tree->Branch("stage2jet_charge", &treeinfo.stage2jet_charge);
    tree->Branch("stage2jet_puEt", &treeinfo.stage2jet_puEt);
    tree->Branch("stage2jet_deltaRGen", &treeinfo.stage2jet_deltaRGen);
    tree->Branch("stage2tau_pt", &treeinfo.stage2tau_pt);
    tree->Branch("stage2tau_eta", &treeinfo.stage2tau_eta);
    tree->Branch("stage2tau_phi", &treeinfo.stage2tau_phi);
    tree->Branch("stage2tau_energy", &treeinfo.stage2tau_energy);
    tree->Branch("stage2tau_mass", &treeinfo.stage2tau_mass);
    tree->Branch("stage2tau_charge", &treeinfo.stage2tau_charge);
    tree->Branch("stage2tau_hasEM", &treeinfo.stage2tau_hasEM);
    tree->Branch("stage2tau_isMerged", &treeinfo.stage2tau_isMerged);
    tree->Branch("stage2tau_isoEt", &treeinfo.stage2tau_isoEt);
    tree->Branch("stage2tau_nTT", &treeinfo.stage2tau_nTT);
    tree->Branch("stage2tau_rawEt", &treeinfo.stage2tau_rawEt);
    tree->Branch("stage2tau_isoBit", &treeinfo.stage2tau_isoBit);
    tree->Branch("stage2tau_deltaRGen", &treeinfo.stage2tau_deltaRGen);
}


L1CaloJetStudies::~L1CaloJetStudies()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1CaloJetStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    nEvents->Fill( 1.0 );

    // Record the standards
    treeinfo.run = iEvent.eventAuxiliary().run();
    treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
    treeinfo.event = iEvent.eventAuxiliary().event();

    iEvent.getByToken(puToken_, puInfo);
    treeinfo.nTruePU = -99;
    if (puInfo.isValid()) 
    {
        if (puInfo->size() > 0) 
        {
            if (puInfo->begin()->getBunchCrossing() == 0) 
            {
                treeinfo.nTruePU = puInfo->begin()->getTrueNumInteractions();
            }
        }
    }
    nTruePUHist->Fill( treeinfo.nTruePU );

    // Get all collections for later in GenJet loop
    // Get Phase-II CaloJet collection
    iEvent.getByToken(caloJetsToken_,caloJetsHandle);
    caloJets = (*caloJetsHandle.product());
    iEvent.getByToken(stage2JetToken_, stage2JetHandle);
    JetBxCollection stage2JetCollection;
    stage2JetCollection = *stage2JetHandle.product();
    iEvent.getByToken(stage2TauToken_, stage2TauHandle);
    TauBxCollection stage2TauCollection;
    stage2TauCollection = *stage2TauHandle.product();
    iEvent.getByToken(genHadronicTausToken_, genHTaus);
    GenJetCollection genHTauCollection = *genHTaus.product();

    // Sort collections once
    // Stage-2 Jets
    JetCollection stage2Jets;
    if ( stage2JetHandle.isValid() )
    {
        // Make stage2 sortable
        for (auto& s2_jet : stage2JetCollection)
        {
            stage2Jets.push_back( s2_jet );
        }
        std::sort(begin(stage2Jets), end(stage2Jets), [](l1t::Jet& a, l1t::Jet& b){return a.pt() > b.pt();});
    }

    // Stage-2 Taus 
    TauCollection stage2Taus;
    if ( stage2TauHandle.isValid() )
    {
        // Make stage2 sortable
        for (auto& s2_tau : stage2TauCollection)
        {
            stage2Taus.push_back( s2_tau );
        }
        std::sort(begin(stage2Taus), end(stage2Taus), [](l1t::Tau& a, l1t::Tau& b){return a.pt() > b.pt();});
    }

    // Gen Tau_h
    if ( genHTaus.isValid() )
    {
        std::sort(begin(genHTauCollection), end(genHTauCollection), [](reco::GenJet& a, reco::GenJet& b){return a.pt() > b.pt();});
    }


    std::cout << " -- Input L1CaloTaus: " << caloJets.size() << std::endl;

    // Sort caloJets so we can always pick highest pt caloJet matching cuts
    std::sort(begin(caloJets), end(caloJets), [](const l1slhc::L1CaloJet& a, const l1slhc::L1CaloJet& b){return a.pt() > b.pt();});


    /*******************************************************
    * If using a min-biase sample and doRate selected, record the
    * Phase-2 and Stage-2 CaloJet objects only
    ************************************************************/
    if (doRate)
    {
        bool stage2_all_filled = false;
        bool phase2_all_filled = false;
        bool stage2_barrel_filled = false;
        bool phase2_barrel_filled = false;
        // Stage-2 Jets
        if ( stage2JetHandle.isValid() )
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                if ( fabs(s2_jet.eta()) < 3.0 && !stage2_all_filled )
                {
                    stage2_rate_all_hist->Fill( s2_jet.pt() );
                    stage2_all_filled = true;
                }
                if ( fabs(s2_jet.eta()) < 1.5 && !stage2_barrel_filled )
                {
                    stage2_rate_barrel_hist->Fill( s2_jet.pt() );
                    stage2_barrel_filled = true;
                }
                if (s2_jet.pt() < 50) continue;
                treeinfo.stage2jet_pt = s2_jet.pt();
                treeinfo.stage2jet_eta = s2_jet.eta();
                treeinfo.stage2jet_phi = s2_jet.phi();
                treeinfo.stage2jet_energy = s2_jet.energy();
                treeinfo.stage2jet_mass = s2_jet.mass();
                treeinfo.stage2jet_charge = s2_jet.charge();
                treeinfo.stage2jet_puEt = s2_jet.puEt();
                treeinfo.stage2jet_deltaRGen = -9;
                // Fill Phase-2 CaloJet with dummy values
                fill_tree_null();
            }

        }
        if ( caloJets.size() > 0 )
        {
            for(const auto& caloJet : caloJets)
            {
                if ( fabs( caloJet.GetExperimentalParam("jet_eta") ) < 3.0 && !phase2_all_filled )
                {
                    phase2_rate_all_hist->Fill( caloJet.GetExperimentalParam("jet_pt") );
                    phase2_all_filled = true;
                }
                if ( fabs( caloJet.GetExperimentalParam("jet_eta") ) < 1.5 && !phase2_barrel_filled )
                {
                    phase2_rate_barrel_hist->Fill( caloJet.GetExperimentalParam("jet_pt") );
                    phase2_barrel_filled = true;
                }
                if (caloJet.pt() < 50) continue;
                // Set Stage-2 to dummy values
                treeinfo.stage2jet_pt = -9; 
                treeinfo.stage2jet_eta = -9;
                treeinfo.stage2jet_phi = -9;
                treeinfo.stage2jet_energy = -9;
                treeinfo.stage2jet_mass = -9;
                treeinfo.stage2jet_charge = -9;
                treeinfo.stage2jet_puEt = -9;
                treeinfo.stage2jet_deltaRGen = -9;
                fill_tree(caloJet);
            } // end Calo Jets loop
        } // have CaloJets
        return;
    } // end doRate




        
    // Loop over all gen jets with pt > 10 GeV and match them to Phase-II CaloJets
    // Generator info (truth)
    iEvent.getByToken(genJetsToken_,genJetsHandle);
    genJets = *genJetsHandle.product();

    // Sort gen jets
    std::sort(begin(genJets), end(genJets), [](const reco::GenJet& a, const reco::GenJet& b){return a.pt() > b.pt();});

    int cnt = 0;
    for (auto& genJet : genJets ) 
    {
        // Skip lowest pT Jets
        if (genJet.pt() < 10) break;  // no need for continue as we sorted by pT so we're done
        // HGCal detector stops at abs(eta)=3.0, keep gen jets up to 3.5
        if ( fabs(genJet.eta())  > 3.5) continue;
        ++cnt;
        //std::cout << cnt << " Gen pT: " << genJet.pt() << std::endl;

        //if ( fabs(genJet.pdgId()) != 11) {
        //      std::cout << "Event without electron as best gen.  Gen pdgId was: " << genJet.pdgId() <<std::endl;
        //      return;
        //}
    
        // Fill basic denominator efficiencies
        eff_all_denom_pt->Fill(genJet.pt());
        if (genJet.pt() > 20) eff_all_denom_eta->Fill(genJet.eta());
        if ( fabs(genJet.eta()) < 1.5 )
        {
            eff_barrel_denom_pt->Fill(genJet.pt());
            if (genJet.pt() > 20) eff_barrel_denom_eta->Fill(genJet.eta());
        }
    
        reco::Candidate::PolarLorentzVector genJetP4(genJet.pt(), genJet.eta(), genJet.phi(), genJet.mass() );
    
    
        // Stage-2 Jets
        bool jet_matched = false;
        if ( stage2JetHandle.isValid() )
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                if ( reco::deltaR( s2_jet.p4(), genJetP4 ) < genMatchDeltaRcut )
                {
                    treeinfo.stage2jet_pt = s2_jet.pt();
                    treeinfo.stage2jet_eta = s2_jet.eta();
                    treeinfo.stage2jet_phi = s2_jet.phi();
                    treeinfo.stage2jet_energy = s2_jet.energy();
                    treeinfo.stage2jet_mass = s2_jet.mass();
                    treeinfo.stage2jet_charge = s2_jet.charge();
                    treeinfo.stage2jet_puEt = s2_jet.puEt();
                    treeinfo.stage2jet_deltaRGen = reco::deltaR( s2_jet.p4(), genJetP4 );

                    // Fill basic numerator efficiencies
                    eff_all_num_stage2jet_pt->Fill(genJet.pt());
                    if (genJet.pt() > 20) eff_all_num_stage2jet_eta->Fill(genJet.eta());
                    if ( fabs(genJet.eta()) < 1.5 )
                    {
                        eff_barrel_num_stage2jet_pt->Fill(genJet.pt());
                        if (genJet.pt() > 20) eff_barrel_num_stage2jet_eta->Fill(genJet.eta());
                    }

                    jet_matched = true;
                    break;
                }
            }

        }
        if (!jet_matched) // No Stage-2 Jets
        {
            treeinfo.stage2jet_pt = -9.;
            treeinfo.stage2jet_eta = -9.;
            treeinfo.stage2jet_phi = -9.;
            treeinfo.stage2jet_energy = -9.;
            treeinfo.stage2jet_mass = -9.;
            treeinfo.stage2jet_charge = -9.;
            treeinfo.stage2jet_deltaRGen = -9.;
        } 
    
    
    
    
        // Stage-2 Taus 
        bool tau_matched = false;
        if ( stage2TauHandle.isValid() )
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_tau : stage2Taus)
            {
                if ( reco::deltaR( s2_tau.p4(), genJetP4 ) < genMatchDeltaRcut )
                {
                    treeinfo.stage2tau_pt = s2_tau.pt();
                    treeinfo.stage2tau_eta = s2_tau.eta();
                    treeinfo.stage2tau_phi = s2_tau.phi();
                    treeinfo.stage2tau_energy = s2_tau.energy();
                    treeinfo.stage2tau_mass = s2_tau.mass();
                    treeinfo.stage2tau_charge = s2_tau.charge();
                    treeinfo.stage2tau_hasEM = s2_tau.hasEM();
                    treeinfo.stage2tau_isMerged = s2_tau.isMerged();
                    treeinfo.stage2tau_isoEt = s2_tau.isoEt();
                    treeinfo.stage2tau_nTT = s2_tau.nTT();
                    treeinfo.stage2tau_rawEt = s2_tau.rawEt();
                    treeinfo.stage2tau_isoBit = s2_tau.hwIso();
                    treeinfo.stage2tau_deltaRGen = reco::deltaR( s2_tau.p4(), genJetP4 );
                    tau_matched = true;
                    break;
                }
            }

        }
        if (!tau_matched) // No Stage-2 Taus
        {
            treeinfo.stage2tau_pt = -9.;
            treeinfo.stage2tau_eta = -9.;
            treeinfo.stage2tau_phi = -9.;
            treeinfo.stage2tau_energy = -9.;
            treeinfo.stage2tau_mass = -9.;
            treeinfo.stage2tau_charge = -9.;
            treeinfo.stage2tau_hasEM = -9.;
            treeinfo.stage2tau_isMerged = -9.;
            treeinfo.stage2tau_isoEt = -9.;
            treeinfo.stage2tau_nTT = -9.;
            treeinfo.stage2tau_rawEt = -9.;
            treeinfo.stage2tau_isoBit = -9.;
            treeinfo.stage2tau_deltaRGen = -9.;
        } 
    
    
        // FIXME Not sure how this will work with caloJets
        //
        //// Get the particle position upon entering ECal
        //RawParticle particle(genJet.p4());
        //particle.setVertex(genJet.vertex().x(), genJet.vertex().y(), genJet.vertex().z(), 0.);
        ////particle.setID(genJet.pdgId());
        //// Skip setID requires some external libraries working well that
        //// define HepPDT::ParticleID
        //// in the end, setID sets the mass and charge of our particle.
        //// Try doing this by hand for the moment
    
        //// Electrons... mainly
        //particle.setMass(.511); // MeV
        //int pdgId = genJet.pdgId();
        //if (pdgId > 0) {
        //    particle.setCharge( -1.0 ); }
        //if (pdgId < 0) {
        //    particle.setCharge( 1.0 ); }
    
        //// Charged pions
        //if (pdgId == -211 || pdgId == 211) {
        //        particle.setCharge( genJet.charge() );
        //        particle.setMass(139.6); // MeV
        //}
    
        //BaseParticlePropagator prop(particle, 0., 0., 4.);
        //BaseParticlePropagator start(prop);
        //prop.propagateToEcalEntrance();
        //if(prop.getSuccess()!=0)
        //{
        //    genJet = reco::Candidate::PolarLorentzVector(prop.E()*sin(prop.vertex().theta()), prop.vertex().eta(), prop.vertex().phi(), 0.);
        //    if ( debug ) std::cout << "Propogated genParticle to ECal, position: " << prop.vertex() << " momentum = " << prop.momentum() << std::endl;
        //    if ( debug ) std::cout << "                              starting position: " << start.vertex() << " momentum = " << start.momentum() << std::endl;
        //    if ( debug ) std::cout << "                          genParticle position: " << genJet.vertex() << " momentum = " << genJet.p4() << std::endl;
        //    if ( debug ) std::cout << "         old pt = " << genJet.pt() << ", new pt = " << genJet.pt() << std::endl;
        //}
        //else
        //{
        //    // something failed?
        //    if ( debug ) std::cout << "Taking defaul, non-propagated gen object" << std::endl;
        //    genJet = genJet.polarP4();
        //}
    
    
    
        treeinfo.genJet_pt = genJet.pt();
        treeinfo.genJet_eta = genJet.eta();
        treeinfo.genJet_phi = genJet.phi();
        treeinfo.genJet_energy = genJet.energy();
        treeinfo.genJet_mass = genJet.mass();
        treeinfo.genJet_charge = genJet.charge();







        // Gen Hadronic Taus
        bool gen_tau_matched = false;
        if ( genHTaus.isValid() )
        {

            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& gen_tau : genHTauCollection)
            {
                if ( reco::deltaR( gen_tau.p4(), genJetP4 ) < 0.3 )
                {
                    treeinfo.genTau_pt = gen_tau.pt();
                    treeinfo.genTau_eta = gen_tau.eta();
                    treeinfo.genTau_phi = gen_tau.phi();
                    treeinfo.genTau_energy = gen_tau.energy();
                    treeinfo.genTau_mass = gen_tau.mass();
                    treeinfo.genTau_charge = gen_tau.charge();
                    gen_tau_matched = true;
                    break;
                }
            }

        }
        if (!gen_tau_matched) // No Stage-2 Jets
        {
            treeinfo.genTau_pt = -9.;
            treeinfo.genTau_eta = -9.;
            treeinfo.genTau_phi = -9.;
            treeinfo.genTau_energy = -9.;
            treeinfo.genTau_mass = -9.;
            treeinfo.genTau_charge = -9.;
        } 
    
    
    
    
    
        //std::cout << "    ---!!!--- L1EG Size: " << caloJets.size() << std::endl;
        bool found_caloJet = false;
        if ( caloJets.size() > 0 )
        {
            // Storing full event info
            float total_et_f = 0.0;
            float nTT_f = 0.0;
            for(const auto& caloJet : caloJets)
            {
                total_et_f = caloJet.GetExperimentalParam("total_et");
                nTT_f = caloJet.GetExperimentalParam("total_nTowers");

                if ( reco::deltaR(caloJet, genJetP4) < genMatchDeltaRcut )
                      //&& fabs(caloJet.pt()-genJetP4.pt())/genJetP4.pt() < genMatchRelPtcut )
                {

                    if ( debug ) std::cout << "using caloJet dr = " << reco::deltaR(caloJet, genJetP4) << std::endl;
                    treeinfo.deltaR = reco::deltaR(caloJet, genJetP4);
                    treeinfo.deltaPhi = reco::deltaPhi(caloJet, genJetP4);
                    treeinfo.deltaEta = genJetP4.eta()-caloJet.eta();
                    
                    fill_tree(caloJet);

                    // Fill basic numerator efficiencies
                    eff_all_num_pt->Fill(genJet.pt());
                    if (genJet.pt() > 20) eff_all_num_eta->Fill(genJet.eta());
                    if ( fabs(genJet.eta()) < 1.5 )
                    {
                        eff_barrel_num_pt->Fill(genJet.pt());
                        if (genJet.pt() > 20) eff_barrel_num_eta->Fill(genJet.eta());
                    }
    
                    found_caloJet = true;
                    break;
    
                } // end passes Pt and dR match
            } // end Calo Jets loop

            // Fill with values from final L1CaloJet (same for all calo jets in the event)
            totalET->Fill(total_et_f);
            nTT->Fill(nTT_f);

            // if not calo_jets were reconstructed to match the gen obj
            if (!found_caloJet) fill_tree_null();
        } // have CaloJets
         // no CaloJets
        if (caloJets.size() == 0 || !found_caloJet)
        {
            // Fill tree with -1 to signify we lose a gen jet        
            fill_tree_null();
        }

    } // end GenJets loop
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1CaloJetStudies::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1CaloJetStudies::endJob() 
{
    if (doRate)
    {
        integrateDown( phase2_rate_all_hist );
        integrateDown( stage2_rate_all_hist );
        integrateDown( phase2_rate_barrel_hist );
        integrateDown( stage2_rate_barrel_hist );
    }
}

// ------------ method called when starting to processes a run  ------------
void 
L1CaloJetStudies::beginRun(edm::Run const& run, edm::EventSetup const& es)
{
    //edm::ESHandle<HepPDT::ParticleDataTable> pdt;
    //es.getData(pdt);
    //if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1CaloJetStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1CaloJetStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1CaloJetStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1CaloJetStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods (ncsmith)
void 
L1CaloJetStudies::integrateDown(TH1F * hist) {
    // integral includes overflow and underflow bins
    double integral=0.;
    for(int i=hist->GetNbinsX()+1; i>=0; i--)
    {
        integral += hist->GetBinContent(i);
        hist->SetBinContent(i, integral);
        hist->SetBinError(i, std::sqrt(integral));
    }
}

void
L1CaloJetStudies::fill_tree(const l1slhc::L1CaloJet& caloJet) {
    // PU Vars
    treeinfo.ecal_PU_pt = caloJet.GetExperimentalParam("ecal_PU_pt");
    treeinfo.ecal_L1EG_jet_PU_pt = caloJet.GetExperimentalParam("ecal_L1EG_jet_PU_pt");
    treeinfo.hcal_PU_pt = caloJet.GetExperimentalParam("hcal_PU_pt");
    treeinfo.ecal_PU_cor_pt = caloJet.GetExperimentalParam("ecal_PU_cor_pt");
    treeinfo.ecal_L1EG_jet_PU_cor_pt = caloJet.GetExperimentalParam("ecal_L1EG_jet_PU_cor_pt");
    treeinfo.hcal_PU_cor_pt = caloJet.GetExperimentalParam("hcal_PU_cor_pt");
    treeinfo.jet_PU_cor_pt = caloJet.GetExperimentalParam("jet_PU_cor_pt");
    treeinfo.iPhi_ET_rings_ecal = caloJet.GetExperimentalParam("iPhi_ET_rings_ecal");
    treeinfo.iPhi_ET_rings_l1eg = caloJet.GetExperimentalParam("iPhi_ET_rings_l1eg");
    treeinfo.iPhi_ET_rings_hcal = caloJet.GetExperimentalParam("iPhi_ET_rings_hcal");
    treeinfo.iPhi_ET_rings_total = caloJet.GetExperimentalParam("iPhi_ET_rings_total");
    treeinfo.iPhi_nTowers_rings_ecal = caloJet.GetExperimentalParam("iPhi_nTowers_rings_ecal");
    treeinfo.iPhi_nTowers_rings_l1eg = caloJet.GetExperimentalParam("iPhi_nTowers_rings_l1eg");
    treeinfo.iPhi_nTowers_rings_hcal = caloJet.GetExperimentalParam("iPhi_nTowers_rings_hcal");
    treeinfo.iPhi_nTowers_rings_total = caloJet.GetExperimentalParam("iPhi_nTowers_rings_total");
    treeinfo.total_et = caloJet.GetExperimentalParam("total_et");
    treeinfo.total_nTowers = caloJet.GetExperimentalParam("total_nTowers");

    // As of 28 May 2018 caloJet_pt is post-calibration
    treeinfo.ecal_pt = caloJet.GetExperimentalParam("ecal_pt");
    treeinfo.ecal_eta = caloJet.GetExperimentalParam("ecal_eta");
    treeinfo.ecal_phi = caloJet.GetExperimentalParam("ecal_phi");
    treeinfo.ecal_mass = caloJet.GetExperimentalParam("ecal_mass");
    treeinfo.ecal_energy = caloJet.GetExperimentalParam("ecal_energy");
    treeinfo.ecal_L1EG_jet_pt = caloJet.GetExperimentalParam("ecal_L1EG_jet_pt");
    treeinfo.ecal_L1EG_jet_eta = caloJet.GetExperimentalParam("ecal_L1EG_jet_eta");
    treeinfo.ecal_L1EG_jet_phi = caloJet.GetExperimentalParam("ecal_L1EG_jet_phi");
    treeinfo.ecal_L1EG_jet_energy = caloJet.GetExperimentalParam("ecal_L1EG_jet_energy");
    treeinfo.hcal_pt = caloJet.GetExperimentalParam("hcal_pt");
    treeinfo.hcal_calibration = caloJet.GetExperimentalParam("hcal_calibration");
    treeinfo.hcal_pt_calibration = caloJet.GetExperimentalParam("hcal_pt_calibration");
    treeinfo.hcal_eta = caloJet.GetExperimentalParam("hcal_eta");
    treeinfo.hcal_phi = caloJet.GetExperimentalParam("hcal_phi");
    treeinfo.hcal_mass = caloJet.GetExperimentalParam("hcal_mass");
    treeinfo.hcal_energy = caloJet.GetExperimentalParam("hcal_energy");
    treeinfo.jet_pt = caloJet.GetExperimentalParam("jet_pt");
    treeinfo.jet_pt_calibration = caloJet.GetExperimentalParam("jet_pt_calibration");
    //treeinfo.transition_calibration = caloJet.GetExperimentalParam("transition_calibration");
    treeinfo.transition_calibration = -9;
    treeinfo.jet_eta = caloJet.GetExperimentalParam("jet_eta");
    treeinfo.jet_phi = caloJet.GetExperimentalParam("jet_phi");
    treeinfo.jet_mass = caloJet.GetExperimentalParam("jet_mass");
    treeinfo.jet_energy = caloJet.GetExperimentalParam("jet_energy");
    treeinfo.hovere = caloJet.hovere();
    treeinfo.seed_pt = caloJet.GetExperimentalParam("seed_pt");
    treeinfo.seed_iEta = caloJet.GetExperimentalParam("seed_iEta");
    treeinfo.seed_iPhi = caloJet.GetExperimentalParam("seed_iPhi");
    treeinfo.seed_eta = caloJet.GetExperimentalParam("seed_eta");
    treeinfo.seed_phi = caloJet.GetExperimentalParam("seed_phi");
    treeinfo.seed_energy = caloJet.GetExperimentalParam("seed_energy");
    treeinfo.hcal_nHits = caloJet.GetExperimentalParam("hcal_nHits");
    treeinfo.hcal_3x3 = caloJet.GetExperimentalParam("hcal_3x3");
    treeinfo.hcal_5x5 = caloJet.GetExperimentalParam("hcal_5x5");
    treeinfo.hcal_7x7 = caloJet.GetExperimentalParam("hcal_7x7");
    treeinfo.hcal_2x2_1 = caloJet.GetExperimentalParam("hcal_2x2_1");
    treeinfo.hcal_2x2_2 = caloJet.GetExperimentalParam("hcal_2x2_2");
    treeinfo.hcal_2x2_3 = caloJet.GetExperimentalParam("hcal_2x2_3");
    treeinfo.hcal_2x2_4 = caloJet.GetExperimentalParam("hcal_2x2_4");
    treeinfo.ecal_leading_pt = caloJet.GetExperimentalParam("ecal_leading_pt");
    treeinfo.ecal_leading_eta = caloJet.GetExperimentalParam("ecal_leading_eta");
    treeinfo.ecal_leading_phi = caloJet.GetExperimentalParam("ecal_leading_phi");
    treeinfo.ecal_leading_energy = caloJet.GetExperimentalParam("ecal_leading_energy");
    treeinfo.ecal_dR0p05 = caloJet.GetExperimentalParam("ecal_dR0p05");
    treeinfo.ecal_dR0p075 = caloJet.GetExperimentalParam("ecal_dR0p075");
    treeinfo.ecal_dR0p1 = caloJet.GetExperimentalParam("ecal_dR0p1");
    treeinfo.ecal_dR0p125 = caloJet.GetExperimentalParam("ecal_dR0p125");
    treeinfo.ecal_dR0p15 = caloJet.GetExperimentalParam("ecal_dR0p15");
    treeinfo.ecal_dR0p2 = caloJet.GetExperimentalParam("ecal_dR0p2");
    treeinfo.ecal_dR0p3 = caloJet.GetExperimentalParam("ecal_dR0p3");
    treeinfo.ecal_dR0p4 = caloJet.GetExperimentalParam("ecal_dR0p4");
    treeinfo.ecal_dR0p1_leading = caloJet.GetExperimentalParam("ecal_dR0p1_leading");
    treeinfo.ecal_nL1EGs = caloJet.GetExperimentalParam("ecal_nL1EGs");
    treeinfo.ecal_nL1EGs_standalone = caloJet.GetExperimentalParam("ecal_nL1EGs_standalone");
    treeinfo.ecal_nL1EGs_trkMatch = caloJet.GetExperimentalParam("ecal_nL1EGs_trkMatch");
    treeinfo.deltaR_ecal_vs_jet = caloJet.GetExperimentalParam("deltaR_ecal_vs_jet");
    treeinfo.deltaR_hcal_vs_jet = caloJet.GetExperimentalParam("deltaR_hcal_vs_jet");
    treeinfo.deltaR_L1EGjet_vs_jet = caloJet.GetExperimentalParam("deltaR_L1EGjet_vs_jet");
    //treeinfo.deltaR_hcal_vs_seed = caloJet.GetExperimentalParam("deltaR_hcal_vs_seed");
    treeinfo.deltaR_ecal_vs_hcal = caloJet.GetExperimentalParam("deltaR_ecal_vs_hcal");
    treeinfo.deltaR_ecal_vs_seed = caloJet.GetExperimentalParam("deltaR_ecal_vs_seed");
    treeinfo.deltaR_ecal_lead_vs_jet = caloJet.GetExperimentalParam("deltaR_ecal_lead_vs_jet");
    treeinfo.deltaR_ecal_lead_vs_ecal = caloJet.GetExperimentalParam("deltaR_ecal_lead_vs_ecal");
    tree->Fill();
}


void
L1CaloJetStudies::fill_tree_null() {
    // Fill with -9 with no CaloJet fround
    treeinfo.ecal_PU_pt = -9;
    treeinfo.ecal_L1EG_jet_PU_pt = -9;
    treeinfo.hcal_PU_pt = -9;
    treeinfo.ecal_PU_cor_pt = -9;
    treeinfo.ecal_L1EG_jet_PU_cor_pt = -9;
    treeinfo.hcal_PU_cor_pt = -9;
    treeinfo.jet_PU_cor_pt = -9;
    treeinfo.iPhi_ET_rings_ecal = -9;
    treeinfo.iPhi_ET_rings_l1eg = -9;
    treeinfo.iPhi_ET_rings_hcal = -9;
    treeinfo.iPhi_ET_rings_total = -9;
    treeinfo.iPhi_nTowers_rings_ecal = -9;
    treeinfo.iPhi_nTowers_rings_l1eg = -9;
    treeinfo.iPhi_nTowers_rings_hcal = -9;
    treeinfo.iPhi_nTowers_rings_total = -9;
    treeinfo.total_et = -9;
    treeinfo.total_nTowers = -9;

    treeinfo.ecal_pt = -9;
    treeinfo.ecal_eta = -9;
    treeinfo.ecal_phi = -9;
    treeinfo.ecal_mass = -9;
    treeinfo.ecal_energy = -9;
    treeinfo.ecal_L1EG_jet_pt = -9;
    treeinfo.ecal_L1EG_jet_eta = -9;
    treeinfo.ecal_L1EG_jet_phi = -9;
    treeinfo.ecal_L1EG_jet_energy = -9;
    treeinfo.hcal_pt = -9;
    treeinfo.hcal_calibration = -9;
    treeinfo.hcal_pt_calibration = -9;
    treeinfo.hcal_eta = -9;
    treeinfo.hcal_phi = -9;
    treeinfo.hcal_mass = -9;
    treeinfo.hcal_energy = -9;
    treeinfo.jet_pt = -9;
    treeinfo.jet_pt_calibration = -9;
    treeinfo.transition_calibration = -9;
    treeinfo.jet_eta = -9;
    treeinfo.jet_phi = -9;
    treeinfo.jet_mass = -9;
    treeinfo.jet_energy = -9;
    treeinfo.hovere = -9;
    treeinfo.seed_pt = -9;
    treeinfo.seed_iEta = -9;
    treeinfo.seed_iPhi = -9;
    treeinfo.seed_eta = -9;
    treeinfo.seed_phi = -9;
    treeinfo.seed_energy = -9;
    treeinfo.hcal_nHits = -9;
    treeinfo.hcal_3x3 = -9;
    treeinfo.hcal_5x5 = -9;
    treeinfo.hcal_7x7 = -9;
    treeinfo.hcal_2x2_1 = -9;
    treeinfo.hcal_2x2_2 = -9;
    treeinfo.hcal_2x2_3 = -9;
    treeinfo.hcal_2x2_4 = -9;
    treeinfo.ecal_leading_pt = -9;
    treeinfo.ecal_leading_eta = -9;
    treeinfo.ecal_leading_phi = -9;
    treeinfo.ecal_leading_energy = -9;
    treeinfo.ecal_dR0p05 = -9;
    treeinfo.ecal_dR0p075 = -9;
    treeinfo.ecal_dR0p1 = -9;
    treeinfo.ecal_dR0p125 = -9;
    treeinfo.ecal_dR0p15 = -9;
    treeinfo.ecal_dR0p2 = -9;
    treeinfo.ecal_dR0p3 = -9;
    treeinfo.ecal_dR0p4 = -9;
    treeinfo.ecal_dR0p1_leading = -9;
    treeinfo.ecal_nL1EGs = -9;
    treeinfo.ecal_nL1EGs_standalone = -9;
    treeinfo.ecal_nL1EGs_trkMatch = -9;
    treeinfo.deltaR_ecal_vs_jet = -9;
    treeinfo.deltaR_hcal_vs_jet = -9;
    treeinfo.deltaR_L1EGjet_vs_jet = -9;
    treeinfo.deltaR_hcal_vs_seed = -9;
    treeinfo.deltaR_ecal_vs_hcal = -9;
    treeinfo.deltaR_ecal_vs_seed = -9;
    treeinfo.deltaR_ecal_lead_vs_jet = -9;
    treeinfo.deltaR_ecal_lead_vs_ecal = -9;
    tree->Fill();
}



//define this as a plug-in
DEFINE_FWK_MODULE(L1CaloJetStudies);
