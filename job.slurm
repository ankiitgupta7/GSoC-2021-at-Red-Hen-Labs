#!/bin/bash
#SBATCH --time=00:20:00      # 20 minutes of wall time
#SBATCH -N 1                 # 1 Node
#SBATCH -n 1                 # 1 processor
#SBATCH -mem=2gb             # Assign 2gb memory; default in 1gb
#SBATCH -o /scratch/users/axg1218/output%A_%a.o


module load python

cd /scratch/users/axg1218
# git clone https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs.git

cd Google-Summer-of-Code-at-Red-Hen-Labs
# https://stackoverflow.com/questions/16508817/how-do-i-provide-input-to-a-c-program-from-bash
./run.sh <<<'100'
