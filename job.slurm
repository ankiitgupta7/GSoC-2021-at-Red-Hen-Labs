#!/bin/bash
#SBATCH -N 1 
#SBATCH -c 1 
#SBATCH --mem-per-cpu=1G 
#SBATCH --time=0-00:15:00 # 15 minutes 
#SBATCH --output=my.stdout 
#SBATCH --mail-user=axg1218@case.edu 
#SBATCH --mail-type=ALL 
#SBATCH --job-name="just_a_test" 
# Put commands for executing job below this line 
# This example is loading the default Python module and then 
# writing out the version of Python 

module load python 

cd /scratch/users/axg1218
# # git clone https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs.git

cd Google-Summer-of-Code-at-Red-Hen-Labs
# https://stackoverflow.com/questions/16508817/how-do-i-provide-input-to-a-c-program-from-bash
./run.sh
