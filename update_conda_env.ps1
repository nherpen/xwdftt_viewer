# Assuming you have a Conda environment named "myenv" that you want to export

# Define the Conda environment name
$condaEnvName = "xwdftt_viewer_env"

# Define the output YAML file path
$outputYamlFile = "environment.yml"

# Run the Conda command to export the environment to a YAML file
conda env export --name $condaEnvName --file $outputYamlFile

# Print a success message
Write-Host "Conda environment $condaEnvName has been exported to $outputYamlFile."
