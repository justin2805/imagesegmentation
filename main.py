import numpy as np
import math
import read_disp_img
import random
from collections import namedtuple
import copy


class Main(object):
    loop = True

    def main_class(self):
        while (self.loop):
            img_choice_obj = read_disp_img.Read_display_images()
            try:
                program_choice = int(input("1. Basic Global Thresholding\n2. K-means Clustering"))
                if program_choice == 1:
                    self.basic_global_thresholding(self.image_selection(), img_choice_obj)
                else:
                    self.k_means(self.image_selection(), img_choice_obj)
            except ValueError as v:
                print(v)
            # except IndexError as v:
            #     print(v)

    def image_selection(self):
        img_choice = int(input("\nSelect an image from the following:\n1. Constant Grey Region\n2.Noisy Region"
                               "\n3. Building Original\n4. HeadCT-Vandy\n5. Van-Orignal\n6. Tooth"
                               "\n7. Marion Airport\n8. Large Septagon\n9. Yeast USC\n10. Iceberg"
                               "\n11. Car on left\n12.Exit\n\n-->"))
        return img_choice

    def basic_global_thresholding(self, img_choice, img_choice_obj):
        threshold = int(input("Please provide initial threshold estimate\n-->"))
        threshold_diff = float(input("Please provide predefined threshold limit\n-->"))
        original_image = img_choice_obj.image_choice(img_choice)
        # print(original_image)
        shape = original_image.shape
        orig_rows = shape[0]
        orig_cols = shape[1]
        segment1 = []
        segment2 = []
        threshold_new = 0
        final_image = np.zeros(shape)
        m1 = 0
        m2 = 0

        # basic global thresholding logic
        while (abs(threshold - threshold_new) > threshold_diff):
            segment1.clear()
            segment2.clear()
            if (threshold_new != 0):
                threshold = threshold_new
            for row in range(orig_rows):
                for col in range(orig_cols):
                    pixel = original_image[row, col]
                    if pixel > threshold:
                        segment1.append(pixel)
                    else:
                        segment2.append(pixel)

            # incase threshold value and actual pixel value in image is too skewed
            # if len(segment1) == 0:
            #     print("\n ERROR:::\nPlease adjust your threshold to a different value: Segment 1 empty")
            # elif len(segment2) == 0:
            #     print("\n ERROR:::\nPlease adjust your threshold to a different value: Segment 2 empty")

            try:
                m1 = sum(segment1) / len(segment1)
            except ZeroDivisionError as z:
                print(z)
            try:
                m2 = sum(segment2) / len(segment2)
            except ZeroDivisionError as z:
                print(z)

            threshold_new = (m1 + m2) / 2
            diff = abs(threshold_new - threshold)
            print(*['Threshold :', threshold, ':: Threshold new:', threshold_new, ':: Threshold Difference:',
                    diff])
            print(*['Average of Segment 1:', m1, ':: Average of Segment 2:', m2,
                    '\n ******** Next Iteration*************'])
        print("Done")

        # segment image based on final threshold value
        for row in range(orig_rows):
            for col in range(orig_cols):
                pixel = original_image[row, col]
                if pixel > threshold:
                    final_image[row, col] = m1
                else:
                    final_image[row, col] = m2

        #  display images
        img_choice_obj.display_image(2, [original_image, final_image], ["Original Image", "Final Image"])

    def k_means(self, img_choice, img_choice_obj):
        k = int(input("Enter k value/ number of clusters"))
        # iterations = int(input("Enter number of iterations"))
        original_image = img_choice_obj.image_choice(img_choice)
        # Pixel = namedtuple('Pixel', ('pixel_value','cluster'))
        shape = original_image.shape
        final_image = np.zeros(shape)
        orig_rows = shape[0]
        orig_cols = shape[1]
        pixel_array = []
        # for row in range(orig_rows):
        #     for col in range(orig_cols):
        #         pixel_array[row][col] = Pixel(original_image[row,col],0)

        Pixel = namedtuple('Pixel', ('row', 'col', 'pixel_value'))
        # Pixel_cluster = namedtuple('Pixel_cluster', ('row', 'col', 'pixel_value','cluster'))
        k_array = []
        for i in range(k):
            # row = random.randrange(0,orig_rows)
            # col = random.randrange(0,orig_cols)
            k_array.append(random.randrange(np.amin(original_image),np.amax(original_image)))
        print(k_array)

        while True:
            cluster_array = []
            new_cluster_array=[]
            new_k_array = []
            for i in range(k):
                new_cluster_array.append([])
                cluster_array.append([])
            for row in range(orig_rows):
                for col in range(orig_cols):
                    pixel = original_image[row,col]
                    gl_dist = -1
                    cluster = 0
                    for i in range(k):
                        # cluster_center = k_array[i].pixel_value
                        # dist = distance.euclidean(k_array[i],pixel)
                        # dist = math.sqrt((k_array[i] - pixel)**2)
                        dist = abs(k_array[i] - pixel)
                        if gl_dist == -1 or dist < gl_dist:
                            gl_dist = dist
                            cluster = i
                    cluster_array[cluster].append(Pixel(row,col,original_image[row,col]))
                    new_cluster_array[cluster].append(Pixel(row,col,original_image[row,col]))

            print("***************** Iteration done ****************************")
            k_flag = False
            # print(new_cluster_array)
            # for i in range(k):
            #     len_1 = len(cluster_array[i])
            #     # for j in range(len_1):
            #     new_cluster_array[i].append(cluster_array[i])

            # new_cluster_array = cluster_array[:]
            for i in range(k):
                sum = 0
                mean = 0
                len_1 = len(new_cluster_array[i])
                print("Lenght of cls_arr: ["+str(i)+"] : "+str(len(cluster_array[i])))
                if not len_1 == 0:
                    for j in range(len_1):
                        sum += new_cluster_array[i].pop().pixel_value
                    mean = int(np.round(sum/len_1))
                print("AFTER POP :Lenght of cls_arr: [" + str(i) + "] : " + str(len(cluster_array[i])))

                new_k_array.append(mean)
                if new_k_array[i] == k_array[i]:
                    k_flag = True

            if not k_flag:
                print("clearing data")
                k_array.clear()
                for i in range(k):
                    k_array.append(new_k_array[i])
                new_k_array.clear()
                cluster_array.clear()
            else:
                print("Done")
                # print(len(cluster_array))
                # print(len(cluster_array[0]))
                for i in range(k):
                    print("Length of cl_array["+str(i)+"] : "+str(len(cluster_array[i])))
                    for j in range(len(cluster_array[i])):
                        pixell = cluster_array[i].pop()
                        _row = pixell.row
                        _col = pixell.col
                        _pixel_value = pixell.pixel_value
                        # print("pixel : "+str(_pixel_value)+"karray["+str(i)+"] :"+str(k_array[i]))
                        final_image[_row,_col] = k_array[i]
                break

        img_choice_obj.display_image(2, [original_image, final_image], ["Original Image", "Final Image"])






m = Main()
m.main_class()
