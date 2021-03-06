import numpy as np
import cv2
import dlib
import math
import os
from align_face import *
from landmarks import *


def rate_face(benchmarks, face):
    rating = 0
    print("Eyes-Nose ratio and benchmark: {} and {}".format(abs(benchmarks[0][0]-face[0]), benchmarks[0][1]))
    if abs(benchmarks[0][0]-face[0]) < benchmarks[0][1]*4:
        if abs(benchmarks[0][0]-face[0]) < benchmarks[0][1]*1.5:
            rating += 1
        rating += 1
    print("Nose ratio and benchmark: {} and {}".format(abs(benchmarks[1][0]-face[1]), benchmarks[1][1]))
    if abs(benchmarks[1][0]-face[1]) < benchmarks[1][1]*9:
        if abs(benchmarks[1][0]-face[1]) < benchmarks[1][1]*4.5:
            rating += 1
        rating += 1
    print("Mouth ratio and benchmark: {} and {}".format(abs(benchmarks[2][0]-face[2]), benchmarks[2][1]))
    if abs(benchmarks[2][0]-face[2]) < benchmarks[2][1]*5:
        if abs(benchmarks[2][0]-face[2]) < benchmarks[2][1]*4:
            rating += 1
        rating += 1
    print("Eyes-Nose angle ratio and benchmark: {} and {}".format(abs(benchmarks[3][0]-face[3]), benchmarks[3][1]))
    if abs(benchmarks[3][0]-face[3]) < benchmarks[3][1]*10:
        if abs(benchmarks[3][0]-face[3]) < benchmarks[3][1]*4.5:
            rating += 1
        rating += 1
    print("Eyes-Mouth ratio and benchmark: {} and {}".format(abs(benchmarks[4][0]-face[4]), benchmarks[4][1]))
    if abs(benchmarks[4][0]-face[4]) < benchmarks[4][1]*6:
        if abs(benchmarks[4][0]-face[4]) < benchmarks[4][1]*5.5:
            rating += 1
        rating += 1
    return rating


def calc_ratios(landmarks):
    landmarks = np.squeeze(np.asarray(landmarks))
    left_eye_w  = landmarks[36]
    left_eye_e  = landmarks[39]
    right_eye_w = landmarks[42]
    right_eye_e = landmarks[45]
    middle_eyes = [
        int(math.floor(left_eye_e[0] + 0.5*(right_eye_w[0]-left_eye_e[0]))), 
        int(math.floor(left_eye_e[1] + 0.5*(right_eye_w[1]-left_eye_e[1])))
    ]
    nose_n      = landmarks[27]
    nose_w      = landmarks[31]
    nose_s      = landmarks[33]
    nose_e      = landmarks[35]
    mouth_n     = landmarks[51]
    mouth_w     = landmarks[48]
    mouth_s     = landmarks[57]
    mouth_e     = landmarks[54]

    eyes_nose_ratio = (
        math.sqrt(
            math.pow((left_eye_e[0]-right_eye_w[0]), 2) + math.pow((left_eye_e[1]-right_eye_w[1]), 2)
        )
        /
        math.sqrt(
            math.pow((middle_eyes[0]-nose_s[0]), 2) + math.pow((middle_eyes[1]-nose_s[1]), 2)
        )
    )

    nose_ratio = (
        math.sqrt(
            math.pow((nose_n[0]-nose_s[0]), 2) + math.pow((nose_n[1]-nose_s[1]), 2)
        )
        /
        math.sqrt(
            math.pow((nose_w[0]-nose_e[0]), 2) + math.pow((nose_w[1]-nose_w[1]), 2)
        )
    )

    mouth_ratio = (
        math.sqrt(
            math.pow((mouth_w[0]-mouth_e[0]), 2) + math.pow((mouth_w[1]-mouth_w[1]), 2)
        )
        /
        math.sqrt(
            math.pow((mouth_n[0]-mouth_s[0]), 2) + math.pow((mouth_n[1]-mouth_s[1]), 2)
        )
    )

    left_eye_nose = math.sqrt(
        math.pow((left_eye_e[0]-nose_s[0]), 2) + math.pow((left_eye_e[1]-nose_s[1]), 2)
    )
    right_eye_nose = math.sqrt(
        math.pow((right_eye_w[0]-nose_s[0]), 2) + math.pow((right_eye_w[1]-nose_s[1]), 2)
    )
    eyes_nose_angle_ratio = (left_eye_nose/right_eye_nose) if left_eye_nose > right_eye_nose else (right_eye_nose/left_eye_nose)

    left_eye_mouth = math.sqrt(
        math.pow((left_eye_e[0]-mouth_w[0]), 2) + math.pow((left_eye_e[1]-mouth_w[1]), 2)
    )
    right_eye_mouth = math.sqrt(
        math.pow((right_eye_w[0]-mouth_e[0]), 2) + math.pow((right_eye_w[1]-mouth_e[1]), 2)
    )
    eyes_mouth_ratio = (left_eye_mouth/right_eye_mouth) if left_eye_mouth > right_eye_mouth else (right_eye_mouth/left_eye_mouth)

    print "Eyes-Nose ratio:", eyes_nose_ratio
    print "Nose ratio:", nose_ratio
    print "Mouth ratio:", mouth_ratio
    print "Eyes-Nose Angle ratio:", eyes_nose_angle_ratio
    print "Eyes-Mouth ratio:", eyes_mouth_ratio

    return {
        'eyes_nose_ratio': eyes_nose_ratio,
        'nose_ratio': nose_ratio,
        'mouth_ratio': mouth_ratio,
        'eyes_nose_angle_ratio': eyes_nose_angle_ratio,
        'eyes_mouth_ratio': eyes_mouth_ratio
    }

