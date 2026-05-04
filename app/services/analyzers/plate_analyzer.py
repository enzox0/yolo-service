import easyocr
import cv2
import numpy as np
import re
from app.core.logging import logger

class PlateAnalyzer:
    """
    Analyzes license plates in a cropped vehicle image using EasyOCR.
    """
    
    def __init__(self):
        try:
            # Initialize reader with English support
            # gpu=True will use CUDA if available
            self.reader = easyocr.Reader(['en'], gpu=True)
            logger.info("PlateAnalyzer (EasyOCR) initialized")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {str(e)}")
            self.reader = None

    def read_plate(self, vehicle_crop: np.ndarray) -> str | None:
        if self.reader is None or vehicle_crop is None or vehicle_crop.size == 0:
            return None

        try:
            # 1. Focus on the lower part of the vehicle where the plate usually is
            h, w = vehicle_crop.shape[:2]
            roi_y1 = int(h * 0.4) # Start from 40% down
            roi = vehicle_crop[roi_y1:h, 0:w]
            
            # 2. Preprocessing for better OCR
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            contrast = clahe.apply(gray)
            
            # 3. Run OCR with detail=1 to get bounding boxes and confidence
            results = self.reader.readtext(contrast, detail=1)
            
            if not results:
                return None

            # 4. Filter and score potential plates
            potential_plates = []
            for (bbox, text, prob) in results:
                if prob < 0.3: # Ignore low confidence results
                    continue
                    
                # Clean text: remove spaces and special chars, keep only alphanumeric
                clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                
                # Philippine plate patterns (approximate)
                # Old: LLL 123 (3 letters, 3 numbers)
                # New: LLL 1234 (3 letters, 4 numbers)
                # MC: 123 LLL or LL 12345
                
                if 3 <= len(clean_text) <= 8:
                    # Score based on alphanumeric mix (plates usually have both)
                    has_alpha = any(c.isalpha() for c in clean_text)
                    has_digit = any(c.isdigit() for c in clean_text)
                    score = prob
                    if has_alpha and has_digit:
                        score += 0.5
                    
                    potential_plates.append((clean_text, score))

            if not potential_plates:
                return None
            
            # Return the one with the highest score
            potential_plates.sort(key=lambda x: x[1], reverse=True)
            logger.debug(f"Detected potential plates: {potential_plates}")
            return potential_plates[0][0]
            
        except Exception as e:
            logger.error(f"OCR error: {str(e)}")
            return None

plate_analyzer = PlateAnalyzer()
