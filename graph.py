def get_braille_density(value):
    density_chars = [' ', '⡇', '⢇', '⢣', '⢱', '⠈', '⠐', '⠠', '⢀', '⢠', '⣀', '⣄', '⣤', '⡎', '⡜', '⡸', '⢸']
    index = int(value * (len(density_chars) - 1))
    return density_chars[index]

def draw_function(width=50, height=25, func=lambda x: x):
    # 2D 그리드 생성
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    middle_y = height // 2
    middle_x = width // 2
    
    # x축 그리기 (얇은 선으로)
    for x in range(width):
        grid[middle_y][x] = '⠂'
        # x축 눈금 표시
        if (x - middle_x) % 5 == 0:
            grid[middle_y][x] = '⠒'
            if x != middle_x:  # 원점 제외
                grid[middle_y + 1][x] = str(abs((x - middle_x) // 5))[-1]
    
    # y축 그리기 (얇은 선으로)
    for y in range(height):
        grid[y][middle_x] = '⠂'
        # y축 눈금 표시
        if (y - middle_y) % 3 == 0:
            grid[y][middle_x] = '⠒'
            if y != middle_y:  # 원점 제외
                grid[y][middle_x + 1] = str(abs((middle_y - y) // 3))[-1]
    
    # 원점 표시
    grid[middle_y][middle_x] = '⠿'
    
    # 함수 그래프 그리기
    points = []
    for x in range(-width//2, width//2):
        try:
            real_x = x / 5
            y = func(real_x)
            plot_y = middle_y - int(y * 3)
            if 0 <= plot_y < height:
                points.append((x + width//2, plot_y))
        except:
            continue
    
    # 점들 사이를 부드럽게 연결
    for i in range(len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
        steps = max(int(distance * 2), 1)
        for step in range(steps):
            t = step / steps
            x = int(x1 + (x2-x1) * t)
            y = int(y1 + (y2-y1) * t)
            if 0 <= x < width and 0 <= y < height:
                if grid[y][x] not in ['⠂', '⠒', '⠿']:  # 축과 겹치지 않게
                    density = 1 - (step/steps)
                    grid[y][x] = get_braille_density(density)
    
    # 그래프 출력
    for row in grid:
        print(''.join(row))

# 사용 예시
# import math

# print("\nsin 함수 그래프:")
# draw_function(func=math.sin*1.1)

# print("\n2차 함수 그래프:")
# draw_function(func=lambda x: -x**2/4)