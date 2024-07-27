import json
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "pose_detection_log.json"

def load_log():
    with open(LOG_FILE, 'r') as f:
        return json.load(f)

def analyze_data(log):
    data = []
    for video, durations in log["pose_durations"].items():
        total_time = sum(durations.values())
        data.append({
            "video": video,
            "sitting_time": durations["Sitting"],
            "standing_time": durations["Standing"],
            "unknown_time": durations["Unknown"],
            "total_time": total_time
        })

    df = pd.DataFrame(data)
    return df

def plot_data(df):
    df.plot(x="video", y=["sitting_time", "standing_time", "unknown_time"], kind="bar", stacked=True)
    plt.xlabel("Video")
    plt.ylabel("Time (seconds)")
    plt.title("Pose Durations")
    plt.legend(["Sitting", "Standing", "Unknown"])
    plt.show()

def main():
    log = load_log()
    df = analyze_data(log)
    print(df)
    plot_data(df)

if __name__ == "__main__":
    main()