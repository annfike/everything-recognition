import cv2

from config import CASCADES

#останавливает выполнение программы с нажатием клавиши q
def is_user_wants_quit(): 
    return cv2.waitKey(1) & 0xFF == ord('q')

#отображает изображение на экране
def show_frame(frame):
    cv2.imshow('Video', frame)

#рисует прямоугольник
def draw_sqare(frame, color):
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

#загружает каскады Хаара для распознавания объектов  
def get_cascades():
    cascades = [
        (cv2.CascadeClassifier(cascade['path']), cascade['color'])
        for title, cascade in CASCADES.items()
        if cascade['draw']
    ]
    return cascades


if __name__ == "__main__":
    cascades = get_cascades() #создает список каскадов
    video_capture = cv2.VideoCapture(0) #Создает объект захвата видео, который помогает передавать или отображать видео
    while True:
        if not video_capture.isOpened(): #если видеофайл не был успешно открыт..
            print("Couldn't find your webcam... Sorry :c")
        _, webcam_frame = video_capture.read() #возвращает кортеж, где 1 элемент—логическое значение (True=видеопоток содержит кадр для чтения), а 2—фактический видеокадр.  
        gray_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2GRAY) #преобразование цветного изображения BGR в оттенки серого
        for cascade, color in cascades: 
            captures = [cascade.detectMultiScale( #ищет объекты (лица например)
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30)
            )]
            for capture in captures:
                for (x, y, w, h) in capture:
                    draw_sqare(webcam_frame, color) #рисует прямоугольники вокруг найденного объекта
        show_frame(webcam_frame) #отображает изображение

        if is_user_wants_quit():#если нажата q - выходит
            break
    video_capture.release() #освобождает объект видеозахвата
    cv2.destroyAllWindows() #закрывает все окна

