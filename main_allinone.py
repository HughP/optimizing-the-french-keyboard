from objectives import * 
from read_input import *
from plotting import *
from reformulation_input import *
from evaluate_reformualtion_solution import * 
from optimize import *
import sys

PYTHONIOENCODING="utf-8"

#Define scenario and weights
w_p, w_a, w_f, w_e =  [0.25,0.25,0.25,0.25]
corpus_weights = {'formal':0.5, 'twitter':0.3, 'code':0.2}
scenario = "scenarioMIN"
char_set = "setFULL"
set_scenario_files(scenario, char_set)

#prepare input file to reformulate the problem
filename=scenario+char_set+"_even"
create_reformulation_input(w_p, w_a, w_f, w_e, corpus_weights, filename,
                           quadratic=1)
#run c++ code to reformulate the problem
print("REFORMULATE")						   
subprocess.run("./reformulation/kaufmannbroeckx << reformulation/input/"+filename+".txt >> reformulation/"+filename+".lp", shell=True, check=True)


#optimize the reformulation

#optimize_reformulation("reformulation/reformulation_input_scenario3.lp")
