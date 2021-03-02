import bucket

tot_buckets=1000000

def display_directory_table(directory_len,buckets):
    for i in range(0,directory_len):
        print("dir id is"+ str(i))
        bid=buckets[tot_buckets-1-i].next_bucket

        cnt=0
        print("local depth is",buckets[bid].local_depth)
        while(bid!=-1):
            if cnt>=1:
                print("showing",cnt,"overflow bucket")
            for each in buckets[bid].records:
                print(each[0])
            bid=buckets[bid].next_bucket
            cnt+=1
        print("...........................")
    print(buckets[0].empty_spaces)
