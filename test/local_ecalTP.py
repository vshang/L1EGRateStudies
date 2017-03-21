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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
# file dataset=/RelValSingleElectronPt35Extended/CMSSW_8_1_0_pre11-PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/GEN-SIM-DIGI-RAW
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0ADFD7B5-4277-E611-8E89-0025905A6132.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C8DF598-1977-E611-95D4-0025905A612E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/148A8242-1577-E611-B3B6-0025905B855E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/149D7C35-1577-E611-992B-0CC47A745282.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1874030D-DC76-E611-8FA7-0CC47A4C8E14.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1C51682A-DD76-E611-A258-0025905B857A.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/1E7C6756-1677-E611-9633-0025905B8560.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2007B6E9-CA76-E611-9B4C-0CC47A745294.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/22926245-C276-E611-9F2A-0025905A48B2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/24EE0F03-D676-E611-B94D-0CC47A4C8E46.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/286DC4E9-CB76-E611-B41B-0CC47A7452D8.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/28CF1A1C-1877-E611-B14F-0025905A60D2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/2C32E900-E076-E611-BA96-0CC47A4C8EA8.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/32FA5232-0D77-E611-A420-0025905B861C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/34E99ED5-1877-E611-B092-0CC47A7C3572.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/40AC3F5E-F376-E611-BAA2-0CC47A4D76D0.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/46C79DBE-1D77-E611-BA00-0025905B8596.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/487702E0-0377-E611-B276-0025905B8560.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/48B2905D-EA76-E611-977F-0025905B85DC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/48BA4FF7-D976-E611-A309-0CC47A4C8F26.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4A47F5E3-C276-E611-8930-0025905B8562.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4CC09DB2-C176-E611-8133-0025905B85DC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/4CF4B0AC-FD76-E611-A394-0CC47A7C3636.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/52297EE9-0D77-E611-AFA8-0025905B85FC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/523271EF-CA76-E611-BC16-0025905A60B0.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/54EE68FD-D976-E611-B407-0025905A6104.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/5A5DF9D7-C276-E611-882F-0025905A60F8.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/62312CE9-CA76-E611-A2CA-0CC47A7C340E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/628AC61E-DE76-E611-8E4B-0CC47A7C35E0.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/64A2D5BB-C276-E611-AEF9-0CC47A4D7634.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/665DC64A-0D77-E611-97B6-0025905B859A.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6C6985EE-CA76-E611-8618-0025905A60BC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6E6A9699-1A77-E611-ADEF-0CC47A4D75EC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6EAE6BA1-E076-E611-96BF-0025905A6064.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/6EF68AA9-DA76-E611-B346-0CC47A7C3420.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/70BC6199-CE76-E611-AF5C-0CC47A7C3472.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/7CF9CC14-1777-E611-961E-0CC47A4C8F18.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/8EBE59A2-E476-E611-B71B-0CC47A78A41C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/904DF162-CE76-E611-B40B-0CC47A4D76CC.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9229C466-3C77-E611-B729-0025905B8564.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/92993D85-D076-E611-871F-0CC47A4D7628.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/94463AB9-D276-E611-9048-0CC47A4C8E26.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9846B648-C376-E611-B4E7-0025905A60F2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/9E218346-C276-E611-ABD1-0025905B858C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A089E4AE-2E77-E611-B9D4-0025905A60CE.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A2B4A634-0F77-E611-8590-0025905B85DA.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/A8814913-E376-E611-BFFC-0CC47A7C3604.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AC20E95E-EB76-E611-8D1D-0025905A6118.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/AE34A0BD-E776-E611-80A9-0CC47A4D76BE.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B0FE2ADE-0677-E611-9253-0025905A60F2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B455252A-DE76-E611-91AA-0CC47A4D760A.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/B4FF0741-C276-E611-8B92-0CC47A78A42E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/BC34DA45-C276-E611-8006-0025905B859E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C439EB44-C376-E611-888A-0025905B85B8.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/C81CF7DB-CF76-E611-BC0B-0CC47A4D760C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/CC275EA2-E376-E611-8240-0CC47A78A33E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D0520AEF-CA76-E611-BE0C-0025905B858E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D05220E8-CF76-E611-AB63-0CC47A7C357A.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D65580CD-C276-E611-B816-0025905A60B2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D80BBA95-1777-E611-A606-0CC47A78A458.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8336CA2-CC76-E611-9491-0025905A60CE.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/D8DA5AF0-CA76-E611-8DE3-0025905A60B6.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/DE731E46-C276-E611-A52C-0025905A60DE.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/E4DA9532-0F77-E611-9313-0CC47A7C340E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/E683D306-CB76-E611-9F38-0CC47A78A4A6.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F023CD86-0B77-E611-8330-0CC47A4D766C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F0B49AC1-C276-E611-BB66-0025905B85F6.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/F441704B-DC76-E611-89A5-0CC47A4D766C.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/FE080CE0-D076-E611-BD1D-0CC47A4D7640.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/FE5F55B4-4777-E611-B8C5-0CC47A4D76A2.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/FEDA422B-DC76-E611-9E14-0CC47A4C8E2A.root',
    )
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
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # Phase-2 Preferred


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

