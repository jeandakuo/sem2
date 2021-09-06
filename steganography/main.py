import PIL.Image as Image
import numpy as np
import PySimpleGUI as sg
from qweqwe import er
from math import sqrt, log
import cv2 as cv
from matplotlib import pyplot as plt


def rgb_gray(path):
    """
    RGB to grayscale
    """
    img = Image.open(f'{path}').convert('L')
    return img


if __name__ == '__main__':

    sg.theme('Random')  # Keep things interesting for your users

    layout = [[sg.Text('Найдите картинки на компуктере')],
              [sg.Text('Картинка-Контейнер  '),
               sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/sample.bmp'), sg.FileBrowse(),
               sg.Button('Картинка-Контейнер появись')],
              [sg.Text('Картинка-Сообщение'),
               sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/FLAG_B24.BMP'),
               sg.FileBrowse(), sg.Button('Картинка-Сообщение появись')],
              [sg.Checkbox('GrayScale', default=False)],
              [sg.Button('Показать Ширину и Высоту')],
              [sg.Text('Сохранить'), sg.Input(), sg.FolderBrowse(), sg.Button('Спрятать сообщение в контейнер')],
              [sg.Text('Открыть   '), sg.Input(), sg.FolderBrowse(), sg.Button('Показать картинку')],
              [sg.Button("Метрики"), sg.Button('Гистограммы')],
              [sg.Button('Read'), sg.Exit()]]

    window = sg.Window('Римляне 21века', layout)
    window2_active = False
    window3_active = False
    while True:  # The Event Loop
        event, values = window.read()
        # sg.Print(event, values)
        if event == 'Показать Ширину и Высоту':
            with Image.open(values[1]) as img:
                sg.Popup(img.size)
                width_sec, height_sec = img.size
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Картинка-Контейнер появись':
            with Image.open(values[0]) as img:
                img.show()
        if event == 'Картинка-Сообщение появись':
            with Image.open(values[1]) as img:
                img.show()
        if event == 'Спрятать сообщение в контейнер' and values[2] == True:
            img_con = Image.open(values[0])
            img_con = img_con.convert('L')
            img_sec = Image.open(values[1])
            img_sec = img_sec.convert('L')
            con_array = np.array(img_con)
            sec_array = np.array(img_sec)
            data = ''
            # print(len(sec_array))
            # print(len(sec_array[0]))
            width_sec = len(sec_array)
            height_sec = len(sec_array[0])
            for i in range(len(sec_array)):
                for j in range(len(sec_array[i])):
                    data = data + er(sec_array[i][j])
            i = 0
            width, height = img_con.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = img_con.getpixel((x, y))
                    if i < len(data):
                        pixel = pixel & ~1 | int(data[i])
                        i += 1
                    img_con.putpixel((x, y), pixel)
            img_con.save("steg_con_gray.bmp", "BMP")
            img_con.show()
        if event == 'Показать картинку' and values[2] == True:
            extracted_bin = []
            with Image.open("steg_con_gray.bmp") as img:
                width, height = img.size
                byte = []
                for x in range(0, width):
                    for y in range(0, height):
                        pixel = img.getpixel((x, y))
                        extracted_bin.append(pixel & 1)
                data = "".join([str(x) for x in extracted_bin])
                data_new = [data[i:i + 8] for i in range(0, len(data), 8)]
                data_array = np.empty([width_sec, height_sec], dtype='int')
                counter = 0
                for i in range(0, width_sec):
                    for j in range(0, height_sec):
                        data_array[i][j] = data_new[counter]
                        # print(j)
                        counter += 1
                for i in range(width_sec):
                    for j in range(height_sec):
                        data_array[i][j] = int(str(data_array[i][j]).strip('[').strip(']'), 2)
                # print(len(data))
                # print(data)
                pil_image = Image.fromarray(data_array)
                pil_image.show()
        if event == 'Спрятать сообщение в контейнер' and values[2] == False:
            img_con = Image.open(values[0])
            img_sec = Image.open(values[1])
            con_array = np.array(img_con)
            sec_array = np.array(img_sec)
            print(img_con.mode)
            print(img_sec.mode)
            data = ''
            width_sec, height_sec = img_sec.size
            # print(sec_array)
            for i in range(len(sec_array)):
                for j in range(len(sec_array[i])):
                    for n in range(3):
                        data = data + er(sec_array[i][j][n])
            width, height = img_con.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img_con.getpixel((x, y)))
                    for n in range(0, 3):
                        if i < len(data):
                            pixel[n] = pixel[n] & ~1 | int(data[i])
                            i += 1
                    img_con.putpixel((x, y), tuple(pixel))
            img_con.save("steg_con.bmp", "BMP")
            img_con.show()
        if event == 'Показать картинку' and values[2] == False:
            extracted_bin = []
            data = ''
            with Image.open("steg_con.bmp") as img:
                width, height = img.size
                byte = []
                for x in range(0, width):
                    for y in range(0, height):
                        pixel = list(img.getpixel((x, y)))
                        for n in range(0, 3):
                            extracted_bin.append(pixel[n] & 1)

            data = "".join([str(x) for x in extracted_bin])
            data_new = [data[i:i + 8] for i in range(0, len(data), 8)]
            data_array = np.empty([len(sec_array), len(sec_array[0]), 3], dtype='int')
            counter = 0
            for i in range(len(sec_array)):
                for j in range(len(sec_array[i])):
                    for n in range(3):
                        data_array[i][j][n] = data_new[counter]
                        counter += 1
            for i in range(len(sec_array)):
                for j in range(len(sec_array[i])):
                    for n in range(3):
                        data_array[i][j][n] = int(str(data_array[i][j][n]).strip('[').strip(']'), 2)
            pil_image = Image.fromarray(sec_array)
            pil_image.show()
        if not window2_active and event == 'Метрики':
            layout2 = [
                [sg.Text('Метрики для цветного:')],
                [sg.Button('ц/в. MSE, RMSE и PSNR')],
                [sg.Text('Исходное изображение:'),
                 sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/sample.bmp'), sg.FileBrowse()],
                [sg.Text('Новое изображение:     '),
                 sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/steg_con.bmp'), sg.FileBrowse()],
                [sg.Text('Метрики для полутона:')],
                [sg.Button('п/т. MSE, RMSE и PSNR')],
                [sg.Text('Исходное изображение:'),
                 sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/sample.bmp'), sg.FileBrowse()],
                [sg.Text('Новое изображение:     '),
                 sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/steg_con_gray.bmp'), sg.FileBrowse()],
                [sg.Exit('Exit')]
            ]
            window2 = sg.Window('Вычислялки', layout2)
            while True:
                event2, values2 = window2.Read()
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                    window2_active = False
                    window2.Close()
                    break
                if event2 == 'ц/в. MSE, RMSE и PSNR':
                    img_I = Image.open(values2[0])
                    array_I = np.array(img_I)
                    img_K = Image.open(values2[1])
                    array_K = np.array(img_K)
                    mse_R = 0
                    mse_G = 0
                    mse_B = 0
                    print(img_I.size)
                    print(img_K.size)
                    for i in range(len(array_I)):
                        for j in range(len(array_I[i])):
                            mse_R += (int(array_I[i][j][0]) - int(array_K[i][j][0])) ** 2
                            mse_G += (int(array_I[i][j][1]) - int(array_K[i][j][1])) ** 2
                            mse_B += (int(array_I[i][j][2]) - int(array_K[i][j][2])) ** 2

                    mse_R = mse_R / len(array_I) / len(array_I[0])
                    mse_G = mse_G / len(array_I) / len(array_I[0])
                    mse_B = mse_B / len(array_I) / len(array_I[0])

                    rmse_R = sqrt(mse_R)
                    rmse_G = sqrt(mse_G)
                    rmse_B = sqrt(mse_B)

                    PSNR = 20 * log(255 / (rmse_R + rmse_G + rmse_B) * 3, 10)

                    sg.Popup(f'MSE_R = {mse_R}  RMSE_R = {rmse_R} '
                             f'\nMSE_G = {mse_G}     RMSE_G = {rmse_G} '
                             f'\nMSE_B = {mse_B}     RMSE_G = {rmse_G} '
                             f'\nPNSR = {PSNR}', title='Вычислялки для цветного))))')
                if event2 == 'п/т. MSE, RMSE и PSNR':
                    img_I = Image.open(values2[2]).convert('L')
                    array_I = np.array(img_I)
                    img_K = Image.open(values2[3])
                    array_K = np.array(img_K)
                    mse = 0
                    for i in range(len(array_I)):
                        for j in range(len(array_I[i])):
                            mse += (int(array_I[i][j]) - int(array_K[i][j])) ** 2

                    mse = mse / len(array_I) / len(array_I[0])

                    rmse = sqrt(mse)

                    PSNR_Y = 20 * log(255 / rmse * 3, 10)

                    sg.Popup(f'MSE_R = {mse}  RMSE_R = {rmse} '
                             f'\nPNSR = {PSNR_Y}', title='Вычислялки для полутона))))')
        if not window3_active and event == 'Гистограммы':
            layout3 = [
                       [sg.Text('Открыть'), sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/sample.bmp'),
                        sg.FileBrowse(), sg.Button('Показать гистограмму цветной картинки')],
                       [sg.Text('Открыть'), sg.Input(default_text='C:/Users/God/PycharmProjects/Steg_Lab1/steg_con_gray.bmp'), sg.FileBrowse(), sg.Button('Показать гистограмму полутонной картинки')],
                       [sg.Exit('Exit')]
                      ]
            window3 = sg.Window('Вычислялки', layout3)
            while True:
                event3, values3 = window3.Read()
                if event3 == sg.WIN_CLOSED or event3 == 'Exit':
                    window3_active = False
                    window3.Close()
                    break
                if event3 == 'Показать гистограмму цветной картинки':
                    img = cv.imread(values3[0])
                    r, g, b = cv.split(img)

                    cv.imshow("image", img)
                    plt.hist(r.ravel(), 256, [0, 256], color='red', histtype='step', label='red values')
                    plt.hist(g.ravel(), 256, [0, 256], color='green', histtype='step', label='green values')
                    plt.hist(b.ravel(), 256, [0, 256], color='blue', histtype='step', label='blue values')
                    plt.legend()
                    plt.show()

                    cv.waitKey(0)
                    cv.destroyAllWindows()
                if event3 == 'Показать гистограмму полутонной картинки':
                    img = cv.imread(values3[0], 0)

                    cv.imshow("image", img)

                    plt.hist(img.ravel(), 256, [0, 256], color='gray', histtype='step', label='grayscale values')
                    plt.legend()
                    plt.show()

                    cv.waitKey(0)
                    cv.destroyAllWindows()

    window.close()
