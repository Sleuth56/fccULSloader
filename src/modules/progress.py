"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Module to handle progress bar display with consistent formatting.
"""

import time
import math
from datetime import timedelta
from tqdm import tqdm

class SmoothProgressBar(tqdm):
    """
    Custom progress bar with smoothed ETA calculation and consistent formatting.
    
    This class extends tqdm to provide:
    - Smoothed time estimates by averaging recent speeds
    - Consistent time format (mm:ss)
    - Custom display format showing size in KB and time in mm:ss
    """
    def __init__(self, *args, **kwargs):
        self.custom_unit = kwargs.pop('custom_unit', 'records')
        self.size_in_kb = kwargs.pop('size_in_kb', False)
        super().__init__(*args, **kwargs)
        self.start_time = time.time()
        self.last_print_time = self.start_time
        self.speeds = []  # Store recent speeds for averaging
        self.max_speed_samples = 10  # Number of samples to average
        self.last_n = 0  # Last displayed n value
        
        # Override the display method to customize the format
        self._original_display = self.display
        self.display = self._custom_display
        
    def format_time(self, seconds):
        """Format time as mm:ss"""
        if seconds is None or not math.isfinite(seconds):
            return "--:--"
        return str(timedelta(seconds=int(seconds)))[2:7]  # Skip hours, just show mm:ss
        
    def get_avg_speed(self):
        """Calculate average speed"""
        if not self.speeds:
            return 0
        return sum(self.speeds) / len(self.speeds)
        
    def update(self, n=1):
        """Update progress with smoothed ETA calculation"""
        now = time.time()
        
        # Calculate current speed
        if now > self.last_print_time:
            current_speed = n / (now - self.last_print_time)
            self.speeds.append(current_speed)
            # Keep only the most recent samples
            if len(self.speeds) > self.max_speed_samples:
                self.speeds.pop(0)
        
        self.last_print_time = now
        self.last_n = n
        super().update(n)
        
    def _generate_bar(self, width=10):
        """Generate a progress bar string"""
        if self.total and self.total > 0:
            percent = self.n / self.total
            filled_length = int(width * percent)
            bar = '█' * filled_length + ' ' * (width - filled_length)
            return bar
        return ' ' * width
    
    def _format_size(self, size_in_bytes):
        """Format size in bytes to a human-readable format (KB, MB, GB)"""
        kb = size_in_bytes / 1024
        if kb < 1000:
            return f"{kb:.0f}KB"
        mb = kb / 1024
        if mb < 1000:
            return f"{mb:.1f}MB"
        gb = mb / 1024
        return f"{gb:.2f}GB"
    
    def _format_speed(self, speed):
        """Format speed to a human-readable format (KB/s, MB/s)"""
        if speed < 1000:
            return f"{speed:.1f} KB/s"
        mb_speed = speed / 1024
        if mb_speed < 1000:
            return f"{mb_speed:.1f} MB/s"
        gb_speed = mb_speed / 1024
        return f"{gb_speed:.2f} MB/s"
        
    def _custom_display(self, msg=None, pos=None):
        """Custom display method with consistent formatting"""
        # Calculate elapsed and remaining time
        elapsed = self.format_time(time.time() - self.start_time)
        
        # Calculate average speed and ETA
        avg_speed = self.get_avg_speed()
        if avg_speed > 0 and self.total:
            remaining_items = self.total - self.n
            eta_seconds = remaining_items / avg_speed
            remaining = self.format_time(eta_seconds)
        else:
            remaining = "--:--"
        
        # Calculate percentage
        percentage = 0
        if self.total:
            percentage = self.n * 100 / self.total
        
        # Format values based on whether we're displaying KB or records
        if self.size_in_kb:
            # For file downloads, show KB/MB/GB
            current_fmt = self._format_size(self.n)
            total_fmt = self._format_size(self.total) if self.total else "?"
            speed_fmt = self._format_speed(avg_speed)
        else:
            # For record loading, show record counts
            current = self.n
            total = self.total if self.total else 0
            current_fmt = f"{current:,d}"
            total_fmt = f"{total:,d}"
            speed_fmt = f"{avg_speed:.1f} {self.custom_unit}/s"
        
        # Generate a simple progress bar
        bar_width = 60  # Width of the progress bar
        bar = self._generate_bar(bar_width)
        
        # Create custom format string
        custom_bar = f"{self.desc}: {percentage:3.0f}%|{bar}| "
        custom_bar += f"{current_fmt}/{total_fmt} "
        custom_bar += f"[{elapsed}<{remaining} {speed_fmt}]"
        
        # Call original display with our custom message
        self._original_display(custom_bar, pos)

def create_download_progress_bar(total_size, desc="Downloading"):
    """
    Create a progress bar for file downloads with size in KB.
    
    Args:
        total_size (int): Total size in bytes
        desc (str): Description for the progress bar
        
    Returns:
        SmoothProgressBar: Configured progress bar
    """
    return SmoothProgressBar(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=desc,
        size_in_kb=True,
        miniters=1
    )

def create_record_progress_bar(total_records, desc="Loading", unit="records"):
    """
    Create a progress bar for record loading with count in records.
    
    Args:
        total_records (int): Total number of records
        desc (str): Description for the progress bar
        unit (str): Unit name for the speed display
        
    Returns:
        SmoothProgressBar: Configured progress bar
    """
    return SmoothProgressBar(
        total=total_records,
        unit=unit,
        desc=desc,
        custom_unit=unit,
        size_in_kb=False,
        miniters=1
    ) 