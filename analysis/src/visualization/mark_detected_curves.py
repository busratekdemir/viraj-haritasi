import argparse
from pathlib import Path

import cv2
import pandas as pd


def draw_rounded_rectangle(
    image,
    top_left,
    bottom_right,
    color,
    radius=20,
):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.rectangle(
        image,
        (x1 + radius, y1),
        (x2 - radius, y2),
        color,
        -1,
    )

    cv2.rectangle(
        image,
        (x1, y1 + radius),
        (x2, y2 - radius),
        color,
        -1,
    )

    cv2.circle(
        image,
        (x1 + radius, y1 + radius),
        radius,
        color,
        -1,
    )

    cv2.circle(
        image,
        (x2 - radius, y1 + radius),
        radius,
        color,
        -1,
    )

    cv2.circle(
        image,
        (x1 + radius, y2 - radius),
        radius,
        color,
        -1,
    )

    cv2.circle(
        image,
        (x2 - radius, y2 - radius),
        radius,
        color,
        -1,
    )


def draw_curve_badge(frame, curve, width):
    panel_width = 330
    panel_height = 105
    margin = 30

    x1 = width - panel_width - margin
    y1 = margin
    x2 = width - margin
    y2 = y1 + panel_height

    overlay = frame.copy()

    draw_rounded_rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        (24, 28, 34),
        radius=20,
    )

    direction = str(curve["direction"]).lower()

    if direction == "right":
        accent_color = (235, 155, 70)
        direction_text = "RIGHT TURN"
        arrow = ">"
    else:
        accent_color = (60, 180, 255)
        direction_text = "LEFT TURN"
        arrow = "<"

    cv2.rectangle(
        overlay,
        (x1, y1 + 18),
        (x1 + 7, y2 - 18),
        accent_color,
        -1,
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.78,
        frame,
        0.22,
        0,
    )

    cv2.putText(
        frame,
        f"CURVE {int(curve['curve_id']):02d}",
        (x1 + 28, y1 + 36),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (185, 190, 198),
        1,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        arrow,
        (x1 + 28, y1 + 83),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        accent_color,
        3,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        direction_text,
        (x1 + 70, y1 + 79),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.82,
        (245, 245, 245),
        2,
        cv2.LINE_AA,
    )


def mark_curves(
    video_path: Path,
    curves_path: Path,
    output_path: Path,
) -> None:
    curves = pd.read_csv(curves_path)
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

        current_time = frame_number / fps

        active_curves = curves[
            (curves["start_time"] <= current_time)
            & (curves["end_time"] >= current_time)
        ]

        if not active_curves.empty:
            draw_curve_badge(
                frame,
                active_curves.iloc[0],
                width,
            )

        writer.write(frame)
        frame_number += 1

    video.release()
    writer.release()

    print("Viraj bilgi kartı videoya eklendi.")
    print(f"İşlenen kare: {frame_number}")
    print(f"Çıktı: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("curves", type=Path)
    parser.add_argument("output", type=Path)

    args = parser.parse_args()

    mark_curves(
        args.video,
        args.curves,
        args.output,
    )


if __name__ == "__main__":
    main()