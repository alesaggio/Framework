import FWCore.ParameterSet.Config as cms

default_configuration = cms.PSet(
        type = cms.string('jets'),
        prefix = cms.string('jet_'),
        enable = cms.bool(True),
        parameters = cms.PSet(
            jets = cms.untracked.InputTag('slimmedJets'),
            cut = cms.untracked.string("pt > 10"),
            btags = cms.untracked.vstring('pfCombinedInclusiveSecondaryVertexV2BJetTags', 'pfJetProbabilityBJetTags', 'pfCombinedMVABJetTags', 'pfCombinedMVAV2BJetTags'),
            scale_factors = cms.untracked.PSet(
                csvv2_loose = cms.untracked.PSet(
                    algorithm = cms.untracked.string('csvv2'),
                    working_point = cms.untracked.string('loose'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_bjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_cjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_lightjets_incl_CSVv2_BtoH_moriond17.json'),
                            ),
                        )
                    ),
                csvv2_medium = cms.untracked.PSet(
                    algorithm = cms.untracked.string('csvv2'),
                    working_point = cms.untracked.string('medium'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_bjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_cjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_lightjets_incl_CSVv2_BtoH_moriond17.json'),
                            ),
                        )
                    ),
                csvv2_tight = cms.untracked.PSet(
                    algorithm = cms.untracked.string('csvv2'),
                    working_point = cms.untracked.string('tight'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_bjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_cjets_comb_CSVv2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_lightjets_incl_CSVv2_BtoH_moriond17.json'),
                            ),
                        )
                    ),
                cmvav2_loose = cms.untracked.PSet(
                    algorithm = cms.untracked.string('cmvav2'),
                    working_point = cms.untracked.string('loose'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_bjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_cjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_loose_lightjets_incl_cmvav2_BtoH_moriond17.json'),
                            ),
                        )
                    ),
                cmvav2_medium = cms.untracked.PSet(
                    algorithm = cms.untracked.string('cmvav2'),
                    working_point = cms.untracked.string('medium'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_bjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_cjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_medium_lightjets_incl_cmvav2_BtoH_moriond17.json'),
                            ),
                        )
                    ),
                cmvav2_tight = cms.untracked.PSet(
                    algorithm = cms.untracked.string('cmvav2'),
                    working_point = cms.untracked.string('tight'),
                    files = cms.untracked.VPSet(
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('bjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_bjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('cjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_cjets_ttbar_cmvav2_BtoH_moriond17.json'),
                            ),
                        cms.untracked.PSet(
                            flavor = cms.untracked.string('lightjets'),
                            file = cms.untracked.FileInPath('cp3_llbb/Framework/data/ScaleFactors/BTagging_tight_lightjets_incl_cmvav2_BtoH_moriond17.json'),
                            ),
                        )
                    )
                ),
                computeRegression = cms.untracked.bool(False),
                regressionFile = cms.untracked.FileInPath('cp3_llbb/Framework/data/BJetRegression/ttbar-spring16-500k-13d-300t.weights.xml')
            )
        )
