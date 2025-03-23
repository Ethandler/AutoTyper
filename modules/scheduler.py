"""
modules/scheduler.py
Scheduling for typing: seconds, minutes, or specific HH:MM time.
Requires: pip install schedule
"""

import schedule
import time
import threading

_scheduler_thread = None
_stop_scheduler = False

def schedule_typing_in_delay(delay_seconds, callback):
    """
    Schedule typing after X seconds.
    """
    schedule.clear('typing-job')
    schedule.every(delay_seconds).seconds.do(_run_once, callback).tag('typing-job')
    _start_schedule_thread()

def schedule_typing_in_minutes(minutes, callback):
    """
    Schedule typing after X minutes.
    """
    schedule.clear('typing-job')
    schedule.every(minutes).minutes.do(_run_once, callback).tag('typing-job')
    _start_schedule_thread()

def schedule_typing_at_specific_time(target_time, callback):
    """
    Schedule typing daily at a specific time (HH:MM, 24-hour format).
    """
    schedule.clear('typing-job')
    schedule.every().day.at(target_time).do(_run_once, callback).tag('typing-job')
    _start_schedule_thread()

def stop_all_schedules():
    """
    Stop all scheduled tasks.
    """
    global _stop_scheduler
    _stop_scheduler = True
    schedule.clear()

def _run_once(callback):
    """
    Run the callback once, then clear the schedule.
    """
    schedule.clear('typing-job')
    callback()

def _start_schedule_thread():
    """
    Start the schedule loop in a background thread if not already running.
    """
    global _scheduler_thread, _stop_scheduler
    _stop_scheduler = False

    if _scheduler_thread is None or not _scheduler_thread.is_alive():
        _scheduler_thread = threading.Thread(target=_run_schedule_loop, daemon=True)
        _scheduler_thread.start()

def _run_schedule_loop():
    """
    Continuously runs schedule.run_pending() until _stop_scheduler is True.
    """
    global _stop_scheduler
    while not _stop_scheduler:
        schedule.run_pending()
        time.sleep(1)
