import sys

# dict to store the page numbers
page_count = {}

def main():
    PAGE_OFFSET = 12  # page is 2^12 = 4KB

    if (len(sys.argv) < 1):
        print("Usage: python trace_reader.py inputfile")
        return

    input_file = sys.argv[1]

    # output file naming
    output_file_path = input_file.split(".")[0] + '_stats.txt'

    try:
        with open(input_file, 'r') as file:
            # Read the trace file contents
            trace_contents = file.readlines()
    except FileNotFoundError:
        print(f"Input '{input_file}' could not be found")
        print("Usage: python trace_reader.py inputfile")
        return

    # track read and write counts
    read_count = 0
    write_count = 0

    with open(input_file, 'r') as trace_file:
        for trace_line in trace_file:

            # if line ends with W or R, inc counter
            if trace_line.strip().endswith('W'):
                write_count += 1

            if trace_line.strip().endswith('R'):
                read_count += 1

            trace_cmd = trace_line.strip().split(" ")
            logical_address = int(trace_cmd[0], 16)
            page_number = logical_address >> PAGE_OFFSET

            # if page number in dict
            if page_number in page_count:
                # inc the count
                page_count[page_number] += 1
            else:
                # else add with count of 1
                page_count[page_number] = 1

    sorted_page_count = sorted(page_count.items(), key=lambda x: x[1], reverse=True)

    # write to file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(f"writes: {write_count}\n")
            output_file.write(f"reads: {read_count}\n") 

            output_file.write(f"\n")    

            for page_number, count in sorted_page_count:
                output_file.write(f"{hex(page_number)}: {count}\n")

    except Exception as e:
        print(f"An error occurred while writing to the output file: {str(e)}")

if __name__ == "__main__":
    main()
                    