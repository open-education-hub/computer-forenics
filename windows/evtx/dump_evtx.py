import sys
from Evtx.Evtx import Evtx
from xml.etree import ElementTree

def dump_xml(evtx_file_path):
    """
    Dumps XML contents.
    """
    try:
        with Evtx(evtx_file_path) as evtx:
            for record in evtx.records():
                xml_string = record.xml()
                print(xml_string)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dump_xml.py <path_to_evtx>", file=sys.stderr)
        sys.exit(1)
    evtx_file_path = sys.argv[1]
    dump_xml(evtx_file_path)
