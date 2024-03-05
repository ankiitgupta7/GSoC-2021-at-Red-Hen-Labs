from pathlib import Path
import itertools
import csv



def getParamRange():
    agentSize = [10]  # means vervet size parameter is 10
    radiusFOV = [50]    # means field of view for vervets is 50 meters
    angleFOV = [200]    # means field of view for vervets is 200 degrees
    popGrowth = [1] # means reproduction is allowed
    numRefuge = [3] # number of refuges in the environment from each predator
    patchDensity = [.6] # means 60% of the patches are occupied with resources
    simAreaParam = [1000]   # makes 1000x1000 px area
    rsm = [.5]  # real speed multiplier, makes 1 m/sec to 0.5 px/frame

    oneGeneration = [10000, 500] # means one generation has 10000 frames, can take values between 1000 to 10000
    breedingProbability = [.1]  # can take values between .1 to 1
    predationSuccessProb = [.5, .8] # can take values between .1 to 1
    eIntakeFactor = [.5]    # can take values between .1 to 1
    forageFactor = [.9] # can take values between .1 to .9
    resourceGrowthRate = [30]   # can take values between 6 to 60
    scanFactor = [1]    # can take values between .2 to 2

    n_predator = [10, 5]
    n_vervet = [300]

    alarmPotency = [0,1,2]  # 0 means no alarm call, 1 means undiffentiated alarm call, 2 means alarm call differentiated by predator type

    return agentSize, radiusFOV, angleFOV, popGrowth, numRefuge, patchDensity, simAreaParam, rsm, oneGeneration, breedingProbability, predationSuccessProb, eIntakeFactor, forageFactor, resourceGrowthRate, scanFactor, n_predator, n_vervet, alarmPotency

def create_folders_and_csv_for_replicates(x, k):
    """
    Generate folders for each condition and replicate. Inside each replicate's folder, 
    create a CSV file with the parameter list for that condition.
    
    Parameters:
    x: The output from getParamRange(), representing the parameter ranges.
    k: Number of replicates for each condition.
    """
    # Parameter names, excluding alarm potency
    param_names = [
        "agentSize", "radiusFOV", "angleFOV", "popGrowth", "numRefuge", 
        "patchDensity", "simAreaParam", "rsm", "oneGeneration", 
        "breedingProbability", "predationSuccessProb", "eIntakeFactor", 
        "forageFactor", "resourceGrowthRate", "scanFactor", "n_predator", 
        "n_vervet", "alarmPotency"
    ]

    *other_params, alarm_potency_values = x  # Separate parameters and alarm potency

    # Generate all possible combinations of parameters excluding alarm_potency
    all_conditions = list(itertools.product(*other_params))
    
    base_path = Path("./data")  # Define the base path for data storage

    for condition_index, condition in enumerate(all_conditions, start=1):
        for replicate_index in range(1, k + 1):
            # Construct folder path for each condition and replicate
            for alarm_potency in alarm_potency_values:
                replicate_folder_path = base_path / f"Condition_{condition_index}" / f"Replicate_{replicate_index}" / f"AlarmPotency_{alarm_potency}"
                
                # Create the directory for the replicate
                replicate_folder_path.mkdir(parents=True, exist_ok=True)
                
                # Path for the CSV file inside the replicate folder
                csv_file_path = replicate_folder_path / "parameters.csv"
                
                with csv_file_path.open(mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(param_names)  # Write the header row
                    
                    # Construct the paramList for the condition, including alarm_potency
                    paramList = list(condition) + [alarm_potency]
                    writer.writerow(paramList)  # Write the paramList to the CSV

            print(f"CSV file created at: {csv_file_path}")

# Define the number of replicates per condition
k_replicates = 3

# Get parameter ranges from your function
param_range = getParamRange()

# Create the folder structure and CSV files for each replicate
create_folders_and_csv_for_replicates(param_range, k_replicates)
