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
                
        // Crystal pt stuff
        TTree * tree;
        struct {
            double run;
            double lumi;
            double event;
            float ecal_pt;
            float ecal_eta;
            float ecal_phi;
            float ecal_mass;
            float ecal_energy;
            float hcal_pt;
            float hcal_eta;
            float hcal_phi;
            float hcal_mass;
            float hcal_energy;
            float jet_pt;
            float jet_eta;
            float jet_phi;
            float jet_mass;
            float jet_energy;
            float hovere;
            float hcal_dR1T;
            float hcal_dR2T;
            float hcal_dR3T;
            float hcal_dR4T;
            float hcal_dR5T;
            float hcal_2x2_1;
            float hcal_2x2_2;
            float hcal_2x2_3;
            float hcal_2x2_4;
            float hcal_jet_pt;
            float hcal_seed_pt;
            float hcal_seed_iEta;
            float hcal_seed_iPhi;
            float hcal_seed_eta;
            float hcal_seed_phi;
            float hcal_seed_energy;
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
            float ecal_dR0p5;
            float ecal_dR0p1_leading;
            float ecal_nL1EGs;
            float deltaR_ecal_vs_jet;
            float deltaR_hcal_vs_jet;
            float deltaR_hcal_vs_hcal_seed;
            float deltaR_ecal_vs_hcal;
            float deltaR_ecal_vs_hcal_seed;
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
            float stage2tau_pt;
            float stage2tau_eta;
            float stage2tau_phi;
            float stage2tau_energy;
            float stage2tau_mass;
            float stage2tau_charge;
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
    debug(iConfig.getUntrackedParameter<bool>("debug", false)),
    genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.3)),
    genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
    caloJetsToken_(consumes<l1slhc::L1CaloJetsCollection>(iConfig.getParameter<edm::InputTag>("L1CaloJetsInputTag"))),
    genJetsToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genJets"))),
    genHadronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genHadronicTauSrc"))),
    stage2JetToken_(consumes<BXVector<l1t::Jet>>(iConfig.getParameter<edm::InputTag>("Stage2JetTag"))),
    stage2TauToken_(consumes<BXVector<l1t::Tau>>(iConfig.getParameter<edm::InputTag>("Stage2TauTag")))
{

    edm::Service<TFileService> fs;

    tree = fs->make<TTree>("tree", "CaloJet values");
    tree->Branch("run", &treeinfo.run);
    tree->Branch("lumi", &treeinfo.lumi);
    tree->Branch("event", &treeinfo.event);
    tree->Branch("ecal_pt", &treeinfo.ecal_pt);
    tree->Branch("ecal_eta", &treeinfo.ecal_eta);
    tree->Branch("ecal_phi", &treeinfo.ecal_phi);
    tree->Branch("ecal_mass", &treeinfo.ecal_mass);
    tree->Branch("ecal_energy", &treeinfo.ecal_energy);
    tree->Branch("hcal_pt", &treeinfo.hcal_pt);
    tree->Branch("hcal_eta", &treeinfo.hcal_eta);
    tree->Branch("hcal_phi", &treeinfo.hcal_phi);
    tree->Branch("hcal_mass", &treeinfo.hcal_mass);
    tree->Branch("hcal_energy", &treeinfo.hcal_energy);
    tree->Branch("jet_pt", &treeinfo.jet_pt);
    tree->Branch("jet_eta", &treeinfo.jet_eta);
    tree->Branch("jet_phi", &treeinfo.jet_phi);
    tree->Branch("jet_mass", &treeinfo.jet_mass);
    tree->Branch("jet_energy", &treeinfo.jet_energy);
    tree->Branch("hovere", &treeinfo.hovere);
    tree->Branch("hcal_dR1T", &treeinfo.hcal_dR1T);
    tree->Branch("hcal_dR2T", &treeinfo.hcal_dR2T);
    tree->Branch("hcal_dR3T", &treeinfo.hcal_dR3T);
    tree->Branch("hcal_dR4T", &treeinfo.hcal_dR4T);
    tree->Branch("hcal_dR5T", &treeinfo.hcal_dR5T);
    tree->Branch("hcal_2x2_1", &treeinfo.hcal_2x2_1);
    tree->Branch("hcal_2x2_2", &treeinfo.hcal_2x2_2);
    tree->Branch("hcal_2x2_3", &treeinfo.hcal_2x2_3);
    tree->Branch("hcal_2x2_4", &treeinfo.hcal_2x2_4);
    tree->Branch("hcal_jet_pt", &treeinfo.hcal_jet_pt);
    tree->Branch("hcal_seed_pt", &treeinfo.hcal_seed_pt);
    tree->Branch("hcal_seed_iEta", &treeinfo.hcal_seed_iEta);
    tree->Branch("hcal_seed_iPhi", &treeinfo.hcal_seed_iPhi);
    tree->Branch("hcal_seed_eta", &treeinfo.hcal_seed_eta);
    tree->Branch("hcal_seed_phi", &treeinfo.hcal_seed_phi);
    tree->Branch("hcal_seed_energy", &treeinfo.hcal_seed_energy);
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
    tree->Branch("ecal_dR0p5", &treeinfo.ecal_dR0p5);
    tree->Branch("ecal_dR0p1_leading", &treeinfo.ecal_dR0p1_leading);
    tree->Branch("ecal_nL1EGs", &treeinfo.ecal_nL1EGs);
    tree->Branch("deltaR_ecal_vs_jet", &treeinfo.deltaR_ecal_vs_jet);
    tree->Branch("deltaR_hcal_vs_jet", &treeinfo.deltaR_hcal_vs_jet);
    tree->Branch("deltaR_hcal_vs_hcal_seed", &treeinfo.deltaR_hcal_vs_hcal_seed);
    tree->Branch("deltaR_ecal_vs_hcal", &treeinfo.deltaR_ecal_vs_hcal);
    tree->Branch("deltaR_ecal_vs_hcal_seed", &treeinfo.deltaR_ecal_vs_hcal_seed);
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
    tree->Branch("stage2tau_pt", &treeinfo.stage2tau_pt);
    tree->Branch("stage2tau_eta", &treeinfo.stage2tau_eta);
    tree->Branch("stage2tau_phi", &treeinfo.stage2tau_phi);
    tree->Branch("stage2tau_energy", &treeinfo.stage2tau_energy);
    tree->Branch("stage2tau_mass", &treeinfo.stage2tau_mass);
    tree->Branch("stage2tau_charge", &treeinfo.stage2tau_charge);
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


    // Record the standards
    treeinfo.run = iEvent.eventAuxiliary().run();
    treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
    treeinfo.event = iEvent.eventAuxiliary().event();


    // Get Phase-II CaloJet collection
    iEvent.getByToken(caloJetsToken_,caloJetsHandle);
    caloJets = (*caloJetsHandle.product());
    std::cout << " -- Input L1CaloTaus: " << caloJets.size() << std::endl;

    // Sort caloJets so we can always pick highest pt caloJet matching cuts
    std::sort(begin(caloJets), end(caloJets), [](const l1slhc::L1CaloJet& a, const l1slhc::L1CaloJet& b){return a.pt() > b.pt();});
        

    // Loop over all gen jets with pt > 10 GeV and match them to Phase-II CaloJets
    // Generator info (truth)
    iEvent.getByToken(genJetsToken_,genJetsHandle);
    genJets = *genJetsHandle.product();
    int cnt = 0;
    for (auto& genJet : genJets ) {
        // Skip lowest pT Jets
        if (genJet.pt() < 10) continue;
        // Skip high eta, keep things hear boundary for future study
        if ( fabs(genJet.eta())  > 2.0) continue;
        ++cnt;
        //std::cout << cnt << " Gen pT: " << genJet.pt() << std::endl;

        //if ( fabs(genJet.pdgId()) != 11) {
        //      std::cout << "Event without electron as best gen.  Gen pdgId was: " << genJet.pdgId() <<std::endl;
        //      return;
        //}
    
    
        reco::Candidate::PolarLorentzVector genJetP4(genJet.pt(), genJet.eta(), genJet.phi(), genJet.mass() );
    
    
        // Stage-2 Jets
        iEvent.getByToken(stage2JetToken_, stage2JetHandle);
        JetBxCollection stage2JetCollection;
        JetCollection stage2Jets;
        bool jet_matched = false;
        if ( stage2JetHandle.isValid() )
        {

            // Make stage2 sortable
            stage2JetCollection = *stage2JetHandle.product();
            for (auto& s2_jet : stage2JetCollection)
            {
                stage2Jets.push_back( s2_jet );
            }

            // Sort
            std::sort(begin(stage2Jets), end(stage2Jets), [](l1t::Jet& a, l1t::Jet& b){return a.pt() > b.pt();});

            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_jet : stage2Jets)
            {
                if ( reco::deltaR( s2_jet.p4(), genJetP4 ) < 0.3 )
                {
                    treeinfo.stage2jet_pt = s2_jet.pt();
                    treeinfo.stage2jet_eta = s2_jet.eta();
                    treeinfo.stage2jet_phi = s2_jet.phi();
                    treeinfo.stage2jet_energy = s2_jet.energy();
                    treeinfo.stage2jet_mass = s2_jet.mass();
                    treeinfo.stage2jet_charge = s2_jet.charge();
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
        } 
    
    
    
    
        // Stage-2 Taus 
        iEvent.getByToken(stage2TauToken_, stage2TauHandle);
        TauBxCollection stage2TauCollection;
        TauCollection stage2Taus;
        bool tau_matched = false;
        if ( stage2TauHandle.isValid() )
        {

            // Make stage2 sortable
            stage2TauCollection = *stage2TauHandle.product();
            for (auto& s2_tau : stage2TauCollection)
            {
                stage2Taus.push_back( s2_tau );
            }

            // Sort
            std::sort(begin(stage2Taus), end(stage2Taus), [](l1t::Tau& a, l1t::Tau& b){return a.pt() > b.pt();});

            // Find stage2 within dR 0.3, beginning with higest pt cand
            for (auto& s2_tau : stage2Taus)
            {
                if ( reco::deltaR( s2_tau.p4(), genJetP4 ) < 0.3 )
                {
                    treeinfo.stage2tau_pt = s2_tau.pt();
                    treeinfo.stage2tau_eta = s2_tau.eta();
                    treeinfo.stage2tau_phi = s2_tau.phi();
                    treeinfo.stage2tau_energy = s2_tau.energy();
                    treeinfo.stage2tau_mass = s2_tau.mass();
                    treeinfo.stage2tau_charge = s2_tau.charge();
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
        iEvent.getByToken(genHadronicTausToken_, genHTaus);
        GenJetCollection genHTauCollection;
        bool gen_tau_matched = false;
        if ( genHTaus.isValid() )
        {

            // Make stage2 sortable
            genHTauCollection = *genHTaus.product();

            // Sort
            std::sort(begin(genHTauCollection), end(genHTauCollection), [](reco::GenJet& a, reco::GenJet& b){return a.pt() > b.pt();});

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
        if ( caloJets.size() > 0 )
        {
            for(const auto& caloJet : caloJets)
            {
                if ( reco::deltaR(caloJet, genJetP4) < genMatchDeltaRcut )
                      //&& fabs(caloJet.pt()-genJetP4.pt())/genJetP4.pt() < genMatchRelPtcut )
                {

                    if ( debug ) std::cout << "using caloJet dr = " << reco::deltaR(caloJet, genJetP4) << std::endl;
                    treeinfo.deltaR = reco::deltaR(caloJet, genJetP4);
                    treeinfo.deltaPhi = reco::deltaPhi(caloJet, genJetP4);
                    treeinfo.deltaEta = genJetP4.eta()-caloJet.eta();
                    
                    fill_tree(caloJet);
    
                } // end passes Pt and dR match
            } // end Calo Jets loop
        } // have CaloJets
        else // no CaloJets
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
    }
}

void
L1CaloJetStudies::fill_tree(const l1slhc::L1CaloJet& caloJet) {
    // As of 28 May 2018 caloJet_pt is post-calibration
    treeinfo.ecal_pt = caloJet.GetExperimentalParam("ecal_pt");
    treeinfo.ecal_eta = caloJet.GetExperimentalParam("ecal_eta");
    treeinfo.ecal_phi = caloJet.GetExperimentalParam("ecal_phi");
    treeinfo.ecal_mass = caloJet.GetExperimentalParam("ecal_mass");
    treeinfo.ecal_energy = caloJet.GetExperimentalParam("ecal_energy");
    treeinfo.hcal_pt = caloJet.GetExperimentalParam("hcal_pt");
    treeinfo.hcal_eta = caloJet.GetExperimentalParam("hcal_eta");
    treeinfo.hcal_phi = caloJet.GetExperimentalParam("hcal_phi");
    treeinfo.hcal_mass = caloJet.GetExperimentalParam("hcal_mass");
    treeinfo.hcal_energy = caloJet.GetExperimentalParam("hcal_energy");
    treeinfo.jet_pt = caloJet.GetExperimentalParam("jet_pt");
    treeinfo.jet_eta = caloJet.GetExperimentalParam("jet_eta");
    treeinfo.jet_phi = caloJet.GetExperimentalParam("jet_phi");
    treeinfo.jet_mass = caloJet.GetExperimentalParam("jet_mass");
    treeinfo.jet_energy = caloJet.GetExperimentalParam("jet_energy");
    treeinfo.hovere = caloJet.hovere();
    treeinfo.hcal_jet_pt = caloJet.GetExperimentalParam("hcal_jet_pt");
    treeinfo.hcal_seed_pt = caloJet.GetExperimentalParam("hcal_seed_pt");
    treeinfo.hcal_seed_iEta = caloJet.GetExperimentalParam("hcal_seed_iEta");
    treeinfo.hcal_seed_iPhi = caloJet.GetExperimentalParam("hcal_seed_iPhi");
    treeinfo.hcal_seed_eta = caloJet.GetExperimentalParam("hcal_seed_eta");
    treeinfo.hcal_seed_phi = caloJet.GetExperimentalParam("hcal_seed_phi");
    treeinfo.hcal_seed_energy = caloJet.GetExperimentalParam("hcal_seed_energy");
    treeinfo.hcal_nHits = caloJet.GetExperimentalParam("hcal_nHits");
    treeinfo.hcal_dR1T = caloJet.GetExperimentalParam("hcal_dR1T");
    treeinfo.hcal_dR2T = caloJet.GetExperimentalParam("hcal_dR2T");
    treeinfo.hcal_dR3T = caloJet.GetExperimentalParam("hcal_dR3T");
    treeinfo.hcal_dR4T = caloJet.GetExperimentalParam("hcal_dR4T");
    treeinfo.hcal_dR5T = caloJet.GetExperimentalParam("hcal_dR5T");
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
    treeinfo.ecal_dR0p5 = caloJet.GetExperimentalParam("ecal_dR0p5");
    treeinfo.ecal_dR0p1_leading = caloJet.GetExperimentalParam("ecal_dR0p1_leading");
    treeinfo.ecal_nL1EGs = caloJet.GetExperimentalParam("ecal_nL1EGs");
    treeinfo.deltaR_ecal_vs_jet = caloJet.GetExperimentalParam("deltaR_ecal_vs_jet");
    treeinfo.deltaR_hcal_vs_jet = caloJet.GetExperimentalParam("deltaR_hcal_vs_jet");
    treeinfo.deltaR_hcal_vs_hcal_seed = caloJet.GetExperimentalParam("deltaR_hcal_vs_hcal_seed");
    treeinfo.deltaR_ecal_vs_hcal = caloJet.GetExperimentalParam("deltaR_ecal_vs_hcal");
    treeinfo.deltaR_ecal_vs_hcal_seed = caloJet.GetExperimentalParam("deltaR_ecal_vs_hcal_seed");
    treeinfo.deltaR_ecal_lead_vs_jet = caloJet.GetExperimentalParam("deltaR_ecal_lead_vs_jet");
    treeinfo.deltaR_ecal_lead_vs_ecal = caloJet.GetExperimentalParam("deltaR_ecal_lead_vs_ecal");
    tree->Fill();
}


void
L1CaloJetStudies::fill_tree_null() {
    // Fill with -9 with no CaloJet fround
    treeinfo.ecal_pt = -9;
    treeinfo.ecal_eta = -9;
    treeinfo.ecal_phi = -9;
    treeinfo.ecal_mass = -9;
    treeinfo.ecal_energy = -9;
    treeinfo.hcal_pt = -9;
    treeinfo.hcal_eta = -9;
    treeinfo.hcal_phi = -9;
    treeinfo.hcal_mass = -9;
    treeinfo.hcal_energy = -9;
    treeinfo.jet_pt = -9;
    treeinfo.jet_eta = -9;
    treeinfo.jet_phi = -9;
    treeinfo.jet_mass = -9;
    treeinfo.jet_energy = -9;
    treeinfo.hovere = -9;
    treeinfo.hcal_jet_pt = -9;
    treeinfo.hcal_seed_pt = -9;
    treeinfo.hcal_seed_iEta = -9;
    treeinfo.hcal_seed_iPhi = -9;
    treeinfo.hcal_seed_eta = -9;
    treeinfo.hcal_seed_phi = -9;
    treeinfo.hcal_seed_energy = -9;
    treeinfo.hcal_nHits = -9;
    treeinfo.hcal_dR1T = -9;
    treeinfo.hcal_dR2T = -9;
    treeinfo.hcal_dR3T = -9;
    treeinfo.hcal_dR4T = -9;
    treeinfo.hcal_dR5T = -9;
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
    treeinfo.ecal_dR0p5 = -9;
    treeinfo.ecal_dR0p1_leading = -9;
    treeinfo.ecal_nL1EGs = -9;
    treeinfo.deltaR_ecal_vs_jet = -9;
    treeinfo.deltaR_hcal_vs_jet = -9;
    treeinfo.deltaR_hcal_vs_hcal_seed = -9;
    treeinfo.deltaR_ecal_vs_hcal = -9;
    treeinfo.deltaR_ecal_vs_hcal_seed = -9;
    treeinfo.deltaR_ecal_lead_vs_jet = -9;
    treeinfo.deltaR_ecal_lead_vs_ecal = -9;
    tree->Fill();
}



//define this as a plug-in
DEFINE_FWK_MODULE(L1CaloJetStudies);
