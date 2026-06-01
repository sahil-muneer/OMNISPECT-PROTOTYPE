import cv2
import numpy as np

def perform_ela(image_bytes: bytes, quality: int = 90, scale: int = 15) -> bytes:
    """
    Computes compression rate variance across the image matrix 
    to highlight sections that have been digitally altered.
    """
    # Convert raw binary incoming stream to an OpenCV matrix
    nparr = np.frombuffer(image_bytes, np.uint8)
    original_matrix = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if original_matrix is None:
        raise ValueError("Provided file asset is unreadable or corrupted.")

    # Compress matrix to standard JPEG format in a temporary memory buffer
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, compressed_buffer = cv2.imencode('.jpg', original_matrix, encode_param)
    
    # Decompress back to compare against the original pixel layout
    decompressed_matrix = cv2.imdecode(compressed_buffer, cv2.IMREAD_COLOR)

    # Calculate the absolute difference between original and re-compressed pixels
    pixel_delta = cv2.absdiff(original_matrix, decompressed_matrix)
    
    # Amplify the differences so structural alterations glow brightly
    visibly_enhanced_heatmap = pixel_delta * scale

    # Convert the resulting mapping matrix back into standard file bytes
    _, final_stream = cv2.imencode('.png', visibly_enhanced_heatmap)
    return final_stream.tobytes()