class bucket:

    def __init__(self,max_records):
        self.empty_spaces=max_records
        self.records = []
        self.next_bucket=-1
        self.local_depth=0