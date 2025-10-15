# eCourts Scraper Project Structure

## Complete Folder Structure


ecourts_scraper/
│
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore file
│
├── src/ # Source code directory
│ ├── init.py # Makes src a package
│ ├── main.py # Entry point of the application
│ ├── scraper.py # Core scraping logic
│ ├── models.py # Data models/classes
│ ├── utils.py # Helper/utility functions
│ └── config.py # Configuration settings
│
├── data/ # Data output directory
│ ├── json/ # JSON output files
│ ├── pdf/ # Downloaded PDFs
│ └── logs/ # Log files
│
├── docs/ # Documentation files
│ ├── README.md # Main documentation
│ ├── quickstart.md # Quick start guide
│ ├── beginners-guide.md # Detailed beginner guide
│ └── ecourts-structure.md # This file
│
└── examples/ # Example usage scripts
├── init.py
└── example_usage.py

## File Purposes

### Root Level Files

**README.md**
- Main project documentation
- Installation instructions
- Usage examples
- Troubleshooting guide

**requirements.txt**
- Lists all Python packages needed
- Install with: `pip install -r requirements.txt`

**.gitignore**
- Tells Git which files to ignore
- Prevents uploading cache files, virtual environments, etc.

### src/ Directory (Source Code)

**__init__.py**
- Makes src a Python package
- Allows importing modules

**main.py**
- Entry point of the application
- Command-line interface (CLI)
- Parses user arguments
- Calls appropriate functions

**scraper.py**
- Core scraping functionality
- Contains ECourtsScraper class
- Handles browser automation
- Extracts data from web pages

**models.py**
- Data structures
- Defines CaseDetails, CaseListing, SearchResult classes
- Organizes scraped data

**utils.py**
- Utility functions
- Date handling, validation, file operations
- Logging setup

**config.py**
- Configuration constants
- URLs, timeouts, file paths
- Centralized settings

### data/ Directory (Output)

**json/**
- Stores search results as JSON files
- Auto-generated filenames

**pdf/**
- Stores downloaded case PDFs
- (Feature to be implemented)

**logs/**
- Application log files
- Debugging information

### docs/ Directory (Documentation)

**README.md**
- Complete project documentation
- Installation and usage guide

**quickstart.md**
- 5-minute quick start guide
- Minimal steps to get running

**beginners-guide.md**
- Detailed explanations for beginners
- Code walkthrough
- Learning resources

**ecourts-structure.md**
- This file
- Project structure overview

### examples/ Directory

**example_usage.py**
- Example scripts
- Shows how to use the scraper
- Different use cases

## How Files Work Together

1. **User runs**: `python src/main.py --cnr ABC123`
2. **main.py** reads config from **config.py**
3. **main.py** creates **scraper.py** instance
4. **scraper.py** uses **models.py** to structure data
5. **scraper.py** uses **utils.py** for validation
6. Results saved to **data/json/**
7. Logs saved to **data/logs/**

## Which Files to Edit

### To change settings:
- Edit **config.py**

### To add new features:
- Edit **scraper.py** (new scraping methods)
- Edit **models.py** (new data structures)
- Edit **main.py** (new CLI options)

### To fix bugs:
- Check **data/logs/** for errors
- Edit relevant source file
- Test changes

## File Dependencies

main.py
├── imports config.py
├── imports scraper.py
├── imports utils.py
└── imports models.py

scraper.py
├── imports config.py
├── imports models.py
└── imports utils.py

utils.py
└── imports config.py

models.py
└── (no dependencies)

config.py
└── (no dependencies)

## Quick Reference

| File | Lines of Code | Complexity | Edit Frequency |
|------|--------------|------------|----------------|
| config.py | ~150 | Low | Often |
| models.py | ~150 | Low | Rarely |
| utils.py | ~200 | Medium | Sometimes |
| scraper.py | ~300 | High | Often |
| main.py | ~250 | Medium | Sometimes |

---

This structure follows Python best practices and makes the project:
- Easy to understand
- Easy to maintain
- Easy to extend
- Professional quality