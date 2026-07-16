import argparse
from pathlib import Path

import cv2


def annotate_video(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Girdi videosu bulunamadı: {input_path.resolve()}"
        )

    video = cv2.VideoCapture(str(input_path))

    if not video.isOpened():
        raise RuntimeError(
            f"Video OpenCV tarafından açılamadı: {input_path}"
        )

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if fps <= 0:
        video.release()
        raise RuntimeError("Videonun FPS bilgisi okunamadı.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    codec = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(output_path),
        codec,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        video.release()
        raise RuntimeError(
            f"Çıktı videosu oluşturulamadı: {output_path}"
        )

    frame_number = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        elapsed_seconds = frame_number / fps

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (20, 20),
            (410, 125),
            (0, 0, 0),
            thickness=-1,
        )

        frame = cv2.addWeighted(
            overlay,
            0.65,
            frame,
            0.35,
            0,
        )

        cv2.putText(
            frame,
            f"Frame: {frame_number}",
            (40, 62),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            f"Time: {elapsed_seconds:.3f} s",
            (40, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        writer.write(frame)
        frame_number += 1

    video.release()
    writer.release()

    duration = frame_number / fps

    print("\nVideo işleme tamamlandı.")
    print(f"Girdi         : {input_path}")
    print(f"Çıktı         : {output_path}")
    print(f"FPS           : {fps:.2f}")
    print(f"İşlenen kare  : {frame_number}/{frame_count}")
    print(f"Süre          : {duration:.2f} saniye")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Videoya kare numarası ve geçen süre bilgisini ekler."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Girdi videosunun yolu",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="İşlenmiş videonun kaydedileceği yol",
    )

    args = parser.parse_args()
    annotate_video(args.input, args.output)


if __name__ == "__main__":
    main()