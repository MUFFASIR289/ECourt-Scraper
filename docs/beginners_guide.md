# Complete Beginner's Guide to the eCourts Scraper Project

## Welcome!

This guide will help you understand EVERYTHING about this project, even if you're completely new to Python and web scraping.

---

## Part 1: Understanding the Basics

### What is Web Scraping?

**Simple explanation**: Web scraping is like teaching a robot to read websites and collect information, just like you would copy information from a webpage into a notebook.

**Real-world example**: 
- You visit eCourts website
- You type in a case number
- You read the information
- You write it down

Web scraping automates this process!

### What Technologies Are We Using?

1. **Python** - The programming language (like the language the robot understands)
2. **Selenium** - Controls a web browser automatically (like remote-controlling Chrome)
3. **BeautifulSoup** - Reads and understands HTML (the language of web pages)
4. **argparse** - Handles command-line options (so users can give instructions)

---

## Part 2: Understanding the Project Structure

### File Organization

Think of the project like a restaurant:



ecourts_scraper/ [The Restaurant Building]
│
├── src/ [The Kitchen - where work happens]
│ ├── main.py [Front desk - takes orders]
│ ├── scraper.py [Head chef - does the main work]
│ ├── models.py [Recipe cards - data structure]
│ ├── utils.py [Kitchen tools - helper functions]
│ └── config.py [Menu - all settings]
│
├── data/ [Storage room]
│ ├── json/ [Cooked dishes - output files]
│ ├── pdf/ [Takeaway boxes]
│ └── logs/ [Kitchen diary - what happened]
│
├── requirements.txt [Shopping list - what to buy]
└── README.md [Restaurant guide]


### What Each File Does

**1. config.py** - The Settings File
- Contains things like URLs, timeouts, file paths
- If the website URL changes, you only need to update it in one place!

**2. models.py** - Data Structures
- Defines what a "case" looks like
- Keeps data organized, like having labeled boxes for different items

**3. utils.py** - Helper Functions
- Small useful functions like validate_cnr(), get_date_string(), save_to_json()
- Don't repeat the same code everywhere. Write once, use everywhere!

**4. scraper.py** - The Brain
- This does the actual work of scraping the website
- Opens browser, goes to website, enters CNR, gets results

**5. main.py** - The Interface
- Handles command-line arguments
- Makes the project easy to use from the command line

---

## Part 3: How the Code Works (Step by Step)

### Scenario: User searches for a case

**Step 1: User runs command**

python main.py --cnr MHAU019999992015 --today


**Step 2: main.py processes command**
1. Parse arguments (understand what user wants)
2. Validate arguments (check if they're correct)
3. Create scraper object
4. Call scraper.search_by_cnr()
5. Display results
6. Save if requested

**Step 3: scraper.py does the work**
1. Open Chrome browser (using Selenium)
2. Go to eCourts website
3. Find the search form
4. Enter the CNR number
5. Wait for CAPTCHA (manual for now)
6. Submit form
7. Wait for results page
8. Extract data from page (using BeautifulSoup)
9. Return organized data

**Step 4: Data flows back**

scraper.py → main.py → User's screen
↘ JSON file (if --save was used)


---

## Part 4: Common Patterns You'll See

### Pattern 1: Try-Except (Error Handling)

try:
# Try to do something
result = scraper.search_by_cnr(cnr)
except TimeoutException:
# If it times out, do this
print("Request timed out!")
except Exception as e:
# For any other error, do this
print(f"Error: {e}")


**Why?** Things can go wrong (network issues, website changes). This prevents crashes.

### Pattern 2: With Statement (Automatic Cleanup)

with ECourtsScraper() as scraper:
result = scraper.search_by_cnr(cnr)
# Automatically calls scraper.close() when done


**Why?** Ensures browser closes even if errors occur. Like auto-save in games!

### Pattern 3: F-strings (Formatted Strings)

name = "John"
age = 30
message = f"Hello, {name}. You are {age} years old."


**Why?** Easier to read and write.

---

## Part 5: How to Use the Project

### Installation (Step by Step)

**1. Install Python**
- Go to python.org
- Download Python 3.8+
- Run installer
- Check "Add to PATH"

**2. Install Chrome**
- Download from google.com/chrome
- Install normally

**3. Download project**

cd ecourts_scraper

and then you can create virtual environment, install requirements.txt and do some sample runs as given below:

cd src
python main.py --cnr MHAU019999992015

Check if listed today
python main.py --cnr MHAU019999992015 --today

Save results
python main.py --cnr MHAU019999992015 --save

Show browser (for debugging)
python main.py --cnr MHAU019999992015 --no-headless

