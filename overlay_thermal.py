import os
import re
import argparse
import shutil
import cv2
import numpy as np


def find_pairs(input_dir):
    # Find files ending with _T.JPG and _Z.JPG and pair by common prefix
    files = os.listdir(input_dir)
    t_files = [f for f in files if f.upper().endswith('_T.JPG')]
    pairs = []
    for t in t_files:
        base = re.sub(r'_T\.JPG$', '', t, flags=re.IGNORECASE)
        z = base + '_Z.JPG'
        if z in files:
            pairs.append((os.path.join(input_dir, t), os.path.join(input_dir, z), base))
        else:
            print(f"Warning: RGB image for thermal '{t}' not found (expected '{z}'). Skipping.")
    return pairs


def align_thermal_to_rgb(thermal_img, rgb_img, min_matches=10):
    # Convert to grayscale
    th_gray = cv2.cvtColor(thermal_img, cv2.COLOR_BGR2GRAY)
    rgb_gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    # ORB detector
    orb = cv2.ORB_create(2000)
    kp1, des1 = orb.detectAndCompute(th_gray, None)
    kp2, des2 = orb.detectAndCompute(rgb_gray, None)

    if des1 is None or des2 is None or len(kp1) < 4 or len(kp2) < 4:
        print('Not enough keypoints detected, falling back to resize.')
        return fallback_resize(thermal_img, rgb_img)

    # Matcher and ratio test
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.knnMatch(des1, des2, k=2)
    good = []
    for m_n in matches:
        if len(m_n) != 2:
            continue
        m, n = m_n
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) < min_matches:
        print(f'Only {len(good)} good matches found (<{min_matches}), falling back to resize.')
        return fallback_resize(thermal_img, rgb_img)

    # Extract matched keypoints
    pts_th = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts_rgb = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Compute homography
    H, mask = cv2.findHomography(pts_th, pts_rgb, cv2.RANSAC, 5.0)
    if H is None:
        print('Homography computation failed, falling back to resize.')
        return fallback_resize(thermal_img, rgb_img)

    # Warp thermal to RGB coordinate space
    h, w = rgb_img.shape[:2]
    warped = cv2.warpPerspective(thermal_img, H, (w, h))
    return warped


def fallback_resize(thermal_img, rgb_img):
    # Simple fallback: resize thermal to match RGB size
    h, w = rgb_img.shape[:2]
    resized = cv2.resize(thermal_img, (w, h), interpolation=cv2.INTER_LINEAR)
    return resized


def process_all(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pairs = find_pairs(input_dir)
    if not pairs:
        print('No image pairs found in', input_dir)
        return

    for t_path, z_path, base in pairs:
        print(f'Processing pair: {os.path.basename(t_path)} <-> {os.path.basename(z_path)}')
        thermal = cv2.imread(t_path)
        rgb = cv2.imread(z_path)
        if thermal is None:
            print('Failed to read', t_path)
            continue
        if rgb is None:
            print('Failed to read', z_path)
            continue

        warped = align_thermal_to_rgb(thermal, rgb)

        # Save warped thermal as XXXX_AT.JPG (Adjusted Thermal)
        out_name_at = f'{base}_AT.JPG'
        out_name_z = f'{base}_Z.JPG'
        out_at_path = os.path.join(output_dir, out_name_at)
        out_z_path = os.path.join(output_dir, out_name_z)

        success = cv2.imwrite(out_at_path, warped)
        if not success:
            print('Failed to write', out_at_path)
        else:
            print('Wrote adjusted thermal:', out_at_path)

        # Copy the RGB (unchanged) into output for convenience
        try:
            shutil.copy2(z_path, out_z_path)
        except Exception:
            print('Failed to copy RGB to output folder')


def main():
    parser = argparse.ArgumentParser(description='Align thermal images to their RGB counterparts and output adjusted thermal images.')
    parser.add_argument('--input', '-i', default='input-images', help='Input folder containing image pairs (default: input-images)')
    parser.add_argument('--output', '-o', default='output', help='Output folder for adjusted thermal images (default: output)')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    if not os.path.isdir(input_dir):
        print('Input directory not found:', input_dir)
        return

    process_all(input_dir, output_dir)


if __name__ == '__main__':
    main()
