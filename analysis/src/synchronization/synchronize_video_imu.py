import argparse
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


def find_nearest_index(values: np.ndarray, target: float) -> int:
    index = int(np.searchsorted(values, target))

    if index == 0:
        return 0

    if index >= len(values):
        return len(values) - 1

    previous_difference = abs(target - values[index - 1])
    next_difference = abs(values[index] - target)

    if previous_difference <= next_difference:
        return index - 1

    return index


def synchronize(
    video_path: Path,
    imu_path: Path,
    output_path: Path,
) -> None:
    if not video_path.exists():
        raise FileNotFoundError(f"Video bulunamadı: {video_path}")

    if not imu_path.exists():
        raise FileNotFoundError(f"IMU dosyası bulunamadı: {imu_path}")

    imu_data = pd.read_csv(imu_path)
    sensor_times = imu_data["elapsed_seconds"].to_numpy()

    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        raise RuntimeError("Video açılamadı.")

    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    if not writer.isOpened():
        video.release()
        raise RuntimeError("Çıktı videosu oluşturulamadı.")

    frame_number = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        frame_time = frame_number / fps
        sensor_index = find_nearest_index(
            sensor_times,
            frame_time,
        )

        sensor = imu_data.iloc[sensor_index]

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (20, 20),
            (500, 260),
            (0, 0, 0),
            -1,
        )

        frame = cv2.addWeighted(
            overlay,
            0.65,
            frame,
            0.35,
            0,
        )

        lines = [
            f"Frame: {frame_number}",
            f"Time: {frame_time:.3f} s",
            f"Sensor sample: {sensor_index}",
            f"AX: {sensor['ax']:.3f} m/s2",
            f"AY: {sensor['ay']:.3f} m/s2",
            f"GZ: {sensor['gz']:.3f} rad/s",
            f"Speed: {sensor['speed']:.2f} m/s",
        ]

        for line_index, line in enumerate(lines):
            cv2.putText(
                frame,
                line,
                (40, 55 + line_index * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        writer.write(frame)
        frame_number += 1

    video.release()
    writer.release()

    print("Video ve IMU eşleştirmesi tamamlandı.")
    print(f"İşlenen kare: {frame_number}")
    print(f"Çıktı: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("video", type=Path)
    parser.add_argument("imu", type=Path)
    parser.add_argument("output", type=Path)

    args = parser.parse_args()

    synchronize(
        args.video,
        args.imu,
        args.output,
    )


if __name__ == "__main__":
    main()
    