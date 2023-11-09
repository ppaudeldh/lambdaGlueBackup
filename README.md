# Boto3 Script to backup AWS Lambda functions and Glue jobs.  

## Running the script
1. Clone the repo  

2. Enter the directory  
    $ cd lambdaGlueBackup  

3. Create a virtual environment  
    $ python -m venv .venv  
    $ source .venv/bin/activate  

4. Install the requirements  
    $ pip install -r requirements.txt

5. Create directory to store the scripts  
    $ mkdir backup  

6. Run the script
    $ python lambda.py backup
    $ python glue.py backup

Note: You must already have AWS credentials setup.  


