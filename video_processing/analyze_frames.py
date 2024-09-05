def analyze_frames(frames):
    # Проверка, что frames является списком целых чисел
    if not isinstance(frames, list) or not all(isinstance(frame, int) for frame in frames):
        raise ValueError("frames должен быть списком целых чисел")

    if not frames:
        return []

    ranges = []
    current_start = frames[0]
    current_end = frames[0]

    for frame in frames[1:]:
        if frame <= current_end + 100:
            current_end = frame
        else:
            # Завершаем текущий диапазон и начинаем новый
            ranges.append([max(current_start - 50, 0), current_end + 50])
            current_start = frame
            current_end = frame

    # Добавляем последний диапазон
    ranges.append([max(current_start - 50, 0), current_end + 50])

    return ranges


if __name__ == "__main__":
    # Пример использования
    frames = [327, 328, 329, 330, 331, 332, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351,
              352, 353, 354, 355, 356, 357, 358, 359, 360, 362, 364, 369, 370, 371, 372, 373, 382, 383, 387]
    results = {
        'frame_number': [327, 328, 329, 330, 331, 332, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349,
                         350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 362, 364, 369, 370, 371, 372, 373, 382,
                         383, 387]}
    result = analyze_frames(results['frame_number'])
    print(result)
