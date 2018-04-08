import expyriment

# Constants
BLANK = 0
RESPOND = 101
INSTRUCTION_FOR_DECISION = 102
INSTRUCTION_FOR_PRIMING = 103
INSTRUCTION_FOR_RESPONSE = 104
INSTRUCTION_FOR_START_PRIMING = 105
INSTRUCTION_FOR_START_EXPERIEMENT = 106

STEP = 5
# priming time should be 180000 (3 mins)
PRIMING_TIME = 5000


def PrepareTrial(emotion_pair, set, left_emotion, right_emotion):
    trial = expyriment.design.Trial()
    blank_screen = expyriment.stimuli.BlankScreen()
    blank_screen.preload()
    trial.add_stimulus(blank_screen)
    for i in range(1, 101):
        stim = expyriment.stimuli.Picture(
            'img-sources/{0}/set{1}/set{2}{3}.png'.format(emotion_pair, set, set, format(i, '03')))
        stim.preload()
        trial.add_stimulus(stim)
    respond_screen = expyriment.stimuli.TextLine('Respond')
    respond_screen.preload()
    trial.add_stimulus(respond_screen)

    instruction_screen = expyriment.stimuli.TextBox(
        'When prompted to response, press <Left> key for {0}, press <Right> key for {1}.\n\n Press <Enter> Key to continue.'.format(
            left_emotion, right_emotion), (1000, 500))
    instruction_screen.preload()
    trial.add_stimulus(instruction_screen)

    priming_instruction_screen = expyriment.stimuli.TextBox(
        'Before the experiement, we will first show you a face for 3 minutes. \n\nPress <Enter> Key to continue.',
        (1000, 500))
    priming_instruction_screen.preload()
    trial.add_stimulus(priming_instruction_screen)

    response_instruction_screen = expyriment.stimuli.TextBox(
        'Before each trial, we will show you a face for 5 seconds before flashing you the face that you need to '
        'respond.\n\nYour response should be based on the FLASHING FACE.\n\nWhen you are ready to start, '
        'press <Enter> Key.',
        (1000, 500))
    response_instruction_screen.preload()
    trial.add_stimulus(response_instruction_screen)

    start_priming_screen = expyriment.stimuli.TextBox(
        'Now we will show you a face for 3 minutes.\n\nPlease focus on it.\n\nWhen ready, press <Enter> key.',
        (1000, 500))
    start_priming_screen.preload()
    trial.add_stimulus(start_priming_screen)

    start_experiment_screen = expyriment.stimuli.TextBox('Now experiment starts.\n\nWhen ready, press <Enter> key.',
                                                         (1000, 500))
    start_experiment_screen.preload()
    trial.add_stimulus(start_experiment_screen)

    return trial


def PerformExperimentTrial(block_idx, trial, condition_id):
    # show instruction
    trial.stimuli[INSTRUCTION_FOR_DECISION].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    trial.stimuli[INSTRUCTION_FOR_PRIMING].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    trial.stimuli[INSTRUCTION_FOR_RESPONSE].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    trial.stimuli[INSTRUCTION_FOR_START_PRIMING].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    # adaption
    trial.stimuli[condition_id].present()
    exp.clock.wait(PRIMING_TIME)

    trial.stimuli[INSTRUCTION_FOR_START_EXPERIEMENT].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    current_number = 50
    reverse_count = 0
    last_action = 0
    while reverse_count < 14:

        trial.stimuli[condition_id].present()
        exp.clock.wait(5000)
        trial.stimuli[0].present()
        exp.clock.wait(250)

        trial.stimuli[current_number].present()
        exp.clock.wait(500)
        trial.stimuli[RESPOND].present()

        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                     expyriment.misc.constants.K_RIGHT])
        exp.data.add(
            [block_idx, trial.id, 'L' if key == expyriment.misc.constants.K_LEFT else 'R', rt, current_number])

        if last_action != key:
            last_action = key
            reverse_count += 1
            exp.data.add([block.name, trial.id, key, rt, 'R {0}'.format(current_number)])

        if key == expyriment.misc.constants.K_LEFT:
            current_number = current_number + STEP
        elif key == expyriment.misc.constants.K_RIGHT:
            current_number = current_number - STEP

        if current_number < 1:
            current_number = 1
        elif current_number > 100:
            current_number = 100


def PerformControlTrial(block_idx, trial):
    # show instruction
    trial.stimuli[INSTRUCTION_FOR_DECISION].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    current_number = 50
    reverse_count = 0
    last_action = 0

    while reverse_count < 14:
        trial.stimuli[current_number].present()
        exp.clock.wait(500)
        trial.stimuli[RESPOND].present()

        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                     expyriment.misc.constants.K_RIGHT])
        exp.data.add(
            [block_idx, trial.id, 'L' if key == expyriment.misc.constants.K_LEFT else 'R', rt, current_number])

        if last_action != key:
            last_action = key
            reverse_count += 1
            exp.data.add([block.name, trial.id, key, rt, 'R {0}'.format(current_number)])

        if key == expyriment.misc.constants.K_LEFT:
            current_number = current_number + STEP
        elif key == expyriment.misc.constants.K_RIGHT:
            current_number = current_number - STEP

        if current_number < 1:
            current_number = 1
        elif current_number > 100:
            current_number = 100


# Main Program
exp = expyriment.design.Experiment(name="Visual Perception Experiement")
expyriment.control.initialize(exp)

block = expyriment.design.Block(name="A name for the block")

block.add_trial(PrepareTrial("HA-AN", 2, "HAPPY", "ANGRY"))
block.add_trial(PrepareTrial("DI-SU", 2, "DISGUST", "SURPRISED"))
exp.add_block(block)

exp.data_variable_names = ["Block", "Trial", "Key", "RT", "Current"]
expyriment.control.set_develop_mode(True)
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        PerformControlTrial(1, trial)

for block in exp.blocks:
    for trial in block.trials:
        PerformExperimentTrial(2, trial, 1)
        PerformExperimentTrial(3, trial, 100)

expyriment.control.end()
