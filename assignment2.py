import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
    """Downloads the data from the specified URL."""
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error downloading data from {url}: {e}")
        print(f"Could not download data. Check errors.log for more info.")
        exit()

def processData(file_content):
    """
    Processes the file line by line and returns a dictionary that maps a person's ID to a tuple of the form (name, birthday).
    """
    results_dict = {}
    lines = file_content.strip().split('\n')  

    for line in lines[1:]:  
        try:
            row = line.split(',')
            person_id = int(row[0])  
            name = row[1]  
            birthday = datetime.datetime.strptime(row[2], '%d/%m/%Y')  
            results_dict[person_id] = (name, birthday)
        except (ValueError, IndexError) as e:
            logging.error(f"Error processing line: {line} - {e}")
    
    return results_dict

def displayPerson(id, personData):
    """Displays the person's name and birthday given an ID."""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id}: {name}, Birthday: {birthday.strftime('%d/%m/%Y')}")
    else:
        print(f"No user found with ID {id}")

def main(url):
    """Main function to download, process, and interactively display person data."""
    
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
   
    file_data = downloadData(url)
    
    
    person_dict = processData(file_data)
    
    while True:
        try:
            user_input = int(input("Enter an ID to lookup or 0 to exit: "))
            if user_input <= 0:
                break
            displayPerson(user_input, person_dict)
        except ValueError:
            print("Please enter a valid Number.")

if __name__ == "__main__":
    """Main entry point"""
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
