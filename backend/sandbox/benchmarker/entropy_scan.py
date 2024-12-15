from EntropyAnalysis import *
from os import listdir
from os.path import isfile, join
import argparse

def main():
    parser = argparse.ArgumentParser(description="Write input text to a file.")
    parser.add_argument("--filename", type=str, default="/tmp/results", help="The name of the file to scan")

    args = parser.parse_args()

    onlyfiles = [f for f in listdir(args.filename) if isfile(join(args.filename, f))]
    for i in onlyfiles:
        entropy = get_full_file_entropy(open(args.filename + '/' + i, 'rb'))

        with open("/tmp/results", "a") as file:  # Open file in append mode
            file.write("\n" + i + " " + entropy + "\n")

if __name__ == "__main__":
    main()

# """
# 5.325985252430504
# """
# print(get_full_file_entropy(open('encodedtext', 'rb')))

# """
# 5.7071198470829385
# 5.97639041518072
# 5.978270051114846
# 5.977068738171774
# 5.9664801326954855
# """
# for score in get_chunks_file_entropy(open('encodedtext', 'rb')):
#     print(score)

# """
# 000000000000-000000000800    5.7071198470829385
# 000000000800-000000001000    5.97639041518072
# 000000001000-000000001800    5.978270051114846
# 000000001800-000000002000    5.977068738171774
# 000000002000-000000002800    5.9664801326954855
# """
# print_chunks_file_entropy(open('encodedtext', 'rb'))

# """
# 000000017c78-000000018478    5.98194720619564
# 000000017cdc-0000000184dc    5.979941867471824
# 000000017d40-000000018540    5.980487897102443
# 000000017da4-0000000185a4    5.980340888775624
# 000000017e08-000000018608    5.979668687769507
# """
# print_parts_chunks_file_entropy(open('encodedtext', 'rb'))