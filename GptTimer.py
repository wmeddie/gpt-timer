import rumps
import threading
from datetime import datetime, timedelta


class CounterApp(rumps.App):
    def __init__(self):
        super(CounterApp, self).__init__("Counter")
        self.counter = 25
        self.timer = None
        self.counter_menu_item = rumps.MenuItem(f"Remaining: {self.counter}", callback=None)
        self.menu = [self.counter_menu_item]
        self.timer_end = datetime.now() + timedelta(hours=3, minutes=1)
        self.update_timer()

    @rumps.clicked("Decrement Counter")
    def decrement_counter(self, _):
        if self.counter > 0:
            self.counter -= 1
            self.counter_menu_item.title = f"Remaining: {self.counter}"
            self.update_timer()

    @rumps.clicked("Reset Timer")
    def reset_timer(self, _):
        self.counter = 25
        self.counter_menu_item.title = f"Remaining: {self.counter}"
        self.timer_end = datetime.now() + timedelta(hours=3, minutes=1)
        self.update_timer()

    def update_timer(self):
        # Keep timer at 3 hours if counter is still 25.
        if self.counter == 25:
            self.timer_end = datetime.now() + timedelta(hours=3, minutes=1)

        time_remaining = self.timer_end - datetime.now()
        if time_remaining <= timedelta():
            self.reset_timer()
            time_remaining = self.timer_end - datetime.now()

        minutes, seconds = divmod(time_remaining.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.title = f"{self.counter} ({hours:02d}:{minutes:02d})"
        self.counter_menu_item.title = f"Remaining: {self.counter}"

        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        self.timer = threading.Timer(60, self.update_timer).start()


if __name__ == "__main__":
    CounterApp().run()


