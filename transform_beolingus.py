from lxml import etree
import re
import input_output


def transform_in_tei(beo_as_dict):
    root = etree.Element('TEI', attrib={"xmlns": 'http://www.tei-c.org/ns/1.0'})

    ##HEADER
    header = etree.SubElement(root, 'teiHeader')

    fileDesc = etree.SubElement(header, 'fileDesc')
    titleStmt = etree.SubElement(fileDesc, 'titleStmt')
    title = etree.SubElement(titleStmt, 'title')
    title.text = 'TEI Version of Beolingus DE-EN'

    publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
    p_publicationStmt = etree.SubElement(publicationStmt, 'p')
    p_publicationStmt.text = 'Original Data: Copyright (c) :: Frank Richter <frank.richter.tu-chemnitz.de>'

    sourceDesc = etree.SubElement(fileDesc, 'sourceDesc')
    p_sourceDesc = etree.SubElement(sourceDesc, 'p')
    p_sourceDesc.text = 'Digi_Lex - TEI Version'

    ##TEXT
    text = etree.SubElement(root, 'text')
    body = etree.SubElement(text, 'body')

    for k1, v1 in beo_as_dict.items():

        if str(v1).count(":") > 1:
            mainentry = etree.Element('superEntry')
        else:
            mainentry = etree.Element('entry')

        for k2, v2 in v1.items():

            splitted_forms = k2.split(';')
            splitted_senses = v2.split(';')

            if len(splitted_forms) > 1:
                for i, u in zip(range(len(splitted_forms)), range(len(splitted_senses))):
                    subentry = etree.SubElement(mainentry, 'entry')
                    form = etree.SubElement(subentry, 'form')
                    orth = etree.SubElement(form, 'orth')
                    f = splitted_forms[i]
                    usg_list = re.findall(r'\[(\w+)\.?\]', f)
                    for usg_entry in usg_list:
                        usg = etree.SubElement(form, 'usg')
                        usg.text = usg_entry
                        f = f.replace("[" + usg_entry + ".]", "")
                        f = f.replace("[" + usg_entry + "]", "")
                    note_list = re.findall(r'(\(\w+.*?\))', f)
                    if note_list:
                        for note_entry in note_list:
                            note = etree.SubElement(form, 'note')
                            note.text = note_entry
                            f = f.replace(note_entry, "")
                    gram_list = re.findall(r'\{(\w+?)}', f)
                    if gram_list:
                        gramgrp = etree.SubElement(subentry, 'gramGrp')
                        for gram_entry in gram_list:
                            gram = etree.SubElement(gramgrp, 'gram')
                            gram.text = gram_entry
                            f = f.replace("{" + gram_entry + "}", "")
                    orth.text = f

                    s = splitted_senses[u]
                    sense = etree.SubElement(subentry, 'sense')
                    sense_def = etree.SubElement(sense, 'def')
                    usg_list = re.findall(r'\[(\w+)\.?\]', s)
                    if usg_list:
                        for usg_entry in usg_list:
                            usg = etree.SubElement(sense, 'usg')
                            usg.text = usg_entry
                            s = s.replace("[" + usg_entry + ".]", "")
                            s = s.replace("[" + usg_entry + "]", "")
                    note_list = re.findall(r'(\(\w+.*?\))', s)
                    if note_list:
                        for note_entry in note_list:
                            note = etree.SubElement(sense, 'note')
                            note.text = note_entry
                            s = s.replace(note_entry, "")
                    sense_def.text = s

            else:
                for f in splitted_forms:
                    form = etree.SubElement(mainentry, 'form')
                    orth = etree.SubElement(form, 'orth')
                    usg_list = re.findall(r'\[(\w+)\.?\]', f)
                    if usg_list:
                        for usg_entry in usg_list:
                            usg = etree.SubElement(form, 'usg')
                            usg.text = usg_entry
                            f = f.replace("[" + usg_entry + ".]", "")
                            f = f.replace("[" + usg_entry + "]", "")
                    note_list = re.findall(r'(\(\w+.*?\))', f)
                    if note_list:
                        for note_entry in note_list:
                            note = etree.SubElement(form, 'note')
                            note.text = note_entry
                            f = f.replace(note_entry, "")
                    gram_list = re.findall(r'\{(\w+?)}', f)
                    if gram_list:
                        gramgrp = etree.SubElement(mainentry, 'gramGrp')
                        for gram_entry in gram_list:
                            gram = etree.SubElement(gramgrp, 'gram')
                            gram.text = gram_entry
                            f = f.replace("{" + gram_entry + "}", "")
                    orth.text = f

                for s in splitted_senses:
                    sense = etree.SubElement(mainentry, 'sense')
                    sense_def = etree.SubElement(sense, 'def')
                    usg_list = re.findall(r'\[(\w+)\.?\]', s)
                    if usg_list:
                        for usg_entry in usg_list:
                            usg = etree.SubElement(sense, 'usg')
                            usg.text = usg_entry
                            s = s.replace("[" + usg_entry + ".]", "")
                            s = s.replace("[" + usg_entry + "]", "")
                    note_list = re.findall(r'(\(\w+.*?\))', s)
                    if note_list:
                        for note_entry in note_list:
                            note = etree.SubElement(sense, 'note')
                            note.text = note_entry
                            s = s.replace(note_entry, "")
                    sense_def.text = s

        body.append(mainentry)

    et = etree.ElementTree(root)
    return et


et = transform_in_tei(input_output.deserialize('data/splitted_beolingus.pickle'))
et.write('data/beolingus_tei.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')