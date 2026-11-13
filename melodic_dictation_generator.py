# Melodic dictation generator
# Piano sounds, give the reference A and then a number of notes comprised within a number of octaves, with a maximum interval between 2 notes given as input

from re import fullmatch
import pygame
import time
from random import choice, randint
from decimal import *
getcontext().prec = 1;

# Constants

MAX_OCTAVE = 7;
MIN_OCTAVE = 1;
NOTE_LENGTH = 0.8; #seconds
REF_A_LENGTH = 2; #seconds

NOTES_NBR_DEFAULT = 6;
PLAY_REF_DEFAULT = 1;
REPETITIONS_DEFAULT = 0;
MAX_INTERVAL_DEFAULT = 14;
OCT_START_DEFAULT = 3;
OCT_END_DEFAULT = 4;
TIMELAPSE_DEFAULT = 0.6;

notes_nbr_reg = NOTES_NBR_DEFAULT;
play_ref_reg = PLAY_REF_DEFAULT;
repetitions_reg = REPETITIONS_DEFAULT;
max_interval_reg = MAX_INTERVAL_DEFAULT;
oct_start_reg = OCT_START_DEFAULT;
oct_end_reg = OCT_END_DEFAULT;
timelapse_reg = TIMELAPSE_DEFAULT;

note_name = {
    4: "C1", 5: "C#1", 6: "D1", 7: "D#1",
    8: "E1", 9: "F1", 10: "F#1", 11: "G1",
    12: "G#1", 13: "A1", 14: "A#1", 15: "B1",

    16: "C2", 17: "C#2", 18: "D2", 19: "D#2",
    20: "E2", 21: "F2", 22: "F#2", 23: "G2",
    24: "G#2", 25: "A2", 26: "A#2", 27: "B2",

    28: "C3", 29: "C#3", 30: "D3", 31: "D#3",
    32: "E3", 33: "F3", 34: "F#3", 35: "G3",
    36: "G#3", 37: "A3", 38: "A#3", 39: "B3",

    40: "C4", 41: "C#4", 42: "D4", 43: "D#4",
    44: "E4", 45: "F4", 46: "F#4", 47: "G4",
    48: "G#4", 49: "A4", 50: "A#4", 51: "B4",

    52: "C5", 53: "C#5", 54: "D5", 55: "D#5",
    56: "E5", 57: "F5", 58: "F#5", 59: "G5",
    60: "G#5", 61: "A5", 62: "A#5", 63: "B5",

    64: "C6", 65: "C#6", 66: "D6", 67: "D#6",
    68: "E6", 69: "F6", 70: "F#6", 71: "G6",
    72: "G#6", 73: "A6", 74: "A#6", 75: "B6",

    76: "C7", 77: "C#7", 78: "D7", 79: "D#7",
    80: "E7", 81: "F7", 82: "F#7", 83: "G7",
    84: "G#7", 85: "A7", 86: "A#7", 87: "B7",

    88: "C8"
}

