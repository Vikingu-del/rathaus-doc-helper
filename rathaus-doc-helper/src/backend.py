# # Dictionary to store English-German word pairs
# fields = {
#     "Last Name:Familiename",
#     "First Name:Vornamen",
#     "Date Of Birth:Geburtsdatum",
#     "Place Of Birth:Geburtsort",
#     "Sex:Geschlecht",
#     "Citizenship:Staatsangehörigkeit",
#     "Passport No:Reisepass-Nr.",
#     "Date Of Issue:Datum der Ausstellung",
#     "Date Of Expiry:Datum des Ablaufs",
#     "Visa Date Of Issue:Datum der Ausstellung des Visums",
#     "Visa Date Of Expiry:Datum des Ablaufs des Visums",
#     "Current Address:Aktuelle Adresse",
#     "Blocked Account:Gesperrtes Konto",
#     "Health Insurance:Krankenkasse",
#     "Occupation:Beruf",
#     "Name Of School:Name der Schule",
#     "Address Of School:Adresse der Schule",
#     "Picture:Bild",
#     "Purpose:Zweck",
#     "Marital Status:Familienstand"
#     "Prev Address:Vorherige Adresse",
#     "House Size:Größe des Hauses",
#     "Criminal Convictions:Strafrechtliche Verurteilungen",
#     "Ongoing Judicial Investigations:Laufende gerichtliche Ermittlungen",
#     "Ever Been Expelled:Wurde jemals ausgewiesen"
#     "Belong To Terrorisst Organization:Gehört zu einer terroristischen Organisation",
#     "Belong To Political Party:Zugehörigkeit zu einer politischen Partei",
#     "Ever Disrupted Democracy:Jemals die Demokratie gestört"
# }

import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Document Intelligence Configuration
ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
API_KEY = "64eef38c646245679931083ecfd1e1e3"

# Initialize DocumentAnalysisClient
document_client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

# Define document paths
documents = {
    "enrollment": "./samples/EnrollmentLetterSample.pdf",
    "insurance": "./samples/HealthInsuranceSample.pdf",
    "blocked": "./samples/BlockedAccountSample.pdf",
    "residence":"./samples/HouseRegistrationSample.pdf"
    # "identity": "./samples/passport.jpg",
}

# Prebuilt models to use
models = {
    "enrollment": "prebuilt-invoice",
    "insurance": "prebuilt-invoice",
    "blocked": "prebuilt-receipt",
    "residence":"prebuilt-invoice"
    # "identity": "prebuilt-idDocument",
}

# Keys to extract from each document type
keys_to_extract = {
    "enrollment": ["VendorName", "VendorAddress"],
    "insurance": ["VendorName"],
    "blocked": ["Total", "MerchantName"],
    "residence":["CustomerAddress"]
    # "identity": [""],
}

# Function to clean and concatenate address fields
def format_address(address):
    if not address:
        return "Not found"
    
    # Extract only non-empty and non-None values from the AddressValue object
    address_parts = [
        address.house_number,
        address.road,
        address.city,
        address.state,
        address.postal_code,
        address.country_region,
        address.street_address
    ]
    
    # Filter out None or empty values and join them with commas
    return ", ".join(filter(None, address_parts))

# Function to analyze a document
def analyze_document(doc_path, model):
    with open(doc_path, "rb") as f:
        poller = document_client.begin_analyze_document(model, f)
        result = poller.result()
    return result

# Process each document type
for doc_type, doc_path in documents.items():
    print(f"\nProcessing {doc_type} document...")
    result = analyze_document(doc_path, models[doc_type])

    # Loop through documents in result
    for doc in result.documents:
        print("\nExtracted Fields:")
        for field in keys_to_extract[doc_type]:
            if field in doc.fields:
                field_value = doc.fields[field].value
                if field in ["VendorAddress", "CustomerAddress"]:
                    formatted_address = format_address(field_value)
                    print(f"{field}: {formatted_address}")
                else:
                    print(f"{field}: {field_value}")
