import cv2
import json
import os

# === SETTINGS ===
IMAGE_PATH = "templates/tor.jpg"  # your template image
OUTPUT_PATH = "coords/tor.json"
DISPLAY_HEIGHT = 1000  # control how tall the image appears
# ================

drawing = False
start_x, start_y = -1, -1
coords = []
current_image = None
display_image = None
scale_ratio = 1.0  # keeps track of resize ratio

def mouse_callback(event, x, y, flags, param):
    global start_x, start_y, drawing, current_image, display_image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp = display_image.copy()
            cv2.rectangle(temp, (start_x, start_y), (x, y), (0, 255, 0), 1)
            cv2.imshow("Select Fields", temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y
        cv2.rectangle(display_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imshow("Select Fields", display_image)

        # Convert displayed coords back to original image scale
        orig_start_x = int(start_x / scale_ratio)
        orig_start_y = int(start_y / scale_ratio)
        orig_end_x = int(end_x / scale_ratio)
        orig_end_y = int(end_y / scale_ratio)

        field_name = input("Enter field name (e.g., name, num, place): ").strip()
        coords.append({
            "field": field_name,
            "x": min(orig_start_x, orig_end_x),
            "y": min(orig_start_y, orig_end_y),
            "w": abs(orig_end_x - orig_start_x),
            "h": abs(orig_end_y - orig_start_y)
        })
        print(f"Added field: {field_name}")

def main():
    global current_image, display_image, scale_ratio

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    current_image = cv2.imread(IMAGE_PATH)

    h, w = current_image.shape[:2]

    # Scale image so that height = DISPLAY_HEIGHT (fit vertically)
    scale_ratio = DISPLAY_HEIGHT / h
    new_w = int(w * scale_ratio)
    new_h = DISPLAY_HEIGHT
    display_image = cv2.resize(current_image, (new_w, new_h))

    # Allow full screen width but vertical scroll only
    cv2.namedWindow("Select Fields", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Select Fields", new_w, new_h)
    cv2.imshow("Select Fields", display_image)
    cv2.setMouseCallback("Select Fields", mouse_callback)

    print("Draw boxes around fields. Press 'q' to finish.")
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

    with open(OUTPUT_PATH, "w") as f:
        json.dump(coords, f, indent=4)
    print(f"Saved {len(coords)} fields to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()