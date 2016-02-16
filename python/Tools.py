import os
import sys

import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

verbosity = True

class StdStreamSilenter(object):
    """
    Temporarily redirect stdout to /dev/null
    """

    def __init__(self):
        self.__stdout = sys.stdout
        self.__stderr = sys.stderr

    def __enter__(self):
        self.__stdout.flush()
        self.__stderr.flush()
        self.__devnull = open(os.devnull, 'w')

        sys.stdout = self.__devnull
        sys.stderr = self.__devnull

    def __exit__(self, exc_type, exc_value, traceback):
        self.__stdout.flush()
        self.__stderr.flush()
        self.__devnull.close()

        sys.stdout = self.__stdout
        sys.stderr = self.__stderr

def change_input_tag_process_(input_tag, process_name_from, process_name_to):
    if not isinstance(input_tag, cms.InputTag):
        input_tag = cms.untracked.InputTag(input_tag)

    if len(input_tag.getProcessName()) > 0 and input_tag.getProcessName() == process_name_from:
        old_input_tag = input_tag.value()
        input_tag.setProcessName(process_name_to)
        if verbosity:
            print("Changing input tag from %r to %r" % (old_input_tag, input_tag.value()))

    return input_tag

def change_input_tag_(input_tag, from_, to_, parameter_name, padding=''):
    if isinstance(input_tag, str):
        if input_tag == from_:
            old_input_tag = input_tag
            input_tag = to_
            if verbosity:
                print("%sChanging value of parameter %s (input tag) from %r to %r" % (padding, parameter_name, old_input_tag, input_tag))
    else:
        if input_tag.getModuleLabel() == from_:
            old_input_tag = input_tag.value()
            input_tag.setModuleLabel(to_)
            if verbosity:
                print("%sChanging value of parameter %s (input tag) from %r to %r" % (padding, parameter_name, old_input_tag, input_tag.value()))

    return input_tag

def change_string_(string_, from_, to_, parameter_name, padding=''):
    if string_.value() == from_:
        old_string = string_.value()
        string_.setValue(to_)
        if verbosity:
            print("%sChanging value of parameter %s (string) from %r to %r" % (padding, parameter_name, old_string, to_))

    return string_

def change_process_name(module, process_name_from, process_name_to):
    if isinstance(module, cms._Parameterizable):
        for name in module.parameters_().keys():
            value = getattr(module, name)
            type = value.pythonTypeName()

            if 'VInputTag' in type:
                for (i, tag) in enumerate(value):
                    value[i] = change_input_tag_process_(tag, process_name_from, process_name_to)
            elif 'InputTag' in type:
                change_input_tag_process_(value, process_name_from, process_name_to)

            if isinstance(value, cms._Parameterizable):
                change_process_name(value, process_name_from, process_name_to)

def change_input_tags_and_strings(module, from_, to_, parameter_name, padding=''):
    if from_ == to_:
        return

    if isinstance(module, cms._Parameterizable):
        for name in module.parameters_().keys():
            value = getattr(module, name)
            type = value.pythonTypeName()
            local_parameter_name = parameter_name + '.' + name

            if 'VInputTag' in type:
                for (i, tag) in enumerate(value):
                    value[i] = change_input_tag_(tag, from_, to_, local_parameter_name, padding)
            elif 'InputTag' in type:
                change_input_tag_(value, from_, to_, local_parameter_name, padding)
            elif 'string' in type:
                value = change_string_(value, from_, to_, local_parameter_name, padding)

            if isinstance(value, cms._Parameterizable):
                change_input_tags_and_strings(value, from_, to_, local_parameter_name, padding)

def module_has_string(module, string):
    if isinstance(module, cms._Parameterizable):
        for name in module.parameters_().keys():
            value = getattr(module, name)
            type = value.pythonTypeName()

            if 'VInputTag' in type:
                for (i, tag) in enumerate(value):
                    if string in tag.value():
                        return True
            elif 'InputTag' in type:
                if string in value.value():
                    return True
            elif 'string' in type:
                if string == value.value():
                    return True

            if isinstance(value, cms._Parameterizable) and module_has_string(value, string):
                return True


    return False

