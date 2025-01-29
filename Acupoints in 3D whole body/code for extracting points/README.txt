Steps for extracting coordinates and labels of acupoints from the point annotation file

1. Use scaffold creator (https://github.com/mlin865/scaffoldmaker/tree/acupoints) to read in the point annotation json file and make a 3D box with acupoints. Rename the output from scaffoldcreator as boxWithAcupoints.exf.

2. Run extract_marker_acupoints.py to generate 3DWholeBody_acupoints.exf