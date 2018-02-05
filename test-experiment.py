import expyriment

exp = expyriment.design.Experiment(name="First Experiment")
expyriment.control.initialize(exp)

block = expyriment.design.Block(name="A name for the block")
trial = expyriment.design.Trial()

stim = expyriment.stimuli.Picture("img-sources/icons8-android-os.png")
stim.preload()
trial.add_stimulus(stim)

stim = expyriment.stimuli.Picture("img-sources/icons8-android-tablet.png")
stim.preload()
trial.add_stimulus(stim)

stim = expyriment.stimuli.Picture("img-sources/icons8-app-windows.png")
stim.preload()
trial.add_stimulus(stim)

block.add_trial(trial)
exp.add_block(block)

exp.data_variable_names = ["Block", "Trial", "Key", "RT"]
expyriment.control.set_develop_mode(True)
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        for stim in trial.stimuli:
            stim.present()
            key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                         expyriment.misc.constants.K_RIGHT])
            exp.data.add([block.name, trial.id, key, rt])

expyriment.control.end()
