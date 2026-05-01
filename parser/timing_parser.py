# timing_parser.py

def parse_timing_report(file_path):
    paths = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_path = {}

    for line in lines:
        line = line.strip()

        if line.startswith("Startpoint"):
            current_path["start"] = line.split(":")[1].strip()

        elif line.startswith("Endpoint"):
            current_path["end"] = line.split(":")[1].strip()

        elif "Slack" in line:
            slack_value = float(line.split(":")[1].strip())
            current_path["slack"] = slack_value

            paths.append(current_path)
            current_path = {}

    return paths


if __name__ == "__main__":
    result = parse_timing_report("data/reports/sample_report.txt")
    print(result)