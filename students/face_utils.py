import insightface
import numpy as np
import io
from PIL import Image

# Load model 1 lần (cho vào global context hoặc init server)
model = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
model.prepare(ctx_id=0)

def extract_face_vector(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_image = np.array(image)

    faces = model.get(np_image)

    if not faces:
        return None

    # Lấy embedding của khuôn mặt đầu tiên
    return faces[0].embedding.tolist()
