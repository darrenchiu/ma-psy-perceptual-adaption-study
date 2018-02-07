import expyriment
import random

exp = expyriment.design.Experiment(name="First Experiment")
expyriment.control.initialize(exp)

block = expyriment.design.Block(name="A name for the block")
trial = expyriment.design.Trial()

for i in range(1, 101):
    stim = expyriment.stimuli.TextLine(text=str(i))
    stim.preload()
    trial.add_stimulus(stim)

block.add_trial(trial)
exp.add_block(block)

exp.data_variable_names = ["Block", "Trial", "Key", "RT"]
expyriment.control.set_develop_mode(True)
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        current_number = random.randint(0, 100)
        reverse_count = 0
        last_action = 0
        lower_bound = 0
        upper_bound = 100

        while reverse_count < 12:
            trial.stimuli[current_number].present()
            key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                         expyriment.misc.constants.K_RIGHT])
            exp.data.add([block.name, trial.id, key, rt])

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
