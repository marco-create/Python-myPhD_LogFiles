import csv, glob, os, pandas
from csv import reader

path2csv = r'C:\Users\Marco\Documents\VS_code\viscachaReports\*.csv'
print(path2csv)

## START THE FOR LOOP THROUGH LOGFILES
for report in glob.glob(path2csv):
    print('\nFILE NAME: {} \n'.format(os.path.basename(report)))
    # open, read and store the file in a list. Print few lines
    open_file = open(report)
    read_file = reader(open_file, delimiter='\t')
    report = list(read_file)
    print('REPORT (first few lines)\n')
    for line in report[:20]:
        print(line)
    # Condition name, participant name
    condition_name = [line[18:] for line in report[1]]
    participant_name = [line[14:] for line in report[10]]
    print(condition_name, participant_name)
    # Find the line where the answers block starts. Select the answers block
    indexLine_startBlock = [report.index(line) for line in report for cell in line if 'Event time' in cell]
    answer_block = report[int(indexLine_startBlock[0])+1:]
    print('\nStart block at line {}'.format(indexLine_startBlock))
    print(answer_block[:10])
    header = str(report[indexLine_startBlock[0]][0]).split(';')
    print('\nHeader: {}.'.format(header))
    # keep only summary of the trial.
    responses = [line for line in answer_block for cell in line if 'Trial summary' in cell]
    responses = [cell.split(';') for line in responses for cell in line]
    responses.insert(0, header)
    print('\nFew trial summaries: \n')
    for line in responses[:10]:
        print(line)
    # slice out useless columns
    responses = [cells[:7] for cells in responses]
    print('\nFinal responses block:\n')
    for line in responses:
        print(line)
    # store the block in a DataFrame. Change column names and set the number of trial as index.
    data2csv = pandas.DataFrame(responses[1:])
    data2csv.columns = responses[0]
    data2csv = data2csv.set_index('Trial').rename(columns={'Event type':'Condition', 'Event time':'Onset'}).replace({'Trial summary': condition_name})
    data2csv.head()
    # replace comma separated numbers with dots
    data2csv['Onset'] = data2csv['Onset'].apply(lambda x: float(x.split()[0].replace(',','.')))
    data2csv['Duration'] = data2csv['Duration'].apply(lambda x: float(x.split()[0].replace(',','.')))
    data2csv = data2csv[['Condition', 'Onset', 'Duration', 'Selection', 'Correct', 'Success']]

    data2csv.to_excel(r'C:\Users\Marco\Documents\VS_code\viscachaReports\_' +participant_name[0]+'_'+condition_name[0]+'.xlsx')
    print('SAVED')
