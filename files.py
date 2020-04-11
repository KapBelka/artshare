import uuid


def create_img_file(img_file):
    if img_file.filename.endswith('.jpg'):
        img_file_name = f"{uuid.uuid4()}.jpg"
        img_file.save(f"static/img/notes/{img_file_name}")
    elif img_file.filename.endswith('.png'):
        img_file_name = f"{uuid.uuid4()}.png"
        img_file.save(f"static/img/notes/{img_file_name}")
    else:
        abort(400, message=f"File type {img_file.filename} not allowed")
    return img_file_name


def create_audio_file(audio_file):
    if audio_file.filename.endswith('.mp3'):
        audio_file_name = f"{uuid.uuid4()}.mp3"
        audio_file.save(f"static/audio/notes/{audio_file_name}")
    else:
        abort(400, message=f"File type {audio_file.filename} not allowed")
    return audio_file_name