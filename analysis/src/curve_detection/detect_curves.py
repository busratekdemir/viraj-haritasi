import argparse
from pathlib import Path

import pandas as pd


def detect_curves(
    imu_path: Path,
    output_path: Path,
    threshold: float,
    minimum_duration: float,
) -> None:
    data = pd.read_csv(imu_path)

    required_columns = {"elapsed_seconds", "gz"}

    if not required_columns.issubset(data.columns):
        raise ValueError(
            "IMU dosyasında elapsed_seconds ve gz bulunmalı."
        )

    is_curve = data["gz"].abs() >= threshold
    detected_curves = []

    start_index = None

    def add_curve(first_index: int, last_index: int) -> None:
        start_time = data.iloc[first_index]["elapsed_seconds"]
        end_time = data.iloc[last_index]["elapsed_seconds"]
        duration = end_time - start_time

        if duration < minimum_duration:
            return

        segment = data.iloc[first_index : last_index + 1]
        mean_gyro = segment["gz"].mean()

        detected_curves.append(
            {
                "curve_id": len(detected_curves) + 1,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "direction": (
                    "right" if mean_gyro > 0 else "left"
                ),
                "mean_gz": mean_gyro,
                "max_abs_gz": segment["gz"].abs().max(),
                "entry_speed": segment.iloc[0]["speed"],
                "minimum_speed": segment["speed"].min(),
            }
        )

    for index, active in enumerate(is_curve):
        if active and start_index is None:
            start_index = index

        if not active and start_index is not None:
            add_curve(start_index, index - 1)
            start_index = None

    if start_index is not None:
        add_curve(start_index, len(data) - 1)

    result = pd.DataFrame(detected_curves)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    print("\nViraj tespiti tamamlandı.")
    print(f"Tespit edilen viraj sayısı: {len(result)}")

    if not result.empty:
        print(result.to_string(index=False))

    print(f"\nÇıktı: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("imu", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=float, default=0.08)
    parser.add_argument(
        "--minimum-duration",
        type=float,
        default=0.5,
    )

    args = parser.parse_args()

    detect_curves(
        args.imu,
        args.output,
        args.threshold,
        args.minimum_duration,
    )


if __name__ == "__main__":
    main()