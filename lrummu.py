from mmu import MMU

class LruMMU(MMU):

    debug: bool

    cache_size: int

    timestep: int

    last_uses: dict[int, int]
    dirty_pages: set[int]

    frames: set[int]

    disk_reads: int
    disk_writes: int
    page_faults: int

    def __init__(self, frames: int):
        self.cache_size = frames
        self.timestep = 0
        self.frames = set()
        self.last_uses = {}
        self.dirty_pages = set()
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number: int):

        # print("Counted disk read!")

        # Track a page fault if relevant
        if page_number not in self.frames:
            self.page_faults += 1
            self.disk_reads += 1
            
            # Is cache full?
            if len(self.frames) == self.cache_size:
                # Kick out the oldest
                oldest = self.timestep
                oldest_frame = None

                for frame in self.frames:
                    if self.last_uses[frame] < oldest:
                        oldest = self.last_uses[frame]
                        oldest_frame = frame
                
                self.frames.remove(oldest_frame)

                if oldest_frame in self.dirty_pages:
                    self.disk_writes += 1
                    self.dirty_pages.remove(oldest_frame)


        # Add page to frames
        self.frames.add(page_number)

        # Track this use
        self.last_uses[page_number] = self.timestep

        # Track disk read
        # self.disk_reads += 1

        # Step forward in time
        self.timestep += 1

        # print("Reading page {}, {} total".format(page_number, self.disk_reads))
        # print(self.frames)

    def write_memory(self, page_number: int):


        # Track a page fault if relevant
        if page_number not in self.frames:
            self.page_faults += 1
            self.disk_reads += 1

            # Is cache full?
            if len(self.frames) == self.cache_size:
                # Kick out the oldest
                oldest = self.timestep
                oldest_frame = None

                for frame in self.frames:
                    if self.last_uses[frame] < oldest:
                        oldest = self.last_uses[frame]
                        oldest_frame = frame
                
                self.frames.remove(oldest_frame)

                if oldest_frame in self.dirty_pages:
                    self.disk_writes += 1
                    self.dirty_pages.remove(oldest_frame)

        # Add page to frames
        self.frames.add(page_number)

        # Track this use
        self.last_uses[page_number] = self.timestep

        # Mark dirty
        self.dirty_pages.add(page_number)

        # Track disk write
        # self.disk_writes += 1

        # Step forward in time
        self.timestep += 1

        # print("Writing page {}".format(page_number))
        # print(self.frames)

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
