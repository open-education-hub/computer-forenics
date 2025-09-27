# Windows Forensics Challenges

This document provides practical exercises covering the forensic analysis of Windows systems.

## Area 1: Logging and Events (EVTX)

These exercises require a tool to parse EVTX files.
We will use `python-evtx`.
Run the commands below for `python-evtx`:

```bash
sudo apt-get -y update
sudo apt-get -y install python3-pip python3-venv
python -m venv .venv
source .venv/bin/activate
pip3 install python-evtx
```

We use the [`EVTX-ATTACK-SAMPLES` repository](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES), consisting of Windows event log files:

```console
git clone https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES
```

### List Contents of .evtx Files

Use the `dump_evtx.py` script to dump (in XML format) the contents of various files in the `EVTX-ATTACK-SAMPLES` repository.
Pass the `.evtx` file as argument, such as:

```console
python dump_evtx.py "EVTX-ATTACK-SAMPLES/Credential Access/babyshark_mimikatz_powershell.evtx"
```

List contents of all `.evtx` files by using:

```console
find EVTX-ATTACK-SAMPLES/ -name '*.evtx' | while read e; do python dump_evtx.py "$e"; done
```

### List Files With a Given Event ID

Use the `has_event.py` script to check if an `.evtx` file contains a given event.
For example, to check whether a file stores the `4624` logon event, use:

```console
$ python has_event.py "EVTX-ATTACK-SAMPLES/Privilege Escalation/privexchange_dirkjan.evtx" 4624
$ echo $?
0
```

If an event ID exists, the script will return `0` as the exit code, otherwise it will return `1`.

To list all files containining a given event use:

```console
find EVTX-ATTACK-SAMPLES/ -name '*.evtx' | while read e; do python has_event.py "$e" 4624 && echo "$e"; done
```

List files that have events: `4625`, `1102`, `4104`, `4648`, `4720`.`4656`, `4771`.

### List Contents of `.evtx` Files with Given ID

Create a script called `dump_evtx_for_event.py` that dumps as XML the event lines in an `.evtx` file that have a given event ID.

### Decode a Malicious PowerShell Command

List the contents of a `ScriptBlockTest` section in a an `.evtx` file for entries using event `4104`.
Take a look at and use the `extract_ps_scripts.py` script.

## Full Windows Forensics

Follow the instructions [here](https://theproghost.github.io/Digital_Forensics_CaseStudy/) and do as many of the 31 steps described as possible.
See the questions and download the imagest to analyze from [here](https://cfreds-archive.nist.gov/Hacking_Case.html).
