def get_points():
    points = []
    while True:
        point = input("Enter a point in the format 'x, y' or leave blank to finish: ")
        if not point:
            break
        x, y = map(int, point.split(','))
        points.append({"x": x, "y": y})
    return points

def ensure_clockwise(points):
    # Use the Shoelace formula to calculate the area
    area = 0.5 * sum(p["x"]*q["y"] - q["x"]*p["y"] for p, q in zip(points, points[1:] + points[:1]))
    # If the area is positive, the points are in clockwise order
    if area <= 0:
        points = points[::-1]  # Reverse the list to make it clockwise
    return points

points = get_points()

if len(points) < 3:
    print("You must enter at least 3 points.")
else:
    points = ensure_clockwise(points)
    print("            [")
    for point in points:
        print(f"                {{\"x\": {point['x']}, \"y\": {point['y']}}},")
    print("            ],")
    print("The points are now in clockwise order.")