import os

import sys
from pathlib import Path

input_dir = sys.argv[1]

path_object = Path(input_dir)

if path_object.is_dir() is False:
    raise ValueError(f"Folder {path_object} does not exist.")

mrc_files = list(path_object.glob("*.mrc"))
xml_files = list(path_object.glob("*.xml"))

renamed_mrc_files = []
for m_file in mrc_files:
    m_file = str(m_file).replace("[", "_")
    m_file = str(m_file).replace("]", "")
    renamed_mrc_files.append(m_file)

renamed_xml_files = []
for x_file in xml_files:
    x_file = str(x_file).replace("[", "_")
    x_file = str(x_file).replace("]", "")
    renamed_xml_files.append(x_file)

print("REMOVING BRACKETS!")
for m_old, n_old in zip(mrc_files, renamed_mrc_files):
    os.rename(m_old, n_old)

for x_old, n_old in zip(xml_files, renamed_xml_files):
    os.rename(x_old, n_old)

print("DONE")
