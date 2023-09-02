from mmu import MMU

import random

class RandMMU(MMU):

    debug: bool

    cache: set[int]
    cache_size: int

    random.seed(42)
    
    dirty_pages: set[int]

    disk_reads: int
    disk_writes: int
    page_faults: int

    def __init__(self, frames: int):
        self.cache_size = frames
        self.timestep = 0
        self.cache = set()
        self.dirty_pages = set()
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    def set_debug(self):
        self.debug = True
        pass

    def reset_debug(self):
        self.debug = False
        pass

    def cache_page(self, page_number: int):

        if self.debug:
            print("Caching page {}".format(page_number))

        # Detect page fault
        if page_number not in self.cache:
            
            # Page faults require a disk read
            self.page_faults += 1
            self.disk_reads += 1

            if self.debug:
                print("Page Fault Disk reads: {}".format(self.disk_reads))
            
            # Is cache full?
            if len(self.cache) == self.cache_size:
                
                # Kick out random frame
                random_frame_number = random.randint(0, self.cache_size)

                random_frame = self.cache[random_frame_number]

                self.cache.remove(random_frame)

                if self.debug:
                    print("Evicting page {}".format(random_frame))

                # If we're evicting a dirty page, we're writing it to disk
                if random_frame in self.dirty_pages:
                    self.disk_writes += 1
                    self.dirty_pages.remove(random_frame)

                    if self.debug:
                        print("Page dirty, disk writes: {}".format(self.disk_writes))
            
            


        # Add page to frames
        self.cache.add(page_number)

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

        self.dirty_pages.add(page_number)

        if self.debug:
            print("Dirty pages:")
            print(self.dirty_pages)

        self.cache_page(page_number)

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults

