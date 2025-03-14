# Rathaus Document Helper

A tool to help process and manage documents using AI form recognition capabilities.

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Vikingu-del/rathaus-doc-helper.git
   cd rathaus-doc-helper
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   If requirements.txt is not available, install the necessary packages:
   ```
   pip install django
   pip install azure-ai-formrecognizer
   ```

5. Configure your environment (if needed):
   - Create a `.env` file with necessary API keys for Azure Form Recognizer
   - Set up any required Django environment variables

### Running the Application

1. Start the development server:
   ```
   python rathaus/manage.py runserver
   ```

3. Access the application:
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

## Check our Presentation link

[View our presentation](https://prezi.com/view/kyRUPFPYCGYUUdbuIELq/)

## License

[Add license information here]