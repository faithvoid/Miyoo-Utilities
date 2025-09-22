from PIL import Image, ImageSequence
import json
import sys

def extract_frames(gif_path, output_prefix="chargingState"):
    gif = Image.open(gif_path)

    frame_number = 0
    frame_delay = None
    target_size = (640, 480)

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")

        if frame.size != target_size:
            frame = frame.resize(target_size, Image.LANCZOS)

        frame_path = f"{output_prefix}{frame_number}.png"
        frame.save(frame_path, format="PNG")
        print(f"Saved {frame_path}")

        if frame_delay is None:
            frame_delay = frame.info.get("duration", 80)

        frame_number += 1

    json_data = {"frame_delay": frame_delay}
    with open(f"{output_prefix}.json", "w") as f:
        json.dump(json_data, f, indent=4)
    print(f"Saved {output_prefix}.json with frame_delay={frame_delay} ms")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gif2charge.py input.gif")
    else:
        extract_frames(sys.argv[1])
