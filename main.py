import os 

samples_dir_path = './samples/'
perturbed_samples_dir_path = './perturbed_samples/'
corrupted_samples_dir_path = './corrupted_samples/'

execution_command = 'timeout 600 java -jar ./perturbation_model/target/perturbation-0.0.1-SNAPSHOT-jar-with-dependencies.jar '

if __name__ == '__main__':
    with os.scandir(samples_dir_path) as entries:
        for entry in entries:
            print(entry.name)
        