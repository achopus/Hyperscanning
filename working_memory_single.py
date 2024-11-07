import os
import csv
from psychopy import core, visual, event
import numpy as np
import matplotlib.pyplot as plt
import time

class WorkingMemory(object):
    def __init__(self, n_trials: int = 120, pause: int = 30, pause_time: int = 15,
                 save_folder: str = "out", filename: str = "default_filename") -> None:

        # Experiment design
        self.n_trials = n_trials
        self.pause = pause
        self.pause_time = pause_time
        
        # Data handling
        self.save_folder = save_folder
        self.filename = filename
        
        # Generate the random sequence
        self.show_numbers, self.differences = self._generate_number_sequence(n_trials)
        
        # Initialize windows
        self.window_A = visual.Window(size=(800, 600), pos=(0, 0), color='black')
        
        self.time_log_A = []
        
        self._show_init_prompt()
    
    def _show_init_prompt(self) -> None:
        text_A = visual.TextStim(win=self.window_A, text="Calculate the result and enter the corresponding number [0-9]", color="white")
        text_A.draw()
        self.window_A.flip()
        core.wait(5)
    
    def _generate_number_sequence(self, n_trials: int) -> tuple[list[int], list[int]]:
        show_numbers: list[int] = []
        differences: list[int] = []
        np.random.seed(0)
        for _ in range(n_trials):
            N = np.random.randint(0, 10)
            D = np.random.randint(-N, 9-N)
            show_numbers.append(N)
            differences.append(D)
        return show_numbers, differences    
    
    def _show_text(self, i: int, N: int, D: int) -> None:
        text = visual.TextStim(win=self.window_A, text=f"{N}", color="yellow")
        text.draw()
        self.window_A.flip()
        core.wait(0.75)
        text = visual.TextStim(win=self.window_A, text=f"", color="yellow")
        text.draw()
        self.window_A.flip()
        core.wait(0.25)
        text = visual.TextStim(win=self.window_A, text=f"{D:+d}", color="white")
        text.draw()
        self.window_A.flip()
        
    def _log(self, i: int, time_start: float) -> None:
        self.time_log_A.append(time.time() - time_start)
            
    def _wait_press(self, i: int, time_start: float) -> None:
        keys = [str(i) for i in range(10)]
        keys.extend([f"num_{k}" for k in keys])
        event.waitKeys(keyList=keys)
        self._log(i, time_start)
        
    def _close(self) -> None:
        self.window_A.close()
        core.quit()
        
    def _save(self) -> None:
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)
        filepath = f"{os.path.join(self.save_folder, self.filename)}.csv"
        
        with open(filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Times"])
            for tA, tB in zip(self.time_log_A):
                writer.writerow([tA, tB])
        
        
    def pause_function(self, i: int) -> None:
        if i == 0: return
        if i % self.pause != 0: return
        
        for t in range(self.pause_time):
            if self.pause_time - t > 5:
                pause_str = "Pause" + t % 4 * "."
                text_A = visual.TextStim(win=self.window_A, text=pause_str.ljust(9), color="white")
            else:
                text_A = visual.TextStim(win=self.window_A, text=f"Resuming in {self.pause_time - t}", color="white")
            text_A.draw()
            
            self.window_A.flip()
            if t < self.pause_time - 1:
                core.wait(1) 
    
    def play(self) -> None:
        time_start = time.time()
        for i, (N, D) in enumerate(zip(self.show_numbers, self.differences)):
            self._show_text(i, N, D)
            ti = time.time()
            self._wait_press(i, time_start)
            # Simulate partner wait time
            core.wait(time.time() - ti)
            self.pause_function(i)
        self._save()
        self._close()
if __name__ == "__main__":
    wm = WorkingMemory(save_folder="wm_out_single", filename="test_file")
    wm.play()