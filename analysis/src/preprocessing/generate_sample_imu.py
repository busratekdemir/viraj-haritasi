import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_imu_data(
    duration: float,
    frequency: int,
    output_path: Path,
    figure_path: Path,
) -> None:
    rng = np.random.default_rng(42)

    sample_count = int(duration * frequency)
    time = np.arange(sample_count) / frequency

    curve_signal = np.zeros_like(time)
    curve_mask = (time >= 2.0) & (time <= 6.0)
    curve_signal[curve_mask] = np.sin(
        ((time[curve_mask] - 2.0) / 4.0) * np.pi
    )

    gyroscope_z = 0.35 * curve_signal + rng.normal(
        0, 0.01, sample_count
    )

    acceleration_y = 2.2 * curve_signal + rng.normal(
        0, 0.08, sample_count
    )

    speed = 14.0 - 2.0 * curve_signal + rng.normal(
        0, 0.05, sample_count
    )

    acceleration_x = np.gradient(
        speed, 1 / frequency
    ) + rng.normal(0, 0.03, sample_count)

    dataframe = pd.DataFrame(
        {
            "timestamp": time,
            "elapsed_seconds": time,
            "ax": acceleration_x,
            "ay": acceleration_y,
            "az": 9.81 + rng.normal(0, 0.05, sample_count),
            "gx": rng.normal(0, 0.005, sample_count),
            "gy": rng.normal(0, 0.005, sample_count),
            "gz": gyroscope_z,
            "speed": speed,
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(output_path, index=False)

    figure, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(time, acceleration_y)
    axes[0].set_ylabel("Yanal ivme")
    axes[0].grid(True)

    axes[1].plot(time, gyroscope_z)
    axes[1].set_ylabel("Gyroscope Z")
    axes[1].grid(True)

    axes[2].plot(time, speed)
    axes[2].set_ylabel("Hız (m/s)")
    axes[2].set_xlabel("Zaman (s)")
    axes[2].grid(True)

    figure.suptitle("Örnek IMU Sensör Verileri")
    figure.tight_layout()
    figure.savefig(figure_path, dpi=150)
    plt.close(figure)

    print(f"IMU dosyası: {output_path}")
    print(f"Grafik: {figure_path}")
    print(f"Örnek sayısı: {sample_count}")
    print(f"Örnekleme sıklığı: {frequency} Hz")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=8.0)
    parser.add_argument("--frequency", type=int, default=50)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/interim/sample_imu.csv"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("results/figures/sample_imu.png"),
    )

    args = parser.parse_args()

    generate_imu_data(
        args.duration,
        args.frequency,
        args.output,
        args.figure,
    )


if __name__ == "__main__":
    main()