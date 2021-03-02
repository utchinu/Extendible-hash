import bucket

buckets=[]
tot_buckets=100000
def simulate(max_records):
    for i in range(0,tot_buckets):
        b=bucket.bucket(max_records)
        buckets.append(b)

    buckets[tot_buckets-1].next_bucket=0
    #print(len(buckets))
    return(buckets)