# def calc_celeb_ratios(landmarks):
#     lefteye = landmarks[0]
#     righteye = landmarks[1]
#     nose = landmarks[2]
#     left_mouth = landmarks[3]
#     right_mouth = landmarks[4]

if __name__ == '__main__':
    write_to_file = False

    current_dir = os.path.dirname(__file__)
    file_path = '../Data/Ratings/{}'.format("benchmarks.txt")
    file_rel_path = os.path.join(current_dir, file_path)
    benchmarks_file = open(file_rel_path, 'r')
    benchmarks = [ [float(b.replace("\r\n", "").split(";")[0]), float(b.replace("\r\n", "").split(";")[1])] for b in benchmarks_file ]
    benchmarks_file.close()
    
    src_dir = '../Data/Datasets/{}'.format("SCUT-FBP")
    files = os.walk(src_dir).next()[2]
    file_names_ratings = []
    image_counter = 1

    current_dir = os.path.dirname(__file__)
    file_path = '../Data/Ratings/{}'.format("Processed_SCUT-FBP_Ratings.txt")
    file_rel_path = os.path.join(current_dir, file_path)
    rating_file = open(file_rel_path, 'w')
    
    for i,file_name in enumerate(files):
        if not (file_name == ".DS_Store" or file_name == "ReadMe.txt"):
            new_filename = "{}.jpg".format(image_counter)
            try:
                p = calc_ratios(get_landmarks(
                    dirname="SCUT-FBP",
                    dest_dir="Processed_SCUT-FBP",
                    filename="{}".format(file_name), 
                    new_filename=new_filename,
                    showimg=False, 
                    dim1=500, 
                    dim2=500, 
                    save_images=True
                ))
                rating = rate_face(benchmarks, [
                    p['eyes_nose_ratio'],
                    p['nose_ratio'],
                    p['mouth_ratio'],
                    p['eyes_nose_angle_ratio'],
                    p['eyes_mouth_ratio']
                ])
                print("{} - {} : {} --> {}".format(i+1, file_name, new_filename, rating))
                rating_file.write("{};{}\r\n".format(new_filename, rating))
                image_counter += 1
            except:
                print("Could not append to people: {}.".format(file_name))
    rating_file.close()
    print("Done writing to file.")
