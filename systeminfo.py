import json
from platform import uname

import psutil


def size_format(size):
    divider = 1024
    for ending in ["", "Kb", "Mb", "Gb", "Tb"]:
        if size < divider:
            return f"{size:.2f}{ending}"
        size /= divider


def get_info():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu_freq = psutil.cpu_freq()
    system_info = {
        "System": {
            "OS version": f"{uname().system} {uname().release}",
            "PC name": uname().node,
            "Version": uname().version,
            'Machine': uname().machine
        },
        "CPU": {
            'name': uname().processor,
            "Load (%)": psutil.cpu_percent(interval=1),
            "Logical CPU Count": psutil.cpu_count(),
            "CPU Count": psutil.cpu_count(logical=False),
            "CPU frequence (Ghz)": {
                "Current": int(cpu_freq.current),
                "Min": int(cpu_freq.min),
                "Max": int(cpu_freq.max)
            },
        },
        "RAM": {
            "Memory": {
                "Total": size_format(ram.total),
                "Available": size_format(ram.available),
                "Load": size_format(ram.percent),
                "Used": size_format(ram.used)
            },
            "Swap": {
                "Total": size_format(swap.total),
                "Used": size_format(swap.used),
                "Free": size_format(swap.free)
            }
        },
        "Temperature": {},
        "Disk": {}
    }

    sensors_temperatures = psutil.sensors_temperatures()
    for name, entries in sensors_temperatures.items():
        for entry in entries:
            system_info["Temperature"][entry.label or name] = '%s °C' % entry.current

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)

            if f"'device': {partition.device}" not in system_info["Disk"]:
                system_info["Disk"][partition.device] = dict()
                system_info["Disk"][partition.device] = {'File system': partition.fstype,
                                                         'Total': size_format(
                                                             partition_usage.total),
                                                         'Used': size_format(
                                                             partition_usage.used),
                                                         'Free': size_format(
                                                             partition_usage.free),
                                                         'Percent':
                                                             f'{partition_usage.percent}'}
        except Exception as err:
            print(err)
            continue
    return system_info


def print_sys_info(system_info):
    for category, values in system_info.items():
        print(f"{category}:")
        if isinstance(values, dict):
            for key, val in values.items():
                if isinstance(val, dict):
                    print(f"  {key}:")
                    for sub_key, sub_val in val.items():
                        print(f"    {sub_key}: {sub_val}")
                else:
                    print(f"  {key}: {val}")
        else:
            print(f"  {values}")
        print()


def main():
    info = get_info()
    with open(f'{uname().node}.json', 'w', encoding='utf-8') as file:
        json.dump(info, file, indent=4, ensure_ascii=False)
    print_sys_info(info)


if __name__ == "__main__":
    main()
