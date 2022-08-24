# google-cloud-skills-boost-progress-checker
Generate reports for your cloud skills boost class from the list of public profile.

# How to use it?
Clone this repo to your local machine.
Update Students.xlsx for student id and their public profile. 

Open main.py and update the required_tasks list, since students profile may contain a lot of completion badges but it is unrelated to your course.

## For the first time, you have to create virtual environment
```
python -m venv venv
```

## Activate the virtual environment
For windows,
```
.\venv\Scripts\Activate.ps1   
```

## Install dependence
```
pip install requirements.txt
```

## Run the program
For windows,
```
python .\main.py
```

You will get the report.xlsx.