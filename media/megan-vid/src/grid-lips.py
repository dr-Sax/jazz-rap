from moviepy import *
import os
import glob

# this is intended to be a set of functions to snap together series of gridded videos
# which lapse in time based on a set of input durations and nxm grid values
# grid_gen: a function to create gridded videos for a certain duration
# dynamic_grid: a second function to call grid_gen and curate a moving image of grids
# media_picker: a function to arrange videos or photos within the grid spaces


######### INIT #####################
vid_path = "../video/lips"

s0 = [
                [5]
            ]
s1 = [
                [2, 3]
            ]

s2 = [
                [4, 5],
                [6, 7]
            ]

s3 = [
                [8, 9, 10, 11],
                [0, 3, 6, 7]
            ]

state_list = [
                {"index_matrix":s0, "duration":0.67},
                {"index_matrix":s1, "duration":0.67},
                {"index_matrix":s2, "duration":0.67},
                {"index_matrix":s3, "duration":0.67},
            ]
#######################################

def grid_gen(index_matrix, duration):
    num_rows = len(index_matrix)
    num_cols = len(index_matrix[0])
    vid_matrix = []
    path_matrix = media_index_to_path(vid_path, index_matrix)
    vid = VideoFileClip(path_matrix[0][0])
    width = vid.w
    height = vid.h

    for r in range(0, num_rows):
        temp_row = []  # to store a row of vids / gets cleared every loop iter
        for c in range(0, num_cols):
            temp_row.append(VideoFileClip(path_matrix[r][c]))
        # end of loop
        vid_matrix.append(temp_row)
    # end of loop
    vid_grid = clips_array(vid_matrix)  # merge clips into a grid
    resized_vid_grid = vid_grid.resized((width, height))  # resize to original vid shape
    time_match = resized_vid_grid.with_duration(duration)

    return time_match

def dynamic_grid(state_list):
    dynamic_vid_list = []
    for state in state_list:
        vid_gen = grid_gen(state["index_matrix"], state["duration"])
        dynamic_vid_list.append(vid_gen)
    dynamic_vid = concatenate_videoclips(dynamic_vid_list)

    return dynamic_vid

def media_index_to_path(folder_path, index_matrix):

    # get media in order
    video_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp4"):
            video_files.append(os.path.join(folder_path, filename))

    for i in range(0, len(index_matrix)):
        for j in range(0, len(index_matrix[0])):
            index = index_matrix[i][j]
            index_matrix[i][j] = video_files[index]
    
    return index_matrix

#### MAIN #####################
grid = dynamic_grid(state_list)

# Write to a temporary file first
temp_file = "temp-grid.mp4"
grid = grid.without_audio()
grid.write_videofile(temp_file)

# Then rename to your desired filename
os.rename(temp_file, "../video/lips-grid.mp4")