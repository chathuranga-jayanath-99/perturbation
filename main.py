import os 
import re 

samples_dir_path = './samples/'
perturbed_samples_dir_path = './perturbed_samples/'
corrupted_samples_dir_path = './corrupted_samples'

arg_selfapr = 'SelfAPR'
arg_buglab = 'BugLab'

base_command = 'timeout 600 java -jar ./perturbation_model/target/perturbation-0.0.1-SNAPSHOT-jar-with-dependencies.jar'

def handle_move_statement_action(perturbed_file_infos, original_file_lines):
    corrupt_file_lines = original_file_lines[:]
    corrupt_combined_lines = perturbed_file_infos[1]

    moved_line_no_1 = int(perturbed_file_infos[2]) - 1
    moved_line_no_2 = int(perturbed_file_infos[3]) - 1

    original_line_1 = original_file_lines[moved_line_no_1]
    original_line_2 = original_file_lines[moved_line_no_2]
    
    spaces_count_1 = len(re.match(r'^\s*', original_line_1).group(0))
    spaces_count_2 = len(re.match(r'^\s*', original_line_2).group(0))
    
    try:
        corrupt_splits = corrupt_combined_lines.split(';')
        corrupt_line_1 = corrupt_splits[0].strip()
        corrupt_line_2 = corrupt_splits[1].strip()

        if (corrupt_line_1 == '' or corrupt_line_2 == ''):
            return None 
        
        corrupt_line_1 = ' ' * spaces_count_1 + corrupt_line_1 + ';\n'
        corrupt_line_2 = ' ' * spaces_count_2 + corrupt_line_2 + ';\n'

        corrupt_file_lines[moved_line_no_1] = corrupt_line_1 
        corrupt_file_lines[moved_line_no_2] = corrupt_line_2

        return corrupt_file_lines
    except Exception as e:
        print(f'Unexpected error: {e}')

def handle_transplant_statement(perturbed_file_infos, original_file_lines):
    corrupt_file_lines = original_file_lines[:]
    corrupt_combined_lines = perturbed_file_infos[1]

    transplanted_line_no = int(perturbed_file_infos[2]) - 1
    original_line = original_file_lines[transplanted_line_no]
    spaces_count = len(re.match(r'^\s*', original_line).group(0))
    
    try:
        corrupt_splits = corrupt_combined_lines.split(';')
        corrupt_line_1 = corrupt_splits[0].strip()
        corrupt_line_2 = corrupt_splits[1].strip()

        if (corrupt_line_1 == '' or corrupt_line_2 == ''):
            return None 
        
        corrupt_line_1 = ' ' * spaces_count + corrupt_line_1 + ';\n'
        corrupt_line_2 = ' ' * spaces_count + corrupt_line_2 + ';\n'

        corrupt_file_lines[transplanted_line_no] = corrupt_line_1
        corrupt_file_lines.insert(transplanted_line_no + 1, corrupt_line_2) 
        return corrupt_file_lines
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    with os.scandir(samples_dir_path) as files:
        for file in files:
            # generate perturbations 
            if (file.name.endswith('.java')):
                print(file.name)
                file_path = samples_dir_path + file.name
                execution_command = f'{base_command} {file_path} {arg_selfapr}'
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
                    # [BugLab_Wrong_Operator]^System.out.println ( "Sum: "  ^  sum ) ;^11^^^^^3^13^System.out.println # issue line
                    print('***start perturbed_file_lines***')
                    print(len(perturbed_file_lines))
                    print('***end perturbed_file_lines***')
                    
                     
                    corrupt_files_count = 0
                    for i in range(len(perturbed_file_lines)):
                        try:
                            perturbed_file_line = perturbed_file_lines[i]
                            perturbed_file_infos = perturbed_file_line.split('^')

                            action = perturbed_file_infos[0]
                            if 'P10' in action:
                                corrupt_file_lines = handle_move_statement_action(perturbed_file_infos, original_file_lines)
                            elif 'P11' in action:
                                corrupt_file_lines = handle_transplant_statement(perturbed_file_infos, original_file_lines)
                            else:
                                corrupt_line_code = perturbed_file_infos[1]
                                corrupt_line_no = int(perturbed_file_infos[2]) - 1
                                
                                original_line_code = original_file_lines[corrupt_line_no]
                                spaces_match = re.match(r'^\s*', original_line_code)
                                original_line_spaces_count = len(spaces_match.group(0))

                                corrupt_line_code = ' '*original_line_spaces_count + corrupt_line_code + '\n'

                                corrupt_file_lines = original_file_lines[:]
                                corrupt_file_lines[corrupt_line_no] = corrupt_line_code
                            
                            if corrupt_file_lines is None:
                                continue
                            # print('***corrupt file lines***')
                            # print(corrupt_file_lines)
                            corrupt_file_path = corrupt_dir_path + f'/{i+1}.java'
                            with open(corrupt_file_path, 'w') as cf:
                                cf.writelines(''.join(corrupt_file_lines))
                            corrupt_files_count += 1
                        except Exception as e:
                            print(f'Unexpected error: {e}')
                    print(f'corrupt_files_count: {corrupt_files_count}')