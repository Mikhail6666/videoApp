def analyze_frames(frame_info):
    frame_numbers = [frame['frame_number'] for frame in frame_info]
    # Проверка, что frames является списком целых чисел
    if not isinstance(frame_numbers, list) or not all(isinstance(frame, int) for frame in frame_numbers):
        raise ValueError("frames должен быть списком целых чисел")

    if not frame_numbers:
        return []

    ranges = []
    current_start = frame_numbers[0]
    current_end = frame_numbers[0]

    for frame in frame_numbers[1:]:
        if frame <= current_end + 100:
            current_end = frame
        else:
            # Завершаем текущий диапазон и начинаем новый
            ranges.append([max(current_start - 50, 0), current_end + 50])
            current_start = frame
            current_end = frame

    # Добавляем последний диапазон
    ranges.append([max(current_start - 50, 0), current_end + 50])
    max_confidence_frames = find_max_confidence_frame(frame_info, ranges)
    return max_confidence_frames


def find_max_confidence_frame(frame_info, ranges):
    for i in range(0, len(ranges)):
        start, end = ranges[i]
        filtered_frames = [frame for frame in frame_info if start <= frame['frame_number'] <= end]
        if filtered_frames:
            max_confidence_frame = max(filtered_frames, key=lambda x: x['confidence'])
            ranges[i].append([max_confidence_frame['frame_number'], int(max_confidence_frame['confidence'] * 100)/100])
        else:
            ranges[i].append(None)  # Если в диапазоне нет фреймов
    return ranges


if __name__ == "__main__":
    # Пример использования
    frame_info = [
{'frame_number': 50, 'confidence': 0.5376182198524475},
{'frame_number': 51, 'confidence': 0.7659245729446411},
{'frame_number': 52, 'confidence': 0.8596360683441162},
{'frame_number': 53, 'confidence': 0.926864743232727},
{'frame_number': 54, 'confidence': 0.9415552020072937},
{'frame_number': 55, 'confidence': 0.8397021889686584},
{'frame_number': 60, 'confidence': 0.5601724982261658},
{'frame_number': 61, 'confidence': 0.7397993206977844},
{'frame_number': 62, 'confidence': 0.9727569818496704},
{'frame_number': 63, 'confidence': 0.961988627910614},
{'frame_number': 64, 'confidence': 0.9269065260887146},
{'frame_number': 65, 'confidence': 0.9432581663131714},
{'frame_number': 66, 'confidence': 0.699774980545044},
{'frame_number': 67, 'confidence': 0.3452432155609131},
{'frame_number': 68, 'confidence': 0.5324564576148987},
{'frame_number': 69, 'confidence': 0.34771445393562317},
{'frame_number': 70, 'confidence': 0.6513993144035339},
{'frame_number': 71, 'confidence': 0.7739019393920898},
{'frame_number': 72, 'confidence': 0.9389711022377014},
{'frame_number': 73, 'confidence': 0.9707053899765015},
{'frame_number': 74, 'confidence': 0.9192243814468384},
{'frame_number': 75, 'confidence': 0.9434117674827576},
{'frame_number': 76, 'confidence': 0.9680799245834351},
{'frame_number': 77, 'confidence': 0.9614390730857849},
{'frame_number': 78, 'confidence': 0.9588556289672852},
{'frame_number': 79, 'confidence': 0.9889539480209351},
{'frame_number': 80, 'confidence': 0.8801830410957336},
{'frame_number': 81, 'confidence': 0.9855653643608093},
{'frame_number': 82, 'confidence': 0.9967664480209351},
{'frame_number': 83, 'confidence': 0.9249813556671143},
{'frame_number': 85, 'confidence': 0.48471832275390625},
{'frame_number': 86, 'confidence': 0.3068307936191559},
{'frame_number': 87, 'confidence': 0.6752668619155884},
{'frame_number': 92, 'confidence': 0.4073377549648285},
{'frame_number': 93, 'confidence': 0.5252292156219482},
{'frame_number': 94, 'confidence': 0.5591802597045898},
{'frame_number': 95, 'confidence': 0.5218154788017273},
{'frame_number': 96, 'confidence': 0.33217793703079224},
{'frame_number': 105, 'confidence': 0.5655806660652161},
{'frame_number': 106, 'confidence': 0.4095684885978699},
{'frame_number': 110, 'confidence': 0.46936678886413574}]
    result = analyze_frames(frame_info)
    print(result) #[[0, 160, [82, 0.99]], [900, 1046, [982, 0.99]]]
