import sys
from Evtx.Evtx import Evtx
from xml.etree import ElementTree

def extract_powershell_scripts(evtx_file_path):
    """
    Extracts PowerShell scripts from EVTX file.
    """

    try:
        with Evtx(evtx_file_path) as evtx:
            for record in evtx.records():
                xml_string = record.xml()
                root = ElementTree.fromstring(xml_string)

                evid = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}EventID[.='4104']")
                if evid is None:
                    continue

                script_block_text_element = root.find(".//*[@Name='ScriptBlockText']")
                if script_block_text_element is not None:
                    script_block_text = script_block_text_element.text
                    if script_block_text:
                        print("Found PowerShell Script:\n", script_block_text)
                        print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_ps_scripts.py <path_to_evtx>", file=sys.stderr)
        sys.exit(1)
    evtx_file_path = sys.argv[1]
    extract_powershell_scripts(evtx_file_path)
