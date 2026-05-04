import cv2
import numpy as np

class ColorAnalyzer:
    """
    Analyzes the dominant color of a cropped image using HSV color space binning.
    """
    
    COLORS = {
        "white":  ([0, 0, 200], [180, 30, 255]),
        "black":  ([0, 0, 0], [180, 255, 50]),
        "gray":   ([0, 0, 50], [180, 50, 200]),
        "red1":   ([0, 70, 50], [10, 255, 255]),
        "red2":   ([170, 70, 50], [180, 255, 255]),
        "blue":   ([100, 150, 50], [140, 255, 255]),
        "green":  ([35, 100, 50], [85, 255, 255]),
        "yellow": ([20, 100, 100], [30, 255, 255]),
        "silver": ([0, 0, 192], [180, 15, 224]),
    }

    @staticmethod
    def get_dominant_color(crop: np.ndarray) -> str:
        if crop is None or crop.size == 0:
            return "unknown"

        # 1. Focus on the center of the crop to avoid background/wheels
        h, w = crop.shape[:2]
        ch1, ch2 = int(h * 0.2), int(h * 0.8)
        cw1, cw2 = int(w * 0.2), int(w * 0.8)
        center_crop = crop[ch1:ch2, cw1:cw2]
        
        if center_crop.size == 0:
            center_crop = crop

        # 2. Use K-Means to find dominant colors
        # Reshape to a list of pixels
        pixels = center_crop.reshape(-1, 3).astype(np.float32)
        
        # Define criteria and apply kmeans
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 3 # Look for top 3 colors
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Count occurrences of each label
        counts = np.bincount(labels.flatten())
        
        # Sort by count descending
        sorted_indices = np.argsort(counts)[::-1]
        
        # Try top colors until we find a match or exhaust k
        for idx in sorted_indices:
            dominant_bgr = centers[idx]
            dominant_hsv = cv2.cvtColor(np.uint8([[dominant_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
            
            # Match against our color definitions
            for color_name, (lower, upper) in ColorAnalyzer.COLORS.items():
                lower_np = np.array(lower)
                upper_np = np.array(upper)
                
                # Special handling for red (it wraps around 180)
                if color_name.startswith("red"):
                    if (lower_np[0] <= dominant_hsv[0] <= upper_np[0] or 
                        (color_name == "red2" and dominant_hsv[0] >= 170)) and \
                       lower_np[1] <= dominant_hsv[1] <= upper_np[1] and \
                       lower_np[2] <= dominant_hsv[2] <= upper_np[2]:
                        return "red"
                else:
                    if np.all(dominant_hsv >= lower_np) and np.all(dominant_hsv <= upper_np):
                        return color_name
        
        return "unknown"

color_analyzer = ColorAnalyzer()
