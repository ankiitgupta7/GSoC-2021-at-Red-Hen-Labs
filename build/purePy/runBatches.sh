#!/bin/bash

# Define parameters
agentSize=(10)
radiusFOV=(50)
angleFOV=(200)
popGrowth=(1)
numRefuge=(3)
patchDensity=(0.6)
simAreaParam=(1000)
rsm=(0.5)
oneGeneration=(1000)
vervetBreedingProbability=(0.5)
predatorBreedingProbability=(0.1)
predationSuccessProb=(0.5)
eIntakeFactor=(0.5)
forageFactor=(0.9)
resourceGrowthRate=(30)
scanFactor=(1)
n_predator=(10 5)
n_vervet=(300)
alarmPotency=(0 1 2)

# Number of replicates
k=3

# Base directory
base_dir="./data"

# Create the base directory if it doesn't exist
mkdir -p "$base_dir"

# Counter for condition index
condition_index=1

# Generate all combinations of parameters (excluding alarmPotency)
for as in "${agentSize[@]}"; do
  for rf in "${radiusFOV[@]}"; do
    for af in "${angleFOV[@]}"; do
      for pg in "${popGrowth[@]}"; do
        for nr in "${numRefuge[@]}"; do
          for pd in "${patchDensity[@]}"; do
            for sap in "${simAreaParam[@]}"; do
              for rs in "${rsm[@]}"; do
                for og in "${oneGeneration[@]}"; do
                  for vbp in "${vervetBreedingProbability[@]}"; do
                    for pbp in "${predatorBreedingProbability[@]}"; do
                      for psp in "${predationSuccessProb[@]}"; do
                        for eif in "${eIntakeFactor[@]}"; do
                          for ff in "${forageFactor[@]}"; do
                            for rgr in "${resourceGrowthRate[@]}"; do
                              for sf in "${scanFactor[@]}"; do
                                for np in "${n_predator[@]}"; do
                                  for nv in "${n_vervet[@]}"; do
                                    # Create folders and CSVs for each replicate
                                    for ((replicate_index=1; replicate_index<=k; replicate_index++)); do
                                      for ap in "${alarmPotency[@]}"; do
                                        # Construct folder path
                                        folder_path="${base_dir}/Condition_${condition_index}/Replicate_${replicate_index}/AlarmPotency_${ap}"
                                        mkdir -p "$folder_path"
                                        
                                        # Path for the CSV file
                                        csv_file_path="${folder_path}/parameters.csv"
                                        
                                        # Write parameters to CSV
                                        echo "agentSize,radiusFOV,angleFOV,popGrowth,numRefuge,patchDensity,simAreaParam,rsm,oneGeneration,vervetBreedingProbability,predatorBreedingProbability,predationSuccessProb,eIntakeFactor,forageFactor,resourceGrowthRate,scanFactor,n_predator,n_vervet,alarmPotency" > "$csv_file_path"
                                        echo "$as,$rf,$af,$pg,$nr,$pd,$sap,$rs,$og,$vbp,$pbp,$psp,$eif,$ff,$rgr,$sf,$np,$nv,$ap" >> "$csv_file_path"
                                        # Construct paramList as a string representation of the list for Python
                                        paramList="[$as, $rf, $af, $pg, $nr, $pd, $sap, $rs, $og, $vbp, $pbp, $psp, $eif, $ff, $rgr, $sf, $np, $nv, $ap]"
                                        
                                        # Call the Python function, passing the paramList and dataPath
                                        # Note: Ensure that the 'execute' module is in your PYTHONPATH or the same directory as the script
                                        python_command="python3 -c \"import execute; execute.runFromBash(1, $paramList, '$csv_file_path')\"" # 1 is the number of generations

                                        # Create a unique SLURM job script for this set of parameters
                                        job_script="slurm_job_${condition_index}_${replicate_index}_${ap}.sh"

# Generate the SLURM job script with the specified directives and the Python command
cat <<EOT > "$job_script"

#!/bin/bash
#SBATCH --job-name=my_job_${condition_index}_${replicate_index}_${ap}
#SBATCH --output=my_job_%j.out
#SBATCH --time=01:00:00  # Example: 12 hours time limit
#SBATCH --ntasks=1
#SBATCH --mem=4G  # Request 4GB of memory

module load Python/3.6.4

# Execute the Python command
$python_command
EOT

# Submit the job to SLURM
sbatch "$job_script"

                                    done
                                  done
                                  ((condition_index++))
                                done
                              done
                            done
                          done
                        done
                      done
                    done
                  done
                done
              done
            done
          done
        done
      done
    done
  done
done

echo "Folder structure and CSV files have been created."
