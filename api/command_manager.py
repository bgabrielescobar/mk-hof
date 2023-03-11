from api.game.farm import Farm
from api.game.create import Create
#from api.game.world_boss import uwb
from api.game.profile import Profile
from api.game.pvp import PVP

class CommandManager:

    filtered_author = ''
    func_command = ''
    message = ''


    def command_selector(self, message):
 
        func_command = message.content.split()[0][1:]

        func_command = func_command.lower()

        self.filtered_author = str(message.author)
        self.message = message
        self.func_command = func_command

        return self.run()
    
    def emoji_selector(self, func_command_param, user):
        self.filtered_author = user
        self.func_command = func_command_param[0]
        self.extra_param = func_command_param[1]
        return self.run()

    def run(self):
        try:
            function_call = eval('self.' + self.func_command)
        except NameError:
            print(f"Function '{self.func_command}' not defined.")
        else:
            if callable(function_call):
                return function_call()
            else:
                print(f"'{self.func_command}' is not a function.")

        return ["", self.func_command]     

    def farm(self):
        return [Farm().start(self.filtered_author, self.message.channel.name.split('-')[1]), self.func_command]

    def create(self):
        return [Create().get_classes(self.filtered_author), self.func_command]
    
    def create_class(self):
        return Create().create_user(self.filtered_author, self.extra_param)

    def profile(self):
        return [Profile().get_user_stats(self.filtered_author), self.func_command]

    def shop(self):
        return ['assets/ui/shop.png', self.func_command]

    def pvp(self):
        return [PVP(self.filtered_author, self.message.content.split("pvp")[1][1:]).start(), self.func_command]
    
    def raid(self):
        return [uwb.farm_wb(self.filtered_author, self.message.content.split()[1]), self.func_command]