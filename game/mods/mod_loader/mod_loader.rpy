python early:
    mods_loaded = False
    skipping_main_menu = True
    lockout_main_menu = False

init python:
    if not mods_loaded:
        config.label_overrides["splashscreen"]="mod_loader_start"

init:
    if not mods_loaded:

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


screen mod_loader():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Mods"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Mods")
