import csv
import random as rd

def get_customer_name():
    name = ''
    for i in range(1,4):
        temp=rd.randint(0,25)
        name+=chr(temp+ord('A'))
    return(name)

def create_initial_dataset(sz):
    fields = ['trans_id', 'trans_sales_amt', 'customer_name', 'category'] 

    filename="records.csv"

    with open (filename,'w') as csvfile:
 
        csvwriter = csv.writer(csvfile) 

        csvwriter.writerow(fields) 
            
        rows=[]

        for i in range(0,sz):
            row=[]
            row.append(rd.randrange(1,65000))
            row.append(rd.randrange(1,500001,1))
            row.append(get_customer_name())
            row.append(rd.randrange(1,1501,1))
            rows.append(row)
        csvwriter.writerows(rows)

