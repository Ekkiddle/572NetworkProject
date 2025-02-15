# Notes in the Brain
A network analysis project focused on analyzing networks to see what areas of the brain are the most important when listening to music, and how brain networks
change when listening to different musical genres.

The original data is a set of fMRI images taken from [https://openneuro.org/datasets/ds003720/versions/1.0.1]

# Network Files
Found in the networks folder, there are node_lists and edge_lists for each genre that subject one listened to. In each network combination, there
are 574 nodes, as a result of some nodes getting dropped after resampling the fMRI parcelation file to fit in the same shape as the fMRI data files
for test runs 1-6. Each node represents areas of the brain under the following definitions:

### Hemisphere
- LH → Left Hemisphere
- RH → Right Hemisphere

### Network Name (7Networks refers to a 7-network parcellation)
- Vis → Visual
- SomMot → Somatomotor
- DorsAttn → Dorsal Attention
- SalVentAttn → Salience/Ventral Attention
- Limbic → Limbic
- Cont → Control (likely Frontoparietal Control)
- Default → Default Mode

### Region/Functionality
- FEF → Frontal Eye Fields
- PrCv → Precentral/Precentral Cortex
- Post → Posterior
- ParOper → Parietal Operculum
- TempOcc → Temporal-Occipital
- PFCl → Lateral Prefrontal Cortex
- Med → Medial
- OFC → Orbitofrontal Cortex
- TempPole → Temporal Pole
- Par → Parietal
- pCun → Precuneus
- Cing → Cingulate
- PFC → Prefrontal Cortex
- PCC → Posterior Cingulate Cortex
- PHC → Parahippocampal Cortex

Which can then also be split into a number of parcelation areas for each of these regions.
