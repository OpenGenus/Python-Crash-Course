from collections import namedtuple

import rx
from rx.core import Observable
from rx.subject import BehaviorSubject
from rx.operators import do_action, map


Time = namedtuple("Time", ["minutes", "seconds"])


class CountDownTimer:
    def __init__(self, duration: Time) -> None:
        self._minutes = min(duration.minutes, 59)
        self._remaining_minutes = self._minutes

        self._seconds = min(duration.seconds, 59)
        self._remaining_seconds = self._seconds + 1

        self._tick_size = 1

        self.depleted = BehaviorSubject(False)

    @property
    def time_remaining(self) -> Observable:

        return rx.timer(0.0, period=1).pipe(
            do_action(lambda _, this=self: this._tick()),
            map(lambda _, this=self: Time(this._remaining_minutes, this._remaining_seconds))
        )

    def _tick(self) -> None:
        is_time_depleted = self.depleted.value
        if not is_time_depleted:
            if self._remaining_minutes == 0 and self._remaining_seconds == 0:
                self.depleted.on_next(True)
                return

            if self._remaining_seconds == 0:  # A minute is complete
                self._remaining_minutes -= 1
                self._remaining_seconds = 60  # Reset the remaining seconds 
            self._remaining_seconds -= self._tick_size

    def pause(self) -> None:
        self._tick_size = 0

    def resume(self) -> None:
        self._tick_size = 1
