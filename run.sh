#!/bin/bash

SCRATCH_USER=/scratch/users/$USER
ROOT_FOLDER=$SCRATCH_USER/Google-Summer-of-Code-at-Red-Hen-Labs/build/pureComputation
HOME_FOLDER=/home/$USER

# Load Module
module load python3

# Change directory into $USER
cd $SCRATCH_USER/

# Clone Source Code
git clone https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs.git

cd $ROOT_FOLDER

python3 execute.py

# Copy the data generated to home
cp -r $ROOT_FOLDER/data/ $HOME_FOLDER
echo "data generated copied to home"



#Remove all Video and Audio files
rm -rf $SCRATCH_USER
