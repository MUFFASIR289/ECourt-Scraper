# ⚡ Quick Start Guide - eCourts Scraper

**Get up and running in 5 minutes!**

---

## Step 1: Install Python & Chrome

**Check if you have them:**
python --version # Should be 3.8+


If not installed:
- **Python**: Download from python.org
- **Chrome**: Download from google.com/chrome

---

## Step 2: Setup Project

**Navigate to project:**
cd ecourts_scraper


**Create virtual environment:**

For Windows:
python -m venv venv
venv\Scripts\activate


For Mac/Linux:
python3 -m venv venv
source venv/bin/activate


**Install dependencies:**
pip install -r requirements.txt


Wait for installation to complete (~2-3 minutes)

---

## Step 3: Run Your First Search

cd src
python main.py --cnr MHAU019999992015 --no-headless


**What happens:**
1. Chrome browser opens
2. Goes to eCourts website
3. You'll see a CAPTCHA - **SOLVE IT MANUALLY**
4. Press Enter in terminal
5. Results appear!

---

## Common Commands

### Search by CNR
python main.py --cnr MHAU019999992015


### Check if listed today
python main.py --cnr MHAU019999992015 --today


### Save results to file
python main.py --cnr MHAU019999992015 --today --save


### Download cause list
python main.py --causelist --today


### Get help
python main.py --help


---

## Expected Output

╔══════════════════════════════════════════════════════════╗
║ eCourts Case Scraper v1.0 ║
╚══════════════════════════════════════════════════════════╝

2025-10-15 22:30:45 - INFO - Initializing eCourts Scraper...
2025-10-15 22:30:46 - INFO - ✓ Browser initialized
2025-10-15 22:30:47 - INFO - Searching for case with CNR: MHAU019999992015
2025-10-15 22:30:48 - INFO - ✓ Loaded case status page
2025-10-15 22:30:49 - WARNING - ⚠ CAPTCHA detected
Please solve the CAPTCHA in the browser window...
Press Enter after you've solved the CAPTCHA...


---

## Important Notes

### CAPTCHA Handling
- Current implementation requires manual CAPTCHA solving
- Solve in browser window, then press Enter in terminal

### Headless vs. Non-Headless
- `--no-headless`: Shows browser (good for debugging)
- Default: Invisible browser (faster, but can't solve CAPTCHA manually)

### File Locations
- **JSON outputs**: `data/json/`
- **PDFs**: `data/pdf/`
- **Logs**: `data/logs/`

---

## Troubleshooting

### Error: "ModuleNotFoundError"
pip install -r requirements.txt


### Error: "ChromeDriver not found"
- Make sure Chrome is installed
- Script will auto-download ChromeDriver

### Browser doesn't open
Add `--no-headless` flag:
python main.py --cnr ABC123 --no-headless


### Can't find elements
Website structure may have changed. Check:
1. Is the website accessible?
2. Try with a real CNR number
3. Check logs in `data/logs/`

---

## Testing the Project

**Test 1: Help Command**
python main.py --help

Should show all options.

**Test 2: Invalid CNR**
python main.py --cnr ABC

Should show validation error.

**Test 3: Valid Search** (with browser visible)
python main.py --cnr MHAU019999992015 --no-headless

Should open browser and search.

**Test 4: Save Results**
python main.py --cnr MHAU019999992015 --save

Should create JSON file in `data/json/`

---

## Next Steps

1. Read **README.md** for detailed documentation
2. Read **beginners-guide.md** for in-depth explanation
3. Check **examples/example_usage.py** for code examples
4. Customize **config.py** for your needs
5. Extend functionality (add features!)

---

## Pre-Submission Checklist

- [ ] Code runs without errors
- [ ] Tested with multiple CNRs
- [ ] Tested error cases (invalid input)
- [ ] README.md is complete
- [ ] Code is commented
- [ ] requirements.txt is up to date
- [ ] .gitignore is present
- [ ] Removed any sensitive data
- [ ] Created GitHub repo (or prepared ZIP)
- [ ] Tested on fresh environment

---

## Pro Tips

- Always use `--no-headless` when debugging
- Check log files when something goes wrong
- Use `--save` to keep records of searches
- Add `--verbose` for more detailed output
- Test with both valid and invalid inputs

---

## Need Help?

1. Check error message carefully
2. Look in `data/logs/ecourts_scraper.log`
3. Run with `--no-headless` to see what's happening
4. Google the error message
5. Check if eCourts website is accessible