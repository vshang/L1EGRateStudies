import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1000)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )

process.source = cms.Source("PoolSource",
# file dataset=/RelValSingleElectronPt35Extended/CMSSW_8_1_0_pre11-PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/GEN-SIM-DIGI-RAW
# file dataset=/RelValSingleElectronPt35Extended/CMSSW_8_1_0_pre11-PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/GEN-SIM-RECO
# file dataset=/RelValTTbar_14TeV/CMSSW_8_1_0_pre11-PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/GEN-SIM-RECO
   fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0067AD1C-3877-E611-949E-0CC47A4D768C.root', 
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/00DB3E49-E876-E611-968D-0CC47A4C8EA8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/02049990-EE76-E611-8EE5-0025905B85DE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/04AA9405-2677-E611-821B-0CC47A4D763C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/04F1F579-2C77-E611-93FC-0025905AA9CC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/06D91E5E-D676-E611-894E-0025905A48E4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/084FCBC0-E576-E611-B820-0025905A6134.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C24421F-EC76-E611-B247-0CC47A78A42E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C445DDC-4377-E611-B24B-0CC47A7C3572.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0CAAD682-D276-E611-AA45-0CC47A4D768E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0E2223CB-E176-E611-8CA3-0025905A48B2.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/10C424A4-4E77-E611-BFA8-0CC47A78A3E8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/14006BE9-3277-E611-95E8-0025905A60EE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/148E00A3-F176-E611-BFD8-0CC47A4D7614.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1A249F39-3977-E611-9E6C-0025905A6084.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1AB35B15-3577-E611-A8AF-0CC47A4D769C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1C578B27-DF76-E611-85B0-0CC47A4C8E3C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1E0E96BA-2377-E611-A1E4-0CC47A4D76B6.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2C22CF47-D276-E611-A461-0CC47A4C8F12.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3640DA17-6F77-E611-94D8-0025905A60BE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/38B352E9-4677-E611-AC34-0025905B8598.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/44E5D267-0577-E611-9105-0CC47A4C8E96.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/44F41F92-E876-E611-A42B-0025905B85DA.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/46031293-5277-E611-8B31-0025905A6122.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/46D53382-5B77-E611-AD53-0CC47A7C361E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/48DF2B5C-0F77-E611-AA7A-0025905A60B4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4A63FF49-CD76-E611-852D-0025905A6092.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4AC2B378-3F77-E611-A57D-0025905A605E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/50F6B0E8-4C77-E611-A023-0CC47A4D76C0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/56790B87-1177-E611-9A1E-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/56AE1812-4E77-E611-A83B-0CC47A4C8E70.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/66085F10-3177-E611-AB5B-003048FFD798.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6C5C4288-EA76-E611-A870-0CC47A4C8F2C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6E782766-E676-E611-9786-0CC47A74524E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/72F787DB-5A77-E611-B7A1-0025905B8564.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/7CF212C9-3277-E611-90C5-0CC47A4D76C0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/80BF4EDC-5877-E611-BC5D-0CC47A4D764A.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/80D1C17B-1677-E611-A988-003048FFD79E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/84920845-3277-E611-B24B-0CC47A7C34A0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/86D68C04-2677-E611-A855-0CC47A4D7600.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8E7BC14E-5E77-E611-8A77-0025905A6132.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/90703BEF-2977-E611-B9A8-0CC47A4C8E0E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/943506A7-2E77-E611-A08D-0CC47A78A468.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/94DFFA2E-2677-E611-BEB1-0025905B85DC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9640AD73-1C77-E611-8236-0025905A60E4.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/98B2D03A-3177-E611-9414-0025905A6118.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9C09B739-2377-E611-8CCE-0025905B855C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A6B08DEC-3D77-E611-9D11-0025905B860E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A8B6F619-5977-E611-A65B-0025905B8562.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AA8DF969-2377-E611-B77E-0CC47A7C35E0.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE19B8C0-6477-E611-9758-0025905A60F8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE55398C-5E77-E611-9AFA-0CC47A4D7664.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B4B41042-7177-E611-A7DE-0CC47A4D7632.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B87636C8-3177-E611-963E-0025905A60DE.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B8BC7408-E176-E611-9317-0025905A48BC.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B8E8B622-E076-E611-9F91-0CC47A4C8E70.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BA76FE20-2877-E611-A76F-0CC47A78A440.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C4163F0A-3177-E611-834C-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C851857D-6077-E611-8A6B-0CC47A78A30E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D0044C8E-2377-E611-91B0-0CC47A78A42C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D42C2DE2-1C77-E611-A2D3-0025905A605E.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8A8A5BB-0477-E611-8B01-0025905B856C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8FA286F-2B77-E611-937E-0025905A608C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DE9244D7-4577-E611-8AFA-0025905A610C.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DEF48CFB-3F77-E611-BAD5-0CC47A4D764A.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/EAFAEEB6-1A77-E611-A2B6-0CC47A4C8E14.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/ECF986F5-3D77-E611-A97D-0025905A48D8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/EE2E50CF-4577-E611-968B-0025905A6068.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F2510F4B-7577-E611-AB88-0CC47A4C8ED8.root',
        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/FC78CFCC-6177-E611-B397-0CC47A4C8F0C.root'
    )
    #fileNames = cms.untracked.vstring(
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/008096EB-0C77-E611-BC44-0025905A48C0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0402D195-0177-E611-AE4B-0CC47A7C3472.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0A69445C-3277-E611-848A-0025905B8600.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C387497-2877-E611-977A-002618FDA265.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0E29488B-3B77-E611-B57C-0CC47A4D765A.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0E805685-EB76-E611-8899-0CC47A4C8F10.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1A78CD7C-F176-E611-87B7-0CC47A4D762E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1E2A60B7-3677-E611-B029-0025905B85B6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/207571D3-0777-E611-9DBE-0CC47A4D7654.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/20825FA1-5277-E611-B69B-003048FFD7A4.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/28009F74-4677-E611-B13E-0025905B8564.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/284D71C6-2A77-E611-B464-0CC47A4C8E22.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2A683615-3B77-E611-9A16-0CC47A78A456.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2EA0AFF6-2B77-E611-B172-0025905A60B6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3024EE22-3177-E611-81BD-0025905B855E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/36407A09-0B77-E611-A89F-0CC47A7C3432.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3823366A-5977-E611-AE0B-0025905A60B6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3C9E47B9-2477-E611-8B84-002618FDA248.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3E14FC6E-3377-E611-AA77-003048FFCBB2.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/3EAAB665-6977-E611-979A-0025905B85BE.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/404DBE00-EB76-E611-9A5F-0025905B85B6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4286A1F3-3D77-E611-956A-0025905A60BE.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/54F58CC3-2E77-E611-B0F0-0025905B85D6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/585278D6-1A77-E611-A419-0CC47A7452DA.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/58F43816-E776-E611-A4D9-0CC47A4C8E5E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5A7C08A5-5D77-E611-9E39-0025905AA9F0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5AAEF46E-1177-E611-8061-0025905B85CC.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5E61EE7F-0977-E611-BFB3-0CC47A78A4B0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5EB8CAE7-0E77-E611-B9E3-0025905A612C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5EF2DF7E-EC76-E611-BB53-0CC47A4D76D6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/60C0BAA7-0477-E611-A0E3-0CC47A4C8E0E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/60EAD886-3777-E611-9C1C-0CC47A4C8E98.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/621F88C0-7677-E611-9211-0025905B8598.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/64176FA5-0B77-E611-9127-0CC47A78A3D8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/662AD93B-3777-E611-84F5-0CC47A4C8E2E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/682F7584-3C77-E611-82AB-0CC47A7C34E6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/703B2610-0577-E611-A5E8-0025905A60F8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/70A4E7D8-2A77-E611-8532-0025905B860E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/74DFE5BA-7477-E611-ACE7-0025905A60CE.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/762240CC-3277-E611-A923-0CC47A4D75F6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/7AB78AB2-4A77-E611-B9F4-0025905A48F0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/82696E74-0977-E611-98C6-0025905A6060.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/82E7DA01-5577-E611-AE46-0CC47A7C3422.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/82E7FA60-3F77-E611-BE7B-0CC47A7C3422.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/86353070-EF76-E611-A2A4-0CC47A4D7600.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8A1BABEB-4577-E611-B167-0025905AA9F0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8EA70EBC-7277-E611-A0A0-0CC47A4D7618.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8EDBF797-1077-E611-A5AF-0025905B860E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/90369E31-5077-E611-9196-0025905A6122.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/92341EA3-2777-E611-B44D-0025905B85C0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/94344C9F-3C77-E611-B1F9-0025905A60C6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/96E5A518-1177-E611-A245-0025905B8606.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9857B9AE-6677-E611-87D6-0CC47A7C35A8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/986FE38E-3A77-E611-AC54-0CC47A78A456.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9C8C2164-3377-E611-A3C2-0025905B85D6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9E48CC18-0777-E611-BA7A-0025905B85DC.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9EBDFFD6-4077-E611-983D-0CC47A4C8E0E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A65BE531-0577-E611-88F9-0CC47A4D76C6.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A6C14B08-FE76-E611-BEE9-0CC47A4D76A0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A6F3EA0F-EE76-E611-B106-0CC47A78A468.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AC737E00-4877-E611-BC7E-0CC47A4D765E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/ACFA3ADF-0C77-E611-80CF-0025905B855E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE248E5E-4077-E611-8548-0CC47A7C35A8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B8394A92-3677-E611-9B30-0CC47A4D769C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B842F17D-0477-E611-8DBA-0CC47A78A414.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B846044F-1277-E611-BDBF-0025905A6122.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BC4B878B-EF76-E611-B406-0CC47A4C8E3C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BE082C49-4177-E611-BDD3-0CC47A78A3D8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BEECDB9D-4E77-E611-B077-0025905AA9CC.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C2F79121-2977-E611-A86C-0CC47A745250.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C472A16A-4477-E611-A3FE-0CC47A4C8F0C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C89CB6A5-3977-E611-AE2D-0CC47A4C8E7E.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C8D1C67C-0477-E611-83D4-0CC47A4C8F12.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D64C7D6D-5B77-E611-8922-0CC47A4D75F8.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8EBF066-4377-E611-BCCC-0025905B856C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DAA53EE5-2477-E611-8D58-0025905A60BE.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DEF1EAE1-6C77-E611-B265-0025905A60CE.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DEFD60AC-2F77-E611-B71D-0CC47A4D7638.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/E0A46A82-4C77-E611-BB13-003048FFD72C.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/E69BBB30-5077-E611-9825-0025905A48F2.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/E8DE1074-2C77-E611-A3AD-0025905B8580.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F250A9AE-6477-E611-A894-0CC47A4D76A0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F2FE3253-3377-E611-9215-0CC47A4D76A0.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F4FC57A5-5C77-E611-85EE-0CC47A78A458.root',
    #   'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre11/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F6A4F6D5-1A77-E611-B644-0025905B8580.root' 
    #)
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V3::All', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D1Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D2Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D3Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D5Reco_cff') # Crashes geometryHelper, this is the default one used for ECAL TPs
#process.load('Configuration.Geometry.GeometryExtended2023D6Reco_cff') # Works


