# -*- coding: utf-8 -*-

"""Docstring

Notes: Ss 105_bb presented with issues during computation of EOG projectors despite
having valid EOG data.
Ss 102_rs No matching events found for word_c254_p50_dot (event id 102)
"""

# Authors: Kambiz Tavabi <ktavabi@gmail.com>
#
#
# License: BSD (3-clause)

          
import numpy as np
import mnefun
from score import score

params = mnefun.Params(tmin=-0.1, tmax=1.0, t_adjust=-39e-3, n_jobs=18,
                       decim=2, n_jobs_mkl=1, proj_sfreq=250,
                       n_jobs_fir='cuda', n_jobs_resample='cuda',
                       filter_length='5s', lp_cut=40., lp_trans='auto',
                       bmin=-0.1)

params.subjects = ['163_1', '163_2', '172_1', '172_2', '180']
params.structurals = [None] * len(params.subjects)
params.run_names = ['%s_1', '%s_2', '%s_3', '%s_4', '%s_5', '%s_6', '%s_7',
                    '%s_8', '%s_9']
params.subject_run_indices = [None, range(6), range(6), range(5), range(6)]
params.dates = [(2014, 0, 00)] * len(params.subjects)
params.subject_indices = range(len(params.subjects))

params.trans_to = 'median'
params.sss_type = 'python'
params.sss_regularize = 'svd'
params.tsss_dur = 4.  # 60 for adults with not much head movements. This was set to 6.

params.score = score  # scoring function to use
params.acq_ssh = 'kambiz@minea.ilabs.uw.edu'  # minea - 172.28.161.8
params.acq_dir = '/sinuhe/data03/jason_words'
params.sws_ssh = 'kam@kasga.ilabs.uw.edu'  # kasga - 172.28.161.8
params.sws_dir = '/data07/kam/nlr'

# epoch rejection criterion
params.reject = dict(grad=np.inf, mag=np.inf, eog=np.inf)
params.flat = dict(grad=1e-13, mag=1e-15)
params.auto_bad_reject = dict(grad=7000e-13, mag=8000e-15)
params.auto_bad_flat = params.flat
params.ssp_ecg_reject = dict(grad=np.inf, mag=np.inf, eog=np.inf)
params.ssp_eog_reject = dict(grad=np.inf, mag=np.inf, eog=np.inf)
params.cov_method = 'shrunk'
params.get_projs_from = range(len(params.run_names))
params.inv_names = ['%s']
params.inv_runs = [range(0, len(params.run_names))]
params.runs_empty = []
params.average_weighting = 'chpi'
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [1, 1, 0],  # EOG # sjjoo-20160826: was 3
                    [0, 0, 0]]  # Continuous (from ERM)

# The scoring function needs to produce an event file with these values
params.in_names = ['word_c254_p20_dot', 'word_c254_p50_dot', 'word_c137_p20_dot',
                   'word_c254_p80_dot', 'word_c137_p80_dot',
                   'bigram_c254_p20_dot', 'bigram_c254_p50_dot', 'bigram_c137_p20_dot',
                   'word_c254_p20_word', 'word_c254_p50_word', 'word_c137_p20_word',
                   'word_c254_p80_word', 'word_c137_p80_word',
                   'bigram_c254_p20_word', 'bigram_c254_p50_word', 'bigram_c137_p20_word']

params.in_numbers = [101, 102, 103, 104, 105, 106, 107, 108,
                     201, 202, 203, 204, 205, 206, 207, 208]

# These lines define how to translate the above event types into evoked files
params.analyses = [
    'All',
    'Conditions'
    ]

params.out_names = [
    ['ALL'],
    ['word_c254_p20_dot', 'word_c254_p50_dot', 'word_c137_p20_dot',
     'word_c254_p80_dot', 'word_c137_p80_dot',
     'bigram_c254_p20_dot', 'bigram_c254_p50_dot', 'bigram_c137_p20_dot',
     'word_c254_p20_word', 'word_c254_p50_word', 'word_c137_p20_word',
     'word_c254_p80_word', 'word_c137_p80_word',
     'bigram_c254_p20_word', 'bigram_c254_p50_word', 'bigram_c137_p20_word']
]

params.out_numbers = [
    [1] * len(params.in_numbers),
    [101, 102, 103, 104, 105, 106, 107, 108,
     201, 202, 203, 204, 205, 206, 207, 208]
    ]

params.must_match = [
    [],
    [],
    ]
# Set what will run
mnefun.do_processing(
    params,
    fetch_raw=False,     # Fetch raw recording files from acquisition machine
    do_score=False,      # Do scoring to slice data into trials

    # Before running SSS, make SUBJ/raw_fif/SUBJ_prebad.txt file with
    # space-separated list of bad MEG channel numbers
    push_raw=False,      # Push raw files and SSS script to SSS workstation
    do_sss=False,        # Run SSS remotely (on sws) or locally with mne-python
    fetch_sss=False,     # Fetch SSSed files from SSS workstation
    do_ch_fix=False,     # Fix channel ordering

    # Before running SSP, examine SSS'ed files and make
    # SUBJ/bads/bad_ch_SUBJ_post-sss.txt; usually, this should only contain EEG
    # channels.
    gen_ssp=False,       # Generate SSP vectors
    apply_ssp=False,     # Apply SSP vectors and filtering
    plot_psd=False,      # Plot raw data power spectra
    write_epochs=False,  # Write epochs to disk
    gen_covs=False,      # Generate covariances

    # Make SUBJ/trans/SUBJ-trans.fif using mne_analyze; needed for fwd calc.
    gen_fwd=False,       # Generate forward solutions (and src space if needed)
    gen_inv=False,       # Generate inverses
    gen_report=True,    # Write mne report html of results to disk
    print_status=True,  # Print completeness status update
)

