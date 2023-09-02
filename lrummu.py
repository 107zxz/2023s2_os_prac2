from mmu import MMU

class LruMMU(MMU):

    debug: bool

    cache: set[int]
    cache_size: int

    timestep: int

    last_uses: dict[int, int]
    dirty_pages: set[int]

    disk_reads: int
    disk_writes: int
    page_faults: int

    def __init__(self, frames: int):
        self.cache_size = frames
        self.timestep = 0
        self.cache = set()
        self.last_uses = {}
        self.dirty_pages = set()
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def cache_page(self, page_number: int):

        # Detect page fault
        if page_number not in self.cache:
            
            # Page faults require a disk read
            self.page_faults += 1
            self.disk_reads += 1
            
            # Is cache full?
            if len(self.cache) == self.cache_size:
                
                # Kick out the oldest
                oldest = self.timestep
                oldest_frame = None

                for frame in self.cache:
                    if self.last_uses[frame] < oldest:
                        oldest = self.last_uses[frame]
                        oldest_frame = frame
                
                self.cache.remove(oldest_frame)

                # If we're evicting a dirty page, we're writing it to disk
                if oldest_frame in self.dirty_pages:
                    self.disk_writes += 1
                    self.dirty_pages.remove(oldest_frame)


        # Add page to frames
        self.cache.add(page_number)

        # Track this use
        self.last_uses[page_number] = self.timestep

        # Step forward in time
        self.timestep += 1
        

    def read_memory(self, page_number: int):
        self.cache_page(page_number)

    def write_memory(self, page_number: int):

        self.dirty_pages.add(page_number)

        self.cache_page(page_number)

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
