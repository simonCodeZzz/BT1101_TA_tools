# BT1101_TA_tools

## Generate grade and feedback files

### File
[generate_message.py](./generate_message.py)

### Steps
1. Make sure that your spreadsheet file that ends with **Final.xlsx** is in the relative directory `./folder/` of **generate_message.py**. [A sample spreadsheet](./examples/T1/BT1101%20T1%20Grade%20Sheet%20Final.xlsx) contains the grade and feedback for each question is provided in `./examples/T1/`.

2. Run the script in your terminal by specifying the `folder` argument with the relative directory that contains the spreadsheet file that ends with **Final.xlsx**.
    ```python 
    python generate_message.py --folder ./examples/T1/
    ```

3. The script will consolidate the feedback of individual questions to email messages and output into **emails.csv**. It will also output relevant columns into **grade.csv** which can be easily imported in Canvas.

## Send personalised feedback

### File
[spreadsheet_gmail.py](./spreadsheet_gmail.py)

### Steps
1. Please follow the steps outlined [here](https://support.google.com/accounts/answer/185833?visit_id=638117389350145242-1419633968&p=InvalidSecondFactor&rd=1) to generate an app password for your Gmail account.

2. Edit the config.ini file to include your Gmail address and Gmail app password. To do this, open the `config.ini` file in a text editor and replace the following lines: Replace **your_email** with your Gmail address, **password_from_Gmail** with your Gmail app password.

3. Make sure that your spreadsheet file **emails.csv** is in the relative directory `./folder/` of **spreadsheet_gmail.py**. [A sample spreadsheet](./examples/T1/emails.csv) is provided in `./examples/T1/`.

4. Run the script in your terminal with by specifying the `folder` argument with the relative directory that contains **emails.csv** and `subject` argument with the Email subject.
    ```python 
    python spreadsheet_gmail.py --folder ./examples/T1/ --subject "Email Subject (e.g. BT1101 Tut 1 Feedback)"
    ```

5. The script will read the email addresses and names from the spreadsheet file, and send an email to each address using your Gmail account. The script will also output a file called **success_emails.xlsx** containing all email addresses where emails were successfully sent. The script will automatically add a delay between 2 and 5 seconds before sending each email to avoid overloading the Gmail server.

## Rename the submission scripts

### File
[rename_submission.py](./rename_submission.py)

### Steps
1. Make sure that the submission scripts are in the relative directory `./folder/` of **rename_submission.py**. The submissions scripts should be downloaded from Canvas and extracted out.

2. Make sure that the roaster that contains student information is in the relative path `./roster` of **rename_submission.py**. [A sample roaster](./examples/BT1101_Roaster.csv) is provided in `./examples/`.

3. Run the script in your terminal by specifying the `folder` argument with the relative directory that contains the submission scripts and `roaster` argument with the relative path of the roaster file.
    ```python 
    python generate_message.py --folder ./examples/T1/submissions/ --roaster ./examples/BT1101_Roaster.csv
    ```

4. The script will rename the files downloaded from Canvas to the Integration ID (i.e. the ID that starts with A) in the same file paths. If you wish to rename using the SIS ID (i.e. the ID that starts with E), you may change line 8 from
    ```python
    id_to_fname_map = dict(zip(roster['ID'], roster['Integration ID']))
    ```
    to
    ```python
    id_to_fname_map = dict(zip(roster['ID'], roster['SIS ID']))
    ```