def main(useRegisteredVariables : bool):

    if not useRegisteredVariables:
    
        # Inputs format checks and processing

        print("\nPlease enter a number of notes, or press ENTER to go with the default ("+str(NOTES_NBR_DEFAULT)+") :");
        param = input().replace(" ", "");
        notes_nbr = NOTES_NBR_DEFAULT;
        while param != "" and not (param.isnumeric() and int(param) > 0) :
            print("\nThe number of notes indicated must be an integer > 0.");
            print("Please enter a number of notes, or press ENTER to go with the default ("+str(NOTES_NBR_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            notes_nbr = int(param);

        print("\nPlease enter whether you want to hear the reference A before the dictation (type 1 for YES, 0 for NO), or press ENTER to go with the default ("+str(PLAY_REF_DEFAULT)+") :");
        param = input().replace(" ", "");
        play_ref = PLAY_REF_DEFAULT;
        while param != "" and not (param.isnumeric() and 0 <= int(param) <= 1) :
            print("\nThe reference A option must be either 1 or 0.");
            print("Please enter whether you want to hear the reference A before the dictation (type 1 for YES, 0 for NO), or press ENTER to go with the default ("+str(PLAY_REF_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            play_ref = bool(int(param));

        print("\nPlease enter the number of repetitions, on demand after key pressed (enter 0 for infinity), or press ENTER to go with the default ("+str(REPETITIONS_DEFAULT)+") :");
        param = input().replace(" ", "");
        repetitions = REPETITIONS_DEFAULT;
        while param != "" and not (param.isnumeric() and int(param) >= 0) :
            print("\nThe number of repetitions must be a positive integer.");
            print("Please enter the number of times you want to hear the dictation (0 for infinite on demand repetitions), or press ENTER to go with the default ("+str(REPETITIONS_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            repetitions = int(param);

        print("\nPlease enter the maximum interval to be played, in number of half-tones (for example a 7m is 10 half-tones), or press ENTER to go with the default (14 (so 9M)) :");
        param = input().replace(" ", "");
        max_interval = MAX_INTERVAL_DEFAULT;
        while param != "" and not (param.isnumeric() and int(param) > 0) :
            print("\nThe maximum interval (in half-tones) must be an integer > 0.");
            print("Please enter the maximum interval to be played, in number of half-tones (for example a 7m is 10 half-tones), or press ENTER to go with the default (14 (so 9M)) :");
            param = input().replace(" ", "");
        if param != "":
            max_interval = int(param);
        
        print("\nPlease enter the lowest octave (between " + str(MIN_OCTAVE) + " and " + str(MAX_OCTAVE) + "), or press ENTER to go with the default ("+str(OCT_START_DEFAULT)+") :");
        param = input().replace(" ", "");
        oct_start = OCT_START_DEFAULT;
        while param != "" and not (param.isnumeric() and MIN_OCTAVE <= int(param) <= MAX_OCTAVE) :
            print("\nThe lowest possible octave is " + str(MIN_OCTAVE) + ".");
            print("Please enter the lowest octave (between " + str(MIN_OCTAVE) + " and " + str(MAX_OCTAVE) + "), or press ENTER to go with the default ("+str(OCT_START_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            oct_start = int(param);
        
        print("\nPlease enter the highest octave (included, between " + str(MIN_OCTAVE) + " and " + str(MAX_OCTAVE) + "), or press ENTER to go with the default ("+str(OCT_END_DEFAULT)+") :");
        param = input().replace(" ", "");
        oct_end = OCT_END_DEFAULT;
        while param != "" and not (param.isnumeric() and oct_start <= int(param) <= MAX_OCTAVE) :
            print("\nThe highest octave possible is " + str(MAX_OCTAVE) + ". The highest octave chosen must be higher than the lowest one (which is currently "+str(oct_start)+").");
            print("Please enter the highest octave (included, between " + str(MIN_OCTAVE) + " and " + str(MAX_OCTAVE) + "), or press ENTER to go with the default ("+str(OCT_END_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            oct_end = int(param);
        
        print("\nPlease enter the time period between 2 notes (in seconds, dot separated decimals accepted), or press ENTER to go with the default ("+str(TIMELAPSE_DEFAULT)+") :");
        param = input().replace(" ", "");
        timelapse = TIMELAPSE_DEFAULT;
        def is_decimal(s):
            return bool(fullmatch(r"-?\d+(\.\d+)?", s))
        while param != "" and not (is_decimal(param) and Decimal(param) > 0) :
            print("\nThe time period between notes must be a decimal > 0.");
            print("Please enter the time period between 2 notes (in seconds, dot separated decimals accepted), or press ENTER to go with the default ("+str(TIMELAPSE_DEFAULT)+") :");
            param = input().replace(" ", "");
        if param != "":
            timelapse = Decimal(param);
        
        # Updating global variables for next main iteration
        global notes_nbr_reg;
        global play_ref_reg;
        global repetitions_reg;
        global max_interval_reg;
        global oct_start_reg;
        global oct_end_reg;
        global timelapse_reg;
        notes_nbr_reg = notes_nbr;
        play_ref_reg = play_ref;
        repetitions_reg = repetitions;
        max_interval_reg = max_interval;
        oct_start_reg = oct_start;
        oct_end_reg = oct_end;
        timelapse_reg = timelapse;
    else :
        notes_nbr = notes_nbr_reg;
        play_ref = play_ref_reg;
        repetitions = repetitions_reg;
        max_interval = max_interval_reg;
        oct_start = oct_start_reg;
        oct_end = oct_end_reg;
        timelapse = timelapse_reg;
    

    # Generating random note sequence

    valid_min_note_nbr = (oct_start-1)*12 + 4;
    valid_max_note_nbr = oct_end*12 + 3;
    if valid_max_note_nbr == 87:
        valid_max_note_nbr = 88;
    # Choosing the reference A
    note = choice([x for x in {13, 25, 37, 49, 61, 73, 85} if valid_min_note_nbr <= x <= valid_max_note_nbr]);
    if play_ref:
        dictation = [note];
    else:
        dictation = [];
    
    for i in range (notes_nbr):
        previous_note = note;
        while previous_note == note:
            note = randint(
                max(valid_min_note_nbr, note-max_interval), 
                min(valid_max_note_nbr, note+max_interval));
        dictation.append(note);

    # Playing

    pygame.mixer.init()

    stop_flag = False;

# and put it on github to build for windows as well
    i = 0;
    while repetitions == 0 or i < repetitions:
        i += 1;
        print("\nReady for repetition number " + str(i) + " ? Press any key to start. Press 'n' to skip to the correction.");
        start = input();
        if start == 'n':
            stop_flag = True;
            repetitions = -1;
        if not stop_flag:
            for j in range(len(dictation)):
                note = dictation[j]
                sound = pygame.mixer.Sound('./85_steinway_tiles_mp3/'+str(note)+'.mp3');
                channel = sound.play();
                if j == 0 and play_ref:
                    time.sleep(REF_A_LENGTH);
                else:
                    time.sleep(NOTE_LENGTH);
                channel.stop(); 
                time.sleep(float(timelapse));
    
    # Display the correct answer

    print("\nReady for the correction ? Press any key to continue.");
    input();
    print([note_name[note] for note in dictation]);
    print("\nNote : The number after the note indicates the octave. All alterations are # .");
    return 0;

run = True;
useRegisteredVariables = False;
print("\nWelcome !");
while run:
    main(useRegisteredVariables);
    cont = input("\nRun again ? (y/n)");
    if cont.lower() != "y":
        run = False;
    else:
        newVars = input("\nWould you like to use the same parameters ? (y/n)")
        if newVars.lower() == "y":
            useRegisteredVariables = True;
        else:
            useRegisteredVariables = False;
print("\nBye !\n")