import cv2
import matplotlib.pyplot as plt

class Read_display_images(object):

    def image_choice(self, img_choice):
        if img_choice == 1:
            image_path = r'images/Fig1001(a)(constant_gray_region).tif'
        elif img_choice == 2:
            image_path = r'images/Fig1001(d)(noisy_region).tif'
        elif img_choice == 3:
            image_path = r'images/Fig1022(a)(building_original).tif'
        elif img_choice == 4:
            image_path = r'images/Fig1026(a)(headCT-Vandy).tif'
        elif img_choice == 5:
            image_path = r'images/Fig1027(a)(van_original).tif'
        elif img_choice == 6:
            image_path = r'images/Fig1030(a)(tooth).tif'
        elif img_choice == 7:
            image_path = r'images/Fig1034(a)(marion_airport).tif'
        elif img_choice == 8:
            image_path = r'images/Fig1040(a)(large_septagon_gaussian_noise_mean_0_std_50_added).tif'
        elif img_choice == 9:
            image_path = r'images/Fig1043(a)(yeast_USC).tif'
        elif img_choice == 10:
            image_path = r'images/Fig1045(a)(iceberg).tif'
        elif img_choice == 11:
            image_path = r'images/Fig1060(a)(car on left).tif'

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return image


    def display_image(self,cols, image_array, img_title):
        fig, ax = plt.subplots(ncols=cols)
        for i in range(len(image_array)):
            ax[i].imshow(image_array[i],cmap='gray')
            ax[i].set_title(img_title[i])
        plt.show()
        # ax[0].imshow(original_image, cmap='gray')
        # ax[0].set_title("Original")
        # ax[1].imshow(final_image, cmap='gray')
        # ax[1].set_title("Final")
        # plt.show()