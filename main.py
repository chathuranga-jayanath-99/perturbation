import os 
import re 

samples_dir_path = './samples/'
perturbed_samples_dir_path = './perturbed_samples/'
corrupted_samples_dir_path = './corrupted_samples'

arg_selfapr = 'SelfAPR'
arg_buglab = 'BugLab'

base_command = 'timeout 600 java -jar ./perturbation_model/target/perturbation-0.0.1-SNAPSHOT-jar-with-dependencies.jar'

if __name__ == '__main__':
    with os.scandir(samples_dir_path) as files:
        for file in files:
            # generate perturbations 
            if (file.name.endswith('.java')):
                print(file.name)
                file_path = samples_dir_path + file.name
                execution_command = f'{base_command} {file_path} {arg_buglab}'
                os.system(execution_command)   

                filname_without_ext = file.name.split('.')[0]
                os.system(f'mv ./{samples_dir_path}/{filname_without_ext}Perturbation.java ./{perturbed_samples_dir_path}')
    
    # read perurb file and generate corrupt file
    with os.scandir(perturbed_samples_dir_path) as perturbed_files:
        for perturbed_file in perturbed_files:
            if (perturbed_file.name.endswith('.java')):
                perturbed_filename = perturbed_file.name
                original_filename = perturbed_filename.replace('Perturbation', '')
                print(f'perturbed_filename: {perturbed_filename}')
                print(f'original_filename: {original_filename}')
                original_filename_without_ext = original_filename.split('.')[0]
                
                perturbed_file_path = f'./{perturbed_samples_dir_path}/{perturbed_filename}'
                original_file_path = f'./{samples_dir_path}/{original_filename}'
                corrupt_dir_path = f'./{corrupted_samples_dir_path}/{original_filename_without_ext}'
                os.makedirs(corrupt_dir_path)

                with open(original_file_path) as of:
                    original_file_lines = of.readlines()


                with open(perturbed_file_path) as pf:
                    perturbed_file_lines = pf.readlines()
                    print(f'perturbed_file_lines: {perturbed_file_lines}')
                    
                    # for perturbed_file_line in perturbed_file_lines:
                    perturbed_file_line = perturbed_file_lines[0]
                    perturbed_file_infos = perturbed_file_line.split('^')

                    action = perturbed_file_infos[0]
                    corrupt_line_code = perturbed_file_infos[1]
                    corrupt_line_no = int(perturbed_file_infos[2]) - 1
                    
                    original_line_code = original_file_lines[corrupt_line_no]
                    spaces_match = re.match(r'^\s*', original_line_code)
                    original_line_spaces_count = len(spaces_match.group(0))

                    corrupt_line_code = ' '*original_line_spaces_count + corrupt_line_code + '\n'

                    corrupt_file_lines = original_file_lines[:]
                    corrupt_file_lines[corrupt_line_no] = corrupt_line_code

                    print(corrupt_file_lines)
                    corrupt_file_path = corrupt_dir_path + '/1.java'
                    with open(corrupt_file_path, 'w') as cf:
                        cf.writelines(''.join(corrupt_file_lines))