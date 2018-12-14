# network-model-creator

Python framework for an easy creation of a network model for scientific pcap creation.

Allows user to specify number of machines, duration of the experiment, number of times the machines change behavior, ip and mac address.

Generates a crontab and a CSV (containing behavior, ip and mac addresses for each change) for each VM and a global CSV containing a mashup of the CSVs of the VMs.

## Usage

You can test the script with the option -t or --test:

```bash
./main.py -t
```

You can use a different configuration file with the option -c or --conf:

```bash
./main.py -c *other_config_file*
```

## Configuration file

A sample configuration file is provided in *config.json* with all the necessary elements for each sub level.

Values for these elements are to be changed to accomodate your preferences.