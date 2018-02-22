python early:
    skipping_main_menu = True
    lockout_main_menu = False

    mods_list = {}
    mpersistent = MultiPersistent("ddlc_mods")

    if mpersistent._loader_major:
        mod_major = mpersistent._loader_major
    else:
        mod_major= "Doki Doki Literature Club (Base Game)"

    if mpersistent._loader_load_mods:
        mods_loaded = mpersistent._loader_load_mods
    else:
        mods_loaded = ["Doki Doki Literature Club (Base Game)"]

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



init python:
    register_mod("Doki Doki Literature Club (Base Game)",True,"")

    if mod_major == "Doki Doki Literature Club (Base Game)":
        config.label_overrides["splashscreen"]="mod_loader_start"
        config.label_overrides["quit"]="mod_loader_quit"

init:
    if mod_major =="Doki Doki Literature Club (Base Game)":

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

                        textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None and not lockout_main_menu)]

                        textbutton _("Save Game") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None and not lockout_main_menu)]

                    textbutton _("Load Game") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None and not lockout_main_menu)]

                    if _in_replay:

                        textbutton _("End Replay") action EndReplay(confirm=True)

                    elif not main_menu:
                        if persistent.playthrough != 3:
                            textbutton _("Main Menu") action [MainMenu(), SensitiveIf(not lockout_main_menu)]
                        else:
                            textbutton _("Main Menu") action NullAction()

                    textbutton _("Mods") action [ShowMenu("mod_loader"), SensitiveIf(renpy.get_screen("mod_loader") == None)]

                    textbutton _("Settings") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None and not lockout_main_menu)]

                    #textbutton _("About") action ShowMenu("about")

                    if renpy.variant("pc"):

                        ## Help isn't necessary or relevant to mobile devices.
                        textbutton _("Help") action Help("README.html")

                        ## The quit button is banned on iOS and unnecessary on Android.
                        textbutton _("Quit") action Quit(confirm=not main_menu)
                else:
                    timer 1.75 action Start("autoload_yurikill")


label mod_loader_start:
    if skipping_main_menu:
        call screen confirm("Would you like to load a mod?", Return(True), Return(False))

        if _return:
            $lockout_main_menu = True
            call screen mod_loader
            $lockout_main_menu = False


    $config.label_overrides["splashscreen"]="splashscreen"
    jump splashscreen

label mod_loader_quit:
    python:
        load_mods = []
        for key in mods_list:
            if mods_list[key]["loaded"]:
                load_mods.append(key)
        load_mods.append(mod_major)

        mpersistent._loader_major=mod_major
        mpersistent._loader_major_settings=mods_list[mod_major]
        mpersistent._loader_load_mods=load_mods

        mpersistent.save()

    $config.label_overrides["quit"]="quit"
    jump quit

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
                    style_prefix "radio"
                    label _("Major Mods")
                    for key in mods_list:
                        if mods_list[key]["major"]:
                            textbutton _(key) action SetVariable("mod_major",key)

                vbox:
                    style_prefix "check"
                    label _("Minor Mods")
                    for key in mods_list:
                        if not mods_list[key]["major"]:
                            textbutton _(key) action ToggleDict(mods_list[key],"loaded")

style loader_vbox:
    xsize 500

style radio_vbox is loader_vbox
style check_vbox is loader_vbox
