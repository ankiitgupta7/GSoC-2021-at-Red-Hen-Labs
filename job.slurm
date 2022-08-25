#!/bin/bash
#SBATCH -N 1 
#SBATCH -c 1 
#SBATCH -n 12
#SBATCH --mem-per-cpu=120G 
#SBATCH --time=0-00:45:00 # 45 minutes 
#SBATCH --output=my.stdout 
#SBATCH --mail-user=axg1218@case.edu 
#SBATCH --mail-type=ALL 
#SBATCH --job-name="test" 



SCRATCH_USER=/scratch/users/axg1218
ROOT_FOLDER=$SCRATCH_USER/Google-Summer-of-Code-at-Red-Hen-Labs
TOOL_FOLDER=$SCRATCH_USER/Google-Summer-of-Code-at-Red-Hen-Labs/build/pureComputation
HOME_FOLDER=/mnt/rds/redhen/gallina/home/axg1218
DATA_DUMP_GALLINA=$HOME_FOLDER/data

# Load Module
module load python

# Change directory into $USER
cd $SCRATCH_USER

# # Clone Source Code
# git clone https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs.git

cd $TOOL_FOLDER

python3 execute.py 

# Copy the data generated to home
cp -r $TOOL_FOLDER/data/. $DATA_DUMP_GALLINA
echo "data generated copied to /mnt/rds/redhen/gallina/home/axg1218/data"

cd $SCRATCH_USER/ 

