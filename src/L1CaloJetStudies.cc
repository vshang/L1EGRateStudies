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
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

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
#include "TGraph.h"
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

#include "DataFormats/L1TCalorimeterPhase2/interface/CaloJet.h"
#include "DataFormats/L1TCalorimeterPhase2/src/classes.h"

#include "FastSimulation/ParticlePropagator/interface/ParticlePropagator.h"

// #include "FastSimulation/Particle/interface/RawParticle.h"

// Stage2
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"

//Victor's track matching edit: track trigger data formats
// #include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
// #include "DataFormats/L1TrackTrigger/interface/TTCluster.h"
// #include "DataFormats/L1TrackTrigger/interface/TTStub.h"
// #include "DataFormats/L1TrackTrigger/interface/TTTrack.h"
// #include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
// #include "SimDataFormats/TrackingAnalysis/interface/TrackingVertex.h"
// #include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
// #include "SimDataFormats/TrackingHit/interface/PSimHit.h"
// #include "SimTracker/TrackTriggerAssociation/interface/TTClusterAssociationMap.h"
// #include "SimTracker/TrackTriggerAssociation/interface/TTStubAssociationMap.h"
// #include "SimTracker/TrackTriggerAssociation/interface/TTTrackAssociationMap.h"
// #include "Geometry/Records/interface/StackedTrackerGeometryRecord.h"
// #include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
// //Also include track matching algorithm
// #include "L1Trigger/L1CaloTrigger/interface/L1TkElectronTrackMatchAlgo.h"
//End of Victor's track matching edit


// 
// class declaration
//
class L1CaloJetStudies : public edm::one::EDAnalyzer<edm::one::SharedResources, edm::one::WatchRuns, edm::one::WatchLuminosityBlocks> {
    typedef BXVector<l1t::Jet> JetBxCollection;
    typedef std::vector<l1t::Jet> JetCollection;
    typedef std::vector<reco::GenJet> GenJetCollection;
    typedef BXVector<l1t::Tau> TauBxCollection;
    typedef std::vector<l1t::Tau> TauCollection;
    // typedef std::vector< TTTrack < Ref_Phase2TrackerDigi_ >> L1TkTrackCollectionType; //Victor's track matching edit: added L1TkTrackCollectionType typedef

    public:
        explicit L1CaloJetStudies(const edm::ParameterSet& iConfig);
        ~L1CaloJetStudies();

        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


    private:
        //----edm control---
        virtual void beginJob() ;
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob() ;

        virtual void beginRun(edm::Run const&, edm::EventSetup const&);
        virtual void endRun(edm::Run const&, edm::EventSetup const&);
        virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
        virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

        // -- user functions
        void integrateDown(TH1F *);
        // bool isJetTrackMatched(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle); //Victor's track matching edit: added function to check if jet is matched to a track
        // float findClosestTrackdR(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle, float pt_cut); //Victor's track matching edit: added function to check min dR between jet and tracks
        // float findMaxTrackPt(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle, float dR_cut); //Victor's track matching edit: added function to check max pT distribution of matched tracks
        // bool isJEFThreshold(float jet_pt, float jet_eta, float jetEnergyFraction); //Victor's JEF edit: added function to check if jet passes JEF threshold
        void fill_tree(const l1tp2::CaloJet& caloJet);
        void fill_tree_null();
        
        // ----------member data ---------------------------
        bool doRate;
        bool debug;
        bool use_gen_taus;
        
        double genMatchDeltaRcut;
        double genMatchRelPtcut;
        
        
        float x_bins[49] = {
            10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 
            150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 
            330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490
        }; 
        float y_bins[49] = {
            1.0,    0.836111,0.75826, 0.634662,0.567179,0.570728,0.604189,0.65972, 0.708608,0.741256,0.763668,0.783147,0.806544,0.815089,0.833782,
            0.828733,0.845086,0.848383,0.854917,0.859798,0.865434,0.864831,0.86911, 0.869681,0.87554, 0.880766,0.880534,
            0.87642, 0.881073,0.883628,0.88495, 0.884165,0.885168,0.880482,0.892404,0.886782,0.892172,0.885196,0.885845,
            0.886959,0.891052,0.890402,0.889508,0.889437,0.890705,0.893328,0.891408,0.895185,0.895725
        }; 

        // Apply stage-2 calibrations to align to gen
        TGraph ptAdjustStage2 = TGraph(49, x_bins, y_bins);

        // edm::EDGetTokenT<L1TkTrackCollectionType> L1TrackInputToken_; // Victor's track matching edit: Get input token for track info from L1CaloJetProducer.cc

        edm::EDGetTokenT<l1tp2::CaloJetsCollection> caloJetsToken_;
        l1tp2::CaloJetsCollection caloJets;
        edm::Handle<l1tp2::CaloJetsCollection> caloJetsHandle;   
 

        //edm::EDGetTokenT<reco::GenParticleCollection> genCollectionToken_;
        //reco::GenParticleCollection genParticles;
        //edm::Handle<reco::GenParticleCollection> genParticleHandle;

        edm::EDGetTokenT<std::vector<reco::GenJet>> genJetsToken_;
        std::vector<reco::GenJet> genJets;
        edm::Handle<std::vector<reco::GenJet>> genJetsHandle;

        edm::EDGetTokenT<std::vector<reco::GenJet>> genHadronicTausToken_;
        edm::Handle<std::vector<reco::GenJet>> genHTaus;

        std::vector<reco::GenJet> * genCollection;

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

        TH1F * eff_noHGCal_denom_pt;
        TH1F * eff_noHGCal_num_pt;
        TH1F * eff_noHGCal_num_stage2jet_pt;

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
        TH1F * phase2_rate_noHGCal_hist;
        TH1F * stage2_rate_noHGCal_hist;
        TH1F * phase2_rate_barrel_hist;
        TH1F * stage2_rate_barrel_hist;
        // rate in eta
        TH1F * phase2_rate_all_eta_hist;
        TH1F * stage2_rate_all_eta_hist;
        TH1F * phase2_rate_barrel_eta_hist;
        TH1F * stage2_rate_barrel_eta_hist;

        TH1F * gen_jet_HTT;
        TH1F * phase2_jet_HTT_300;
        TH1F * phase2_jet_HTT_400;
        TH1F * phase2_jet_HTT_500;
        TH1F * phase2_jet_HTT_600;
        TH1F * phase2_jet_HTT_rate_hist;
                
        // Crystal pt stuff
        TTree * tree;
        struct {
            double run;
            double lumi;
            double event;
            float nTruePU;
            float total_et;
            //float total_nTowers;
            float ecal_pt;
            float ecal_seed;
            float l1eg_pt;
            float l1eg_seed;
            //float ecal_eta;
            //float ecal_phi;
            //float ecal_mass;
            //float ecal_energy;
            //float ecal_L1EG_jet_eta;
            //float ecal_L1EG_jet_phi;
            //float ecal_L1EG_jet_mass;
            //float ecal_L1EG_jet_energy;
            float hcal_pt;
            float hcal_seed;
            float hcal_calibration;
            float hcal_pt_calibration;
            //float hcal_eta;
            //float hcal_phi;
            //float hcal_mass;
            //float hcal_energy;
            float jet_pt;
            float jet_pt_calibration;
            float transition_calibration;
            float jet_eta;
            float jet_phi;
            float jet_mass;
            float jet_energy;
            float hovere;
            //float hcal_3x3;
            float hcal_3x5;
            //float hcal_5x5;
            //float hcal_5x7;
            float hcal_7x7;
            //float hcal_2x2;
            //float hcal_2x3;
            //float ecal_3x3;
            float ecal_3x5;
            //float ecal_5x5;
            //float ecal_5x7;
            float ecal_7x7;
            //float ecal_2x2;
            //float ecal_2x3;
            //float l1eg_3x3;
            float l1eg_3x5;
            //float l1eg_5x5;
            //float l1eg_5x7;
            float l1eg_7x7;
            //float l1eg_2x2;
            //float l1eg_2x3;
            float seed_pt;
            float seed_iEta;
            float seed_iPhi;
            float seed_eta;
            float seed_phi;
            float seed_energy;
            float hcal_nHits;
            float ecal_nHits;
            float l1eg_nHits;

	    // //Victor's edit: added different tower configuration variables
	    // float hcal_3x3;
	    // float hcal_1x3;
	    // float hcal_3x1;
	    // float hcal_Cross;
	    // float hcal_X;

	    // float ecal_3x3;
	    // float ecal_1x3;
	    // float ecal_3x1;
	    // float ecal_Cross;
	    // float ecal_X;

	    // float l1eg_3x3;
	    // float l1eg_1x3;
	    // float l1eg_3x1;
	    // float l1eg_Cross;
	    // float l1eg_X;

	    // float total_3x3;
	    // float total_1x3;
	    // float total_3x1;
	    // float total_Cross;
	    // float total_X;

	    // float total_7x7;
	    // float total_3x5;

	    // //Individual tower energies in 3x5 array. 11 corresponds to lower left corner (least eta, least phi)
	    // float hcal_11;
	    // float hcal_12;
	    // float hcal_13;
	    // float hcal_21;
	    // float hcal_22;
	    // float hcal_23;
	    // float hcal_31;
	    // float hcal_33;
	    // float hcal_41;
	    // float hcal_42;
	    // float hcal_43;
	    // float hcal_51;
	    // float hcal_52;
	    // float hcal_53;

	    // float ecal_11;
	    // float ecal_12;
	    // float ecal_13;
	    // float ecal_21;
	    // float ecal_22;
	    // float ecal_23;
	    // float ecal_31;
	    // float ecal_33;
	    // float ecal_41;
	    // float ecal_42;
	    // float ecal_43;
	    // float ecal_51;
	    // float ecal_52;
	    // float ecal_53;

	    // float l1eg_11;
	    // float l1eg_12;
	    // float l1eg_13;
	    // float l1eg_21;
	    // float l1eg_22;
	    // float l1eg_23;
	    // float l1eg_31;
	    // float l1eg_33;
	    // float l1eg_41;
	    // float l1eg_42;
	    // float l1eg_43;
	    // float l1eg_51;
	    // float l1eg_52;
	    // float l1eg_53;

	    // float total_seed;
	    // float total_11;
	    // float total_12;
	    // float total_13;
	    // float total_21;
	    // float total_22;
	    // float total_23;
	    // float total_31;
	    // float total_33;
	    // float total_41;
	    // float total_42;
	    // float total_43;
	    // float total_51;
	    // float total_52;
	    // float total_53;

	    // //Also added branch to check dR and Pt distribution of reco taus/tracks
	    // float jet_and_track_dR;
	    // float jet_and_track_dR_2GeV;
	    // float jet_and_track_dR_10GeV;
	    // float max_track_pt_dR0p2;

	    // //End of Victor's edit

            //float ecal_leading_pt;
            //float ecal_leading_eta;
            //float ecal_leading_phi;
            //float ecal_leading_energy;
            //float ecal_dR0p05;
            //float ecal_dR0p075;
            //float ecal_dR0p1;
            //float ecal_dR0p125;
            //float ecal_dR0p15;
            //float ecal_dR0p2;
            //float ecal_dR0p3;
            //float ecal_dR0p4;
            //float ecal_dR0p1_leading;
            float l1eg_nL1EGs;
            float l1eg_nL1EGs_standaloneSS;
            float l1eg_nL1EGs_standaloneIso;
            float l1eg_nL1EGs_trkMatchSS;
            float l1eg_nL1EGs_trkMatchIso;
            float n_l1eg_HoverE_LessThreshold;

