import sys
from xml.dom.minidom import Document
import re
 
def main(args):
    doc = Document()
    element_catalog = doc.createElement("catalog")
    doc.appendChild(element_catalog)
    element_maxid = doc.createElement("maxid")
    element_catalog.appendChild(element_maxid)
    element_str = doc.createTextNode("4")
    element_maxid.appendChild(element_str)
    print(re.sub(r'(<[^/][^<>]*[^/]>)\s*([^<>]{,40}?)\s*(</[^<>]*>)', r'\1\2\3', doc.toprettyxml())) 
if __name__ == "__main__":
    main(sys.argv)