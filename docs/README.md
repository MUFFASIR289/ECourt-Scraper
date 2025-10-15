# eCourts Case Scraper

A Python-based web scraper to fetch court case information and listings from the Indian eCourts portal (https://services.ecourts.gov.in/ecourtindia_v6/).

## 📋 Features

✅ Search cases by CNR number or case details  
✅ Check if cases are listed today or tomorrow  
✅ Display serial number and court name for listed cases  
✅ Download complete cause lists  
✅ Save results as JSON files  
✅ Command-line interface with multiple options  
✅ Colored logging and progress indicators  
✅ Robust error handling  

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher  
- Google Chrome browser installed  
- Internet connection  

### Step 1: Clone or Download the Project

If using Git
git clone <your-repo-url>
cd ecourts_scraper

Or download and extract the ZIP file
text

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
python -m venv venv
venv\Scripts\activate

text

**On Linux/Mac:**
python3 -m venv venv
source venv/bin/activate

text

### Step 3: Install Dependencies

pip install -r requirements.txt

text

This will install all required packages:  
- `selenium` - Browser automation  
- `beautifulsoup4` - HTML parsing  
- `requests` - HTTP requests  
- `webdriver-manager` - Automatic ChromeDriver management  
- `colorlog` - Colored logging  

## 📁 Project Structure

ecourts_scraper/
│
├── src/ # Source code
│ ├── main.py # CLI entry point
│ ├── scraper.py # Core scraping logic
│ ├── models.py # Data models
│ ├── utils.py # Utility functions
│ └── config.py # Configuration settings
│
├── data/ # Output directory
│ ├── json/ # JSON results
│ ├── pdf/ # Downloaded PDFs
│ └── logs/ # Log files
│
├── docs/ # Documentation
│ ├── README.md # This file
│ ├── quickstart.md
│ ├── beginners-guide.md
│ └── ecourts-structure.md
│
├── examples/ # Example usage scripts
├── requirements.txt # Python dependencies
└── .gitignore # Git ignore rules

text

## 🎯 Usage

Navigate to the `src` directory before running commands:

cd src

text

### Basic Commands

**1. Search by CNR Number**

python main.py --cnr MHAU019999992015 --today

text

**2. Search by Case Details**

python main.py --case-type CS --case-number 123 --year 2015 --tomorrow

text

**3. Download Cause List**

python main.py --causelist --today

text

**4. Save Results to File**

python main.py --cnr MHAU019999992015 --save

text

**5. Debug Mode (Show Browser)**

python main.py --cnr MHAU019999992015 --no-headless

text

**6. Get Help**

python main.py --help

text

## 📖 Command-Line Options

- `--cnr TEXT` — Search by CNR number (16-character alphanumeric)  
- `--case-type TEXT` — Case type (e.g., CS, CRL.A)  
- `--case-number TEXT` — Case number (numeric)  
- `--year TEXT` — Case year (e.g., 2015)  
- `--today` — Check if case is listed today  
- `--tomorrow` — Check if case is listed tomorrow  
- `--causelist` — Download complete cause list  
- `--date TEXT` — Specific date for cause list (DD-MM-YYYY)  
- `--save` — Save results to JSON file  
- `--output TEXT` — Custom output filename  
- `--download-pdf` — Download case PDF (if available)  
- `--no-headless` — Show browser window (useful for debugging)  
- `--verbose` — Enable verbose output  
- `--version` — Show version information  
- `--help` — Show help message  

## 📊 Output Examples

### Console Output

======================================================================
SEARCH RESULTS
✅ Case found successfully

📋 CASE DETAILS:
CNR Number: MHAU019999992015
Case Type: CS
Case Number: 123
Case Year: 2015
Petitioner: John Doe
Respondent: Jane Doe
Court Name: District Court
Status: Pending

📅 LISTING STATUS:
✓ Case IS LISTED
Date: 16-10-2025
Serial Number: 5
Court: District Court
text

### JSON Output

{
"success": true,
"message": "Case found successfully",
"case_details": {
"cnr": "MHAU019999992015",
"case_type": "CS",
"case_number": "123",
"case_year": "2015",
"petitioner": "John Doe",
"respondent": "Jane Doe",
"status": "Pending"
},
"is_listed": true,
"listing_info": {
"serial_number": 5,
"listing_date": "2025-10-16"
},
"search_timestamp": "2025-10-15T22:35:45.123456"
}

text

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**  
pip install -r requirements.txt

text

2. **ChromeDriver Error**  
- Ensure Chrome is installed  
- The script auto-downloads ChromeDriver  

3. **Element Not Found**  
- Use `--no-headless` to debug  
- Check if website is accessible  
- Increase wait times in `config.py`  

4. **CAPTCHA Issues**  
- Solve CAPTCHA manually in browser  
- Press Enter to continue  

### Viewing Logs

Logs are saved in `data/logs/ecourts_scraper.log`.

## ⚠️ Important Notes

- **CAPTCHA Handling**: Manual solving required  
- **Website Structure**: Parsing logic may need updates  
- **Ethical Use**: Respect eCourts terms; avoid overloading

## 🤝 Contributing

Improvements welcome:
- Implement full cause list download  
- Add PDF download feature  
- Automate CAPTCHA handling  
- Extend search methods  