import expyriment
import random

# Constants
BLANK = 0
RESPOND = 101
INSTRUCTION = 102
# control condition
CONDITION = 1
STEP = 5
# priming time should be 180000 (3 mins)
PRIMING_TIME = 10


def PrepareTrial(emotion_pair, set, left_emotion, right_emotion):
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

    instruction_screen = expyriment.stimuli.TextLine(
        'When prompted to response, press <Left> key for {0}, press <Right> key for {1}. When ready, press <Enter> key.'.format(
            left_emotion, right_emotion))
    instruction_screen.preload()
    trial.add_stimulus(instruction_screen)
    return trial


def PerformExperimentTrial(block_idx, trial):
    # show instruction
    trial.stimuli[INSTRUCTION].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    # adaption
    trial.stimuli[CONDITION].present()
    exp.clock.wait(PRIMING_TIME)
    current_number = 50
    reverse_count = 0
    last_action = 0
    while reverse_count < 12:
        if reverse_count != 0:
            trial.stimuli[CONDITION].present()
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
            exp.data.add([block_idx, trial.id, key, rt, 'R {0}'.format(current_number)])

        if key == expyriment.misc.constants.K_LEFT:
            current_number = current_number + STEP
        elif key == expyriment.misc.constants.K_RIGHT:
            current_number = current_number - STEP


def PerformControlTrial(block_idx, trial):
    # show instruction
    trial.stimuli[INSTRUCTION].present()
    exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

    current_number = 50
    reverse_count = 0
    last_action = 0

    while reverse_count < 12:
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


# Main Program
exp = expyriment.design.Experiment(name="Experiment - Condition: " + str(CONDITION))
expyriment.control.initialize(exp)

block = expyriment.design.Block(name="A name for the block")
trial = expyriment.design.Trial()

PrepareTrial("HA-AN", 1, "HAPPY", "ANGRY")

block.add_trial(trial)
exp.add_block(block)

exp.data_variable_names = ["Block", "Trial", "Key", "RT", "Current"]
expyriment.control.set_develop_mode(True)
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        PerformControlTrial(1, trial)

for block in exp.blocks:
    for trial in block.trials:
        PerformExperimentTrial(2, trial)


expyriment.control.end()
