from sgtk.platform import Application
import sgtk
import sys
import os
logger = sgtk.platform.get_logger(__name__)

class CFALoaderApp(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """
    
    def init_app(self):
        if not self.engine.has_ui:
            logger.debug("CFA Loader App---")
            return
        app_payload = self.import_module("app")

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # first, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app
        menu_callback = lambda : app_payload.dialog.show_dialog(self)

        menu_caption = "%s..." % self.get_setting("menu_name")
        menu_options = {
            "short_name": self.get_setting("menu_name").replace(" ", "_"),

            # dark themed icon for engines that recognize this format
            "icons": {
                "dark": {
                    "png": os.path.join(
                        os.path.dirname(__file__),
                        "resources",
                        "sg_logo.png",
                    ),
                }
            }
        }

        # now register the command with the engine
        self.engine.register_command(menu_caption, menu_callback,menu_options)
        
