# test_driver.py
from main import Solution

# Apni video file ka sahi path yaha daalo
video_path = "/home/wireshark10/DATASET/Dataset/vehant_hackathon_video_1.avi" 

if __name__ == "__main__":
    # Solution class ko initialize karo
    solver = Solution()
    
    print(f"Processing video: {video_path}...")
    
    # Forward function call karo
    try:
        count = solver.forward(video_path)
        print("-" * 30)
        print(f"SUCCESS! Final Vehicle Count: {count}")
        print("-" * 30)
    except FileNotFoundError:
        print("Error: Video file nahi mili. Path check karo.")
    except Exception as e:
        print(f"Error aaya: {e}")