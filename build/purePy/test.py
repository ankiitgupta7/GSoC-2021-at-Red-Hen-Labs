# # import datetime
# # import os

# # from pathlib import Path

# # now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# # Path("./data").mkdir(parents=True, exist_ok=True)

# # Path("./data/"+str(now)).mkdir(parents=True, exist_ok=True)

# # print(str(now))

# import itertools

# def getParamList(x):
#     # Extract alarmPotency values and other parameters separately
#     alarm_potency_values = x[-1]
#     other_params = x[:-1]

#     # Initialize a dictionary to hold combinations for each alarmPotency condition
#     param_list_by_alarm_potency = {}

#     for alarm_potency in alarm_potency_values:
#         # Generate all possible combinations for the current alarmPotency, 
#         # along with the combinations of other parameters
#         all_combinations = list(itertools.product(*other_params, [alarm_potency]))
        
#         # Sort the combinations based on the elements at index 7 (real speed multiplier, rsm)
#         sorted_combinations = sorted(all_combinations, key=lambda combination: combination[7])
        
#         # Store the sorted combinations for the current alarmPotency
#         param_list_by_alarm_potency[alarm_potency] = sorted_combinations
        
#         print(f"total {len(sorted_combinations)} input parameter sets to execute for alarmPotency = {alarm_potency}")

#     return param_list_by_alarm_potency



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

# paramRange = getParamRange()

# paramList = getParamList(paramRange)

# # i = 1
# # for param in paramList:
# #     print(i)
# #     print("agentSize: ", param[0], ", radiusFOV: ", param[1], ", angleFOV: ", param[2], ", popGrowth: ", param[3], ", numRefuge: ", param[4], ", patchDensity: ", param[5], ", simAreaParam: ", param[6], ", rsm: ", param[7], ", oneGeneration: ", param[8], ", breedingProbability: ", param[9], ", predationSuccessProb: ", param[10], ", eIntakeFactor: ", param[11], ", forageFactor: ", param[12], ", resourceGrowthRate: ", param[13], ", scanFactor: ", param[14], ", n_predator: ", param[15], ", n_vervet: ", param[16], ", alarmPotency: ", param[17]) 
# #     print("\n")
# #     i += 1



# # Iterate through each alarmPotency and its corresponding parameter sets
# for alarm_potency, combinations in paramList.items():
#     print(f"Alarm Potency: {alarm_potency}, Total Combinations: {len(combinations)}")
#     i = 1
#     for combination in combinations:
#         print(f"Combination {i}:")
#         print("agentSize:", combination[0], ", radiusFOV:", combination[1], ", angleFOV:", combination[2], 
#               ", popGrowth:", combination[3], ", numRefuge:", combination[4], ", patchDensity:", combination[5], 
#               ", simAreaParam:", combination[6], ", rsm:", combination[7], ", oneGeneration:", combination[8], 
#               ", breedingProbability:", combination[9], ", predationSuccessProb:", combination[10], 
#               ", eIntakeFactor:", combination[11], ", forageFactor:", combination[12], 
#               ", resourceGrowthRate:", combination[13], ", scanFactor:", combination[14], 
#               ", n_predator:", combination[15], ", n_vervet:", combination[16], ", alarmPotency:", combination[17])
#         print("\n")
#         i += 1


# import itertools
# import random

# def get_conditions_with_replicates(x, k):
#     """
#     Generate a dictionary of conditions, each with variations for alarm_potency, 
#     including k replicates for each alarm_potency variation within each condition.
    
#     Parameters:
#     x: The output from getParamRange(), representing the parameter ranges.
#     k: Number of replicates for each condition and alarm_potency variation.
    
#     Returns:
#     A nested dictionary with structure {condition_index: {alarm_potency: [replicates]}}
#     """
#     # Split parameter ranges into alarmPotency and other parameters
#     *other_params, alarm_potency_values = x
    
#     # Generate all possible combinations of parameters excluding alarm_potency
#     all_conditions = list(itertools.product(*other_params))
    
#     # Initialize the conditions dictionary
#     conditions_dict = {}
    
#     # Populate the dictionary with conditions, alarm_potency variations, and replicates
#     for condition_index, condition in enumerate(all_conditions, start=1):
#         conditions_dict[condition_index] = {}
#         for alarm_potency in alarm_potency_values:
#             # Generate k replicates for each condition-alarm_potency combination
#             conditions_dict[condition_index][alarm_potency] = [condition + (alarm_potency,) for _ in range(k)]
    
#     return conditions_dict

# # Define the number of replicates per condition and alarm_potency
# k_replicates = 3

# # Get parameter ranges
# param_range = getParamRange()

# # Generate conditions with replicates
# conditions_with_replicates = get_conditions_with_replicates(param_range, k_replicates)

# # Example: Print out the structure or details of the generated conditions
# for condition_index, alarm_potencies in conditions_with_replicates.items():
#     print(f"Condition {condition_index}:")
#     for alarm_potency, replicates in alarm_potencies.items():
#         print(f"  Alarm Potency {alarm_potency}: {len(replicates)} Replicates")
#         # Optionally, print details of each replicate
#         for replicate in replicates:
#             print("    ", replicate)
#     print()  # Add a newline for better readability


import itertools

def get_conditions_with_replicates_and_print(x, k):
    """
    Generate and print conditions with their parameters, including k replicates 
    for each condition and alarm_potency variation, along with the type of data.
    
    Parameters:
    x: The output from getParamRange(), representing the parameter ranges.
    k: Number of replicates for each condition and alarm_potency variation.
    """
    # Parameter names, excluding alarm_potency which is handled separately
    param_names = [
        "agentSize", "radiusFOV", "angleFOV", "popGrowth", "numRefuge", 
        "patchDensity", "simAreaParam", "rsm", "oneGeneration", 
        "breedingProbability", "predationSuccessProb", "eIntakeFactor", 
        "forageFactor", "resourceGrowthRate", "scanFactor", "n_predator", "n_vervet"
    ]

    # Split parameter ranges into alarm_potency and other parameters
    *other_params, alarm_potency_values = x

    # Generate all possible combinations of parameters excluding alarm_potency
    all_conditions = list(itertools.product(*other_params))

    for condition_index, condition in enumerate(all_conditions, start=1):
        for alarm_potency in alarm_potency_values:
            # Generate k replicates for each condition-alarm_potency combination
            replicates = [condition + (alarm_potency,) for _ in range(k)]

            # Print the condition index and alarm potency
            print(f"Condition {condition_index}, Alarm Potency {alarm_potency}:")
            for replicate_index, replicate in enumerate(replicates, start=1):
                # Print each parameter with its name, value, and type
                print(f"  Replicate {replicate_index}:")
                for param_name, value in zip(param_names + ["alarmPotency"], replicate):
                    print(f"    {param_name}: {value} (Type: {type(value).__name__})")
                print()  # Newline for readability

# Define the number of replicates per condition and alarm_potency
k_replicates = 1

# Get parameter ranges
param_range = getParamRange()

# Generate conditions with replicates and print details including types
get_conditions_with_replicates_and_print(param_range, k_replicates)
