#!/bin/env python3
PATH = "/path/to/folder" # Change this.
PATH += "/"
mrc_files = glob.glob(PATH + "*.mrc")
xml_files = glob.glob(PATH + "*.xml")

renamed_mrc_files = []
for files in mrc_files:
    files = files.replace("[", "_")
    files = files.replace("]", "")
    renamed_mrc_files.append(files)

renamed_xml_files = []
for x_files in xml_files:
    x_files = x_files.replace("[", "_")
    x_files = x_files.replace("]", "")
    renamed_xml_files.append(x_files)

print("REMOVING BRACKETS!")
for m_old, n_old in zip(mrc_files, renamed_mrc_files):
    os.rename(m_old, n_old)

for x_old, n_old in zip(xml_files, renamed_xml_files):
    os.rename(x_old, n_old)

print("DONE")
