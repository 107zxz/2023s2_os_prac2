from mmu import MMU

class ClockMMU(MMU):

    debug: bool

    # Cache is an ordered list, because it needs to be cycled around by index
    cache: list[int]
    cache_size: int

    # Clock hand
    clock_hand: int
    clock_bits: dict[int, bool]
    
    dirty_pages: set[int]

    disk_reads: int
    disk_writes: int
    page_faults: int

    def __init__(self, frames: int):
        self.cache_size = frames
        self.timestep = 0
        self.cache = []
        self.dirty_pages = set()
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.clock_hand = 0
        self.clock_bits = {}

    def set_debug(self):
        self.debug = True
        pass

    def reset_debug(self):
        self.debug = False
        pass

    def cache_page(self, page_number: int):

        if self.debug:
            print("Checking page {} against cache".format(page_number))

        # Detect page fault
        if page_number not in self.cache:
            
            # Page faults require a disk read
            self.page_faults += 1
            self.disk_reads += 1

            if self.debug:
                print("Page Fault! Disk reads: {}".format(self.disk_reads))
            
            # Is cache full?
            if len(self.cache) == self.cache_size:
                
                # It's time to spin the wheel of death!
                while self.clock_bits[self.cache[self.clock_hand]] == True:

                    next_clock_idx = (self.clock_hand + 1) % self.cache_size

                    if self.debug:
                        print("Clock ticks {}->{}. Next element {} with read {}".format(
                            self.clock_hand, next_clock_idx,
                            self.cache[next_clock_idx], self.clock_bits[self.cache[next_clock_idx]]
                            ))
                    self.clock_bits[self.cache[self.clock_hand]] = False
                    self.clock_hand = next_clock_idx

                biggest_loser = self.cache[self.clock_hand]

                # Dock of shame, boat of losers etc etc...
                del self.clock_bits[biggest_loser]

                if self.debug:
                    print("Evicting page {}".format(biggest_loser))

                # If we're evicting a dirty page, we're writing it to disk
                if biggest_loser in self.dirty_pages:
                    self.disk_writes += 1
                    self.dirty_pages.remove(biggest_loser)

                    if self.debug:
                        print("Page dirty, disk writes: {}".format(self.disk_writes))
            
                # If a page was evicted we should replace it
                self.cache[self.clock_hand] = page_number

            else: # If cache ISN'T full
                # Append page to frames
                self.cache.append(page_number)

        self.clock_bits[page_number] = True

        if self.debug:
            print("Current cache:")
            print(self.cache)

    def read_memory(self, page_number: int):

        if self.debug:
            print("Reading page {}".format(page_number))

        self.cache_page(page_number)


    def write_memory(self, page_number):

        if self.debug:
            print("Writing page {}".format(page_number))

        self.cache_page(page_number)

        self.dirty_pages.add(page_number)

        if self.debug:
            print("Dirty pages:")
            print(self.dirty_pages)

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults

