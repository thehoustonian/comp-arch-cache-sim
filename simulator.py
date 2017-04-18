

class CacheSimulator(object):
    def __init__(self, filename, cache_size, block_size, assoc_level, repl_policy, write_alloc_policy):
        """
        accepts the arguments from the command line and assigns them to class attributes. 
        :param filename: string
        :param cache_size: int
        :param block_size: int
        :param assoc_level: int
        :param repl_policy: str ('l', 'r', 'f')
        :param write_alloc_policy: str ('a', 'n')
        """
        self.filename = filename
        self.cache_size = cache_size
        self.block_size = block_size
        self.assoc_level = assoc_level
        self.repl_policy = repl_policy
        self.write_alloc_policy = write_alloc_policy
        self.trace = []
        self.hit_count = 0
        self.miss_count = 0

        self.num_cache_lines = int(self.cache_size / (self.assoc_level * self.block_size))
        self.cacheLines = [CacheLine(self.assoc_level) for i in range (0, self.num_cache_lines)]
        self.process_file()

    def simulate(self):
        """
        Implements the actual cache simulation. loops through each line in the file, calculates the tag, block address,
        line number, and access type, and then determines whether or not it's a hit or miss.
        :return:
        """
        for line in self.trace:
            tag = int(line[1] / (self.num_cache_lines * self.block_size))  # tag calculation
            block_addr = int(line[1] / self.block_size)  # block address calculation
            line_number = block_addr % self.num_cache_lines  # cache line calculation
            access_type = line[0]  # access type is 0 (read data),1 (write data), 2 (inst fetch), 3 (treat as unknown), 4 (flush cache)
            cache_line = self.cacheLines[line_number]

            if self.is_hit(cache_line, tag):
                self.hit_count += 1
            else:
                self.miss_count += 1
                self.process_miss(access_type, cache_line, tag)

    def process_miss(self, access_type, cache_line, tag):
        if self.write_alloc_policy == 'n' and access_type == 1:
            return  # don't do anything on a cache miss that's a write access and the write policy is never allocate

        elif access_type == 0 or access_type == 2:  # read access
            self.replace_block(access_type, cache_line, tag)

        elif access_type == 1 and self.write_alloc_policy == 'a':  # write access w/ always allocate
            self.replace_block(access_type, cache_line, tag)

        elif access_type == 4:  # escape record (flush cache)
            self.flush_cache()

        else:
            raise Exception("Unknown Access Type! (", access_type, ")")

    def flush_cache(self):
        for line in self.cacheLines:
            for block in line.blockList:
                block.valid = False
                block.counter = 0
                block.tag = None

    def replace_block(self, access_type, cache_line, tag):
        """
        Processes the steps necessary to replace a block based on the LRU or FIFO replacement algorithms
        :param access_type:
        :param cache_line:
        :param tag:
        :return:
        """
        if self.repl_policy == 'l' or self.repl_policy == 'f':  # LRU or FIFO
            if len(cache_line) == 1:
                repl_block_index = 0
            else:
                repl_block_index = cache_line.blockList.index(max(cache_line))  # this is probably bad form

            cache_line.blockList[repl_block_index].valid = True
            cache_line.blockList[repl_block_index].tag = tag
            cache_line.blockList[repl_block_index].counter = 0
            for block in cache_line:
                block.counter += 1
        else:
            raise Exception("Unrecognized replacement policy.")

    def is_hit(self, cache_line, tag):
        """
        Checks to see if there is a hit on the current cache line based on the tag value matching a valid block.
        :param cache_line: list of CacheBlock objects on this cache line
        :param tag: tag number to look for.
        :return: boolean indicating whether or not a hit has been found
        """
        for block in cache_line:
            if block.valid is False:
                continue
            elif block.tag == tag:
                if self.repl_policy == 'l':
                    block.counter = 0  # zero out the counter for this block if the policy is LRU
                    for block in cache_line:
                        block.counter += 1

                return True

        return False

    def process_file(self):
        """
        Opens file, reads in each line, strips newline, splits into two, converts both to ints
        :return: 
        """
        with open(self.filename) as file:
            for line in file:
                temp_arr = line.strip().split()
                temp_arr[0] = int(temp_arr[0])
                temp_arr[1] = int(temp_arr[1], 16)  # convert hex to int here
                self.trace.append(temp_arr)


class CacheLine(object):
    def __init__(self, associativity):
        """
        
        :param associativity: determines how many blocks each CacheLine object will hold.
        """
        self.blockList = [CacheBlock() for i in range(0, associativity)]  # list holding all the CacheBlock objects.

    def increment_counters(self):
        for block in self.blockList:
            block.counter += 1

    def clear_counter(self, block_index):
        self.blockList[block_index].counter = 0

    def __iter__(self):
        return iter(self.blockList)

    def __len__(self):
        return len(self.blockList)


class CacheBlock(object):
    def __init__(self):
        self.valid = False  # will be false initially, then once this block is used will always be 1
        self.tag = None  # the tag that represents what "data" is stored in this block
        self.counter = 0

    def __eq__(self, other):
        return (self.counter == other.counter) and (self.valid == other.valid)

    def __lt__(self, other):
        if self.valid and not other.valid:
            return True
        elif (not self.valid) and other.valid:
            return False
        else:
            return self.counter < other.counter
