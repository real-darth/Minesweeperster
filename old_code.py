# fromg grid.py

def get_cell_data(self, px, r, c):

        def get_number_from_color(color_pixel) -> int:
            # convert from tuple to array
            color_array = np.asarray(color_pixel)
            # get the difference of all colors, the closest color will be closer to zero
            diff = abs(self.colors - color_array)
            # sum the 3 RGB values
            diff_sum = diff.sum(axis=1)
            # return the index smallest difference, that is our key / number
            return np.argmin(diff_sum)
        
        pixel_pos = [self.cell_scale[0] * r, self.cell_scale[1] * c]

        # let's try just checking two pixels in total!!
        x, y = round(pixel_pos[0] + self.cell_scale[0] / 2), round(pixel_pos[1] + self.cell_scale[1] / 2 + 2)

        color_pixel_1 = px[x, y] 
        color_pixel_2 = px[pixel_pos[0] + self.cell_scale[0] / 2 , pixel_pos[1]  + self.cell_scale[1] / 2]

        #bingus = np.asarray(color_pixel_1)
        #bangus = abs(self.colors - bingus)
        #binus = bangus.sum(axis=1)

        #testis = np.argmin(binus)
        test_1 = get_number_from_color(color_pixel_1)
        test_2 = get_number_from_color(color_pixel_2)

        # get the largest number
        result = max(test_1, test_2)

        #print(testis)

        #test = min(sum(self.colors), key=lambda x: sum(color_pixel))

        #test_sum = sum(testis)
        #num = self.number_dict[test_sum]
        
        # DEBUG COLORS
        px[x, y] = (255, 0, 0)
        px[pixel_pos[0] + self.cell_scale[0] / 2 , pixel_pos[1]  + self.cell_scale[1] / 2] = (0, 255, 0)

        # if number is zero, we check for unclicked (white)
        if result == 0:
            white_pixel_1 = px[x, pixel_pos[1] + 2]
            white_pixel_2 = px[pixel_pos[0], y]

            # DEBUG COLOR
            px[x, pixel_pos[1] + 1] = (0, 0, 0)
            px[pixel_pos[0] + 2, y] = (0, 0, 0)

            # TODO: testa också bara jämföra direkt...
            if (np.asarray(white_pixel_1) == [255, 255, 255]).all():
                return 'X'

            if (np.asarray(white_pixel_2) == [255, 255, 255]).all():
                return 'X'

            #boba = np.asarray(white_pixel)
            #biba = abs(boba - [189, 189, 189], [boba - [255, 255, 255]])
            #beba = np.argmin(biba.sum(axis=1))

            #if beba == 1:
            #    return 'X'

        return result