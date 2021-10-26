# LTPAL

## Linear Temporal Public Announcement Logic: a new perspective for reasoning about the knowledge of multi-classifiers


We developed the LTPAL tool is developed to verify the properties of multiple classifiers. Here, properties would appear in the form of LTPAL formulas. Such properties could be investigated for single-framed data (i.e., images) or data-streams (i.e., videos). 

## Input

As it said, the tool could apply to an ensemble of classifiers. Therefore, one should collect classifiers that are suitable for the purpose. Then, each input (and its neighborhoods) should be fed into the classifiers. The output would be a list of detected objects for each data-frame, so there is a list of lists of objects for each data-stream. The input should consist:

* LTPAL formulas (properties),
* PAL formulas,
* Classifiers' output class domain,
* Overlap threshold (this value would define how much overlap for objects is allowed if "one" assigned to this value any overlaps are allowed and "zero" means no overlaps are allowed),
* Number of frames (1 for single data-frame),
* Classifiers' ids,
* For each classifier, predictions for each frame should be written,
* For each classifier, the location of each predicted class should be written ("br{x,y}" and "tl{x,y}" are "Bottom Right" and "Top Left" of the object's location), 
* Sub-features of all classes.

Sample inputs are provided on the tool's webpage ("classifiersPredictions.json" and "subsetDict.json" files). 

## Output

The expected output is a log file, which involves:

* Each frame's Kripke model,
* All execution paths,   
* Evaluation of each property over paths,
* Define whether each formula is a verified or possible answer,
* The transition system with probabilities of each arrow,
* The most probable path.

Sample output file is provided on the tool's webpage ("output_log_file.log" and "result.json" files).


## Execution
After configuration of the input files, "MASKS.py" could be executed using the Python3 compiler (interpreter). 