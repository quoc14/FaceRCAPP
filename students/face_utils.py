import face_recognition
import io

def extract_face_vector(image_bytes):
    image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0].tolist()
    return None