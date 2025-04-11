# ChainingHashTable
# Ref: Lysecky, R., & Vahid, F. (2018, June). C950: Data Structures and Algorithms II. zyBooks.
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.

class ChainingHashTable:
    # Default constructor
    #->  O(N)
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Get the key of the provided item
    #->  O(1)
    def getkey(self, key):
        return hash(key) % len(self.table)

    # Insert into the hash table using the key-value pair. Use Chaining to allow multiple packages in one bucket
    #->  O(N)
    def insert(self, key, item):
        bucket = self.getkey(key)  # hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)

    # Search for the package using key-value pair. Search the bucket list if more than one package occupies the bucket
    #->  O(N)
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # value
        return None


    #Removes the item provided by looking up they key value pair
    #-> O(N)
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)

    #Print each item in the hash table
    #-> O(N)
    def print(self):
        for i in range(1, 41):
            print("Package: {}".format(self.search(i)))