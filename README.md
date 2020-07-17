# datagen

Python library for an easy creation of a network model from a pcap.

## Usage

To get the usage info on this library, try this in the command line:

```bash
python src/pcap.py
```

You can test the script with the option -t or --test:

```bash
python src/pcap.py path/to/pcap -t
```

When you want to import your resulting json in a neo4j database at the end of the process, you have 2 options:

- run the script to populate the database yourself:
```bash
python src/populate -u user -p password -a database.address path/to/json/file
```

- use the programm to import it automatically after the analysis of the pcap:
```bash
python src/pcap.py -u user -p password -a database.address path/to/pcap
```
