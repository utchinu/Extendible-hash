import csv
import random as rd
import dataset_creation
import simulate_secondary
import bucket
import extendible_hashing
import display_directory as dd

buckets=[]
main_memory=[]
global_depth=0
directory_len=1
bucket_cnt=1
max_size=2
filename="records.csv"

def bulk_hash():
    global directory_len,global_depth,main_memory,buckets,bucket_cnt,main_memory,max_size
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields=next(csvreader)
        for row in csvreader:
            directory_len,global_depth,main_memory,buckets,bucket_cnt = extendible_hashing.insert(buckets,global_depth,directory_len,row,main_memory,bucket_cnt,max_size)

while(1):
    print("Enter a choice")
    print("Press 1:Simulate secondary memory")
    print("Press 2:Create random dataset")
    print("Press 3:Input dataset from csv file")
    print("Press 4: Bulk hash")
    print("Press 5:Add individual record")
    print("Press 6: To visualize")
    choice=int(input())

    if choice ==1:
        print("Enter the max size for each bucket")
        max_size=int(input())
        buckets.clear()
        buckets=[]
        main_memory.clear()
        global_depth=0
        directory_len=1
        bucket_cnt=1
        buckets=simulate_secondary.simulate(max_size)
        main_memory.clear()
        for i in range(0,1024):
            main_memory.append(-1)
        main_memory[0]=0
    
    elif choice == 2:
        print("Enter the size of dataset")
        sz=int(input())
        dataset_creation.create_initial_dataset(sz)
        filename="records.csv"

    elif choice ==3:
        print("Enter filename")
        filename=input()
    elif choice ==4:
        bulk_hash()
    elif choice==5:
        print("Enter trans_id,trans_sales_amt,customer_name,category")
        row=[]
        row.append(input())
        row.append(input())
        row.append(input())
        row.append(input())
        directory_len,global_depth,main_memory,buckets,bucket_cnt = extendible_hashing.insert(buckets,global_depth,directory_len,row,main_memory,bucket_cnt,max_size)
    else:
        dd.display_directory_table(directory_len,buckets)
