import json
import psutil


def size_format(size):
    divider = 1024
    for ending in ["", "Kb", "Mb", "Gb", "Tb"]:
        if size < divider:
            return f"{size:.2f}{ending}"
        size /= divider


def get_info():
    print(psutil.cpu_percent(interval=1))  # текущая загрузка ЦП в масштабах всей системы в процентах.
    print(psutil.cpu_count())  # количество логических процессоров в системе
    print(psutil.cpu_count(logical=False))  # количество логических процессоров в системе
    print(psutil.cpu_freq())
    print([x / psutil.cpu_count() * 100 for x in
           psutil.getloadavg()])  # Возвращает среднюю загрузку системы за последние 1, 5 и 15 минут в виде кортежа.
    """total: total physical memory (exclusive swap).
        available: the memory that can be given instantly to processes without the system going into swap. This is 
        calculated by summing different memory metrics that vary depending on the platform. It is supposed to be used to 
        monitor actual memory usage in a cross platform fashion.
        percent: the percentage usage calculated as (total - available) / total * 100.
        Other metrics:
        used: memory used, calculated differently depending on the platform and designed for informational purposes 
        only. total - free does not necessarily match used.
        free: memory not being used at all (zeroed) that is readily available; note that this doesn’t reflect the actual 
        memory available (use available instead). total - used does not necessarily match free.
        active (UNIX): memory currently in use or very recently used, and so it is in RAM.
        inactive (UNIX): memory that is marked as not used.
        buffers (Linux, BSD): cache for things like file system metadata.
        cached (Linux, BSD): cache for various things.
        shared (Linux, BSD): memory that may be simultaneously accessed by multiple processes.
        slab (Linux): in-kernel data structures cache."""
    print(psutil.virtual_memory())
    """total: total swap memory in bytes
    used: used swap memory in bytes
    free: free swap memory in bytes
    percent: the percentage usage calculated as (total - available) / total * 100"""
    print(psutil.swap_memory())
    """device: the device path (e.g. "/dev/hda1"). On Windows this is the drive letter (e.g. "C:\\").
    mountpoint: the mount point path (e.g. "/"). On Windows this is the drive letter (e.g. "C:\\").
    fstype: the partition filesystem (e.g. "ext3" on UNIX or "NTFS" on Windows).
    opts: a comma-separated string indicating different mount options for the drive/partition. Platform-dependent.
    maxfile: the maximum length a file name can have.
    maxpath: the maximum length a path name (directory name + base file name) can have."""
    print(psutil.disk_partitions())
    print(psutil.disk_usage('/'))  # argument - path to disk example: '/', '/home', "C:\\"
    # Нужно будет иттерироваться по psutil.disk_partitions()

    print(psutil.sensors_temperatures())

def main():
    get_info()


if __name__ == "__main__":
    main()
