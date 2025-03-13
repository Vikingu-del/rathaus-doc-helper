

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
    "residence":"./samples/HouseRegistrationSample.pdf",
    "identity": "./samples/passport.jpg",
    # "visa": "./samples/visa.jpg",
}

# Prebuilt models to use
models = {
    "enrollment": "prebuilt-invoice",
    "insurance": "prebuilt-invoice",
    "blocked": "prebuilt-receipt",
    "residence":"prebuilt-invoice",
    "identity": "prebuilt-idDocument",
    # "visa": "prebuilt-idDocument",
}

# Keys to extract from each document type
keys_to_extract = {
    "enrollment": ["VendorName", "VendorAddress"],
    "insurance": ["VendorName"],
    "blocked": ["Total", "MerchantName"],
    "residence":["CustomerAddress"],
    "identity": ["DocumentNumber", "LastName", "FirstName", "DateOfBirth", "PlaceOfBirth", "Sex", "Nationality", "DateOfIssue", "DateOfExpiration"],
    # "visa": ["DocumentNumber", "LastName", "FirstName", "DateOfBirth", "PlaceOfBirth", "Sex", "Nationality", "DateOfIssue", "DateOfExpiration"],
}

frontend = {
    "Familiename": None,
    "Vornamen": None,
    "Geburtsdatum": None,
    "Geburtsort": None,
    "Geschlecht": None,
    "Staatsangehörigkeit": None,
    "Reisepass-Nr.": None,
    "Datum der Ausstellung": None,
    "Datum des Ablaufs": None,
    "Visa Date Of Issue": None,
    "Visa Date Of Expiry": None,
    "Aktuelle Adresse": None,
    "Gesperrtes Konto": None,
    "Kontostand": None,
    "Krankenkasse": None,
    "Beruf": "Student",  # Static value
    "Name der Schule": None,
    "Adresse der Schule": None,
    "Bild": None,
    "Familienstand": None,
    "Vorherige Adresse": None,
    "Größe des Hauses": None,
    "Strafrechtliche Verurteilungen": None,
    "Laufende gerichtliche Ermittlungen": None,
    "Wurde jemals ausgewiesen": None,
    "Gehört zu einer terroristischen Organisation": None,
    "Zugehörigkeit zu einer politischen Partei": None,
    "Jemals die Demokratie gestört": None
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

for doc_type, doc_path in documents.items():
    print(f"\nProcessing {doc_type} document...")
    result = analyze_document(doc_path, models[doc_type])

    for doc in result.documents:
        for field in keys_to_extract[doc_type]:
            if field in doc.fields:
                field_value = doc.fields[field].value.amount if field == "Total" else doc.fields[field].value
                
                # Format address fields properly
                if field in ["VendorAddress", "CustomerAddress"]:
                    field_value = format_address(field_value)

                # Define mapping of document fields to frontend keys
                field_mapping = {
                    "LastName": "Familiename",
                    "FirstName": "Vornamen",
                    "DateOfBirth": "Geburtsdatum",
                    "PlaceOfBirth": "Geburtsort",
                    "Sex": "Geschlecht",
                    "Nationality": "Staatsangehörigkeit",
                    "DocumentNumber": "Reisepass-Nr.",
                    "DateOfIssue": "Datum der Ausstellung",
                    "DateOfExpiration": "Datum des Ablaufs",
                    "CustomerAddress": "Aktuelle Adresse",
                    "MerchantName": "Gesperrtes Konto",
                    "Total": "Kontostand",
                    "VendorName": "Krankenkasse" if doc_type == "insurance" else "Name der Schule",
                    "VendorAddress": "Adresse der Schule",
                }

                # Ensure correct key assignment
                mapped_key = field_mapping.get(field)
                if mapped_key:
                    frontend[mapped_key] = field_value



# Debug: Print final JSON-like dictionary
for key, value in frontend.items():
    print(f"{key}: {value}")