            float n_l1eg_HoverE_Less0p25;
            float n_l1eg_HoverE_Less0p25_trkSS;
            float n_l1eg_HoverE_Less0p25_saSS;
            float n_l1eg_HoverE_0p5to1p0;
            float n_l1eg_HoverE_0p5to1p0_trkSS;
            float n_l1eg_HoverE_0p5to1p0_saSS;
            float n_l1eg_HoverE_Gtr0p25;
            float n_l1eg_HoverE_Gtr0p25_trkSS;
            float n_l1eg_HoverE_Gtr0p25_saSS;
            float n_l1eg_avgHoverE;

            float tau_pt;
            float tau_pt_calibration_value;
            float tau_iso_et;
            float tau_total_iso_et;
            float loose_iso_tau_wp;

            float deltaR_ecal_vs_jet;
            float deltaR_hcal_vs_jet;
            float deltaR_L1EGjet_vs_jet;
            float deltaR_hcal_vs_seed;
            float deltaR_ecal_vs_hcal;
            float deltaR_ecal_vs_seed;
            float deltaR_ecal_lead_vs_jet;
            float deltaR_ecal_lead_vs_ecal;
            float deltaR;
            float deltaR_phase2_stage2;
            float deltaPhi;
            float deltaEta;
            float genJet;
            float genTau;
            float genJet_pt;
            float genJet_eta;
            float genJet_phi;
            float genJet_energy;
            float genJet_mass;
            float genJet_charge;
            float genTau_n_prongs;
            float genTau_n_photons;
            float genTau_pt_prongs;
            float genTau_pt_photons;
            float stage2jet_pt;
            float stage2jet_pt_calib;
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
    use_gen_taus(iConfig.getUntrackedParameter<bool>("use_gen_taus", false)),
    genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.3)),
    genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
    // L1TrackInputToken_(consumes<L1TkTrackCollectionType>(iConfig.getParameter<edm::InputTag>("L1TrackInputTag"))), //Victor's track matching edit: Store track info from L1CaloJetProducer in token
    caloJetsToken_(consumes<l1tp2::CaloJetsCollection>(iConfig.getParameter<edm::InputTag>("L1CaloJetsInputTag"))),
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
    eff_all_denom_eta = fs->make<TH1F>("eff_all_denom_eta", "Gen. eta;Gen. #eta; Counts", 180, -7, 7);
    eff_all_num_eta = fs->make<TH1F>("eff_all_num_eta", "Gen. eta;Gen. #eta; Counts", 180, -7, 7);
    eff_all_num_stage2jet_eta = fs->make<TH1F>("eff_all_num_stage2jet_eta", "Gen. eta;Gen. #eta; Counts", 180, -7, 7);

    eff_noHGCal_denom_pt = fs->make<TH1F>("eff_noHGCal_denom_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_noHGCal_num_pt = fs->make<TH1F>("eff_noHGCal_num_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_noHGCal_num_stage2jet_pt = fs->make<TH1F>("eff_noHGCal_num_stage2jet_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);

    eff_barrel_denom_pt = fs->make<TH1F>("eff_barrel_denom_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_num_pt = fs->make<TH1F>("eff_barrel_num_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_num_stage2jet_pt = fs->make<TH1F>("eff_barrel_num_stage2jet_pt", "Gen. pt;Gen. pT (GeV); Counts", 30, 0, 300);
    eff_barrel_denom_eta = fs->make<TH1F>("eff_barrel_denom_eta", "Gen. eta;Gen. #eta; Counts", 80, -2, 2);
    eff_barrel_num_eta = fs->make<TH1F>("eff_barrel_num_eta", "Gen. eta;Gen. #eta; Counts", 80, -2, 2);
    eff_barrel_num_stage2jet_eta = fs->make<TH1F>("eff_barrel_num_stage2jet_eta", "Gen. eta;Gen. #eta; Counts", 80, -2, 2);

    nTruePUHist = fs->make<TH1F>("nTruePUHist", "nTrue PU", 250, 0, 250);
    totalET = fs->make<TH1F>("totalET", "Total ET", 500, 0, 5000);
    nTT = fs->make<TH1F>("nTT", "nTT", 500, 0, 5000);
    phase2_rate_all_hist = fs->make<TH1F>("phase2_rate_all_hist", "phase2_rate_all_hist", 500, 0, 500);
    stage2_rate_all_hist = fs->make<TH1F>("stage2_rate_all_hist", "stage2_rate_all_hist", 500, 0, 500);
    phase2_rate_noHGCal_hist = fs->make<TH1F>("phase2_rate_noHGCal_hist", "phase2_rate_noHGCal_hist", 500, 0, 500);
    stage2_rate_noHGCal_hist = fs->make<TH1F>("stage2_rate_noHGCal_hist", "stage2_rate_noHGCal_hist", 500, 0, 500);
    phase2_rate_barrel_hist = fs->make<TH1F>("phase2_rate_barrel_hist", "phase2_rate_barrel_hist", 500, 0, 500);
    stage2_rate_barrel_hist = fs->make<TH1F>("stage2_rate_barrel_hist", "stage2_rate_barrel_hist", 500, 0, 500);

    phase2_rate_all_eta_hist = fs->make<TH1F>("phase2_rate_all_eta_hist", "phase2_rate_all_eta_hist", 120, -6, 6);
    stage2_rate_all_eta_hist = fs->make<TH1F>("stage2_rate_all_eta_hist", "stage2_rate_all_eta_hist", 120, -6, 6);
    phase2_rate_barrel_eta_hist = fs->make<TH1F>("phase2_rate_barrel_eta_hist", "phase2_rate_barrel_eta_hist", 40, -2, 2);
    stage2_rate_barrel_eta_hist = fs->make<TH1F>("stage2_rate_barrel_eta_hist", "stage2_rate_barrel_eta_hist", 40, -2, 2);

    gen_jet_HTT = fs->make<TH1F>("gen_jet_HTT", "gen_jet_HTT;Gen Jet HTT", 100, 0, 1000);
    phase2_jet_HTT_300 = fs->make<TH1F>("phase2_jet_HTT_300", "phase2_jet_HTT_300;Gen Jet HTT;L1 Efficiency", 100, 0, 1000);
    phase2_jet_HTT_400 = fs->make<TH1F>("phase2_jet_HTT_400", "phase2_jet_HTT_400;Gen Jet HTT;L1 Efficiency", 100, 0, 1000);
    phase2_jet_HTT_500 = fs->make<TH1F>("phase2_jet_HTT_500", "phase2_jet_HTT_500;Gen Jet HTT;L1 Efficiency", 100, 0, 1000);
    phase2_jet_HTT_600 = fs->make<TH1F>("phase2_jet_HTT_600", "phase2_jet_HTT_600;Gen Jet HTT;L1 Efficiency", 100, 0, 1000);
    phase2_jet_HTT_rate_hist = fs->make<TH1F>("phase2_jet_HTT_rate_hist", "phase2_jet_HTT_rate_hist", 100, 0, 1000);

    tree = fs->make<TTree>("tree", "CaloJet values");
    tree->Branch("run", &treeinfo.run);
    tree->Branch("lumi", &treeinfo.lumi);
    tree->Branch("event", &treeinfo.event);
    tree->Branch("nTruePU", &treeinfo.nTruePU);
    tree->Branch("total_et", &treeinfo.total_et);
    //tree->Branch("total_nTowers", &treeinfo.total_nTowers);
    tree->Branch("ecal_pt", &treeinfo.ecal_pt);
    tree->Branch("ecal_seed", &treeinfo.ecal_seed);
    tree->Branch("l1eg_pt", &treeinfo.l1eg_pt);
    tree->Branch("l1eg_seed", &treeinfo.l1eg_seed);
    //tree->Branch("ecal_eta", &treeinfo.ecal_eta);
    //tree->Branch("ecal_phi", &treeinfo.ecal_phi);
    //tree->Branch("ecal_mass", &treeinfo.ecal_mass);
    //tree->Branch("ecal_energy", &treeinfo.ecal_energy);
    //tree->Branch("ecal_L1EG_jet_eta", &treeinfo.ecal_L1EG_jet_eta);
    //tree->Branch("ecal_L1EG_jet_phi", &treeinfo.ecal_L1EG_jet_phi);
    //tree->Branch("ecal_L1EG_jet_mass", &treeinfo.ecal_L1EG_jet_mass);
    //tree->Branch("ecal_L1EG_jet_energy", &treeinfo.ecal_L1EG_jet_energy);
    tree->Branch("hcal_pt", &treeinfo.hcal_pt);
    tree->Branch("hcal_seed", &treeinfo.hcal_seed);
    tree->Branch("hcal_calibration", &treeinfo.hcal_calibration);
    tree->Branch("hcal_pt_calibration", &treeinfo.hcal_pt_calibration);
    //tree->Branch("hcal_eta", &treeinfo.hcal_eta);
    //tree->Branch("hcal_phi", &treeinfo.hcal_phi);
    //tree->Branch("hcal_mass", &treeinfo.hcal_mass);
    //tree->Branch("hcal_energy", &treeinfo.hcal_energy);
    tree->Branch("jet_pt", &treeinfo.jet_pt);
    tree->Branch("jet_pt_calibration", &treeinfo.jet_pt_calibration);
    tree->Branch("transition_calibration", &treeinfo.transition_calibration);
    tree->Branch("jet_eta", &treeinfo.jet_eta);
    tree->Branch("jet_phi", &treeinfo.jet_phi);
    tree->Branch("jet_mass", &treeinfo.jet_mass);
    tree->Branch("jet_energy", &treeinfo.jet_energy);
    tree->Branch("hovere", &treeinfo.hovere);

    // //Victor's edit: added additional tower configurations to tree branches
    // tree->Branch("hcal_3x3", &treeinfo.hcal_3x3);
    // tree->Branch("hcal_1x3", &treeinfo.hcal_1x3);
    // tree->Branch("hcal_3x1", &treeinfo.hcal_3x1);
    // tree->Branch("hcal_Cross", &treeinfo.hcal_Cross);
    // tree->Branch("hcal_X", &treeinfo.hcal_X);

    // tree->Branch("ecal_3x3", &treeinfo.ecal_3x3);
    // tree->Branch("ecal_1x3", &treeinfo.ecal_1x3);
    // tree->Branch("ecal_3x1", &treeinfo.ecal_3x1);
    // tree->Branch("ecal_Cross", &treeinfo.ecal_Cross);
    // tree->Branch("ecal_X", &treeinfo.ecal_X);

    // tree->Branch("l1eg_3x3", &treeinfo.l1eg_3x3);
    // tree->Branch("l1eg_1x3", &treeinfo.l1eg_1x3);
    // tree->Branch("l1eg_3x1", &treeinfo.l1eg_3x1);
    // tree->Branch("l1eg_Cross", &treeinfo.l1eg_Cross);
    // tree->Branch("l1eg_X", &treeinfo.l1eg_X);

    // tree->Branch("total_3x3", &treeinfo.total_3x3);
    // tree->Branch("total_1x3", &treeinfo.total_1x3);
    // tree->Branch("total_3x1", &treeinfo.total_3x1);
    // tree->Branch("total_Cross", &treeinfo.total_Cross);
    // tree->Branch("total_X", &treeinfo.total_X);

    // tree->Branch("total_7x7", &treeinfo.total_7x7);
    // tree->Branch("total_3x5", &treeinfo.total_3x5);

    // //Add individual tower energies in 3x5 array to branches. 11 corresponds to lower left corner (least eta, least phi)
    // tree->Branch("hcal_11", &treeinfo.hcal_11);
    // tree->Branch("hcal_12", &treeinfo.hcal_12);
    // tree->Branch("hcal_13", &treeinfo.hcal_13);
    // tree->Branch("hcal_21", &treeinfo.hcal_21);
    // tree->Branch("hcal_22", &treeinfo.hcal_22);
    // tree->Branch("hcal_23", &treeinfo.hcal_23);
    // tree->Branch("hcal_31", &treeinfo.hcal_31);
    // tree->Branch("hcal_33", &treeinfo.hcal_33);
    // tree->Branch("hcal_41", &treeinfo.hcal_41);
    // tree->Branch("hcal_42", &treeinfo.hcal_42);
    // tree->Branch("hcal_43", &treeinfo.hcal_43);
    // tree->Branch("hcal_51", &treeinfo.hcal_51);
    // tree->Branch("hcal_52", &treeinfo.hcal_52);
    // tree->Branch("hcal_53", &treeinfo.hcal_53);

    // tree->Branch("ecal_11", &treeinfo.ecal_11);
    // tree->Branch("ecal_12", &treeinfo.ecal_12);
    // tree->Branch("ecal_13", &treeinfo.ecal_13);
    // tree->Branch("ecal_21", &treeinfo.ecal_21);
    // tree->Branch("ecal_22", &treeinfo.ecal_22);
    // tree->Branch("ecal_23", &treeinfo.ecal_23);
    // tree->Branch("ecal_31", &treeinfo.ecal_31);
    // tree->Branch("ecal_33", &treeinfo.ecal_33);
    // tree->Branch("ecal_41", &treeinfo.ecal_41);
    // tree->Branch("ecal_42", &treeinfo.ecal_42);
    // tree->Branch("ecal_43", &treeinfo.ecal_43);
    // tree->Branch("ecal_51", &treeinfo.ecal_51);
    // tree->Branch("ecal_52", &treeinfo.ecal_52);
    // tree->Branch("ecal_53", &treeinfo.ecal_53);

    // tree->Branch("l1eg_11", &treeinfo.l1eg_11);
    // tree->Branch("l1eg_12", &treeinfo.l1eg_12);
    // tree->Branch("l1eg_13", &treeinfo.l1eg_13);
    // tree->Branch("l1eg_21", &treeinfo.l1eg_21);
    // tree->Branch("l1eg_22", &treeinfo.l1eg_22);
    // tree->Branch("l1eg_23", &treeinfo.l1eg_23);
    // tree->Branch("l1eg_31", &treeinfo.l1eg_31);
    // tree->Branch("l1eg_33", &treeinfo.l1eg_33);
    // tree->Branch("l1eg_41", &treeinfo.l1eg_41);
    // tree->Branch("l1eg_42", &treeinfo.l1eg_42);
    // tree->Branch("l1eg_43", &treeinfo.l1eg_43);
    // tree->Branch("l1eg_51", &treeinfo.l1eg_51);
    // tree->Branch("l1eg_52", &treeinfo.l1eg_52);
    // tree->Branch("l1eg_53", &treeinfo.l1eg_53);

    // tree->Branch("total_seed", &treeinfo.total_seed);
    // tree->Branch("total_11", &treeinfo.total_11);
    // tree->Branch("total_12", &treeinfo.total_12);
    // tree->Branch("total_13", &treeinfo.total_13);
    // tree->Branch("total_21", &treeinfo.total_21);
    // tree->Branch("total_22", &treeinfo.total_22);
    // tree->Branch("total_23", &treeinfo.total_23);
    // tree->Branch("total_31", &treeinfo.total_31);
    // tree->Branch("total_33", &treeinfo.total_33);
    // tree->Branch("total_41", &treeinfo.total_41);
    // tree->Branch("total_42", &treeinfo.total_42);
    // tree->Branch("total_43", &treeinfo.total_43);
    // tree->Branch("total_51", &treeinfo.total_51);
    // tree->Branch("total_52", &treeinfo.total_52);
    // tree->Branch("total_53", &treeinfo.total_53);

    // //Also add branch for min_dR to check dR and Pt distribution between reco tau jets and tracks
    // tree->Branch("jet_and_track_dR", &treeinfo.jet_and_track_dR);
    // tree->Branch("jet_and_track_dR_2GeV", &treeinfo.jet_and_track_dR_2GeV);
    // tree->Branch("jet_and_track_dR_10GeV", &treeinfo.jet_and_track_dR_10GeV);
    // tree->Branch("max_track_pt_dR0p2", &treeinfo.max_track_pt_dR0p2);

    // //End of Victor's edit

    //tree->Branch("hcal_3x3", &treeinfo.hcal_3x3);
    tree->Branch("hcal_3x5", &treeinfo.hcal_3x5);
    //tree->Branch("hcal_5x5", &treeinfo.hcal_5x5);
    //tree->Branch("hcal_5x7", &treeinfo.hcal_5x7);
    tree->Branch("hcal_7x7", &treeinfo.hcal_7x7);
    //tree->Branch("hcal_2x2", &treeinfo.hcal_2x2);
    //tree->Branch("hcal_2x3", &treeinfo.hcal_2x3);
    //tree->Branch("ecal_3x3", &treeinfo.ecal_3x3);
    tree->Branch("ecal_3x5", &treeinfo.ecal_3x5);
    //tree->Branch("ecal_5x5", &treeinfo.ecal_5x5);
    //tree->Branch("ecal_5x7", &treeinfo.ecal_5x7);
    tree->Branch("ecal_7x7", &treeinfo.ecal_7x7);
    //tree->Branch("ecal_2x2", &treeinfo.ecal_2x2);
    //tree->Branch("ecal_2x3", &treeinfo.ecal_2x3);
    //tree->Branch("l1eg_3x3", &treeinfo.l1eg_3x3);
    tree->Branch("l1eg_3x5", &treeinfo.l1eg_3x5);
    //tree->Branch("l1eg_5x5", &treeinfo.l1eg_5x5);
    //tree->Branch("l1eg_5x7", &treeinfo.l1eg_5x7);
    tree->Branch("l1eg_7x7", &treeinfo.l1eg_7x7);
    //tree->Branch("l1eg_2x2", &treeinfo.l1eg_2x2);
    //tree->Branch("l1eg_2x3", &treeinfo.l1eg_2x3);
    tree->Branch("seed_pt", &treeinfo.seed_pt);
    tree->Branch("seed_iEta", &treeinfo.seed_iEta);
    tree->Branch("seed_iPhi", &treeinfo.seed_iPhi);
    tree->Branch("seed_eta", &treeinfo.seed_eta);
    tree->Branch("seed_phi", &treeinfo.seed_phi);
    tree->Branch("seed_energy", &treeinfo.seed_energy);
    tree->Branch("hcal_nHits", &treeinfo.hcal_nHits);
    tree->Branch("ecal_nHits", &treeinfo.ecal_nHits);
    tree->Branch("l1eg_nHits", &treeinfo.l1eg_nHits);
    //tree->Branch("ecal_leading_pt", &treeinfo.ecal_leading_pt);
    //tree->Branch("ecal_leading_eta", &treeinfo.ecal_leading_eta);
    //tree->Branch("ecal_leading_phi", &treeinfo.ecal_leading_phi);
    //tree->Branch("ecal_leading_energy", &treeinfo.ecal_leading_energy);
    //tree->Branch("ecal_dR0p05", &treeinfo.ecal_dR0p05);
    //tree->Branch("ecal_dR0p075", &treeinfo.ecal_dR0p075);
    //tree->Branch("ecal_dR0p1", &treeinfo.ecal_dR0p1);
    //tree->Branch("ecal_dR0p125", &treeinfo.ecal_dR0p125);
    //tree->Branch("ecal_dR0p15", &treeinfo.ecal_dR0p15);
    //tree->Branch("ecal_dR0p2", &treeinfo.ecal_dR0p2);
    //tree->Branch("ecal_dR0p3", &treeinfo.ecal_dR0p3);
    //tree->Branch("ecal_dR0p4", &treeinfo.ecal_dR0p4);
    //tree->Branch("ecal_dR0p1_leading", &treeinfo.ecal_dR0p1_leading);
    tree->Branch("l1eg_nL1EGs", &treeinfo.l1eg_nL1EGs);
    tree->Branch("l1eg_nL1EGs_standaloneSS", &treeinfo.l1eg_nL1EGs_standaloneSS);
    tree->Branch("l1eg_nL1EGs_standaloneIso", &treeinfo.l1eg_nL1EGs_standaloneIso);
    tree->Branch("l1eg_nL1EGs_trkMatchSS", &treeinfo.l1eg_nL1EGs_trkMatchSS);
    tree->Branch("l1eg_nL1EGs_trkMatchIso", &treeinfo.l1eg_nL1EGs_trkMatchIso);
    tree->Branch("n_l1eg_HoverE_LessThreshold", &treeinfo.n_l1eg_HoverE_LessThreshold);

    tree->Branch("n_l1eg_HoverE_Less0p25",         &treeinfo.n_l1eg_HoverE_Less0p25);
    tree->Branch("n_l1eg_HoverE_Less0p25_trkSS",   &treeinfo.n_l1eg_HoverE_Less0p25_trkSS);
    tree->Branch("n_l1eg_HoverE_Less0p25_saSS",    &treeinfo.n_l1eg_HoverE_Less0p25_saSS);
    tree->Branch("n_l1eg_HoverE_0p5to1p0",        &treeinfo.n_l1eg_HoverE_0p5to1p0);
    tree->Branch("n_l1eg_HoverE_0p5to1p0_trkSS",  &treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS);
    tree->Branch("n_l1eg_HoverE_0p5to1p0_saSS",   &treeinfo.n_l1eg_HoverE_0p5to1p0_saSS);
    tree->Branch("n_l1eg_HoverE_Gtr0p25",          &treeinfo.n_l1eg_HoverE_Gtr0p25);
    tree->Branch("n_l1eg_HoverE_Gtr0p25_trkSS",    &treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS);
    tree->Branch("n_l1eg_HoverE_Gtr0p25_saSS",     &treeinfo.n_l1eg_HoverE_Gtr0p25_saSS);
    tree->Branch("n_l1eg_avgHoverE",              &treeinfo.n_l1eg_avgHoverE);

    tree->Branch("tau_pt",     &treeinfo.tau_pt);
    tree->Branch("tau_pt_calibration_value",     &treeinfo.tau_pt_calibration_value);
    tree->Branch("tau_iso_et",     &treeinfo.tau_iso_et);
    tree->Branch("tau_total_iso_et",     &treeinfo.tau_total_iso_et);
    tree->Branch("loose_iso_tau_wp",     &treeinfo.loose_iso_tau_wp);

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
    tree->Branch("deltaR_phase2_stage2", &treeinfo.deltaR_phase2_stage2);
    tree->Branch("deltaPhi_gen", &treeinfo.deltaPhi);
    tree->Branch("deltaEta_gen", &treeinfo.deltaEta);
    tree->Branch("genJet", &treeinfo.genJet);
    tree->Branch("genTau", &treeinfo.genTau);
    tree->Branch("genJet_pt", &treeinfo.genJet_pt);
    tree->Branch("genJet_eta", &treeinfo.genJet_eta);
    tree->Branch("genJet_phi", &treeinfo.genJet_phi);
    tree->Branch("genJet_energy", &treeinfo.genJet_energy);
    tree->Branch("genJet_mass", &treeinfo.genJet_mass);
    tree->Branch("genJet_charge", &treeinfo.genJet_charge);
    tree->Branch("genTau_n_prongs", &treeinfo.genTau_n_prongs);
    tree->Branch("genTau_n_photons", &treeinfo.genTau_n_photons);
    tree->Branch("genTau_pt_prongs", &treeinfo.genTau_pt_prongs);
    tree->Branch("genTau_pt_photons", &treeinfo.genTau_pt_photons);
    // Stage-2
    tree->Branch("stage2jet_pt", &treeinfo.stage2jet_pt);
    tree->Branch("stage2jet_pt_calib", &treeinfo.stage2jet_pt_calib);
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
    if (debug) printf("Starting L1CaloJetStudies Analyzer\n");
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

    // Victor's track matching edit: Get L1 Tracks from token and store them in handle
    // edm::Handle<L1TkTrackCollectionType> l1trackHandle;
    // iEvent.getByToken(L1TrackInputToken_, l1trackHandle);
    // End of Victor's track matching edit

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


    //std::cout << " -- Input L1CaloTaus: " << caloJets.size() << std::endl;

    // Sort caloJets so we can always pick highest pt caloJet matching cuts
    std::sort(begin(caloJets), end(caloJets), [](const l1tp2::CaloJet& a, const l1tp2::CaloJet& b){return a.pt() > b.pt();});


    /*******************************************************
    * If using a min-bias sample and doRate selected, record the
    * Phase-2 and Stage-2 CaloJet objects only
    ************************************************************/
    if (doRate)
    {

        // Reset these to defaults -9
        treeinfo.stage2jet_pt = -9;
        treeinfo.stage2jet_pt_calib = -9;
        treeinfo.stage2jet_eta = -9;
        treeinfo.stage2jet_phi = -9;
        treeinfo.stage2jet_energy = -9;
        treeinfo.stage2jet_mass = -9;
        treeinfo.stage2jet_charge = -9;
        treeinfo.stage2jet_puEt = -9;
        treeinfo.stage2jet_deltaRGen = -9;

        treeinfo.stage2tau_pt = -9;
        treeinfo.stage2tau_eta = -9;
        treeinfo.stage2tau_phi = -9;
        treeinfo.stage2tau_energy = -9;
        treeinfo.stage2tau_mass = -9;
        treeinfo.stage2tau_charge = -9;
        treeinfo.stage2tau_hasEM = -9;
        treeinfo.stage2tau_isMerged = -9;
        treeinfo.stage2tau_isoEt = -9;
        treeinfo.stage2tau_nTT = -9;
        treeinfo.stage2tau_rawEt = -9;
        treeinfo.stage2tau_isoBit = -9;

        treeinfo.n_l1eg_HoverE_Less0p25 = -9;
        treeinfo.n_l1eg_HoverE_Less0p25_trkSS = -9;
        treeinfo.n_l1eg_HoverE_Less0p25_saSS = -9;
        treeinfo.n_l1eg_HoverE_0p5to1p0 = -9;
        treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS = -9;
        treeinfo.n_l1eg_HoverE_0p5to1p0_saSS = -9;
        treeinfo.n_l1eg_HoverE_Gtr0p25 = -9;
        treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS = -9;
        treeinfo.n_l1eg_HoverE_Gtr0p25_saSS = -9;
        treeinfo.n_l1eg_avgHoverE = -9;

        bool stage2_all_filled = false;
        bool phase2_all_filled = false;
        bool stage2_noHGCal_filled = false;
        bool phase2_noHGCal_filled = false;
        bool stage2_barrel_filled = false;
        bool phase2_barrel_filled = false;
        // Stage-2 Jets
        if ( stage2JetHandle.isValid() && !use_gen_taus ) // use_gen_taus is a stand in for "Do Tau Analysis"
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                float calib_pt = s2_jet.pt() * ptAdjustStage2.Eval( s2_jet.pt() );
                float abs_eta = fabs(s2_jet.eta());
                if ( abs_eta < 6.0 && !stage2_all_filled )
                {
                    stage2_rate_all_hist->Fill( calib_pt );
                    stage2_rate_all_eta_hist->Fill( s2_jet.eta() );
                    stage2_all_filled = true;
                }
                if (( abs_eta < 1.5 || (abs_eta < 6.0 && abs_eta > 3.0)) && !stage2_noHGCal_filled )
                {
                    stage2_rate_noHGCal_hist->Fill( calib_pt );
                    stage2_noHGCal_filled = true;
                }
                if ( abs_eta < 1.5 && !stage2_barrel_filled )
                {
                    stage2_rate_barrel_hist->Fill( calib_pt );
                    stage2_rate_barrel_eta_hist->Fill( s2_jet.eta() );
                    stage2_barrel_filled = true;
                }
                if (s2_jet.pt() < 10) continue;
                treeinfo.stage2jet_pt = s2_jet.pt();
                treeinfo.stage2jet_pt_calib = calib_pt;
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

            treeinfo.stage2jet_pt = -9;
            treeinfo.stage2jet_pt_calib = -9;
            treeinfo.stage2jet_eta = -9;
            treeinfo.stage2jet_phi = -9;
            treeinfo.stage2jet_energy = -9;
            treeinfo.stage2jet_mass = -9;
            treeinfo.stage2jet_charge = -9;
            treeinfo.stage2jet_puEt = -9;
            treeinfo.stage2jet_deltaRGen = -9;

        }
        // Stage-2 Taus
        if ( stage2TauHandle.isValid() && use_gen_taus ) // use_gen_taus is a stand in for "Do Tau Analysis"
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_tau : stage2Taus)
            {
                if (fabs(s2_tau.eta()) > 3.0) continue;
                //float calib_pt = s2_tau.pt() * ptAdjustStage2.Eval( s2_tau.pt() );
                //float abs_eta = fabs(s2_tau.eta());
                //if ( abs_eta < 6.0 && !stage2_all_filled )
                //{
                //    stage2_rate_all_hist->Fill( calib_pt );
                //    stage2_rate_all_eta_hist->Fill( s2_tau.eta() );
                //    stage2_all_filled = true;
                //}
                //if (( abs_eta < 1.5 || (abs_eta < 6.0 && abs_eta > 3.0)) && !stage2_noHGCal_filled )
                //{
                //    stage2_rate_noHGCal_hist->Fill( calib_pt );
                //    stage2_noHGCal_filled = true;
                //}
                //if ( abs_eta < 1.5 && !stage2_barrel_filled )
                //{
                //    stage2_rate_barrel_hist->Fill( calib_pt );
                //    stage2_rate_barrel_eta_hist->Fill( s2_tau.eta() );
                //    stage2_barrel_filled = true;
                //}
                if (s2_tau.pt() < 10) continue;
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
                // Fill Phase-2 CaloJet with dummy values
                fill_tree_null();
            }

            treeinfo.stage2tau_pt = -9;
            treeinfo.stage2tau_eta = -9;
            treeinfo.stage2tau_phi = -9;
            treeinfo.stage2tau_energy = -9;
            treeinfo.stage2tau_mass = -9;
            treeinfo.stage2tau_charge = -9;
            treeinfo.stage2tau_hasEM = -9;
            treeinfo.stage2tau_isMerged = -9;
            treeinfo.stage2tau_isoEt = -9;
            treeinfo.stage2tau_nTT = -9;
            treeinfo.stage2tau_rawEt = -9;
            treeinfo.stage2tau_isoBit = -9;

        }
        // CaloJets/Taus
        float f_phase2_jet_HTT = 0.;
        if ( caloJets.size() > 0 )
        {
            for(const auto& caloJet : caloJets)
            {
	        // //Victor's track matching edit: added track matching condition to minBias code as well (doRate = true)
	        // float jet_phi = caloJet.experimentalParam("jet_phi");
		// float jet_eta = caloJet.experimentalParam("jet_eta");
		// float jet_energy = caloJet.experimentalParam("jet_energy");
		// bool found_jetTrack = isJetTrackMatched(jet_phi, jet_eta, jet_energy, l1trackHandle);

		// //Victor's JEF edit: added JEF threshold condition to minBias code (doRate = true)
		// float total_seed = caloJet.experimentalParam("total_seed");
		// float total_22 = caloJet.experimentalParam("total_22");
		// float total_31 = caloJet.experimentalParam("total_31");
		// float total_33 = caloJet.experimentalParam("total_33");
		// float total_42 = caloJet.experimentalParam("total_42");
		// float total_3x5 = caloJet.experimentalParam("total_3x5");

		// float crossTowerList[5] = {total_seed, total_22, total_31, total_33, total_42};
		// std::sort(crossTowerList, crossTowerList+5, std::greater<float>());
		// float max2inCross = crossTowerList[0] + crossTowerList[1];
		// float jetEnergyFraction = max2inCross/total_3x5;
		
		// float tau_pt = caloJet.experimentalParam("tau_pt");
		// bool pass_JEFThreshold = isJEFThreshold(tau_pt, jet_eta, jetEnergyFraction);
		// //End of Victor's JEF edit

	        if ( true ) //pass_JEFThreshold ) //found_jetTrack ) //Change to true to turn off track matching and JEF threshold condition
		{

		  if ( caloJet.experimentalParam("jet_pt_calibration") > 30 && fabs(caloJet.experimentalParam("jet_eta")) < 2.4 )
		    {
		      f_phase2_jet_HTT += caloJet.experimentalParam("jet_pt_calibration");
		    }

		  if (use_gen_taus && fabs(caloJet.eta()) > 3.0) continue;
		  float abs_eta = fabs( caloJet.experimentalParam("jet_eta") );
		  if ( abs_eta < 6.0 && !phase2_all_filled )
		    {
		      phase2_rate_all_hist->Fill( caloJet.experimentalParam("jet_pt") );
		      phase2_rate_all_eta_hist->Fill( caloJet.experimentalParam("jet_eta") );
		      phase2_all_filled = true;
		    }
		  if ( (abs_eta < 1.5 || (abs_eta < 6.0 && abs_eta > 3.0)) && !phase2_noHGCal_filled )
		    {
		      phase2_rate_noHGCal_hist->Fill( caloJet.experimentalParam("jet_pt") );
		      phase2_noHGCal_filled = true;
		    }
		  if ( abs_eta < 1.5 && !phase2_barrel_filled )
		    {
		      phase2_rate_barrel_hist->Fill( caloJet.experimentalParam("jet_pt") );
		      phase2_rate_barrel_eta_hist->Fill( caloJet.experimentalParam("jet_eta") );
		      phase2_barrel_filled = true;
		    }
		  if (caloJet.pt() < 10) continue;

		  // CaloTau L1EG Info
		  treeinfo.n_l1eg_HoverE_Less0p25 = 0.;
		  treeinfo.n_l1eg_HoverE_Less0p25_trkSS = 0.;
		  treeinfo.n_l1eg_HoverE_Less0p25_saSS = 0.;
		  treeinfo.n_l1eg_HoverE_0p5to1p0 = 0.;
		  treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS = 0.;
		  treeinfo.n_l1eg_HoverE_0p5to1p0_saSS = 0.;
		  treeinfo.n_l1eg_HoverE_Gtr0p25 = 0.;
		  treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS = 0.;
		  treeinfo.n_l1eg_HoverE_Gtr0p25_saSS = 0.;
		  treeinfo.n_l1eg_avgHoverE = 0.;
		  for (auto info : caloJet.associated_l1EGs())
		    {
		      //printf("l1eg pt %f, HCAL ET %f, ECAL ET %f, dEta %i, dPhi %i, trkSS %i, trkIso %i, standaloneSS %i, standaloneIso %i\n",
		      //    info[0], info[1], info[2], int(info[3]), int(info[4]), int(info[5]), int(info[6]), int(info[7]), int(info[8]));
		      float HoverE = info[1] / (info[0] + info[2]);
		      treeinfo.n_l1eg_avgHoverE += HoverE / caloJet.associated_l1EGs().size();
		      if (HoverE < 0.25)
			{
			  treeinfo.n_l1eg_HoverE_Less0p25 += 1.;
			  if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_Less0p25_trkSS += 1.;
			  if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_Less0p25_saSS += 1.;
			}
		      //else if (HoverE < 1.0)
		      //{
		      //    treeinfo.n_l1eg_HoverE_0p5to1p0 += 1.;
		      //    if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS += 1.;
		      //    if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_0p5to1p0_saSS += 1.;
		      //}
		      else if (HoverE >= 0.25)
			{
			  treeinfo.n_l1eg_HoverE_Gtr0p25 += 1.;
			  if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS += 1.;
			  if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_Gtr0p25_saSS += 1.;
			}
		    }
		  fill_tree(caloJet);

	        } //End of found_jetTrack loop
		//End of Victor's track matching edit
            } // end Calo Jets loop
        } // have CaloJets
        phase2_jet_HTT_rate_hist->Fill( f_phase2_jet_HTT );
        return;
    } // end doRate




        
  if (!doRate) {
    
    iEvent.getByToken(genHadronicTausToken_, genHTaus);
    GenJetCollection genHTauCollection = *genHTaus.product();

    // Gen Tau_h
    if ( genHTaus.isValid() )
    {
        std::sort(begin(genHTauCollection), end(genHTauCollection), [](reco::GenJet& a, reco::GenJet& b){return a.pt() > b.pt();});
    }

    // Loop over all gen jets with pt > 10 GeV and match them to Phase-II CaloJets
    // Generator info (truth)
    iEvent.getByToken(genJetsToken_,genJetsHandle);
    genJets = *genJetsHandle.product();

    // Sort gen jets
    std::sort(begin(genJets), end(genJets), [](const reco::GenJet& a, const reco::GenJet& b){return a.pt() > b.pt();});

    // Use a bool to toggel between matching to genJets and genTaus
    if (use_gen_taus)
    {
        genCollection = &genHTauCollection;
    }
    else
    {
        genCollection = &genJets;
    }


    float f_gen_jet_HTT = 0.;
    int cnt = 0;
    for (auto& genJet : *genCollection ) 
    {

        if (genJet.pt() > 30 && fabs(genJet.eta()) < 2.4)
        {
            f_gen_jet_HTT += genJet.pt();
        }

        // Skip lowest pT Jets, don't skip for low pT taus
        if (!use_gen_taus && genJet.pt() < 10) break;  // no need for continue as we sorted by pT so we're done
        if (use_gen_taus && fabs(genJet.eta()) > 3.5) continue; // HGCal ends at 3.0, so go a little further
        // HGCal detector stops at abs(eta)=3.0, keep gen jets up to 3.5
        //if ( fabs(genJet.eta())  > 3.5) continue;
        ++cnt;


        // Record DM (essentially) for the taus
        treeinfo.genTau_n_prongs = 0;
        treeinfo.genTau_n_photons = 0;
        treeinfo.genTau_pt_prongs = 0;
        treeinfo.genTau_pt_photons = 0;
        if (use_gen_taus)
        {
            for (auto& part : genJet.getGenConstituents())
            {
                //printf(" --- part idgId %i,    pt: %f     isDirectPromptTauDecayProductFinalState %i  isLastCopy %i\n", part->pdgId(), part->pt(), int(part->isDirectPromptTauDecayProductFinalState()), int(part->isLastCopy()) );
                if ( abs(part->pdgId()) == 211 && part->isDirectPromptTauDecayProductFinalState() ) 
                {
                    treeinfo.genTau_n_prongs += 1;
                    treeinfo.genTau_pt_prongs += part->pt();
                }
                if ( part->pdgId() == 22 && part->isLastCopy() )
                {
                    treeinfo.genTau_n_photons += 1;
                    treeinfo.genTau_pt_photons += part->pt();
                }
            }
            //printf(" - tau %i   pt: %f,    n_prongs %f,   n_photons %f,   pt_prongs/pt %f,    pt_photons/pt %f\n", cnt, genJet.pt(), treeinfo.genTau_n_prongs, treeinfo.genTau_n_photons, treeinfo.genTau_pt_prongs/genJet.pt(), treeinfo.genTau_pt_photons/genJet.pt() );
        }



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


            // Find stage2, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                if ( reco::deltaR( s2_jet.p4(), genJetP4 ) < genMatchDeltaRcut )
                {
                    treeinfo.stage2jet_pt = s2_jet.pt();
                    treeinfo.stage2jet_pt_calib = s2_jet.pt() * ptAdjustStage2.Eval( s2_jet.pt() );
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
            treeinfo.stage2jet_pt_calib = -9.;
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
    
    
    
        if (use_gen_taus)
        {
            treeinfo.genTau = 1.;
            treeinfo.genJet = 0.;
        }
        else
        {
            treeinfo.genTau = 0.;
            treeinfo.genJet = 1.;
        }
        treeinfo.genJet_pt = genJet.pt();
        treeinfo.genJet_eta = genJet.eta();
        treeinfo.genJet_phi = genJet.phi();
        treeinfo.genJet_energy = genJet.energy();
        treeinfo.genJet_mass = genJet.mass();
        treeinfo.genJet_charge = genJet.charge();





        // Start at zero for these.  They are not filled normally as the others.
        treeinfo.n_l1eg_HoverE_Less0p25 = -9.;
        treeinfo.n_l1eg_HoverE_Less0p25_trkSS = -9.;
        treeinfo.n_l1eg_HoverE_Less0p25_saSS = -9.;
        treeinfo.n_l1eg_HoverE_0p5to1p0 = -9.;
        treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS = -9.;
        treeinfo.n_l1eg_HoverE_0p5to1p0_saSS = -9.;
        treeinfo.n_l1eg_HoverE_Gtr0p25 = -9.;
        treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS = -9.;
        treeinfo.n_l1eg_HoverE_Gtr0p25_saSS = -9.;
        treeinfo.n_l1eg_avgHoverE = -9.;
    
        //std::cout << "    ---!!!--- L1EG Size: " << caloJets.size() << std::endl;
        bool found_caloJet = false;
        if ( caloJets.size() > 0 )
        {
            // Storing full event info
            float total_et_f = 0.0;
            float nTT_f = 0.0;
            //printf("-----\n");
            for(const auto& caloJet : caloJets)
            {

                total_et_f = caloJet.experimentalParam("total_et");
                //nTT_f = caloJet.experimentalParam("total_nTowers");

		// //Victor's track matching edit: get jet info for matching to tracks
		// float jet_phi = caloJet.experimentalParam("jet_phi");
		// float jet_eta = caloJet.experimentalParam("jet_eta");
		// float jet_energy = caloJet.experimentalParam("jet_energy");
		// bool found_jetTrack = isJetTrackMatched(jet_phi, jet_eta, jet_energy, l1trackHandle);
		// float min_dR = findClosestTrackdR(jet_phi, jet_eta, jet_energy, l1trackHandle, 0.);
		// float min_dR_2GeV = findClosestTrackdR(jet_phi, jet_eta, jet_energy, l1trackHandle, 2.);
		// float min_dR_10GeV = findClosestTrackdR(jet_phi, jet_eta, jet_energy, l1trackHandle, 10.);
		// float max_track_pt_dR0p2 = findMaxTrackPt(jet_phi, jet_eta, jet_energy, l1trackHandle, 0.2);
		// //End of Victor's track matching edit

		// //Victor's JEF edit: added JEF threshold condition
		// float total_seed = caloJet.experimentalParam("total_seed");
		// float total_22 = caloJet.experimentalParam("total_22");
		// float total_31 = caloJet.experimentalParam("total_31");
		// float total_33 = caloJet.experimentalParam("total_33");
		// float total_42 = caloJet.experimentalParam("total_42");
		// float total_3x5 = caloJet.experimentalParam("total_3x5");

		// float crossTowerList[5] = {total_seed, total_22, total_31, total_33, total_42};
		// std::sort(crossTowerList, crossTowerList+5, std::greater<float>());
		// float max2inCross = crossTowerList[0] + crossTowerList[1];
		// float jetEnergyFraction = max2inCross/total_3x5;

		// float tau_pt = caloJet.experimentalParam("tau_pt");
		// bool pass_JEFThreshold = isJEFThreshold(tau_pt, jet_eta, jetEnergyFraction);
		// //End of Victor's JEF edit

		if ( reco::deltaR(caloJet, genJetP4) < genMatchDeltaRcut )// && pass_JEFThreshold )// && found_jetTrack ) //Victor's track matching edit: added track matching condition found_jetTrack == true. 
                      //&& fabs(caloJet.pt()-genJetP4.pt())/genJetP4.pt() < genMatchRelPtcut )
                {

		    // Victor's edit: store min_dR in event tree for each reco tau jet and max_track_pt for each matched track
		    // treeinfo.jet_and_track_dR = min_dR; 
		    // treeinfo.jet_and_track_dR_2GeV = min_dR_2GeV; 
		    // treeinfo.jet_and_track_dR_10GeV = min_dR_10GeV; 
		    // treeinfo.max_track_pt_dR0p2 = max_track_pt_dR0p2;

                    treeinfo.n_l1eg_HoverE_Less0p25 = 0.;
                    treeinfo.n_l1eg_HoverE_Less0p25_trkSS = 0.;
                    treeinfo.n_l1eg_HoverE_Less0p25_saSS = 0.;
                    treeinfo.n_l1eg_HoverE_0p5to1p0 = 0.;
                    treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS = 0.;
                    treeinfo.n_l1eg_HoverE_0p5to1p0_saSS = 0.;
                    treeinfo.n_l1eg_HoverE_Gtr0p25 = 0.;
                    treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS = 0.;
                    treeinfo.n_l1eg_HoverE_Gtr0p25_saSS = 0.;
                    treeinfo.n_l1eg_avgHoverE = 0.;
                    for (auto info : caloJet.associated_l1EGs())
                    {
                        //printf("l1eg pt %f, HCAL ET %f, ECAL ET %f, dEta %i, dPhi %i, trkSS %i, trkIso %i, standaloneSS %i, standaloneIso %i\n",
                        //    info[0], info[1], info[2], int(info[3]), int(info[4]), int(info[5]), int(info[6]), int(info[7]), int(info[8]));
                        float HoverE = info[1] / (info[0] + info[2]);
                        treeinfo.n_l1eg_avgHoverE += HoverE / caloJet.associated_l1EGs().size();
                        if (HoverE < 0.25)
                        {
                            treeinfo.n_l1eg_HoverE_Less0p25 += 1.;
                            if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_Less0p25_trkSS += 1.;
                            if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_Less0p25_saSS += 1.;
                        }
                        //else if (HoverE < 1.0)
                        //{
                        //    treeinfo.n_l1eg_HoverE_0p5to1p0 += 1.;
                        //    if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_0p5to1p0_trkSS += 1.;
                        //    if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_0p5to1p0_saSS += 1.;
                        //}
                        else if (HoverE >= 0.25)
                        {
                            treeinfo.n_l1eg_HoverE_Gtr0p25 += 1.;
                            if (int(info[5]) > 0.5) treeinfo.n_l1eg_HoverE_Gtr0p25_trkSS += 1.;
                            if (int(info[7]) > 0.5) treeinfo.n_l1eg_HoverE_Gtr0p25_saSS += 1.;
                        }
                    }

                    if ( debug ) std::cout << "using caloJet dr = " << reco::deltaR(caloJet, genJetP4) << std::endl;
                    treeinfo.deltaR = reco::deltaR(caloJet, genJetP4);
                    treeinfo.deltaPhi = reco::deltaPhi(caloJet, genJetP4);
                    treeinfo.deltaEta = genJetP4.eta()-caloJet.eta();
                    if (treeinfo.stage2tau_eta != -9)
                    {
                        treeinfo.deltaR_phase2_stage2 = reco::deltaR( treeinfo.stage2tau_eta, treeinfo.stage2tau_phi, caloJet.eta(), caloJet.phi() );
                    }
                    

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
        if (caloJets.size() == 0)// || !found_caloJet) //Victor's track matching edit: removed !found_caloJet condition so that unmatched genJets are not double counted 
        {
            // Fill tree with -1 to signify we lose a gen jet        
            fill_tree_null();
        }

    } // end GenJets loop



    // Fill gen Jet HTT hists for all events
    gen_jet_HTT->Fill( f_gen_jet_HTT );

    // Need to loop over all Phase-2 CaloJets without matching to genJets
    float f_phase2_jet_HTT = 0.;
    if ( caloJets.size() > 0 )
    {
        for(const auto& caloJet : caloJets)
        {
            if (caloJet.experimentalParam("jet_pt_calibration") > 30 && fabs(caloJet.experimentalParam("jet_eta")) < 2.4)
            {
                f_phase2_jet_HTT += caloJet.experimentalParam("jet_pt_calibration");
            }
        }
    }
    // Fill simulating a Jet_HTT_300 threshold
    if (f_phase2_jet_HTT > 300)
    {
        phase2_jet_HTT_300->Fill( f_gen_jet_HTT );
    }
    // Fill simulating a Jet_HTT_400 threshold
    if (f_phase2_jet_HTT > 400)
    {
        phase2_jet_HTT_400->Fill( f_gen_jet_HTT );
    }
    // Fill simulating a Jet_HTT_500 threshold
    if (f_phase2_jet_HTT > 500)
    {
        phase2_jet_HTT_500->Fill( f_gen_jet_HTT );
    }
    // Fill simulating a Jet_HTT_600 threshold
    if (f_phase2_jet_HTT > 600)
    {
        phase2_jet_HTT_600->Fill( f_gen_jet_HTT );
    }



  } // end if NOT doRate
    if (debug) printf("Ending L1CaloJetStudies Analyzer\n");


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
        integrateDown( phase2_rate_noHGCal_hist );
        integrateDown( stage2_rate_noHGCal_hist );
        integrateDown( phase2_rate_barrel_hist );
        integrateDown( stage2_rate_barrel_hist );
        integrateDown( phase2_jet_HTT_rate_hist );
    }
    phase2_jet_HTT_300->Divide( gen_jet_HTT );
    phase2_jet_HTT_400->Divide( gen_jet_HTT );
    phase2_jet_HTT_500->Divide( gen_jet_HTT );
    phase2_jet_HTT_600->Divide( gen_jet_HTT );
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

void 
L1CaloJetStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------

void 
L1CaloJetStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------

void 
L1CaloJetStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1CaloJetStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods (vshang)
// //Victor's track matching edit: method isJetTrackMatched takes in a jet's phi, eta, and energy as well as a track handle l1trackHandle and
// //returns true if the jet is matched to a track and false otherwise. The jet must be within a certian dR of the
// //track and the track pt and chi2 must pass certain selection cuts.
// bool 
// L1CaloJetStudies::isJetTrackMatched(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle) {
//     if ( l1trackHandle.isValid() )
//     {
//         // cout << "track Handle is valid";
//         float dR_cut = 0.2;
//         float pt_cut = 10.;
//         //float chi2_cut = 100.;
// 	for(size_t track_index=0; track_index < l1trackHandle->size(); ++track_index)
// 	{
// 	    edm::Ptr< TTTrack< Ref_Phase2TrackerDigi_ > > ptr(l1trackHandle, track_index);
//             float pt = ptr->getMomentum().perp();
//             float dR = L1TkElectronTrackMatchAlgo::deltaR(L1TkElectronTrackMatchAlgo::calorimeterPosition(jet_phi, jet_eta, jet_energy), ptr);
// 	    //float chi2 = ptr->getChi2();
// 	    if ( dR < dR_cut && pt > pt_cut )// && chi2 < chi2_cut )
// 	    {
// 	        // cout << "jet is matched";
// 	        return true;
// 	    }
// 	} //end track loop
//     } //end isValid
//     // cout << "jet fails matching";
//     return false;
// }

// //method findClosestTrackdR takes in a jet's phi, eta, and energy as well as a track handle l1trackHandle and a track pt cut and
// //returns the minimum dR between the jet and all the tracks with pt > pt_cut. Used to study the dR distribution of reco jets.
// float 
// L1CaloJetStudies::findClosestTrackdR(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle, float pt_cut) {
//     float min_dR = 9999.0;
//     if ( l1trackHandle.isValid() )
//     {
//         // cout << "track Handle is valid";
// 	for(size_t track_index=0; track_index < l1trackHandle->size(); ++track_index)
// 	{
// 	    edm::Ptr< TTTrack< Ref_Phase2TrackerDigi_ > > ptr(l1trackHandle, track_index);
// 	    float pt = ptr->getMomentum().perp();
//             float dR = L1TkElectronTrackMatchAlgo::deltaR(L1TkElectronTrackMatchAlgo::calorimeterPosition(jet_phi, jet_eta, jet_energy), ptr);
// 	    if ( dR < min_dR and pt > pt_cut)
// 	    {
// 	        // cout << "jet is matched";
// 	        min_dR = dR;
// 	    }
// 	} //end track loop
//     } //end isValid
//     // cout << "jet fails matching";
//     return min_dR;
// }

// //method findMaxTrackPt takes in a jet's phi, eta, and energy as well as a track handle l1trackHandle and a track dR cut and
// //returns the track with the highest pT with dR < dR_cut. Used to study the pT distribution of matched tracks.
// float 
// L1CaloJetStudies::findMaxTrackPt(float jet_phi, float jet_eta, float jet_energy, edm::Handle<L1TkTrackCollectionType> l1trackHandle, float dR_cut) {
//     float max_pt = -9.0;
//     if ( l1trackHandle.isValid() )
//     {
//         // cout << "track Handle is valid";
// 	for(size_t track_index=0; track_index < l1trackHandle->size(); ++track_index)
// 	{
// 	    edm::Ptr< TTTrack< Ref_Phase2TrackerDigi_ > > ptr(l1trackHandle, track_index);
// 	    float pt = ptr->getMomentum().perp();
//             float dR = L1TkElectronTrackMatchAlgo::deltaR(L1TkElectronTrackMatchAlgo::calorimeterPosition(jet_phi, jet_eta, jet_energy), ptr);
// 	    if ( pt > max_pt and dR < dR_cut )
// 	    {
// 	        // cout << "jet is matched";
// 	        max_pt = pt;
// 	    }
// 	} //end track loop
//     } //end isValid
//     // cout << "jet fails matching";
//     return max_pt;
// }
// //End of Victor's track matching edit

// //Victor's JEF edit: method isJEFThreshold takes in a tau jet's pt, eta, and jet energy fraction value and returns true if 
// // max2inCross is greater than some threshold between 0 and 1 based on the tau jet pt and eta, where max2inCross is 
// // a jet energy fraction variable used to distinguish between ggHTT and QCD samples. If the eta is outside the endcap region 
// // (eta > 2.6), we do not put a threshold at all (return true by default).
// bool 
// L1CaloJetStudies::isJEFThreshold(float jet_pt, float jet_eta, float jetEnergyFraction) {
//     cout << "jet pt: " << jet_pt << endl;
//     cout << "jet eta: " << jet_eta << endl;
//     cout << "abs(jet eta): " << fabs(jet_eta) << endl;
//     cout << "JEF: " << jetEnergyFraction << endl;
//     if ( fabs(jet_eta) < 1.6 )
//     {
//       cout << "abs(jet_eta) < 1.6\n";
//         if ( jet_pt < 40. ) 
// 	{
// 	    cout << "jet_pt < 40\n";
// 	    if ( jetEnergyFraction < 0.8 ) 
// 	    {
// 	        cout << "JEF < 0.8\n";
// 	        return false;
// 	    }
// 	}
// 	else if ( jet_pt > 40. && jet_pt < 60. ) 
// 	{
// 	    cout << "40 < jet_pt < 60\n";
// 	    if ( jetEnergyFraction < 0.8 ) 
// 	    {
// 	        cout << "JEF < 0.8\n";
// 	        return false;
// 	    }
// 	}
// 	else if ( jet_pt > 60. ) 
// 	{
// 	    cout << "jet_pt > 60\n";
// 	    if ( jetEnergyFraction < 0.85 ) 
// 	    {
// 	        cout << "JEF < 0.85\n";
// 	        return false;
// 	    }
// 	}
//     }
//     else if ( fabs(jet_eta) > 1.6 && fabs(jet_eta) < 2.8 )
//     {
//         cout << "1.6 < abs(jet_eta) < 2.8\n";
//         if ( jet_pt < 40. ) 
// 	{
// 	    cout << "jet_pt < 40\n";
// 	    if ( jetEnergyFraction < 0.65 ) 
// 	    {
// 	        cout << "JEF < 0.65\n";
// 	        return false;
// 	    }
// 	}
// 	else if ( jet_pt > 40. && jet_pt < 60. ) 
// 	{
// 	    cout << "40 < jet_pt < 60\n";
// 	    if ( jetEnergyFraction < 0.65 ) 
// 	    {
// 	        cout << "JEF < 0.65\n";
// 	        return false;
// 	    }
// 	}
// 	else if ( jet_pt > 60. ) 
// 	{
// 	    cout << "jet_pt > 60\n";
// 	    if ( jetEnergyFraction < 0.75 ) 
// 	    {
// 	        cout << "JEF < 0.75\n";
// 	        return false;
// 	    }
// 	}
//     }
//     cout << "all pt and eta checks failed\n";
//     return true;
// }
// //End of Victor's JEF edit


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
L1CaloJetStudies::fill_tree(const l1tp2::CaloJet& caloJet) {
    // PU Vars
    treeinfo.total_et = caloJet.experimentalParam("total_et");
    //treeinfo.total_nTowers = caloJet.experimentalParam("total_nTowers");

    // As of 28 May 2018 caloJet_pt is post-calibration
    treeinfo.ecal_pt = caloJet.experimentalParam("ecal_pt");
    treeinfo.ecal_seed = caloJet.experimentalParam("ecal_seed");
    treeinfo.l1eg_pt = caloJet.experimentalParam("l1eg_pt");
    treeinfo.l1eg_seed = caloJet.experimentalParam("l1eg_seed");
    //treeinfo.ecal_eta = caloJet.experimentalParam("ecal_eta");
    //treeinfo.ecal_phi = caloJet.experimentalParam("ecal_phi");
    //treeinfo.ecal_mass = caloJet.experimentalParam("ecal_mass");
    //treeinfo.ecal_energy = caloJet.experimentalParam("ecal_energy");
    //treeinfo.ecal_L1EG_jet_eta = caloJet.experimentalParam("ecal_L1EG_jet_eta");
    //treeinfo.ecal_L1EG_jet_phi = caloJet.experimentalParam("ecal_L1EG_jet_phi");
    //treeinfo.ecal_L1EG_jet_energy = caloJet.experimentalParam("ecal_L1EG_jet_energy");
    treeinfo.hcal_pt = caloJet.experimentalParam("hcal_pt");
    treeinfo.hcal_seed = caloJet.experimentalParam("hcal_seed");
    treeinfo.hcal_calibration = caloJet.experimentalParam("hcal_calibration");
    treeinfo.hcal_pt_calibration = caloJet.experimentalParam("hcal_pt_calibration");
    //treeinfo.hcal_eta = caloJet.experimentalParam("hcal_eta");
    //treeinfo.hcal_phi = caloJet.experimentalParam("hcal_phi");
    //treeinfo.hcal_mass = caloJet.experimentalParam("hcal_mass");
    //treeinfo.hcal_energy = caloJet.experimentalParam("hcal_energy");
    treeinfo.jet_pt = caloJet.experimentalParam("jet_pt");
    treeinfo.jet_pt_calibration = caloJet.experimentalParam("jet_pt_calibration");
    //treeinfo.transition_calibration = caloJet.experimentalParam("transition_calibration");
    treeinfo.transition_calibration = -9;
    treeinfo.jet_eta = caloJet.experimentalParam("jet_eta");
    treeinfo.jet_phi = caloJet.experimentalParam("jet_phi");
    treeinfo.jet_mass = caloJet.experimentalParam("jet_mass");
    treeinfo.jet_energy = caloJet.experimentalParam("jet_energy");
    treeinfo.hovere = caloJet.hovere();
    treeinfo.seed_pt = caloJet.experimentalParam("seed_pt");
    treeinfo.seed_iEta = caloJet.experimentalParam("seed_iEta");
    treeinfo.seed_iPhi = caloJet.experimentalParam("seed_iPhi");
    treeinfo.seed_eta = caloJet.experimentalParam("seed_eta");
    treeinfo.seed_phi = caloJet.experimentalParam("seed_phi");
    treeinfo.seed_energy = caloJet.experimentalParam("seed_energy");
    treeinfo.hcal_nHits = caloJet.experimentalParam("hcal_nHits");

    // //Victor's edit: fill tree branches for additional tower congifurations
    // treeinfo.hcal_3x3 = caloJet.experimentalParam("hcal_3x3");
    // treeinfo.hcal_1x3 = caloJet.experimentalParam("hcal_1x3");
    // treeinfo.hcal_3x1 = caloJet.experimentalParam("hcal_3x1");
    // treeinfo.hcal_Cross = caloJet.experimentalParam("hcal_Cross");
    // treeinfo.hcal_X = caloJet.experimentalParam("hcal_X");

    // treeinfo.ecal_3x3 = caloJet.experimentalParam("ecal_3x3");
    // treeinfo.ecal_1x3 = caloJet.experimentalParam("ecal_1x3");
    // treeinfo.ecal_3x1 = caloJet.experimentalParam("ecal_3x1");
    // treeinfo.ecal_Cross = caloJet.experimentalParam("ecal_Cross");
    // treeinfo.ecal_X = caloJet.experimentalParam("ecal_X");

    // treeinfo.l1eg_3x3 = caloJet.experimentalParam("l1eg_3x3");
    // treeinfo.l1eg_1x3 = caloJet.experimentalParam("l1eg_1x3");
    // treeinfo.l1eg_3x1 = caloJet.experimentalParam("l1eg_3x1");
    // treeinfo.l1eg_Cross = caloJet.experimentalParam("l1eg_Cross");
    // treeinfo.l1eg_X = caloJet.experimentalParam("l1eg_X");

    // treeinfo.total_3x3 = caloJet.experimentalParam("total_3x3");
    // treeinfo.total_1x3 = caloJet.experimentalParam("total_1x3");
    // treeinfo.total_3x1 = caloJet.experimentalParam("total_3x1");
    // treeinfo.total_Cross = caloJet.experimentalParam("total_Cross");
    // treeinfo.total_X = caloJet.experimentalParam("total_X");

    // treeinfo.total_7x7 = caloJet.experimentalParam("total_7x7");
    // treeinfo.total_3x5 = caloJet.experimentalParam("total_3x5");

    // //Fill branches with individual tower energies in 3x5 array. 11 corresponds to lower left corner (least eta, least phi)
    // treeinfo.hcal_11 = caloJet.experimentalParam("hcal_11");
    // treeinfo.hcal_12 = caloJet.experimentalParam("hcal_12");
    // treeinfo.hcal_13 = caloJet.experimentalParam("hcal_13");
    // treeinfo.hcal_21 = caloJet.experimentalParam("hcal_21");
    // treeinfo.hcal_22 = caloJet.experimentalParam("hcal_22");
    // treeinfo.hcal_23 = caloJet.experimentalParam("hcal_23");
    // treeinfo.hcal_31 = caloJet.experimentalParam("hcal_31");
    // treeinfo.hcal_33 = caloJet.experimentalParam("hcal_33");
    // treeinfo.hcal_41 = caloJet.experimentalParam("hcal_41");
    // treeinfo.hcal_42 = caloJet.experimentalParam("hcal_42");
    // treeinfo.hcal_43 = caloJet.experimentalParam("hcal_43");
    // treeinfo.hcal_51 = caloJet.experimentalParam("hcal_51");
    // treeinfo.hcal_52 = caloJet.experimentalParam("hcal_52");
    // treeinfo.hcal_53 = caloJet.experimentalParam("hcal_53");

    // treeinfo.ecal_11 = caloJet.experimentalParam("ecal_11");
    // treeinfo.ecal_12 = caloJet.experimentalParam("ecal_12");
    // treeinfo.ecal_13 = caloJet.experimentalParam("ecal_13");
    // treeinfo.ecal_21 = caloJet.experimentalParam("ecal_21");
    // treeinfo.ecal_22 = caloJet.experimentalParam("ecal_22");
    // treeinfo.ecal_23 = caloJet.experimentalParam("ecal_23");
    // treeinfo.ecal_31 = caloJet.experimentalParam("ecal_31");
    // treeinfo.ecal_33 = caloJet.experimentalParam("ecal_33");
    // treeinfo.ecal_41 = caloJet.experimentalParam("ecal_41");
    // treeinfo.ecal_42 = caloJet.experimentalParam("ecal_42");
    // treeinfo.ecal_43 = caloJet.experimentalParam("ecal_43");
    // treeinfo.ecal_51 = caloJet.experimentalParam("ecal_51");
    // treeinfo.ecal_52 = caloJet.experimentalParam("ecal_52");
    // treeinfo.ecal_53 = caloJet.experimentalParam("ecal_53");

    // treeinfo.l1eg_11 = caloJet.experimentalParam("l1eg_11");
    // treeinfo.l1eg_12 = caloJet.experimentalParam("l1eg_12");
    // treeinfo.l1eg_13 = caloJet.experimentalParam("l1eg_13");
    // treeinfo.l1eg_21 = caloJet.experimentalParam("l1eg_21");
    // treeinfo.l1eg_22 = caloJet.experimentalParam("l1eg_22");
    // treeinfo.l1eg_23 = caloJet.experimentalParam("l1eg_23");
    // treeinfo.l1eg_31 = caloJet.experimentalParam("l1eg_31");
    // treeinfo.l1eg_33 = caloJet.experimentalParam("l1eg_33");
    // treeinfo.l1eg_41 = caloJet.experimentalParam("l1eg_41");
    // treeinfo.l1eg_42 = caloJet.experimentalParam("l1eg_42");
    // treeinfo.l1eg_43 = caloJet.experimentalParam("l1eg_43");
    // treeinfo.l1eg_51 = caloJet.experimentalParam("l1eg_51");
    // treeinfo.l1eg_52 = caloJet.experimentalParam("l1eg_52");
    // treeinfo.l1eg_53 = caloJet.experimentalParam("l1eg_53");

    // treeinfo.total_seed = caloJet.experimentalParam("total_seed");
    // treeinfo.total_11 = caloJet.experimentalParam("total_11");
    // treeinfo.total_12 = caloJet.experimentalParam("total_12");
    // treeinfo.total_13 = caloJet.experimentalParam("total_13");
    // treeinfo.total_21 = caloJet.experimentalParam("total_21");
    // treeinfo.total_22 = caloJet.experimentalParam("total_22");
    // treeinfo.total_23 = caloJet.experimentalParam("total_23");
    // treeinfo.total_31 = caloJet.experimentalParam("total_31");
    // treeinfo.total_33 = caloJet.experimentalParam("total_33");
    // treeinfo.total_41 = caloJet.experimentalParam("total_41");
    // treeinfo.total_42 = caloJet.experimentalParam("total_42");
    // treeinfo.total_43 = caloJet.experimentalParam("total_43");
    // treeinfo.total_51 = caloJet.experimentalParam("total_51");
    // treeinfo.total_52 = caloJet.experimentalParam("total_52");
    // treeinfo.total_53 = caloJet.experimentalParam("total_53");
    // //End of Victor's edit

    //treeinfo.hcal_3x3 = caloJet.experimentalParam("hcal_3x3");
    treeinfo.hcal_3x5 = caloJet.experimentalParam("hcal_3x5");
    //treeinfo.hcal_5x5 = caloJet.experimentalParam("hcal_5x5");
    //treeinfo.hcal_5x7 = caloJet.experimentalParam("hcal_5x7");
    treeinfo.hcal_7x7 = caloJet.experimentalParam("hcal_7x7");
    //treeinfo.hcal_2x2 = caloJet.experimentalParam("hcal_2x2");
    //treeinfo.hcal_2x3 = caloJet.experimentalParam("hcal_2x3");
    //treeinfo.ecal_3x3 = caloJet.experimentalParam("ecal_3x3");
    treeinfo.ecal_3x5 = caloJet.experimentalParam("ecal_3x5");
    //treeinfo.ecal_5x5 = caloJet.experimentalParam("ecal_5x5");
    //treeinfo.ecal_5x7 = caloJet.experimentalParam("ecal_5x7");
    treeinfo.ecal_7x7 = caloJet.experimentalParam("ecal_7x7");
    //treeinfo.ecal_2x2 = caloJet.experimentalParam("ecal_2x2");
    //treeinfo.ecal_2x3 = caloJet.experimentalParam("ecal_2x3");
    //treeinfo.l1eg_3x3 = caloJet.experimentalParam("l1eg_3x3");
    treeinfo.l1eg_3x5 = caloJet.experimentalParam("l1eg_3x5");
    //treeinfo.l1eg_5x5 = caloJet.experimentalParam("l1eg_5x5");
    //treeinfo.l1eg_5x7 = caloJet.experimentalParam("l1eg_5x7");
    treeinfo.l1eg_7x7 = caloJet.experimentalParam("l1eg_7x7");
    //treeinfo.l1eg_2x2 = caloJet.experimentalParam("l1eg_2x2");
    //treeinfo.l1eg_2x3 = caloJet.experimentalParam("l1eg_2x3");
    treeinfo.ecal_nHits = caloJet.experimentalParam("ecal_nHits");
    treeinfo.l1eg_nHits = caloJet.experimentalParam("l1eg_nHits");
    //treeinfo.ecal_leading_pt = caloJet.experimentalParam("ecal_leading_pt");
    //treeinfo.ecal_leading_eta = caloJet.experimentalParam("ecal_leading_eta");
    //treeinfo.ecal_leading_phi = caloJet.experimentalParam("ecal_leading_phi");
    //treeinfo.ecal_leading_energy = caloJet.experimentalParam("ecal_leading_energy");
    //treeinfo.ecal_dR0p05 = caloJet.experimentalParam("ecal_dR0p05");
    //treeinfo.ecal_dR0p075 = caloJet.experimentalParam("ecal_dR0p075");
    //treeinfo.ecal_dR0p1 = caloJet.experimentalParam("ecal_dR0p1");
    //treeinfo.ecal_dR0p125 = caloJet.experimentalParam("ecal_dR0p125");
    //treeinfo.ecal_dR0p15 = caloJet.experimentalParam("ecal_dR0p15");
    //treeinfo.ecal_dR0p2 = caloJet.experimentalParam("ecal_dR0p2");
    //treeinfo.ecal_dR0p3 = caloJet.experimentalParam("ecal_dR0p3");
    //treeinfo.ecal_dR0p4 = caloJet.experimentalParam("ecal_dR0p4");
    //treeinfo.ecal_dR0p1_leading = caloJet.experimentalParam("ecal_dR0p1_leading");
    treeinfo.l1eg_nL1EGs = caloJet.experimentalParam("l1eg_nL1EGs");
    treeinfo.l1eg_nL1EGs_standaloneSS = caloJet.experimentalParam("l1eg_nL1EGs_standaloneSS");
    treeinfo.l1eg_nL1EGs_standaloneIso = caloJet.experimentalParam("l1eg_nL1EGs_standaloneIso");
    treeinfo.l1eg_nL1EGs_trkMatchSS = caloJet.experimentalParam("l1eg_nL1EGs_trkMatchSS");
    treeinfo.l1eg_nL1EGs_trkMatchIso = caloJet.experimentalParam("l1eg_nL1EGs_trkMatchIso");
    treeinfo.n_l1eg_HoverE_LessThreshold = caloJet.experimentalParam("n_l1eg_HoverE_LessThreshold");

    treeinfo.tau_pt = caloJet.experimentalParam("tau_pt");
    treeinfo.tau_pt_calibration_value = caloJet.experimentalParam("tau_pt_calibration_value");
    treeinfo.tau_iso_et = caloJet.experimentalParam("tau_iso_et");
    treeinfo.tau_total_iso_et = caloJet.experimentalParam("tau_total_iso_et");
    treeinfo.loose_iso_tau_wp = caloJet.experimentalParam("loose_iso_tau_wp");

    //treeinfo.deltaR_ecal_vs_jet = caloJet.experimentalParam("deltaR_ecal_vs_jet");
    //treeinfo.deltaR_hcal_vs_jet = caloJet.experimentalParam("deltaR_hcal_vs_jet");
    //treeinfo.deltaR_L1EGjet_vs_jet = caloJet.experimentalParam("deltaR_L1EGjet_vs_jet");
    ////treeinfo.deltaR_hcal_vs_seed = caloJet.experimentalParam("deltaR_hcal_vs_seed");
    //treeinfo.deltaR_ecal_vs_hcal = caloJet.experimentalParam("deltaR_ecal_vs_hcal");
    //treeinfo.deltaR_ecal_vs_seed = caloJet.experimentalParam("deltaR_ecal_vs_seed");
    //treeinfo.deltaR_ecal_lead_vs_jet = caloJet.experimentalParam("deltaR_ecal_lead_vs_jet");
    //treeinfo.deltaR_ecal_lead_vs_ecal = caloJet.experimentalParam("deltaR_ecal_lead_vs_ecal");
    tree->Fill();
}


void
L1CaloJetStudies::fill_tree_null() {
    // Fill with -9 with no CaloJet fround
    treeinfo.total_et = -9;
    //treeinfo.total_nTowers = -9;

    treeinfo.ecal_pt = -9;
    treeinfo.ecal_seed = -9;
    treeinfo.l1eg_pt = -9;
    treeinfo.l1eg_seed = -9;
    //treeinfo.ecal_eta = -9;
    //treeinfo.ecal_phi = -9;
    //treeinfo.ecal_mass = -9;
    //treeinfo.ecal_energy = -9;
    //treeinfo.ecal_L1EG_jet_eta = -9;
    //treeinfo.ecal_L1EG_jet_phi = -9;
    //treeinfo.ecal_L1EG_jet_energy = -9;
    treeinfo.hcal_pt = -9;
    treeinfo.hcal_seed = -9;
    treeinfo.hcal_calibration = -9;
    treeinfo.hcal_pt_calibration = -9;
    //treeinfo.hcal_eta = -9;
    //treeinfo.hcal_phi = -9;
    //treeinfo.hcal_mass = -9;
    //treeinfo.hcal_energy = -9;
    treeinfo.jet_pt = -9;
    treeinfo.jet_pt_calibration = -9;
    treeinfo.transition_calibration = -9;
    treeinfo.jet_eta = -9;
    treeinfo.jet_phi = -9;
    treeinfo.jet_mass = -9;
    treeinfo.jet_energy = -9;
    treeinfo.hovere = -9;
    treeinfo.seed_pt = -9;
    treeinfo.seed_iEta = -99;
    treeinfo.seed_iPhi = -99;
    treeinfo.seed_eta = -9;
    treeinfo.seed_phi = -9;
    treeinfo.seed_energy = -9;
    treeinfo.hcal_nHits = -9;
    //treeinfo.hcal_3x3 = -9;
    treeinfo.hcal_3x5 = -9;

    // //Victor's edit: fill null tree for additional tower configurations
    // treeinfo.hcal_3x3 = -9;
    // treeinfo.hcal_1x3 = -9;
    // treeinfo.hcal_3x1 = -9;
    // treeinfo.hcal_Cross = -9;
    // treeinfo.hcal_X = -9;

    // treeinfo.ecal_3x3 = -9;
    // treeinfo.ecal_1x3 = -9;
    // treeinfo.ecal_3x1 = -9;
    // treeinfo.ecal_Cross = -9;
    // treeinfo.ecal_X = -9;

    // treeinfo.l1eg_3x3 = -9;
    // treeinfo.l1eg_1x3 = -9;
    // treeinfo.l1eg_3x1 = -9;
    // treeinfo.l1eg_Cross = -9;
    // treeinfo.l1eg_X = -9;

    // treeinfo.total_3x3 = -9; 
    // treeinfo.total_1x3 = -9;
    // treeinfo.total_3x1 = -9;
    // treeinfo.total_Cross = -9;
    // treeinfo.total_X = -9;

    // treeinfo.total_7x7 = -9;
    // treeinfo.total_3x5 = -9;

    // //Fill null branches with individual tower energies in 3x5 array. 11 corresponds to lower left corner (least eta, least phi)
    // treeinfo.hcal_11 = -9;
    // treeinfo.hcal_12 = -9;
    // treeinfo.hcal_13 = -9;
    // treeinfo.hcal_21 = -9;
    // treeinfo.hcal_22 = -9;
    // treeinfo.hcal_23 = -9;
    // treeinfo.hcal_31 = -9;
    // treeinfo.hcal_33 = -9;
    // treeinfo.hcal_41 = -9;
    // treeinfo.hcal_42 = -9;
    // treeinfo.hcal_43 = -9;
    // treeinfo.hcal_51 = -9;
    // treeinfo.hcal_52 = -9;
    // treeinfo.hcal_53 = -9;

    // treeinfo.ecal_11 = -9;
    // treeinfo.ecal_12 = -9;
    // treeinfo.ecal_13 = -9;
    // treeinfo.ecal_21 = -9;
    // treeinfo.ecal_22 = -9;
    // treeinfo.ecal_23 = -9;
    // treeinfo.ecal_31 = -9;
    // treeinfo.ecal_33 = -9;
    // treeinfo.ecal_41 = -9;
    // treeinfo.ecal_42 = -9;
    // treeinfo.ecal_43 = -9;
    // treeinfo.ecal_51 = -9;
    // treeinfo.ecal_52 = -9;
    // treeinfo.ecal_53 = -9;

    // treeinfo.l1eg_11 = -9;
    // treeinfo.l1eg_12 = -9;
    // treeinfo.l1eg_13 = -9;
    // treeinfo.l1eg_21 = -9;
    // treeinfo.l1eg_22 = -9;
    // treeinfo.l1eg_23 = -9;
    // treeinfo.l1eg_31 = -9;
    // treeinfo.l1eg_33 = -9;
    // treeinfo.l1eg_41 = -9;
    // treeinfo.l1eg_42 = -9;
    // treeinfo.l1eg_43 = -9;
    // treeinfo.l1eg_51 = -9;
    // treeinfo.l1eg_52 = -9;
    // treeinfo.l1eg_53 = -9;

    // treeinfo.total_seed = -9;
    // treeinfo.total_11 = -9;
    // treeinfo.total_12 = -9;
    // treeinfo.total_13 = -9;
    // treeinfo.total_21 = -9;
    // treeinfo.total_22 = -9;
    // treeinfo.total_23 = -9;
    // treeinfo.total_31 = -9;
    // treeinfo.total_33 = -9;
    // treeinfo.total_41 = -9;
    // treeinfo.total_42 = -9;
    // treeinfo.total_43 = -9;
    // treeinfo.total_51 = -9;
    // treeinfo.total_52 = -9;
    // treeinfo.total_53 = -9;

    // treeinfo.jet_and_track_dR = -9; 
    // treeinfo.jet_and_track_dR_2GeV = -9;
    // treeinfo.jet_and_track_dR_10GeV = -9; 
    // treeinfo.max_track_pt_dR0p2 = -9;
    // //End of Victor's edit

    //treeinfo.hcal_5x5 = -9;
    //treeinfo.hcal_5x7 = -9;
    treeinfo.hcal_7x7 = -9;
    //treeinfo.hcal_2x2 = -9;
    //treeinfo.hcal_2x3 = -9;
    //treeinfo.ecal_3x3 = -9;
    treeinfo.ecal_3x5 = -9;
    //treeinfo.ecal_5x5 = -9;
    //treeinfo.ecal_5x7 = -9;
    treeinfo.ecal_7x7 = -9;
    //treeinfo.ecal_2x2 = -9;
    //treeinfo.ecal_2x3 = -9;
    //treeinfo.l1eg_3x3 = -9;
    treeinfo.l1eg_3x5 = -9;
    //treeinfo.l1eg_5x5 = -9;
    //treeinfo.l1eg_5x7 = -9;
    treeinfo.l1eg_7x7 = -9;
    //treeinfo.l1eg_2x2 = -9;
    //treeinfo.l1eg_2x3 = -9;
    treeinfo.ecal_nHits = -9;
    treeinfo.l1eg_nHits = -9;
    //treeinfo.ecal_leading_pt = -9;
    //treeinfo.ecal_leading_eta = -9;
    //treeinfo.ecal_leading_phi = -9;
    //treeinfo.ecal_leading_energy = -9;
    //treeinfo.ecal_dR0p05 = -9;
    //treeinfo.ecal_dR0p075 = -9;
    //treeinfo.ecal_dR0p1 = -9;
    //treeinfo.ecal_dR0p125 = -9;
    //treeinfo.ecal_dR0p15 = -9;
    //treeinfo.ecal_dR0p2 = -9;
    //treeinfo.ecal_dR0p3 = -9;
    //treeinfo.ecal_dR0p4 = -9;
    //treeinfo.ecal_dR0p1_leading = -9;
    treeinfo.l1eg_nL1EGs = -9;
    treeinfo.l1eg_nL1EGs_standaloneSS = -9;
    treeinfo.l1eg_nL1EGs_standaloneIso = -9;
    treeinfo.l1eg_nL1EGs_trkMatchSS = -9;
    treeinfo.l1eg_nL1EGs_trkMatchIso = -9;
    treeinfo.n_l1eg_HoverE_LessThreshold = -9;
    treeinfo.tau_pt = -9;
    treeinfo.tau_pt_calibration_value = -9;
    treeinfo.tau_iso_et = -9;
    treeinfo.tau_total_iso_et = -9;
    treeinfo.loose_iso_tau_wp = -9;
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