# --------------------------------------------------------------------------------------------
#
# ----    Produce the ECAL TPs

#process.simEcalEBTriggerPrimitiveDigis = cms.EDProducer("EcalEBTrigPrimProducer",
process.EcalEBTrigPrimProducer = cms.EDProducer("EcalEBTrigPrimProducer",
    BarrelOnly = cms.bool(True),
#    barrelEcalDigis = cms.InputTag("simEcalUnsuppressedDigis","ebDigis"),
    barrelEcalDigis = cms.InputTag("simEcalDigis","ebDigis"),
#    barrelEcalDigis = cms.InputTag("selectDigi","selectedEcalEBDigiCollection"),
    binOfMaximum = cms.int32(6), ## optional from release 200 on, from 1-10
    TcpOutput = cms.bool(False),
    Debug = cms.bool(False),
    Famos = cms.bool(False),
    nOfSamples = cms.int32(1)
)

process.pNancy = cms.Path( process.EcalEBTrigPrimProducer )



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

# first you need the ECAL RecHIts :
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   debug = cms.untracked.bool(False),
   useRecHits = cms.bool(False),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   #hcalRecHit = cms.InputTag("hbhereco") # for testing non-2023 geometry configurations
   #hcalRecHit = cms.InputTag("hltHbhereco","","L1AlgoTest")
   #hcalRecHit = cms.InputTag("hltHbhereco")
   hcalRecHit = cms.InputTag("hbhereco"),
   #hcalRecHit = cms.InputTag("hbheUpgradeReco")
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),

   #useTowerMap = cms.untracked.bool(False)
   useTowerMap = cms.untracked.bool(True)
   #towerMapName = cms.untracked.string("map1.json")
)

process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )



# --------------------------------------------------------------------------------------------
#
# ----  Match the L1EG stage-2 objects created by the SLHCCaloTrigger sequence above
#	with the crystal-level clusters.
#	This produces a new collection of L1EG objects, starting from the original
#	L1EG collection. The eta and phi of the L1EG objects is corrected using the
#	information of the xtal level clusters.

#process.l1ExtraCrystalProducer = cms.EDProducer("L1ExtraCrystalPosition",
#   eGammaSrc = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
#   eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
#)
#process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)




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
   useRecHits = cms.bool(False),
   useEcalTPs = cms.bool(True),
   hasGenInfo = cms.bool(True),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   hcalRecHit = cms.InputTag("hbhereco"),
   genParticles = cms.InputTag("genParticles")
)
process.p1 = cms.Path(process.HitAnalyzer)

# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for L1EG TPs
process.analyzer = cms.EDAnalyzer('L1EGPreclusterAnalysis',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
)
process.p2 = cms.Path(process.analyzer)


process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('ecalTP.root')
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



