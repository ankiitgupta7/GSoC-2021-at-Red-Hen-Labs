#!/bin/bash
#SBATCH --time=00:20:00      
#SBATCH -N 1                 
#SBATCH -n 1                 
#SBATCH -mem=2gb             


module load python

cd /scratch/users/axg1218
# git clone https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs.git

cd Google-Summer-of-Code-at-Red-Hen-Labs
# https://stackoverflow.com/questions/16508817/how-do-i-provide-input-to-a-c-program-from-bash
./run.sh <<<'100'
