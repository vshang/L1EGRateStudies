// -*- C++ -*-
//
// Package:     L1GCTJetStudies
// Class:        L1GCTJetStudies
// 
/**\class L1GCTJetStudies L1GCTJetStudies.cc L1Trigger/L1EGRateStudies/src/L1GCTJetStudies.cc

 Description: [one line class summary]

 Implementation:
      [Notes on implementation]
*/
//
// Original Author:  Victor Shang
//            Created:  May 17, 2023
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

#include "DataFormats/L1TCalorimeterPhase2/interface/Phase2L1CaloJet.h"
#include "DataFormats/L1TCalorimeterPhase2/src/classes.h"

#include "FastSimulation/ParticlePropagator/interface/ParticlePropagator.h"

// #include "FastSimulation/Particle/interface/RawParticle.h"

// Stage2
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"


// 
// class declaration
//
class L1GCTJetStudies : public edm::one::EDAnalyzer<edm::one::SharedResources, edm::one::WatchRuns, edm::one::WatchLuminosityBlocks> {
    typedef BXVector<l1t::Jet> JetBxCollection;
    typedef std::vector<l1t::Jet> JetCollection;
    typedef std::vector<reco::GenJet> GenJetCollection;
    typedef BXVector<l1t::Tau> TauBxCollection;
    typedef std::vector<l1t::Tau> TauCollection;

    public:
        explicit L1GCTJetStudies(const edm::ParameterSet& iConfig);
        ~L1GCTJetStudies();

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
        void fill_tree(const l1tp2::Phase2L1CaloJet& caloJet);
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

        edm::EDGetTokenT<l1tp2::Phase2L1CaloJetCollection> caloJetsToken_;
        l1tp2::Phase2L1CaloJetCollection caloJets;
        edm::Handle<l1tp2::Phase2L1CaloJetCollection> caloJetsHandle;   
 

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
        TH1F * nTruePUHist;
                
        // Crystal pt stuff
        TTree * tree;
        struct {
            double run;
            double lumi;
            double event;
            float nTruePU;

