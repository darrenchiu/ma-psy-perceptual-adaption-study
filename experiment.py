import expyriment
import random

# Constants
BLANK = 0
RESPOND = 101
# control condition
CONDITION = 1

exp = expyriment.design.Experiment(name="Experiment - Condition: " + str(CONDITION))
expyriment.control.initialize(exp)

block = expyriment.design.Block(name="A name for the block")
trial = expyriment.design.Trial()

blank_screen = expyriment.stimuli.BlankScreen()
blank_screen.preload()
trial.add_stimulus(blank_screen)

for i in range(1, 101):
    stim = expyriment.stimuli.Picture('img-sources/HA-AN/set1/set1' + format(i, '03') + '.png')
    stim.preload()
    trial.add_stimulus(stim)

respond_screen = expyriment.stimuli.TextLine('Respond')
respond_screen.preload()
trial.add_stimulus(respond_screen)

block.add_trial(trial)
exp.add_block(block)

exp.data_variable_names = ["Block", "Trial", "Key", "RT", "Current"]
expyriment.control.set_develop_mode(True)
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        # adaption
        trial.stimuli[CONDITION].present()
        exp.clock.wait(180000)

        current_number = random.randint(1, 100)
        reverse_count = 0
        last_action = 0
        lower_bound = 0
        upper_bound = 100

        while reverse_count < 12 and upper_bound != lower_bound:
            if reverse_count != 0:
                trial.stimuli[CONDITION].present()
                exp.clock.wait(5000)
                trial.stimuli[0].present()
                exp.clock.wait(250)

            trial.stimuli[current_number].present()
            exp.clock.wait(500)
            # stimuli is always blank screen
            trial.stimuli[RESPOND].present()

            key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                         expyriment.misc.constants.K_RIGHT])
            exp.data.add([block.name, trial.id, key, rt, current_number])

            if key == expyriment.misc.constants.K_LEFT:
                step = random.randint(0, upper_bound - current_number)
                lower_bound = current_number
                current_number = current_number + step
            elif key == expyriment.misc.constants.K_RIGHT:
                step = random.randint(0, current_number - lower_bound)
                upper_bound = current_number
                current_number = current_number - step

            if last_action != key:
                last_action = key
                reverse_count += 1


expyriment.control.end()
