from datetime import datetime
from PIL import Image

def circle(data, center, radius, color, size):
    for x in range(size):
        for y in range(size):
            if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2:
                data[x * size  + y ] = color
    return data


def main(size, circle_centre, circle_radius, thickness):
    start_time = datetime.now()
    circle_color = (0, 0, 0)
    circle_amount = 2 
    data = [(255, 255, 255)] * size ** 2  
    img = Image.new('RGB',(size,size),'white')

    for i in range(circle_amount):
        data = circle(data, circle_centre, circle_radius, circle_color, size)
        circle_radius = int(circle_radius/thickness)
        circle_color = (255, 255, 255)

    img.putdata(data)
    img.save("image/circle.png", "PNG")

    print("Python Task to Draw Circle")
    print("Circle image is saved in image directory")
    print(f"Time needed: {datetime.now() - start_time}")


if __name__ == "__main__":
    # Inputs
    size = 400
    circle_centre = (int(size/2), int(size/2))
    circle_radius = circle_centre[0]
    thickness = 1.2

    main(size, circle_centre, circle_radius, thickness)