import xml.etree.ElementTree as ET
import subprocess
import sys


def create_xml(path, conf_file, conf_type):
    properties = get_configs(conf_type)
    if properties[0]:
        xml_doc = ET.Element('configuration')
        for p in properties:
            aux = p.split("=")
            value = aux[1]
            name = ".".join(aux[0].split("_")[3:])

            property_xml = ET.SubElement(xml_doc, 'property')
            ET.SubElement(property_xml, 'name').text = name
            ET.SubElement(property_xml, 'value').text = value

        ET.indent(xml_doc)
        tree = ET.ElementTree(xml_doc)

        tree.write(path + conf_file, encoding='UTF-8', xml_declaration=True)


def get_configs(arg):
    out = subprocess.getoutput(f"env | grep {arg}")
    return out.split("\n")


path = sys.argv[1]
create_xml(path, "/core-site.xml", "CORE_SITE_CONF")
create_xml(path, "/hdfs-site.xml", "HDFS_SITE_CONF")
create_xml(path, "/hive-site.xml", "HIVE_SITE_CONF")
create_xml(path, "/yarn-site.xml", "YARN_SITE_CONF")
create_xml(path, "/mapred-site.xml", "MAPRED_SITE_CONF")
