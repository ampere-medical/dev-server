import pandas as pd
from core import ai
import hashlib
import datetime

def entries_to_html(entries):
    # Initialize variables
    previous_hash = ''
    data = []

    # Iterate over entries
    for entry in entries:
        # Generate timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Hash the entry with the previous hash and timestamp (blockchain style)
        hasher = hashlib.sha3_256()
        hasher.update((previous_hash + timestamp + entry).encode('utf-8'))
        current_hash = hasher.hexdigest()

        # Add the data to the list
        data.append([timestamp, current_hash, entry])

        # Update the previous hash
        previous_hash = current_hash

    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=['Timestamp', 'Hash', 'Data'])

    # Convert the DataFrame to HTML
    html_output = df.to_html(index=False)

    return html_output


def get_patient_html_by_name(name):
    response = ai.chatGPTRequest(
        f"Generate a series of about 10 FHIR entries for a fictional patient named {name}. The first entry type should be a Patient resource, and should also include the patient's name, birthday, age, and gender. The second entry type should be an Observation resource. The third entry type should be a Condition resource. The fourth entry type should be a Medication resource. The fifth entry type should be a Procedure resource. The sixth entry type should be a DiagnosticReport resource. The seventh entry type should be a CarePlan resource. The eighth entry type should be an Immunization resource. The ninth entry type should be a FamilyMemberHistory resource. The tenth entry type should be a DocumentReference resource. Make the entries realistic, but also in human readable format. Separate each entry with a single plus sign (as entries may contain whitespace in themselves for readability)."
    )

    entries = response.split("+")

    return entries_to_html(entries)