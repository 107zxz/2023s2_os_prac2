from mmu import MMU

class RandMMU(MMU):

    debug_mode = False;

    # make a new function to handle debug prints?
        # or do a if(debug_mode = True) type thing

    total_disk_reads = 0;
    total_disk_writes = 0;
    total_page_faults = 0;

    # any extra variables needed for specific replacement policy
            # i.e for rand, might need some random seeding thing


    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU

        # make storage thingy that can hold [frames] amount of page frames
            # maybe vector
        
        pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        
        self.debug_mode = True;

        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode

        self.debug_mode = False;

        pass

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory

        

        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory



        pass

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads;

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes;

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults;
