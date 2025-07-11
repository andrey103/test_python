import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# Укажите путь к скачанной модели
MODEL_PATH = "vosk-model-small-ru-0.22"
q = queue.Queue()

def callback(indata, frames, time, status):
    """Эта функция вызывается автоматически потоком аудиозаписи."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    # Загружаем модель
    model = Model(MODEL_PATH)
    
    # Создаем объект распознавателя
    rec = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        while True:
            data = q.get()
            
            if len(data) == 0:
                break
                
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_dict = json.loads(result)
                text = result_dict['text']
                print(f'Речь: {text}')
        
except KeyboardInterrupt:
    print("Прервано пользователем")
except Exception as e:
    print(e)