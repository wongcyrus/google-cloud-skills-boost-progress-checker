# google-cloud-skills-boost-progress-checker
Generate reports for your cloud skills boost class from the list of public profile.

# How to use it?

## Using GitHub Action
1. Fork this repo, and clone it to your local machine.
2. Update GitHub Project with Public Google Spread Sheet ID in Action Secret for student id (Student ID) and their public profile (Public Profile URL). https://docs.github.com/en/actions/security-guides/encrypted-secrets 
3. Open main.py and update the required_tasks list, since students profile may contain a lot of completion badges but it is unrelated to your course.
4. Push it back to GitHub.
5. report.xlsx will be updated every night.

## Manual Mode
1. Clone this repo to your local machine.
2. Update Students.xlsx for student id and their public profile. 
3. Open main.py and update the required_tasks list, since students profile may contain a lot of completion badges but it is unrelated to your course.

### For the first time, you have to create virtual environment
```
python -m venv venv
```

### Activate the virtual environment
For windows,
```
.\venv\Scripts\Activate.ps1   
```

### Install dependences
```
pip install requirements.txt
```

### Run the program
For windows,
```
python .\main.py
```

You will get the report.xlsx.