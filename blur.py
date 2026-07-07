import cv2
import numpy as np
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fog = False
mask = None
prev_pos = None

fog_opacity = 0.0      
target_opacity = 0.0   
fade_speed = 0.04      

def finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if mask is None:
        mask = np.zeros((h, w), dtype=np.uint8)

    current_gesture = "UNKNOWN"
    x, y = None, None

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark

            index = finger_up(lm, 8, 6)
            middle = finger_up(lm, 12, 10)
            ring = finger_up(lm, 16, 14)
            pinky = finger_up(lm, 20, 18)

            if index and middle and ring and pinky:
                current_gesture = "HI"
                fog = False
                target_opacity = 0.0
                mask[:] = 0
                prev_pos = None

            elif index and middle and not ring and not pinky:
                current_gesture = "PEACE"
                if not fog:
                    fog = True
                    mask[:] = 0  
                target_opacity = 1.0
                prev_pos = None

            elif index and not middle and not ring and not pinky:
                current_gesture = "INDEX_ONLY"
                x = int(lm[8].x * w)
                y = int(lm[8].y * h)

            drawing_utils.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    # --- TRACKING USAPAN JARI ---
    if fog_opacity > 0 and current_gesture == "INDEX_ONLY" and x is not None and y is not None:
        if prev_pos is None:
            prev_pos = (x, y)
        
        # Ketebalan usapan utama jari
        cv2.line(mask, prev_pos, (x, y), 255, thickness=65)
        prev_pos = (x, y)
    else:
        prev_pos = None

    if fog_opacity < target_opacity:
        fog_opacity = min(fog_opacity + fade_speed, target_opacity)
    elif fog_opacity > target_opacity:
        fog_opacity = max(fog_opacity - fade_speed, target_opacity)

    # --- PROSES VISUAL: REALISTIK KACA EMBUN & SAKUAN AIR ---
    if fog_opacity > 0:
        # 1. Efek kabut embun dasar + uap putih hangat
        medium_blur = cv2.GaussianBlur(frame, (65, 65), 0)
        white_layer = np.full_like(frame, 255)
        fog_layer = cv2.addWeighted(medium_blur, 0.88, white_layer, 0.12, 0)
        
        # 2. PROSEDURAL TEPIAN AIR BASAH (WET-EDGE EFFECT)
        # Menghasilkan noise acak untuk merusak kehalusan garis agar organik
        noise = np.random.randint(0, 50, (h, w), dtype=np.uint8)
        dirty_mask = cv2.subtract(mask, noise)
        
        # Ekstrak garis tepi usapan dengan membandingkan masker asli dan masker yang dilebarkan
        kernel_edge = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        dilated_mask = cv2.dilate(dirty_mask, kernel_edge, iterations=1)
        edge_water = cv2.absdiff(dilated_mask, mask)
        edge_water = cv2.GaussianBlur(edge_water, (15, 15), 0)
        
        # Masker utama untuk memisahkan area jernih dan berembun
        smooth_mask = cv2.GaussianBlur(dirty_mask, (25, 25), 0)
        _, final_mask = cv2.threshold(smooth_mask, 60, 255, cv2.THRESH_BINARY)
        final_mask = cv2.GaussianBlur(final_mask, (11, 11), 0)
        final_mask_inv = cv2.bitwise_not(final_mask)
        
        # 3. PENGGABUNGAN FRAME UTAMA
        clear_part = cv2.bitwise_and(frame, frame, mask=final_mask)
        foggy_part = cv2.bitwise_and(fog_layer, fog_layer, mask=final_mask_inv)
        combined_frame = cv2.add(clear_part, foggy_part)
        
        # 4. TERAPKAN GRADASI TEPIAN AIR (Membuat pinggiran usapan terlihat basah & menggelap)
        # Efek menggelap disimulasikan dengan menurunkan kecerahan kamera di area tepi air
        dark_edge_layer = cv2.convertScaleAbs(combined_frame, alpha=0.65, beta=0) 
        
        # Gabungkan lapisan pinggiran gelap ke frame utama menggunakan masker edge_water
        edge_water_inv = cv2.bitwise_not(edge_water)
        normal_part = cv2.bitwise_and(combined_frame, combined_frame, mask=edge_water_inv)
        wet_edges = cv2.bitwise_and(dark_edge_layer, dark_edge_layer, mask=edge_water)
        full_fog_frame = cv2.add(normal_part, wet_edges)
        
        # 5. Aplikasikan transisi memudar (Fade-in / Out)
        output = cv2.addWeighted(frame, 1.0 - fog_opacity, full_fog_frame, fog_opacity, 0)
        
        cv2.imshow("Fog Camera", output)
    else:
        cv2.imshow("Fog Camera", frame)

    key = cv2.waitKey(1)
    if key == 27: 
        break

cap.release()
cv2.destroyAllWindows()