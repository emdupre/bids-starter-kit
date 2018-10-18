"""
WARNING:
This script was created in October 2018 when the specification
for MP2RAGE files was not fully finalized. Please double check with
latest version of the specs to make sure this is accurate.

This script will create the JSON files required for an MP2RAGE file.
To function it requires a BIDS data set with properly named image files:
The script will through all the folders of a BIDS data set and will create
the JSON files in every folder where it finds a file ending
with '_MPRAGE.nii.gz'.

Created by RG 2018-10-03
"""

import os
import json
from shutil import copyfile
from collections import OrderedDict


# DEFINE CONTENT OF JSON FILES

# sub-*_inv-1_MPRAGE.json
data_inv_1 = OrderedDict([
    ('InversionTime', '900'),
    ('FlipAngle', '5') # ms
])

# sub-*_inv-2_MPRAGE.json
data_inv_2 = OrderedDict([
    ('InversionTime', '2750'),
    ('FlipAngle', '3') # ms
])

# sub-*_T1map.json
# sub-*_T1w.json
data_T1 = OrderedDict([
    ('EstimationMethod', 'Marques et al., 2013'),
])


# sub-*_MPRAGE.json
data_MP2RAGE = OrderedDict([
    ('MagneticFieldStrength',  ''),
    ('ExcitationRepetitionTime',  ''),
    ('InversionRepetitionTime',  ''),
    ('NumberShots',  ''),
    ('Manufacturer',  ''),
    ('ManufacturersModelName',  ''),
    ('DeviceSerialNumber',  ''),
    ('SoftwareVersions',  ''),
    ('StationName',  ''),
    ('InstitutionName',  ''),
    ('InstitutionAddress',  ''),
    ('InstitutionalDepartmentName',  ''),
    ('ReceiveCoilName',  ''),
    ('ReceiveCoilActiveElements',  ''),
    ('GradientSetType',  ''),
    ('MRTransmitCoilSequence',  ''),
    ('MatrixCoilMode',  ''),
    ('CoilCombinationMethod',  ''),
    ('NonlinearGradientCorrection',  ''),
    ('WaterFatShift',  ''),
    ('EchoTrainLength',  ''),
    ('DwellTime',  ''),
    ('MultibandAccelerationFactor',  ''),
    ('AnatomicalLandmarkCoordinates',  ''),
    ('MRAcquisitionType',  ''),
    ('ScanningSequence',  ''),
    ('SequenceVariant',  ''),
    ('ScanOptions',  ''),
    ('SequenceName',  ''),
    ('PulseSequenceType',  'MP2RAGE'),
    ('PulseSequenceDetails',  ''),
    ('ParallelReductionFactorInPlane',  ''),
    ('ParallelAcquisitionTechnique',  ''),
    ('PartialFourier',  ''),
    ('PartialFourierDirection',  ''),
    ('EffectiveEchoSpacing',  ''),
    ('TotalReadoutTime',  ''),
    ('PhaseEncodingDirection',  ''),
    ('EchoTime1',  ''),  # sec
    ('EchoTime2',  ''),  # sec
    ('SliceThickness',  '')  # mm
])

# WRITE THEM

start_dir = ""  # insert here path to your BIDS data set

# list all subjects
subj_ls = next(os.walk(start_dir))[1]

for iSubj in subj_ls:
    print(iSubj)
    # list all subfolders and files for that subject
    subj_dir = os.walk(os.path.join(start_dir, iSubj))
    # go through all the files for that subject
    for path, subdirs, files in subj_dir:
        for name in files:
            # creates the json files in the folder where the the MP2RAGE file is found
            if '_MPRAGE.nii.gz' in name:
                print(os.path.join(path, name))

                json_folder = path

                # _inv-1_MPRAGE.json
                json_name = name[:12] + '_inv-1_MPRAGE.json'
                # create the file
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_inv_1, ff, sort_keys=False, indent=4)

                # _inv-2_MPRAGE.json
                json_name = name[:12] + '_inv-2_MPRAGE.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_inv_2, ff, sort_keys=False, indent=4)

                # _MPRAGE.json
                json_name = name[:12] + '_MPRAGE.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_MP2RAGE, ff, sort_keys=False, indent=4)

                # sub-01_T1map.json
                # sub-01_T1w.json
                data_T1['BasedOn'] = \
                    os.path.join('anat', name[:12] + '_inv1_part-mag_MPRAGE.nii.gz') + ', ' + \
                    os.path.join('anat', name[:12] + '_inv1_part-phase_MPRAGE.nii.gz') + ', ' + \
                    os.path.join('anat', name[:12] + '_inv1_part-mag_MPRAGE.nii.gz') + ', ' + \
                    os.path.join('anat', name[:12] + '_inv1_part-phase_MPRAGE.nii.gz') + ', '

                json_name = name[:12] + '_T1map.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_T1, ff, sort_keys=False, indent=4)

                json_name = name[:12] + '_T1w.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_T1, ff, sort_keys=False, indent=4)