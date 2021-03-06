#The mod loader allows multiple DDLC mods to be installed simultaneously
#It adds a store called `loader` with a number of functions and variables
#It also adds the mod_loader() menu screen, which can be added to navigation


#Create a store for mod_loader specific variables and functions
#This has to be in an early block to be accessible to the next section
python early in loader:
    lockout_main_menu = False
    skipping_main_menu = True
    mods_list = {}
    mod_major = "Doki Doki Literature Club (Base Game)"
    mods_loaded = []
    next_major = None
    restart_prompt_seen = False

    def register_mod(mod_name, major, prefix, label_overrides = None,dependencies = None,config_settings=None):
        mods_list[mod_name] = {}

        mods_list[mod_name]["loaded"]=False
        mods_list[mod_name]["major"]=major

        #Major mod specific fields
        if major and label_overrides:
            mods_list[mod_name]["label_overrides"]=label_overrides
        else:
            mods_list[mod_name]["label_overrides"]=None

        if major and config_settings:
            mods_list[mod_name]["config_settings"]=config_settings
        else:
            mods_list[mod_name]["config_settings"]=None

        #Minor mod specific fields
        if not major and dependencies:
            mods_list[mod_name]["dependencies"]=dependencies
        else:
            mods_list[mod_name]["dependencies"]=None

        return

    def is_loaded(mod_name):
        return mod_name in mods_loaded

    def is_installed(mod_name):
        return mod_name in mods_list

#This section checks to see if mods are to be loaded
#We then set specific configuration variables that need to be set in an early block
python early:
    #Load the multi-game persistent for DDLC Mods
    mpersistent = MultiPersistent("ddlc_mods")

    if mpersistent._loader_major:
        loader.mod_major = mpersistent._loader_major
        loader.mods_loaded = [mpersistent._loader_major]
    else:
        loader.mods_loaded = ["Doki Doki Literature Club (Base Game)"]

    if mpersistent._loader_load_mods:
        loader.mods_loaded = mpersistent._loader_load_mods

    loader.next_major = loader.mod_major

    def loader_update_next_load():

        temp_load_mods = []
        for key in loader.mods_list:
            if loader.mods_list[key]["loaded"] and not loader.mods_list[key]["major"]:
                temp_load_mods.append(key)

        mpersistent._loader_major=loader.next_major
        mpersistent._loader_major_settings=loader.mods_list[loader.next_major]
        mpersistent._loader_load_mods=temp_load_mods

        mpersistent.save()

        return


#The mod loader screen is a settings page which can be added to the main menu of
#any mod.
screen mod_loader():

    style_prefix "loader"
    tag menu

    if renpy.mobile:
        $ cols = 1
    else:
        $ cols = 1

    use game_menu(_("Mods"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:
                    style_prefix "loader_radio"
                    label _("Major Mods")
                    for key in loader.mods_list:
                        if loader.mods_list[key]["major"]:
                            textbutton _(key) action [SetField(loader,"next_major",key), Function(loader_update_next_load), If(not loader.restart_prompt_seen, Show("dialog",transition=None,message="The game must be restarted for changes to take effect.",ok_action=[Hide("dialog"), SetField(loader,"restart_prompt_seen",True)]))]

                vbox:
                    style_prefix "loader_check"
                    label _("Minor Mods")
                    for key in loader.mods_list:
                        if not loader.mods_list[key]["major"]:
                            textbutton _(key) action [ToggleDict(loader.mods_list[key],"loaded"), Function(loader_update_next_load), If(not loader.restart_prompt_seen, Show("dialog",transition=None,message="The game must be restarted for changes to take effect.",ok_action=[Hide("dialog"), SetField(loader,"restart_prompt_seen",True)]))]

style loader_vbox:
    xsize 500

style loader_radio is radio
style loader_check is check
style loader_radio_vbox is loader_vbox
style loader_check_vbox is loader_vbox

#This section defines the base DDLC game as if it were a major mod
#The mod launcher uses this so that mods can be loaded in the base game
init python:
    loader.register_mod("Doki Doki Literature Club (Base Game)",True,"")

    if loader.is_loaded("Doki Doki Literature Club (Base Game)"):
        config.label_overrides["splashscreen"]="mod_loader_start"

#If you're running the base game, we need to add the mods pane to settings
init:
    if loader.is_loaded("Doki Doki Literature Club (Base Game)"):

        screen navigation():

            vbox:
                style_prefix "navigation"

                xpos gui.navigation_xpos
                yalign 0.8

                spacing gui.navigation_spacing

                if not persistent.autoload or not main_menu:

                    if main_menu:

                        if persistent.playthrough == 1:
                            textbutton _("ŔŗñĮ¼»ŧþŀÂŻŕěōì«") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))
                        else:
                            textbutton _("New Game") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))

                    else:

                        textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None and not loader.lockout_main_menu)]

                        textbutton _("Save Game") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None and not loader.lockout_main_menu)]

                    textbutton _("Load Game") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None and not loader.lockout_main_menu)]

                    if _in_replay:

                        textbutton _("End Replay") action EndReplay(confirm=True)

                    elif not main_menu:
                        if persistent.playthrough != 3:
                            textbutton _("Main Menu") action [MainMenu(), SensitiveIf(not loader.lockout_main_menu)]
                        else:
                            textbutton _("Main Menu") action NullAction()

                    textbutton _("Mods") action [ShowMenu("mod_loader"), SensitiveIf(renpy.get_screen("mod_loader") == None)]

                    textbutton _("Settings") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None and not loader.lockout_main_menu)]

                    #textbutton _("About") action ShowMenu("about")

                    if renpy.variant("pc"):

                        ## Help isn't necessary or relevant to mobile devices.
                        textbutton _("Help") action Help("README.html")

                        ## The quit button is banned on iOS and unnecessary on Android.
                        textbutton _("Quit") action Quit(confirm=not main_menu)
                else:
                    timer 1.75 action Start("autoload_yurikill")

#This logic needs to run when the game starts, so mods can be loaded even if the
#player never reaches the main menu.
label mod_loader_start:
    if loader.skipping_main_menu:
        call screen confirm("Would you like to load a mod?", Return(True), Return(False))

        if _return:
            $loader.lockout_main_menu = True
            call screen mod_loader
            $loader.lockout_main_menu = False


    $config.label_overrides["splashscreen"]="splashscreen"
    jump splashscreen
