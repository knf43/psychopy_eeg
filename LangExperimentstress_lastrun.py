#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Mon Apr  7 11:53:28 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

import serial
import time
import threading
from psychopy.hardware import joystick

# Pulse width (10 ms)
PulseWidth = 0.01
Connected = True

# COM3 TriggerBox port
port = serial.Serial("COM3", baudrate=9600)

# Function to listen for responses from the TriggerBox (optional, but safe to include)
def ReadThread(port):
    global Connected
    while Connected:
        try:
            if port.in_waiting > 0:
                print("0x%X" % ord(port.read(1)))
        except Exception as e: 
            print(f"Serial read error: {e}")
            break
            
# Start the read thread
thread = threading.Thread(target=ReadThread, args=(port,))
thread.start()

def send_trigger(trigger_val):
    val = int(round(trigger_val))
    port.write([val])
    time.sleep(PulseWidth)
    port.write([0x00])

# Set the port to an initial state
port.write([0x00])
time.sleep(PulseWidth)

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'LangExperimentnonstød'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': '',
    'version': ['1','2'],
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1280, 800]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/kayleefernandez/Desktop/psychopy zips/Psychopy experiment/LangExperimentstress_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # create speaker 'test_sound'
    deviceManager.addDevice(
        deviceName='test_sound',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    if deviceManager.getDevice('key_resp_2') is None:
        # initialise key_resp_2
        key_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_2',
        )
    if deviceManager.getDevice('key_resp_4') is None:
        # initialise key_resp_4
        key_resp_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_4',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='psychopy',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instructions" ---
    instr = visual.TextStim(win=win, name='instr',
        text='Is the verb in the present or past tense?\nAnswer as quickly as you can.\n\nPress B to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.08, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "test" ---
    test_sound = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='test_sound',    name='test_sound'
    )
    test_sound.setVolume(1)
    key_resp_2 = keyboard.Keyboard(deviceName='key_resp_2')
    fixationcross = visual.ShapeStim(
        win=win, name='fixationcross', vertices='cross',
        size=(0.15, 0.15),
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[-1,-1,-1], fillColor=[-1,-1,-1],
        opacity=1, depth=-2.0, interpolate=True)
    
    # --- Initialize components for Routine "takeabreak" ---
    text_3 = visual.TextStim(win=win, name='text_3',
        text='Træk vejret. \n\nTryk på mellemrumstasten for at fortsætte.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_4 = keyboard.Keyboard(deviceName='key_resp_4')
    
    # --- Initialize components for Routine "Thanks" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='Tak fordi du deltog i dette studie.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    response_clock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instr, key_resp],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    instructions.forceEnded = routineForceEnded = not continueRoutine
    
    sent_triggers = set()  # track which triggers have been sent
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr* updates
        
        # if instr is starting this frame...
        if instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr.frameNStart = frameN  # exact frame index
            instr.tStart = t  # local t and not account for scr refresh
            instr.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr.started')
            # update status
            instr.status = STARTED
            instr.setAutoDraw(True)
        
        # if instr is active this frame...
        if instr.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(response_clock.reset)
        if key_resp_4.status == STARTED:
            if 'joy' in globals():
                buttons = joy.getAllButtons()
                if len(buttons) > 1 and buttons[1]:  # B button to continue
                    key_resp_4.keys = 'b'
                    key_resp_4.rt = response_clock.getTime()
                    continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    core.wait(0.01)  # short pause after instructions
    
    # --- Load and shuffle experimental trials ---
    import pandas as pd
    import random

    # Load full conditions list
    trials_conditions = data.importConditions('conditions_stress.xlsx')
    trials_df = pd.DataFrame(trials_conditions)
    
    # Extract sentence ID and condition
    trials_df['sentence_id'] = trials_df['sounds'].str.extract(r'(\d+)')[0]
    trials_df['condition'] = trials_df['sounds'].str.extract(r'\d+([a-d])')[0]

    # Create a randomized list of sentence IDs
    sentence_ids = trials_df['sentence_id'].unique().tolist()
    random.shuffle(sentence_ids)

    # Assign each to a condition (a–d), cycling evenly
    condition_map = ['a', 'b', 'c', 'd']
    assigned_trials = []
    for i, sid in enumerate(sentence_ids[:40]):  # select 40 trials
        target_cond = condition_map[i % 4]
        subset = trials_df[(trials_df['sentence_id'] == sid) & (trials_df['condition'] == target_cond)]
        if not subset.empty:
            assigned_trials.append(subset.sample(1).iloc[0])

    # Convert back to dicts
    trials_selected = pd.DataFrame(assigned_trials).sample(frac=1).to_dict(orient='records')

    # Create the randomized trial handler
    trials = data.TrialHandler2(
        name='trials',
        nReps=1,
        method='sequential',
        extraInfo=expInfo,
        originPath=-1,
        trialList=trials_selected,
        seed=0,
    )
    thisExp.addLoop(trials)
    thisTrial = trials.trialList[0]
    if thisTrial is not None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]

    # --- Setup practice trials ---
    import pandas as pd
    import random

    # Load and prepare the practice conditions
    practice_conditions = data.importConditions('conditions_stress_practice.xlsx')
    practice_df = pd.DataFrame(practice_conditions)
    practice_df['sentence_id'] = practice_df['sounds'].str.extract(r'(p\d)')[0]
    practice_df['condition'] = practice_df['sounds'].str.extract(r'p\d([a-d])')[0]

    # Define fixed practice order (one per condition)
    practice_orders = [
    [('p1', 'a'), ('p2', 'b'), ('p3', 'c'), ('p4', 'd')],
    [('p1', 'b'), ('p2', 'c'), ('p3', 'd'), ('p4', 'a')],
    [('p1', 'c'), ('p2', 'd'), ('p3', 'a'), ('p4', 'b')],
    [('p1', 'd'), ('p2', 'a'), ('p3', 'b'), ('p4', 'c')]
    ]
    selected_order = random.choice(practice_orders)

    # Select matching rows
    practice_rows = []
    for sid, cond in selected_order:
        row = practice_df[(practice_df['sentence_id'] == sid) & (practice_df['condition'] == cond)]
        if not row.empty:
            practice_rows.append(row.sample(1).iloc[0])
    practice_rows = [row.to_dict() for row in practice_rows]

    # Create the practice loop
    practice = data.TrialHandler(
        name='practice',
        trialList=practice_rows,
        nReps=1,
        method='sequential',
        extraInfo=expInfo,
        seed=0
    )
    thisExp.addLoop(practice)

    # --- Run practice loop using the test routine ---
    for thisPractice in practice:
        currentLoop = practice
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisPractice is not None:
            for paramName in thisPractice:
                globals()[paramName] = thisPractice[paramName]
            corrAns = button_mapping[thisPractice['corrAns']]
        
        test = data.Routine(
            name='test',
            components=[test_sound, key_resp_2, fixationcross],
        )
        test.status = NOT_STARTED
        continueRoutine = True
        test_sound.setSound(sounds, hamming=True)
        test_sound.setVolume(1, log=False)
        test_sound.seek(0)
        key_resp_2.keys = []
        key_resp_2.rt = []
        test.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        test.tStart = globalClock.getTime(format='float')
        test.status = STARTED
        thisExp.addData('test.started', test.tStart)
        #sent_triggers = set()  # track which triggers have been sent
        test.maxDuration = None
        testComponents = test.components
        for thisComponent in test.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1

        test.forceEnded = routineForceEnded = not continueRoutine
        
        sent_triggers = set()
        while continueRoutine:
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1

            if test_sound.status == NOT_STARTED and tThisFlip >= 1 - frameTolerance:
                test_sound.frameNStart = frameN
                test_sound.tStart = t
                test_sound.tStartRefresh = tThisFlipGlobal
                thisExp.addData('test_sound.started', tThisFlipGlobal)
                test_sound.status = STARTED
                test_sound.play(when=win)

            if test_sound.status == STARTED and test_sound.isFinished:
                test_sound.tStop = t
                test_sound.tStopRefresh = tThisFlipGlobal
                test_sound.frameNStop = frameN
                thisExp.timestampOnFlip(win, 'test_sound.stopped')
                test_sound.status = FINISHED
                test_sound.stop()

            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                key_resp_2.frameNStart = frameN
                key_resp_2.tStart = t
                key_resp_2.tStartRefresh = tThisFlipGlobal
                win.timeOnFlip(key_resp_2, 'tStartRefresh')
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                key_resp_2.status = STARTED
                win.callOnFlip(key_resp_2.clock.reset)
                win.callOnFlip(response_clock.reset)

            if key_resp_2.status == STARTED:
                buttons = joy.getAllButtons()
                if buttons[4]:  # LB
                    key_resp_2.keys = 'left'
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    key_resp_2.corr = 1 if key_resp_2.keys == corrAns else 0
                    continueRoutine = False
                elif buttons[5]:  # RB
                    key_resp_2.keys = 'right'
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    key_resp_2.corr = 1 if key_resp_2.keys == corrAns else 0
                    continueRoutine = False

            if fixationcross.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                fixationcross.frameNStart = frameN
                fixationcross.tStart = t
                fixationcross.tStartRefresh = tThisFlipGlobal
                thisExp.timestampOnFlip(win, 'fixationcross.started')
                fixationcross.status = STARTED
                fixationcross.setAutoDraw(True)

            # Send serial triggers using COM3 at the right timepoints
            trigger_schedule = [
                (ID_item, trigger_item),
                (ID_senonset, trigger_senonset),
                (ID_verbonset, trigger_verbsonset),
                (ID_1_F0, trigger_1_F0),
                (ID_suffix, trigger_suffix),
                (ID_2_F0, trigger_2_F0)
            ]

            for trig_id, trig_time in trigger_schedule:
                if t >= trig_time - frameTolerance and trig_id not in sent_triggers:
                    send_trigger(trig_id)
                    sent_triggers.add(trig_id)

            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED

            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return

            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp,
                    win=win,
                    timers=[routineTimer],
                    playbackComponents=[test_sound]
                )
                continue

            if not continueRoutine:
                test.forceEnded = routineForceEnded = True
                break
            continueRoutine = False
            for thisComponent in test.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break

            if continueRoutine:
                win.flip()

        for thisComponent in test.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test.tStop = globalClock.getTime(format='float')
        test.tStopRefresh = tThisFlipGlobal
        thisExp.addData('test.stopped', test.tStop)
        test_sound.pause()

        if key_resp_2.keys in ['', [], None]:
            key_resp_2.keys = None
            if str(corrAns).lower() == 'none':
                key_resp_2.corr = 1
            else:
                key_resp_2.corr = 0

        practice.addData('key_resp_2.keys', key_resp_2.keys)
        practice.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys is not None:
            practice.addData('key_resp_2.rt', key_resp_2.rt)

        routineTimer.reset()
        thisExp.nextEntry()

    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
                
            corrAns = button_mapping[thisTrial['corrAns']]

    # --- Show instructions again before main trials ---
    instructions = data.Routine(
        name='instructions',
        components=[instr, key_resp],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    routineTimer.reset()
    frameN = -1
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    
    sent_triggers = set()  # Track which triggers have been sent
    while continueRoutine:
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN += 1

        if instr.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            instr.frameNStart = frameN
            instr.tStart = t
            instr.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(instr, 'tStartRefresh')
            thisExp.timestampOnFlip(win, 'instr.started')
            instr.status = STARTED
            instr.setAutoDraw(True)

        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            key_resp.frameNStart = frameN
            key_resp.tStart = t
            key_resp.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(key_resp, 'tStartRefresh')
            thisExp.timestampOnFlip(win, 'key_resp.started')
            key_resp.status = STARTED
            win.callOnFlip(key_resp.clock.reset)
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')

        if key_resp.status == STARTED:
            if 'joy' in globals():
                buttons = joy.getAllButtons()
                if len(buttons) > 1 and buttons[1]:  # B button to continue
                    key_resp.keys = 'b'
                    key_resp.rt = globalClock.getTime()
                    continueRoutine = False

        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED

        if not continueRoutine:
            break

        win.flip()

    for thisComponent in [instr, key_resp]:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    thisExp.nextEntry()
    routineTimer.reset()

    core.wait(0.01)  # Optional pause before test trials

    # --- Prepare to start Routine "test" ---
    # create an object to store info about Routine test
    test = data.Routine(
        name='test',
        components=[test_sound, key_resp_2, fixationcross],
    )
    test.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    test_sound.setSound(sounds, hamming=True)
    test_sound.setVolume(1, log=False)
    test_sound.seek(0)
    # create starting attributes for key_resp_2
    key_resp_2.keys = []
    key_resp_2.rt = []

    # store start times for test
    test.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    test.tStart = globalClock.getTime(format='float')
    test.status = STARTED
    thisExp.addData('test.started', test.tStart)
    #sent_triggers = set()  # Track which triggers have been sent
    test.maxDuration = None
    # keep track of which components have finished
    testComponents = test.components
    for thisComponent in test.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
        
    # --- Run Routine "test" ---
    # if trial has changed, end Routine now
    if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
        continueRoutine = False
    test.forceEnded = routineForceEnded = not continueRoutine
    
    sent_triggers = set()
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
            
        # *test_sound* updates
            
        # if test_sound is starting this frame...
        if test_sound.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
            # keep track of start time/frame for later
            test_sound.frameNStart = frameN  # exact frame index
            test_sound.tStart = t  # local t and not account for scr refresh
            test_sound.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('test_sound.started', tThisFlipGlobal)
            # update status
            test_sound.status = STARTED
            test_sound.play(when=win)  # sync with win flip
            
        # if test_sound is stopping this frame...
        if test_sound.status == STARTED:
            if bool(False) or test_sound.isFinished:
                # keep track of stop time/frame for later
                test_sound.tStop = t  # not accounting for scr refresh
                test_sound.tStopRefresh = tThisFlipGlobal  # on global time
                test_sound.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_sound.stopped')
                # update status
                test_sound.status = FINISHED
                test_sound.stop()
            
        # *key_resp_2* updates
        waitOnFlip = False
            
        # if key_resp_2 is starting this frame...
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_2.started')
            # update status
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip:
            win.callOnFlip(response_clock.reset)
        if key_resp_2.status == STARTED:
            buttons = joy.getAllButtons()
            if buttons[4]:  # LB = left
                key_resp_2.keys = 'left'
                key_resp_2.rt = response_clock.getTime()
                key_resp_2.corr = 1 if key_resp_2.keys == corrAns else 0
                continueRoutine = False
            elif buttons[5]:  # RB = right
                key_resp_2.keys = 'right'
                key_resp_2.rt = response_clock.getTime()
                key_resp_2.corr = 1 if key_resp_2.keys == corrAns else 0
                continueRoutine = False
                    
        # *fixationcross* updates
            
        # if fixationcross is starting this frame...
        if fixationcross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fixationcross.frameNStart = frameN  # exact frame index
            fixationcross.tStart = t  # local t and not account for scr refresh
            fixationcross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixationcross, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixationcross.started')
            # update status
            fixationcross.status = STARTED
            fixationcross.setAutoDraw(True)
            
        # if fixationcross is active this frame...
        if fixationcross.status == STARTED:
            # update params
            pass

        # Send 6 serial triggers at their respective times
        trigger_schedule = [
            (ID_item, trigger_item),
            (ID_senonset, trigger_senonset),
            (ID_verbonset, trigger_verbsonset),
            (ID_1_F0, trigger_1_F0),
            (ID_suffix, trigger_suffix),
            (ID_2_F0, trigger_2_F0)
        ]

        for trig_id, trig_time in trigger_schedule:
            if t >= trig_time - frameTolerance and trig_id not in sent_triggers:
                send_trigger(trig_id)
                sent_triggers.add(trig_id)

        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[test_sound]
            )
            # skip the frame we paused on
            continue
            
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            test.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in test.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
            
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        
        # --- Ending Routine "test" ---
        for thisComponent in test.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for test
        test.tStop = globalClock.getTime(format='float')
        test.tStopRefresh = tThisFlipGlobal
        thisExp.addData('test.stopped', test.tStop)
        test_sound.pause()  # ensure sound has stopped at end of Routine
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               key_resp_2.corr = 1;  # correct non-response
            else:
               key_resp_2.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        trials.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
            
        # the Routine "test" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "takeabreak" ---
        # create an object to store info about Routine takeabreak
        takeabreak = data.Routine(
            name='takeabreak',
            components=[text_3, key_resp_4],
        )
        takeabreak.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_4
        key_resp_4.keys = []
        key_resp_4.rt = []

        # Run 'Begin Routine' code from code
        # Conditionally execute this pause routine:
        if not trials.thisN in [79, 159, 239]: # on most trials:
            continueRoutine = False # don't even start this routine
        # store start times for takeabreak
        takeabreak.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        takeabreak.tStart = globalClock.getTime(format='float')
        takeabreak.status = STARTED
        thisExp.addData('takeabreak.started', takeabreak.tStart)
        takeabreak.maxDuration = None
        # keep track of which components have finished
        takeabreakComponents = takeabreak.components
        for thisComponent in takeabreak.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "takeabreak" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        takeabreak.forceEnded = routineForceEnded = not continueRoutine
        
        sent_triggers = set()
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_3* updates
            
            # if text_3 is starting this frame...
            if text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_3.frameNStart = frameN  # exact frame index
                text_3.tStart = t  # local t and not account for scr refresh
                text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_3.started')
                # update status
                text_3.status = STARTED
                text_3.setAutoDraw(True)
            
            # if text_3 is active this frame...
            if text_3.status == STARTED:
                # update params
                pass
            
            # *key_resp_4* updates
            waitOnFlip = False
            
            # if key_resp_4 is starting this frame...
            if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_4.frameNStart = frameN  # exact frame index
                key_resp_4.tStart = t  # local t and not account for scr refresh
                key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_4.started')
                # update status
                key_resp_4.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(response_clock.reset)
            if key_resp.status == STARTED:
                if 'joy' in globals():
                    buttons = joy.getAllButtons()
                    if len(buttons) > 1 and buttons[1]:  # B button to continue
                        key_resp.keys = 'b'
                        key_resp.rt = globalClock.getTime()
                        continueRoutine = False

            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                takeabreak.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in takeabreak.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "takeabreak" ---
        for thisComponent in takeabreak.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for takeabreak
        takeabreak.tStop = globalClock.getTime(format='float')
        takeabreak.tStopRefresh = tThisFlipGlobal
        thisExp.addData('takeabreak.stopped', takeabreak.tStop)
        # check responses
        if key_resp_4.keys in ['', [], None]:  # No response was made
            key_resp_4.keys = None
        trials.addData('key_resp_4.keys',key_resp_4.keys)
        if key_resp_4.keys != None:  # we had a response
            trials.addData('key_resp_4.rt', key_resp_4.rt)
        # the Routine "takeabreak" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Thanks" ---
    # create an object to store info about Routine Thanks
    Thanks = data.Routine(
        name='Thanks',
        components=[text_2],
    )
    Thanks.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for Thanks
    Thanks.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Thanks.tStart = globalClock.getTime(format='float')
    Thanks.status = STARTED
    thisExp.addData('Thanks.started', Thanks.tStart)
    Thanks.maxDuration = None
    # keep track of which components have finished
    ThanksComponents = Thanks.components
    for thisComponent in Thanks.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Thanks" ---
    Thanks.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            pass
        
        # if text_2 is stopping this frame...
        if text_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_2.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                text_2.tStop = t  # not accounting for scr refresh
                text_2.tStopRefresh = tThisFlipGlobal  # on global time
                text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_2.stopped')
                # update status
                text_2.status = FINISHED
                text_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Thanks.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Thanks.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Thanks" ---
    for thisComponent in Thanks.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Thanks
    Thanks.tStop = globalClock.getTime(format='float')
    Thanks.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Thanks.stopped', Thanks.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if Thanks.maxDurationReached:
        routineTimer.addTime(-Thanks.maxDuration)
    elif Thanks.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    
    # Determine correct answer mapping based on selected version
    if expInfo['version'] == '1':
        button_mapping = {'num_1': 'left', 'num_2': 'right'}
    else:
        button_mapping = {'num_1': 'right', 'num_2': 'left'}

    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)

    # Initialize joystick
    joystick.backend = 'pyglet'
    nJoysticks = joystick.getNumJoysticks()
    if nJoysticks > 0:
        globals()['joy'] = joystick.Joystick(0)
        print("Controller connected:", joy.getName())
    else:
        raise RuntimeError("No joystick/gamepad detected!")

    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    
    # --- Reset TriggerBox and close serial port ---
    port.write([0xFF])
    time.sleep(PulseWidth)

    Connected = False
    thread.join(1.0)
    port.close()
    
    quit(thisExp=thisExp, win=win)
