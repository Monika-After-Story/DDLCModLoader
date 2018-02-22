init python:
    register_mod(
        mod_name="DDLC Mod Template",
        major=True,
        prefix="template",
        label_overrides={"splashscreen":"template_splash"},
        dependencies=None,
        config_settings={
            "config.name":"DDLC Mod Template",
            "build.name":"DDLCModTemplate",
            "config.version":"2.0.0",
            "config.save_directory":"DDLC_Mod_Template"
            }
        )

init:
    if mod_major == "DDLC Mod Template":

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
