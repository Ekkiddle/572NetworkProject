"""
Python script to split and fMRI image into 600 nodes with edges between nodes representing functional connectivity
"""
import os
import numpy as np
import nibabel as nib
import pandas as pd
from nilearn import datasets, input_data
from nilearn.image import resample_to_img

TR = 1.5 # repition time (time that each image takes up)


# Load Schaefer 600 parcellation atlas
schaefer = datasets.fetch_atlas_schaefer_2018(n_rois=600, resolution_mm=2, yeo_networks=7)
atlas_img = nib.load(schaefer.maps)
atlas_labels = schaefer.labels

# Load all fMRI images in the data directory (taking from subject 1 and averaging all 6 test trials)
directory = "data"

#fmri_images = []
#for filename in os.listdir(directory):
#    if filename.endswith(".nii"):
#        filepath = os.path.join(directory, filename)
#        fmri_img = nib.load(filepath)
#        # Append the image to a list of the images that I would like to use.
#        fmri_images.append(fmri_img)

# Load one fMRI image (replace with actual file path)
fmri_img = nib.load("data/sub-001_task-Test_run-01_bold.nii")

timestamps = pd.read_csv("data/sub-001_task-Test_run-01_events.tsv", sep="\t")

# Resample atlas to match fMRI
resampled_atlas = resample_to_img(
    atlas_img, fmri_img, interpolation="nearest", 
    force_resample=True, copy_header=True
)

# Extract time series for each parcel
masker = input_data.NiftiLabelsMasker(resampled_atlas, standardize=True)
time_series = masker.fit_transform(fmri_img)

genre_fmri_indices = {}
# Loop through all rows
for _, row in timestamps.iterrows():
    genre = row['genre']
    onset = row['onset']
    duration = row['duration']
    
    # Compute fMRI indices
    start_index = int(onset / TR)
    end_index = int((onset + duration) / TR)
    
    # Create list of fMRI indices in this range
    indices = list(range(start_index, end_index))
    
    # Store in dictionary
    if genre in genre_fmri_indices:
        genre_fmri_indices[genre].extend(indices)
    else:
        genre_fmri_indices[genre] = indices

# Remove duplicates and sort indices for each genre
for genre in genre_fmri_indices:
    genre_fmri_indices[genre] = sorted(set(genre_fmri_indices[genre]))
    print(genre)

pop_time_series = time_series[genre_fmri_indices["pop"]]



# Compute correlation matrix
#correlation_matrix = np.corrcoef(time_series.T)

# Create node list
#node_list = pd.DataFrame({"Node": range(1, 601), "Label": atlas_labels})
#node_list.to_csv("node_list.csv", index=False)

# Create edge list with correlation threshold > 0.5
#edges = []
#n_nodes = correlation_matrix.shape[0]
#for i in range(n_nodes):
#    for j in range(i + 1, n_nodes):  # Avoid duplicates
#        if correlation_matrix[i, j] > 0.5:
#            edges.append((i + 1, j + 1, correlation_matrix[i, j]))

#edge_list = pd.DataFrame(edges, columns=["Node1", "Node2", "Correlation"])
#edge_list.to_csv("edge_list.csv", index=False)

#print("Node list and edge list have been saved.")
