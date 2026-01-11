import cv2
import numpy as np

class Solution:
    def __init__(self):
        # Initializing Background Subtractor 
        
        self.back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=200, detectShadows=True)
        
        
        # Kernel for morphological operations 
        
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        
        
        # Line Position for counting (0.50 = Middle of the screen we have kept)
        
        
        self.line_position = 0.50 

    def forward(self, video_path: str) -> int:
        
        
        cap = cv2.VideoCapture(video_path)
        
        
        if not cap.isOpened():
            return 0

        total_vehicle_count = 0
        
        prev_centroids = []
        
        while True:
            
            ret, frame = cap.read()
            
            if not ret:
                
                break
            
            # Step 1. Resize the Frame 
            
            height, width = frame.shape[:2]
            
            new_width = 640
            
            new_height = int(height * (new_width / width))
            
            frame = cv2.resize(frame, (new_width, new_height))
            
            line_y = int(new_height * self.line_position)

            # Step 2. Pre-processing step using gaussian blur
 
            blurred = cv2.GaussianBlur(frame, (3, 3), 0)
 
            fg_mask = self.back_sub.apply(blurred)
            
            # Thresholding to remove shadows
 
            _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
            
 
            # Step 3. Morphological Operations done here to clean noise
            
            fg_mask = cv2.erode(fg_mask, None, iterations=1)
            
            fg_mask = cv2.dilate(fg_mask, self.kernel, iterations=3)

            # Step 4. Finding Contours
            
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            current_centroids = []
            
            for cnt in contours:
                
                x, y, w, h = cv2.boundingRect(cnt)
                
                area = cv2.contourArea(cnt)
                
                if h == 0: continue
                
                aspect_ratio = float(w) / h
                
                # Filtering application is carried out here
                # Area > 1200: To ignore small noise
                # Aspect Ratio > 0.5: To ignore thin vertical objects
                if area > 1200 and aspect_ratio > 0.5:
                    
                    
                    cx = int(x + w / 2)
                    
                    cy = int(y + h / 2)
                    
                    current_centroids.append((cx, cy))

            # Step 5. Counting Logic implemented
            
            for (cx, cy) in current_centroids:
            
                for (prev_cx, prev_cy) in prev_centroids:
            
                    dist = np.hypot(cx - prev_cx, cy - prev_cy)
                    
            
                    if dist < 60: 
                        
                        if prev_cy > line_y and cy <= line_y:
                            total_vehicle_count += 1

            
            prev_centroids = current_centroids

        
        cap.release()
        
        return total_vehicle_count