def configure_slimmedmet_(met):
    del met.t01Variation
    del met.t1Uncertainties
    del met.t1SmearedVarsAndUncs
    del met.tXYUncForRaw
    del met.tXYUncForT1
    del met.tXYUncForT01
    del met.tXYUncForT1Smear
    del met.tXYUncForT01Smear

def add_ak4_chs_jets_(process, isData, bTagDiscriminators):
    from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
    if verbosity:
        jetToolbox(process, 'ak4', 'ak4CHSJetSequence', 'out', PUMethod='CHS', runOnMC=not isData, miniAOD=True, addPUJetID=False, bTagDiscriminators=bTagDiscriminators)
    else:
        with StdStreamSilenter():
            jetToolbox(process, 'ak4', 'ak4CHSJetSequence', 'out', PUMethod='CHS', runOnMC=not isData, miniAOD=True, addPUJetID=False, bTagDiscriminators=bTagDiscriminators)

    if (hasattr(process, 'softPFElectronsTagInfosAK4PFCHS')):
        process.softPFElectronsTagInfosAK4PFCHS.electrons = cms.InputTag('slimmedElectrons')

    if (hasattr(process, 'softPFMuonsTagInfosAK4PFCHS')):
        process.softPFMuonsTagInfosAK4PFCHS.muons = cms.InputTag('slimmedMuons')

def setup_jets_mets_(process, isData):
    """
    Create a new jets collection and a new MET collection with new JECs applied

    Return a tuple of newly created collections (jet, met)
    """

    # Jets

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJets"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = 'AK4PFchs')

    if isData:
        process.patJetCorrFactorsReapplyJEC.levels.append('L2L3Residual')


    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.slimmedJetsNewJEC = patJetsUpdated.clone(
            jetSource = cms.InputTag("slimmedJets"),
            jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
            )

    process.shiftedMETCorrModuleForNewJEC = cms.EDProducer('ShiftedParticleMETcorrInputProducer',
       srcOriginal = cms.InputTag('slimmedJets'),
       srcShifted = cms.InputTag('slimmedJetsNewJEC')
       )

    process.slimmedMETsNewJEC = cms.EDProducer('CorrectedPATMETProducer',
            src = cms.InputTag('slimmedMETs'),
            srcCorrections = cms.VInputTag(cms.InputTag('shiftedMETCorrModuleForNewJEC'))
            )

    return ('slimmedJetsNewJEC', 'slimmedMETsNewJEC')


def check_tag_(db_file, tag):
    import sqlite3

    db_file = db_file.replace('sqlite:', '')
    connection = sqlite3.connect(db_file)
    res = connection.execute('select TAG_NAME from IOV where TAG_NAME=?', tag).fetchall()

    return len(res) != 0

def append_jec_to_db_(process, label, prefix):

    for set in process.jec.toGet:
        if set.label == label:
            return

    tag = 'JetCorrectorParametersCollection_%s_%s' % (prefix, label)
    if not check_tag_(process.jec.connect.value(), (tag,)):
        print("WARNING: The JEC payload %r is not present in the database you want to use. Corrections for this payload will be loaded from the Global Tag" % label)
        return

    process.jec.toGet += [cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string(tag),
            label  = cms.untracked.string(label)
            )]

def load_jec_from_db(process, db, algorithmes):
    """
    Inform CMSSW to read the JEC from a database instead of the GT for the given list of algorithmes
    """

    import os
    if not os.path.isfile(db):
        raise ValueError('Database %r does not exist.' % db)

    if os.path.isabs(db):
        raise ValueError('You cannot use an absolute for the database, as it breaks crab submission. Please put the database in the same folder as your python configuration file and pass only the filename as argument of the create function')

    process.load("CondCore.DBCommon.CondDBCommon_cfi")

    if verbosity:
        print("Using database %r for JECs\n" % db)

    process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(0)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(),

            connect = cms.string('sqlite:%s' % db)
            )

    process.gridin.input_files += [os.path.abspath(db)]

    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')

    prefix = os.path.splitext(db)[0]
    for algo in algorithmes:
        append_jec_to_db_(process, algo, prefix)
