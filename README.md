# google-cloud-skills-boost-progress-checker
Generate PII-free progress reports (`report.xlsx`, `report.html`, and `report.csv`) for your Google Cloud Skills Boost class from a Google Spreadsheet of student public profiles.

The generated reports include only each student's `ID`, completion summary (`Complete All`, `Finished`), and required badge completion marks/dates—public profile URLs and other personal information are excluded from the output.

# How to use it?

## Google Spreadsheet Format
Prepare a public (viewable with link) Google Spreadsheet with a sheet named `Form Responses 1` containing the following columns:
- `Student ID`
- `Public Profile Url`

## Using GitHub Action
1. Fork this repo, and clone it to your local machine.
2. Add your Google Spreadsheet ID to GitHub Actions Secrets as `SHEET_ID`: https://docs.github.com/en/actions/security-guides/encrypted-secrets
3. Open `main.py` and update the `required_tasks` list to match the required badges for your course.
4. Push your changes back to GitHub.
5. `report.xlsx`, `report.html`, and `report.csv` will be updated automatically every day (or via manual workflow dispatch).

## Manual Mode
1. Clone this repo to your local machine.
2. Create a `.env` file in the project root (ignored by Git) with your Google Spreadsheet ID:
   ```env
   SHEET_ID=your_google_spreadsheet_id
   ```
3. Open `main.py` and update the `required_tasks` list to match the required badges for your course.

### Create a virtual environment (first time only)
```powershell
python -m venv venv
```

### Activate the virtual environment
For Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

### Install dependencies
```powershell
pip install -r requirements.txt
```

### Run the program
With `.env` configured:
```powershell
python main.py
```

Or by passing `SHEET_ID` directly in PowerShell:
```powershell
$env:SHEET_ID="your_google_spreadsheet_id"; python main.py
```

This will generate `report.xlsx`, `report.html`, and `report.csv`.
