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


#  NEW FUNCTION
def compute_metrics(paths):
    slacks = [p["slack"] for p in paths]

    wns = min(slacks)  # Worst Negative Slack
    tns = sum([s for s in slacks if s < 0])  # Total Negative Slack
    violations = [p for p in paths if p["slack"] < 0]

    return {
        "WNS": wns,
        "TNS": tns,
        "violations": violations
    }


if __name__ == "__main__":
    paths = parse_timing_report("data/reports/sample_report.txt")
    metrics = compute_metrics(paths)

    print("Parsed Paths:")
    print(paths)

    print("\nMetrics:")
    print(metrics)