import cv2

CoinConfig = {
    "1 Rub": {
        "value": 1,
        "radius": 20.5,
        "ratio": 1,
        "count": 0,
    },
    "10 Rub": {
        "value": 10,
        "radius": 22,
        "ratio": 1.07317,
        "count": 0,
    },
    "2 Rub": {
        "value": 2,
        "radius": 23,
        "ratio": 1.12195,
        "count": 0,
    },
    "5 Rub": {
        "value": 5,
        "radius": 25,
        "ratio": 1.21951,
        "count": 0,
    },
}


# Предварительная обработка и поиск окружностей
def detect_coins(coins):
    # Приводим изображение к оттенкам серого
    img = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    # Размываем изображение с апертурой 7
    img = cv2.medianBlur(img, 7)
    # Преобразование Хафа по кругу
    return cv2.HoughCircles(
        img,  # исходное изображение
        cv2.HOUGH_GRADIENT,  # Тип распознавания
        1,
        50,
        param1=100,
        param2=50,
        minRadius=15,
        maxRadius=400
    )[0]


def calculate_amount(mapped_image):
    circles = detect_coins(mapped_image)
    radius = []
    coordinates = []

    for x, y, detected_radius in circles:
        radius.append(detected_radius)
        coordinates.append([x, y])

    smallest = min(radius)
    threshold = 0.035
    total_money = 0
    coins_on_board = 0
    font = cv2.FONT_HERSHEY_COMPLEX

    # По каждому найденому кругу
    for circle in circles:
        ratio_to_check = circle[2] / smallest
        # По каждой известной монете
        for rub in CoinConfig:
            if abs(ratio_to_check - CoinConfig[rub]['ratio']) <= threshold:
                value = CoinConfig[rub]['value']
                CoinConfig[rub]['count'] += 1
                total_money += value
                cv2.putText(mappedImage, str(value), (int(circle[0]) - 25, int(circle[1]) + 20), font, 3,
                            (0, 0, 0), 5)
                coins_on_board += 1
                break

    cv2.imwrite("mappedMoney.jpg", mappedImage)

    height, width, channels = mappedImage.shape
    avg_color = mappedImage.mean(axis=0).mean(axis=0).round()
    return height, width, avg_color, coins_on_board, total_money


mappedImage = cv2.imread('money.jpg', 1)
res = calculate_amount(mappedImage)
print(res)
