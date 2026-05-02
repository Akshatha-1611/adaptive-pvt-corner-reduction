# timing_parser.py

def parse_timing_report(file_path):
    path_dict = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    start = None
    end = None

    for line in lines:
        line = line.strip()

        if line.startswith("Startpoint"):
            start = line.split(":")[1].strip()

        elif line.startswith("Endpoint"):
            end = line.split(":")[1].strip()

        elif "Slack" in line:
            slack = float(line.split(":")[1].strip())

            #  unique path id
            path_id = f"{start}->{end}"

            path_dict[path_id] = slack

    return path_dict


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