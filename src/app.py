from entities.reading_tip import ReadingTip

class App:
    def __init__(self, reading_tip_service, io, tags_service):
        self.io = io
        self.reading_tip_service = reading_tip_service
        self.tags_service = tags_service

        # Initialize (command id -> command handler) map.
        self.commands = {
            1: self.add_reading_tip,
            2: self.modify_reading_tip,
            3: self.delete_reading_tip,
            4: self.see_all_reading_tips,
            5: self.search_reading_tips_by_title,
            6: self.exit_app,
            7: self.add_tag,
            8: self.see_all_tags
        }

    def add_reading_tip(self):
        title = self.io.read("Give reading tip title: ")
        link = self.io.read("Give reading tip a link: ")
        self.reading_tip_service.create(title, link=link)
        self.io.write("New Reading Tip added!")

    def add_tag(self):
        new_tag = self.io.read("Give new tag: ")
        self.tags_service.create_tag(new_tag)
        self.io.write("New tag added")

    def modify_reading_tip(self):
        tip_id = self.io.read("Which reading tip you want to modify? Please give id: \n")
        reading_tip = self.reading_tip_service.get_by_id(tip_id)

        if reading_tip is None:
            self.io.writeline(f"Reading tip with id {tip_id} was not found.")
        else:
            self.print_reading_tip(reading_tip)
            new_title = self.io.read("Enter new title: \n")

            reading_tip.title = new_title
            self.reading_tip_service.update(reading_tip)
            self.io.write("Modification done successfully.")

    def delete_reading_tip(self):
        try:
            tip_id = int(self.io.read("Which reading tip you want to delete? Please give id: "))
        except:
            self.io.write("Invalid reading tip id")
        self.reading_tip_service.delete(tip_id)

    def see_all_reading_tips(self):
        all_tips = self.reading_tip_service.get_all()
        if all_tips:
            self.print_list_of_tips(all_tips)

    def see_all_tags(self):
        all_tags = self.tags_service.get_all_tags()
        if all_tags:
            self.print_list_of_tags(all_tags)

    def search_reading_tips_by_title(self):
        title = self.io.read("Enter title to search for: ")
        tips = self.reading_tip_service.search_by_title(title)
        if tips:
            self.print_list_of_tips(tips)
        else:
            self.io.write(f"No reading tips found for title query \"{title}\".")

    def exit_app(self):
        # Raise exit exception.
        # This will stop execution of the app and is not caught by the default exception handler.
        raise SystemExit()

    def print_list_of_tips(self, tips):
        self.io.write(f"{len(tips)} reading tips found:")
        for tip in tips:
            self.print_reading_tip(tip)

    def print_list_of_tags(self, tags):
        self.io.write(f"{len(tags)} tags found:")
        for tag in tags:
            self.print_tags(str(tag))

    def print_tags(self, tags):
        self.io.write(tags)

    def print_reading_tip(self, tip: ReadingTip):
        self.io.write(tip.format())

    def print_all_operations(self):
        self.io.write("Choose from the following operations:")
        self.io.write(" 1. Add a Reading Tip")
        self.io.write(" 2. Modify a Reading Tip")
        self.io.write(" 3. Delete a Reading Tip")
        self.io.write(" 4. See all Reading Tips")
        self.io.write(" 5. Search Reading Tips by title")
        self.io.write(" 6. Exit software")
        self.io.write(" 7. Add new tag")
        self.io.write(" 8. See all tags")

    def run(self):
        self.io.write("Welcome to Reading Tip software!")
        self.print_all_operations()

        while True:
            command = self.io.read("Select the operation you want to run (numbers only): \n")
            try:
                command_id = int(command.strip())

                # Attempt to lookup a matching command handler by the given id
                command_handler = self.commands.get(command_id)

                # If the corresponding command handler was found, call it.
                # If not; write an error message.
                if command_handler:
                    command_handler()
                else:
                    self.io.write(f"No operation found for given number \"{command_id}\"!")
                    self.print_all_operations()

            except Exception as error:
                # This exception handler is a catch-all for all of the command handlers.
                # If the command handler does not have own exception handling,
                # this exception block handles it by simply printing the error to user.
                self.io.write(str(error))
            except SystemExit:
                break
