import bucket
import display_directory as dd
tot_buckets=100000


def get_hash(num,global_depth):
    binary=[]

    n=int(num)
    while(n>0):
        binary.append(n%2)
        n=int(n/2)

    while(len(binary)<16):
        binary.append(0)
    prefix=0

    for i in range(0,global_depth):
        l=len(binary)
        prefix=prefix*2+binary[l-1-i]

    return(prefix)

def get_bucket_id(trans_id,main_memory,buckets,global_depth):
    prefix=get_hash(trans_id,global_depth)

    #Retriving from main memory    
    if(prefix<1024):
        return main_memory[prefix]

    return(buckets[tot_buckets-1-prefix].next_bucket)

def rearrange(trans_id,buckets,global_depth,max_size,bucket_cnt,rec,main_memory):
    print("increasing local depth for ",rec[0])
    records=[]
    all_buckets=[]

    records.append(rec)

    prefix=get_hash(trans_id,global_depth)

    cur_bucket_id=get_bucket_id(trans_id,main_memory,buckets,global_depth)

    temp_local_depth=buckets[cur_bucket_id].local_depth+1
    
    start=prefix
    while((start>0)and(buckets[tot_buckets-1-start+1].next_bucket==cur_bucket_id)):
        start-=1
    
    end=prefix
    while((end+1 < 2**global_depth)and(buckets[tot_buckets-1-end-1].next_bucket==cur_bucket_id)):
        end+=1

    mid=int((start+end)/2)

    while(cur_bucket_id!=-1):
        all_buckets.append(cur_bucket_id)
        for each in buckets[cur_bucket_id].records:
            records.append(each)
        buckets[cur_bucket_id].records.clear()
        buckets[cur_bucket_id].empty_spaces=max_size
        cur_bucket_id=buckets[cur_bucket_id].next_bucket

    if(len(all_buckets)==1):
        all_buckets.append(bucket_cnt)
        bucket_cnt+=1

    pos=2    

    cur1=all_buckets[0]
    cur2=all_buckets[1]

    buckets[cur1].next_bucket=-1
    buckets[cur1].local_depth=temp_local_depth
    buckets[cur1].records.clear()
    buckets[cur1].empty_spaces=max_size

    buckets[cur2].next_bucket=-1
    buckets[cur2].local_depth=temp_local_depth
    buckets[cur2].records.clear()
    buckets[cur2].empty_spaces=max_size

    for each in records:
        prefix1=get_hash(each[0],global_depth)
        if(prefix1<=mid):
            if(buckets[cur1].empty_spaces==0):
                if(pos==len(all_buckets)):
                    buckets[cur1].next_bucket=bucket_cnt
                    cur1=bucket_cnt
                    buckets[cur1].next_bucket=-1
                    buckets[cur1].local_depth=temp_local_depth
                    bucket_cnt+=1
                else:
                    buckets[cur1].next_bucket=all_buckets[pos]
                    cur1=all_buckets[pos]
                    buckets[cur1].empty_spaces=max_size
                    buckets[cur1].local_depth=temp_local_depth
                    buckets[cur1].next_bucket=-1
                    pos+=1

            buckets[cur1].records.append(each)
            buckets[cur1].empty_spaces-=1

        else:
            if(buckets[cur2].empty_spaces==0):
                if(pos==len(all_buckets)):
                    buckets[cur2].next_bucket=bucket_cnt
                    cur2=bucket_cnt
                    buckets[cur2].next_bucket=-1
                    buckets[cur2].local_depth=temp_local_depth
                    bucket_cnt+=1
                else:
                    buckets[cur2].next_bucket=bucket_cnt
                    cur2=all_buckets[pos]
                    buckets[cur2].next_bucket=-1
                    buckets[cur2].local_depth=temp_local_depth
                    pos+=1

            buckets[cur2].records.append(each)
            buckets[cur2].empty_spaces-=1

    for i in range(start,mid+1):
        buckets[tot_buckets-1-i].next_bucket=all_buckets[0]
        if i<1024:
            main_memory[i]=all_buckets[0]

    for i in range(mid+1,end+1):
        buckets[tot_buckets-1-i].next_bucket=all_buckets[1]
        if i<1024:
            main_memory[i]=all_buckets[1]

    return buckets,global_depth,bucket_cnt,main_memory            

def double_directory(dir_len,buckets,trans_id,global_depth,bucket_cnt,max_size,rec,main_memory):
    print("doubing directory due to",rec[0])
    for i in range(0,dir_len):
        buckets[tot_buckets-1-2*(dir_len-i)+1].next_bucket=buckets[tot_buckets-1-(dir_len-i-1)].next_bucket
        buckets[tot_buckets-1-2*(dir_len-i)+2].next_bucket=buckets[tot_buckets-1-(dir_len-i-1)].next_bucket
        if((2*(dir_len-i)-1)<1024):
            main_memory[2*(dir_len-i)-1]=buckets[tot_buckets-1-(dir_len-i-1)].next_bucket
        if((2*(dir_len-i)-2)<1024):
            main_memory[2*(dir_len-i)-2]=buckets[tot_buckets-1-(dir_len-i-1)].next_bucket            

    dir_len*=2
    global_depth+=1
    
    buckets,global_depth,bucket_cnt,main_memory=rearrange(trans_id,buckets,global_depth,max_size,bucket_cnt,rec,main_memory)

    return dir_len,buckets,global_depth,bucket_cnt

def insert(buckets,global_depth,dir_len,record,main_memory,bucket_cnt,max_size):
    trans_id=record[0]
    b_id=get_bucket_id(trans_id,main_memory,buckets,global_depth)

    b_id1=b_id

    while(buckets[b_id1].next_bucket!=-1):
        b_id1=buckets[b_id1].next_bucket

    if buckets[b_id1].empty_spaces!=0:
        print("Enough space available to insert without overflowing for",record[0])
        buckets[b_id1].records.append(record)
        buckets[b_id1].empty_spaces-=1
        return dir_len,global_depth,main_memory,buckets,bucket_cnt
    
    if buckets[b_id].local_depth < global_depth:
        buckets,global_depth,bucket_cnt,main_memory=rearrange(trans_id,buckets,global_depth,max_size,bucket_cnt,record,main_memory)
    else:
        dir_len,buckets,global_depth,bucket_cnt=double_directory(dir_len,buckets,trans_id,global_depth,bucket_cnt,max_size,record,main_memory)

    return dir_len,global_depth,main_memory,buckets,bucket_cnt
