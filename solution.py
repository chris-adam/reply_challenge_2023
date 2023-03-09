import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def solution(input):
    # my code here
    output = input
    return output


input_files = os.listdir("input")
for file_name in input_files:
    with open(os.path.join(INPUT_DIR, file_name), "r") as file:
        input_content = file.read()
    output = solution(input_content)

    with open(os.path.join(OUTPUT_DIR, file_name), "w") as file:
        file.write(output)