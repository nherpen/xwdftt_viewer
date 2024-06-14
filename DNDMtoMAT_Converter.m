%Converts all files in Directory to MAT files. 
%Saves them on CurrentDir/PythonData

%Creates save directory (if it does not exist) and obtains all .res
%filenames

% filesInfo = dir(saveDir + '\*.res');
f = dir(pwd + "/reference_data/traces/*.res");

%If DNDM ASML import tool is not available it installs it
if ~exist('DNDM2MAT')
    disp('DNDM2MAT is not yet available. Run start up files ....')
    addpath('M:\HQ_T&D\Software\Matlab\matlab_toolbox\asml_toolbox');
    asml_startup
    addpath('M:\HQ_T&D\Software\Matlab\matlab_toolbox\nl011013_u\servo_twin');
    startup
    disp('Start up files are loaded. DNDM2MAT should be available now')
end

for i=1:length(f)
    dataset = DNDM2MAT(pwd + "\reference_data\traces\" + f(i).name);
    fileTosave = dataset.traces;       
    save(pwd + "\reference_data\traces\mat_files\" + f(i).name + '.MAT', 'fileTosave')
end
