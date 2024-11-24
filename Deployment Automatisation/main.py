import custom_functions

source_folder = "C:/APP/ETL/DM9_ETL/DM9_ETL/"
destination_folder = "C:/Users/merostiashvili/Downloads/"
jira_user_name = 'merostiashvili@tbcbank.com.ge'
jira_api_token = ''
package_is_new = ""
user_selected_file = ""
Jira_issue_number = ""
needs_script_update = ""
needs_configuration_update = ""
instructions = ""

jira_issue_number = input("გთხოვ შეიყვანო დანერგვის ამოცანის ნომერი (SQDDM9-ს გარეშე)\n").upper()
instructions += "დანერგვის ინსტრუქცია:\n"
if "SQDDM9" not in jira_issue_number:
    jira_issue_number = "SQDDM9-" + jira_issue_number
destination_folder_path = f'{destination_folder}{jira_issue_number} - დანერგვა'  # Change this to your desired folder

package_update_type = "არსებულს გადაეწეროს"
package_is_deployed = input("პაკეტი ინერგება ? y/n\n")
if package_is_deployed.lower() == "y":
    user_selected_file = custom_functions.pick_file_from_directory(source_folder)
    custom_functions.copy_etl_files_to_new_folder(user_selected_file, destination_folder_path)
    # upload_attachment_to_jira(jira_issue_number, user_selected_file, jira_user_name, jira_api_token)
    package_is_new = input("პაკეტი ახალია ? y/n \n")
    if package_is_new.lower() == "y":
        package_update_type = "ჩაიწეროს"

    instructions += f"""FCDMREPSRV -სერვერზე\nD:\\SSISPackages\\FICODM9 -საქაღალდეში უნდა {package_update_type} შემდეგი ფაილი: 
    {user_selected_file}\n"""
    needs_configuration_update = input("კონფიგურაციას აახლებ y/n ?\n")
    # Specify the file path
    file_path = f'{source_folder}{user_selected_file.replace('.dtsx', '')}.dtsConfig'

    # Call the function

    if needs_configuration_update.lower() == "y":
        instructions += f"""\nD:\\SSISPackages\\FICODM9\\Config -საქაღალდეში უნდა {package_update_type} შემდეგი ფაილი:
        {user_selected_file}.dtsConfig\n"""
        instructions += custom_functions.check_file_for_stars(file_path)
        custom_functions.copy_etl_files_to_new_folder(f"{user_selected_file.replace(".dtsx","")}.dtsConfig", destination_folder_path)
        # upload_attachment_to_jira(jira_issue_number, f"{user_selected_file.replace(".dtsx","")}.dtsConfig", jira_user_name, jira_api_token)

needs_script_update = input("სკრიპტის გადატარება გჭირდება? y/n \n")
if needs_script_update.lower() == "y":
    instructions += f"""FCDMDB -სერვერზე უნდა გადატარდეს {jira_issue_number}.sql სკრიპტი\n\n"""
    custom_functions.save_text_to_file("", destination_folder_path, f"{jira_issue_number}.sql")

# save instruction file
file_name = f'{jira_issue_number} - დანერგვის ინსტრუქცია.txt'  # Name of the file to save
text_to_save = instructions

custom_functions.save_text_to_file(text_to_save, destination_folder_path, file_name)
new_folder = "file://" + destination_folder_path.replace('\\',r"/")
new_folder_to_move = "f" + destination_folder_path.replace('\\',r"/")

custom_functions.subprocess.Popen(['explorer',new_folder])
# update_jira_custom_field(jira_issue_number, next_tuesday_or_friday(),  jira_user_name, jira_api_token)



