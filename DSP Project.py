import cv2
import PySimpleGUI as sg
import os

# هنا بحدد مسار الصوره الي هحطها من الجهاز بتاعي ومسار الصوره الي انا عدلتها او عملتلها معالجه
input_image_path = None
output_image_path = None

# دي بدايه كود ال processsing  الي بضيفها على الصور 


# اول حاجه بيقرا الصوره الي انا حددتها او اخترتها 
def read_image(image_path):
    # بستخدم عشان اقرا الصوره OpenCV
    image = cv2.imread(image_path)
    if image is None:
     #هنا لو مجطتش صوره هيطلعلي ايرور
        sg.popup('Could not open the image. Please check the path.')
        return None
    return image

# تحسين جودة الصورة
def enhance_image(image):
    if image is None:
        return None
    # تحسين الصورة باستخدام OpenCV
    return cv2.detailEnhance(image)

# تطبيق  تحديد الحواف
def apply_edge_detection(image):
    if image is None:
        return None
    # تطبيق تحديد الحواف باستخدام OpenCV
    return cv2.Canny(image, 100, 200)

# هنا بغيير حجم الصورة 
def resize_image(image, width, height):
    if image is None:
        return None
    # تغيير حجم الصورة باستخدام OpenCV
    return cv2.resize(image, (100, 200))


# تحويل الصورة إلى اللون الرمادي
def convert_to_gray(image):
    if image is None:
        return None
    # تحويل الصورة إلى اللون الرمادي باستخدام OpenCV
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# تحويل الصورة إلى الأبيض والأسود باستخدام اللون الرمادي وتطبيق القيمة المحددة من التمرير
def convert_to_bw_dynamic(image, threshold_value):
    if image is None:
        return None
    # تحويل الصورة إلى اللون الرمادي
    gray_image = convert_to_gray(image)
    # تحويل الصورة الرمادية إلى الأبيض والأسود باستخدام قيمة التمرير المحددة
    _, bw_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    return bw_image



# حفظ الصورة الي عملت ليها معالجه
def save_image(image, output_path):
    if image is None:
        return
    # استخراج مسار الدليل من مسار الصورة المدخلة
    save_path = os.path.dirname(input_image_path)
    # بعمل اسم ملف جديد للصورة الي عملتلها معالجه
    filename = 'output_image.jpg' 
    # انضمام بين المسار واسم الملف
    output_image_path = os.path.join(save_path, filename)
    # حفظ الصورة باستخدام OpenCV
    cv2.imwrite(output_image_path, image)
    sg.popup('تم حفظ الصورة بنجاح!')

# نهاية كود معالجة الصور

# بداية كود gui

# هنا اول حاجه بعمل رساله ترحيب بعمل باتون اختار منه الصوره
layout = [
    [sg.Text('Welcome to Image Processor', size=(30, 1), font=('Helvetica', 20), justification='center')],
    [sg.Button('Choose Image', size=(20, 2))],
]

# إنشاء النافذة الرئيسية
window = sg.Window('Image Processor', layout, element_justification='c', background_color='pink')

#  يعني على حسب ما تختار انت بوايل لوب  الحدث الرئيسي لمعالجة الصور
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Choose Image':
        # اختيار الصورة
        input_image_path = sg.popup_get_file('Choose an image to process')
        if input_image_path:
            # تحميل الصورة الي اخترتها
            image = read_image(input_image_path)
            window.close()
            # عرض نافذة اختيار الميزات بعد اختيار الصورة
            layout = [
                [sg.Button('Enhance Image', size=(20, 2))],
                [sg.Button('Apply Edge Detection', size=(20, 2))],
                [sg.Button('Resize Image', size=(20, 2))],
                [sg.Button('Convert to Black & White', size=(20, 2))],
            ]
            window = sg.Window('Image Processor', layout, element_justification='c', background_color='pink')
        else:
            sg.popup('No image selected. Please select an image.')

    elif event == sg.WINDOW_CLOSED:
        break

    elif event == 'Enhance Image':
        enhanced_image = enhance_image(image)
        save_image(enhanced_image, output_image_path)

    elif event == 'Apply Edge Detection':
        edges_image = apply_edge_detection(image)
        save_image(edges_image, output_image_path)

    elif event == 'Resize Image':
        resized_image = resize_image(image, 500, 500)
        save_image(resized_image, output_image_path)

    elif event == 'Convert to Black & White':
        threshold_value = 127  # يمكنك تغيير هذه القيمة وفقًا لاحتياجاتك
        bw_image = convert_to_bw_dynamic(image, threshold_value)
        save_image(bw_image, output_image_path)

window.close()