	    float jetEt;
	    float tauEt;
	    int jetIEta;
	    int jetIPhi;
	    float jetEta;
	    float jetPhi;
	    float towerEt;
	    int towerIEta;
	    int towerIPhi;
	    float towerEta;
	    float towerPhi;

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
L1GCTJetStudies::L1GCTJetStudies(const edm::ParameterSet& iConfig) :
    doRate(iConfig.getUntrackedParameter<bool>("doRate", false)),
    debug(iConfig.getUntrackedParameter<bool>("debug", false)),
    use_gen_taus(iConfig.getUntrackedParameter<bool>("use_gen_taus", false)),
    genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.3)),
    genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
    caloJetsToken_(consumes<l1tp2::Phase2L1CaloJetCollection>(iConfig.getParameter<edm::InputTag>("GCTJetsInputTag"))),
    genJetsToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genJets"))),
    genHadronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genHadronicTauSrc"))),
    stage2JetToken_(consumes<BXVector<l1t::Jet>>(iConfig.getParameter<edm::InputTag>("Stage2JetTag"))),
    stage2TauToken_(consumes<BXVector<l1t::Tau>>(iConfig.getParameter<edm::InputTag>("Stage2TauTag"))),
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc")))
{

    edm::Service<TFileService> fs;

    nEvents = fs->make<TH1F>("nEvents", "nEvents", 1, 0.5, 1.5);
    nTruePUHist = fs->make<TH1F>("nTruePUHist", "nTrue PU", 250, 0, 250);

    tree = fs->make<TTree>("tree", "CaloJet values");
    tree->Branch("run", &treeinfo.run);
    tree->Branch("lumi", &treeinfo.lumi);
    tree->Branch("event", &treeinfo.event);
    tree->Branch("nTruePU", &treeinfo.nTruePU);
    tree->Branch("jetEt", &treeinfo.jetEt);
    tree->Branch("tauEt", &treeinfo.tauEt);
    tree->Branch("jetIEta", &treeinfo.jetIEta);
    tree->Branch("jetIPhi", &treeinfo.jetIPhi);
    tree->Branch("jetEta", &treeinfo.jetEta);
    tree->Branch("jetPhi", &treeinfo.jetPhi);
    tree->Branch("towerEt", &treeinfo.towerEt);
    tree->Branch("towerIEta", &treeinfo.towerIEta);
    tree->Branch("towerIPhi", &treeinfo.towerIPhi);
    tree->Branch("towerEta", &treeinfo.towerEta);
    tree->Branch("towerPhi", &treeinfo.towerPhi);

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


L1GCTJetStudies::~L1GCTJetStudies()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1GCTJetStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    if (debug) printf("Starting L1GCTJetStudies Analyzer\n");
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


    // Sort caloJets so we can always pick highest pt caloJet matching cuts
    std::sort(begin(caloJets), end(caloJets), [](const l1tp2::Phase2L1CaloJet& a, const l1tp2::Phase2L1CaloJet& b){return a.pt() > b.pt();});


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
        // Stage-2 Jets
        if ( stage2JetHandle.isValid() && !use_gen_taus ) // use_gen_taus is a stand in for "Do Tau Analysis"
        {


            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                float calib_pt = s2_jet.pt() * ptAdjustStage2.Eval( s2_jet.pt() );
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
        if ( caloJets.size() > 0 )
        {
	  reco::Candidate::PolarLorentzVector testp4(0, 0, 0, 0);

            for(const auto& caloJet : caloJets) 
	    {
	        // std::cout << "CaloJet.pt = " << caloJet.pt() << " | caloJet.jetEt = " << caloJet.jetEt() << std::endl;
		// std::cout << "CaloJet.eta = " << caloJet.eta() << " | caloJet.jetEta = " << caloJet.jetEta() << std::endl;
		// std::cout << "CaloJet.phi = " << caloJet.phi() << " | caloJet.jetPhi = " << caloJet.jetPhi() << std::endl;
		// std::cout << "deltaRv1 = " << reco::deltaR(caloJet, testp4) << " | deltaRv2 = " << reco::deltaR(caloJet.p4(), testp4) << " | deltaRv3 " << reco::deltaR(caloJet.jetEta(), caloJet.jetPhi(), 0, 0) << std::endl;
		if (use_gen_taus && fabs(caloJet.eta()) > 3.0) continue;
	        if (caloJet.pt() < 10) continue;

		// CaloTau L1EG Info
	        fill_tree(caloJet);

            } // end Calo Jets loop
        } // have CaloJets
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


    for (auto& genJet : *genCollection ) 
    {

        // Skip lowest pT Jets, don't skip for low pT taus
        if (!use_gen_taus && genJet.pt() < 10) break;  // no need for continue as we sorted by pT so we're done
        if (use_gen_taus && fabs(genJet.eta()) > 3.5) continue; // HGCal ends at 3.0, so go a little further
        // HGCal detector stops at abs(eta)=3.0, keep gen jets up to 3.5
        //if ( fabs(genJet.eta())  > 3.5) continue;


        // Record DM (essentially) for the taus
        treeinfo.genTau_n_prongs = 0;
        treeinfo.genTau_n_photons = 0;
        treeinfo.genTau_pt_prongs = 0;
        treeinfo.genTau_pt_photons = 0;
        if (use_gen_taus)
        {
            for (auto& part : genJet.getGenConstituents())
            {
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

    
        //std::cout << "    ---!!!--- L1EG Size: " << caloJets.size() << std::endl;
        bool found_caloJet = false;
        if ( caloJets.size() > 0 )
        {
            for(const auto& caloJet : caloJets)
            {

	      if ( reco::deltaR(caloJet, genJetP4) < genMatchDeltaRcut )
	      {
                    if ( debug ) std::cout << "using caloJet dr = " << reco::deltaR(caloJet, genJetP4) << std::endl;
                    treeinfo.deltaR = reco::deltaR(caloJet, genJetP4);
                    treeinfo.deltaPhi = reco::deltaPhi(caloJet, genJetP4);
                    treeinfo.deltaEta = genJetP4.eta()-caloJet.eta();
                    if (treeinfo.stage2tau_eta != -9)
                    {
                        treeinfo.deltaR_phase2_stage2 = reco::deltaR( treeinfo.stage2tau_eta, treeinfo.stage2tau_phi, caloJet.eta(), caloJet.phi() );
                    }
                    

                    fill_tree(caloJet);
                    found_caloJet = true;
                    break;
    
              } // end passes Pt and dR match
            } // end Calo Jets loop

            // if not calo_jets were reconstructed to match the gen obj
            if (!found_caloJet) fill_tree_null();
        } // have CaloJets
         // no CaloJets
        if (caloJets.size() == 0)
        {
            // Fill tree with -1 to signify we lose a gen jet        
            fill_tree_null();
        }

    } // end GenJets loop

  } // end if NOT doRate
    if (debug) printf("Ending L1GCTJetStudies Analyzer\n");


}


// ------------ method called once each job just before starting event loop  ------------
void 
L1GCTJetStudies::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1GCTJetStudies::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
L1GCTJetStudies::beginRun(edm::Run const& run, edm::EventSetup const& es)
{
    //edm::ESHandle<HepPDT::ParticleDataTable> pdt;
    //es.getData(pdt);
    //if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

// ------------ method called when ending the processing of a run  ------------

void 
L1GCTJetStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------

void 
L1GCTJetStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------

void 
L1GCTJetStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1GCTJetStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods

void
L1GCTJetStudies::fill_tree(const l1tp2::Phase2L1CaloJet& caloJet) {
    treeinfo.jetEt = caloJet.jetEt();
    treeinfo.tauEt = caloJet.tauEt();
    treeinfo.jetIEta = caloJet.jetIEta();
    treeinfo.jetIPhi = caloJet.jetIPhi();
    treeinfo.jetEta = caloJet.jetEta();
    treeinfo.jetPhi = caloJet.jetPhi();
    treeinfo.towerEt = caloJet.towerEt();
    treeinfo.towerIEta = caloJet.towerIEta();
    treeinfo.towerIPhi = caloJet.towerIPhi();
    treeinfo.towerEta = caloJet.towerEta();
    treeinfo.towerPhi = caloJet.towerPhi();
    tree->Fill();
}


void
L1GCTJetStudies::fill_tree_null() {
    // Fill with -9 with no CaloJet found
    treeinfo.jetEt = -9;
    treeinfo.tauEt = -9;
    treeinfo.jetIEta = -9;
    treeinfo.jetIPhi = -9;
    treeinfo.jetEta = -9;
    treeinfo.jetPhi = -9;
    treeinfo.towerEt = -9;
    treeinfo.towerIEta = -9;
    treeinfo.towerIPhi = -9;
    treeinfo.towerEta = -9;
    treeinfo.towerPhi = -9;
    tree->Fill();
}



//define this as a plug-in
DEFINE_FWK_MODULE(L1GCTJetStudies);