process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
#process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
#process.load('Geometry.TrackerGeometryBuilder.StackedTrackerGeometry_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')

#process.load('Configuration/StandardSequences/L1HwVal_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load("SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff")

# bug fix for missing HCAL TPs in MC RAW
#from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
#HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
#process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
#process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")
#
#process.slhccalo = cms.Path( process.RawToDigi + process.valHcalTriggerPrimitiveDigis+process.SLHCCaloTrigger)
#
# run L1Reco to produce the L1EG objects corresponding
# to the current trigger
#process.load('Configuration.StandardSequences.L1Reco_cff')
#process.L1Reco = cms.Path( process.l1extraParticles )

# producer for UCT2015 / Stage-1 trigger objects
#process.load("L1Trigger.UCT2015.emulationMC_cfi")
#process.load("L1Trigger.UCT2015.uctl1extraparticles_cfi")
#process.pUCT = cms.Path(
#    process.emulationSequence *
#    process.uct2015L1Extra
#)


process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
process.load("RecoLocalCalo.Configuration.hcalGlobalReco_cff")

#from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *
#localreco = cms.Sequence(ecalLocalRecoSequence)
#process.load("RecoLocalCalo.EcalRecProducers.ecalLocalRecoSequence_cff")




# ----------------------------------------------------------------------------------------------
# 
# Do offline reconstruction step for electron matching
# First we need to run EcalSeverityLevelESProducer ES Producer

process.load('RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi')

#process.load('RecoEcal.Configuration.RecoEcal_cff')
#process.ecalClusters = cms.Path(process.ecalClustersNoPFBox)

# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for ECAL TPs / RecHits
process.HitAnalyzer = cms.EDAnalyzer('HitAnalyzer',
   #useEcalRecHits = cms.bool(True),
   useEcalRecHits = cms.bool(False),
   useHcalRecHits = cms.bool(True),
   useEcalTPs = cms.bool(False),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   hcalRecHit = cms.InputTag("hbhereco")
)
process.p1 = cms.Path(process.HitAnalyzer)



process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('recHits.root')
                                   )


# -------------------------------------------------------------------------------------------
#
### Uncomment this section to save the edm version of L1EG TPs
#process.Out = cms.OutputModule( "PoolOutputModule",
#    fileName = cms.untracked.string( "l1egBorderTest3.root" ),
#    fastCloning = cms.untracked.bool( False ),
#    outputCommands = cms.untracked.vstring( "keep *_L1EGammaCrystalsProducer_*_*")
#)
#process.end = cms.EndPath( process.Out )



