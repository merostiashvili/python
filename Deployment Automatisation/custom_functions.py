from datetime import datetime, timedelta
import os
import shutil
import ssl
import requests.auth
import subprocess
import requests
import json
from requests.auth import HTTPBasicAuth
import certifi

def next_tuesday_or_friday():
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    # Check if today is Tuesday or Friday before 3 PM
    if (now.weekday() == 1 or now.weekday() == 4) and current_time < datetime.strptime("15:00", "%H:%M").time():
        return today

    # Calculate the next Tuesday and Friday
    days_ahead = {
        1: (1 - now.weekday() + 7) % 7,  # Days until next Tuesday
        4: (4 - now.weekday() + 7) % 7   # Days until next Friday
    }

    # Get the nearest date
    next_dates = {day: today + timedelta(days=days) for day, days in days_ahead.items() if days > 0}
    nearest_day = min(next_dates, key=next_dates.get)
    result = format(next_dates[nearest_day], "yyyy/mm/dd")
    return result



import requests
import json
from requests.auth import HTTPBasicAuth


def update_jira_custom_field(issue_key, jira_user_name, jira_api_token, custom_field_name, custom_field_value):
    import base64
    import http.client
    import json
    import ssl

    context = ssl._create_unverified_context()
    context.options |= ssl.OP_LEGACY_SERVER_CONNECT

    creds = base64.b64encode(f'{jira_user_name}:{jira_api_token}'.encode()).decode()

    conn = http.client.HTTPSConnection("tbcbank.atlassian.net", context=context)
    payload = json.dumps({
        "fields": {
            f"{custom_field_name}": f"{custom_field_value}"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {creds}',
        'Cookie': 'atlassian.xsrf.token=e6273ce248894926b58d44207deec97b932275da_lin'
    }
    conn.request("PUT", f"/rest/api/3/issue/{issue_key}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))



def get_user_name(string):
    try:

        if 'USR_DM9_ETL' in string:
            return 'USR_DM9_ETL-ის პაროლი'
        elif 'ExchangeServiceUserPassword' in string:
            return 'dm9_info-ის პაროლი'
        elif 'dm9forjira' in string:
            return 'dm9forjira-ს ტოკენი'

    except FileNotFoundError:
        print(f"Error: The file at {string} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_file_for_stars(_file_path):
    results = []  # List to store all results
    try:
        with open(_file_path, 'r') as file:
            lines = file.readlines()

            for i in range(1, len(lines)):
                if '***' in lines[i] or 'password' in lines[i] or '123' in lines[i] or 'Aa123' in lines[i]:
                    result = f"""\n {lines[i - 1].strip().replace('<Configuration ConfiguredType="Property" ', '').replace(' ValueType="String">', '')} მისათითებელია  {get_user_name(lines[i])} """
                    results.append(result)  # Append each result to the list

    except FileNotFoundError:
        print(f"Error: The file at {_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return "\n".join(results)  # Join all results into a single string


def copy_etl_files_to_new_folder(file_name, destination_folder_path, source_folder):
    source_file = source_folder + file_name
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # Construct the full destination file path
    destination_file = os.path.join(destination_folder_path, os.path.basename(source_file))

    try:
        # Copy the file
        shutil.copy2(source_file, destination_file)
        print(f"File copied successfully to {destination_file}")
    except FileNotFoundError:
        print("The specified source file does not exist.")
    except PermissionError:
        print("You do not have permission to access the file or folder.")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_text_to_file(text, folder_path, file_name):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Create the full file path
    file_path = os.path.join(folder_path, file_name)

    # Write the text to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Text saved to {file_path}")

def pick_file_from_directory(directory):
    while True:
        # List files in the specified directory
        files = os.listdir(directory)

        # Check if there are any files
        if not files:
            print("No files available in the directory.")
            return None

        # Display the files to the user
        print("Please pick a file from the following options:")
        files_dictionary = []
        index = 0

        for file in files:
            if '.dtsx' in file and 'DM9_' in file:
                index += 1
                print(f"{index}: {file}")
                # Store only the file name in the list
                files_dictionary.append(file)

        # Get user input
        choice = input("შეიყვანე პაკეტის შესაბამისი ნომერი (ან 'q' პროცესის შესაწყვეტად): ")

        # Allow the user to quit
        if choice.lower() == 'q':
            print("Exiting.")
            return None

        # Validate the input
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(files_dictionary):
                selected_file = files_dictionary[choice_index]
                print(f"You selected: {selected_file}")

                # Store the user's choice in a variable for later use
                user_choice = selected_file
                return user_choice  # Return just the file name
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


# Example usage