import argparse
import os
import pandas as pd

def generate_message(folder):
    input_sheet = [f for f in os.listdir(folder) if f.endswith('Final.xlsx')]
    if len(input_sheet) == 1:
        input_sheet = input_sheet[0]
        print(f"Final sheet located as {input_sheet}.")
    else:
        print("Error reading in the final sheet")
    output_email = f'{folder}/emails.csv'
    output_grade = f'{folder}/grade.csv'
    
    input_sheet_path = os.path.join(folder, input_sheet)
    df = pd.read_excel(input_sheet_path)  # Read CSV file

    df.dropna(how='all', inplace=True)
    columns = df.columns
    
    # Genearte clean Grade file to be imported into Canvas
    pd.concat([df.iloc[:, :6], df.iloc[:, -1]], axis=1).to_csv(output_grade, index=False)
    print(f'Grade generated into {output_grade}.')
    
    # Initialize the "Message" column with empty strings
    df['Message'] = ""
    
    # Create a list of column pairs (mark, comment) to process
    mark_columns = list(range(6, len(columns)-1, 2))
    comment_columns = list(range(6+1, len(columns), 2))

    # Concatenate comments for each column pair into the "Message" column
    for mark_col, comment_col in zip(mark_columns, comment_columns):
        df['Message'] += df.apply(lambda row: f"{columns[mark_col]}: {row[mark_col]}, {row[comment_col]}\n", axis=1)
    
    # Save the email file
    df['Email'] = df['SIS User ID'].apply(lambda x: x + '@u.nus.edu')
    
    # Modify message here
    df['Message'] = df.apply(lambda row: f"Dear {row['Student']},\n\nHere is your result and feedback for last week's Tutorial Assignment submission:\n\n{row['Message']} \
                             \nI hope you find the feedback helpful in understanding the areas where you can improve. If you have any questions or concerns, please do not hesitate to reach out to us.\n\nThank you!", axis=1)
    df[['Email', 'Message']].to_csv(output_email, index=False)
    print(f'Feedback email generated into {output_email}.')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an email file based on final grade sheet.')
    parser.add_argument('folder', type=str, help='Path to the final grade sheet.')
    args = parser.parse_args()

    generate_message(args.folder)