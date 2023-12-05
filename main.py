import os 

samples_dir_path = './samples/'
perturbed_samples_dir_path = './perturbed_samples/'
corrupted_samples_dir_path = './corrupted_samples/'

arg_selfapr = 'SelfAPR'
arg_buglab = 'BugLab'

base_command = 'timeout 600 java -jar ./perturbation_model/target/perturbation-0.0.1-SNAPSHOT-jar-with-dependencies.jar'

if __name__ == '__main__':
    with os.scandir(samples_dir_path) as files:
        for file in files:
            if (file.name.endswith('.java')):
                print(file.name)
                file_path = samples_dir_path + file.name
                execution_command = f'{base_command} {file_path} {arg_selfapr}'
                os.system(execution_command)        