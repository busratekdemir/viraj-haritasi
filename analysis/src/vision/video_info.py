import argparse
from pathlib import Path

import cv2


def read_video_info(video_path: Path) -> None:
    if not video_path.exists():
        raise FileNotFoundError(
            f"Video bulunamadı: {video_path.resolve()}"
        )

    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        raise RuntimeError(
            f"Video OpenCV tarafından açılamadı: {video_path}"
        )

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    print("\nViraj Haritası - Video Bilgileri")
    print("--------------------------------")
    print(f"Dosya        : {video_path.name}")
    print(f"Çözünürlük   : {width} x {height}")
    print(f"FPS          : {fps:.2f}")
    print(f"Kare sayısı  : {frame_count}")
    print(f"Süre         : {duration:.2f} saniye")

    video.release()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bir sürüş videosunun teknik bilgilerini gösterir."
    )

    parser.add_argument(
        "video",
        type=Path,
        help="Analiz edilecek videonun dosya yolu",
    )

    args = parser.parse_args()
    read_video_info(args.video)


if __name__ == "__main__":
    main()