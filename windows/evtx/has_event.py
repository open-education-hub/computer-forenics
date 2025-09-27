import sys
from Evtx.Evtx import Evtx
from xml.etree import ElementTree

def has_event(evtx_file_path, evid):
    """
    Dumps XML contents.
    """
    ret = False
    try:
        with Evtx(evtx_file_path) as evtx:
            for record in evtx.records():
                xml_string = record.xml()
                root = ElementTree.fromstring(xml_string)

                item = root.find(f".//{{http://schemas.microsoft.com/win/2004/08/events/event}}EventID[.='{evid}']")
                if item is None:
                    continue
                ret = True
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    return ret

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dump_xml.py <path_to_evtx> <event_id>", file=sys.stderr)
        sys.exit(1)
    evtx_file_path = sys.argv[1]
    evid = int(sys.argv[2])
    if has_event(evtx_file_path, evid):
        sys.exit(0)
    else:
        sys.exit(1)
