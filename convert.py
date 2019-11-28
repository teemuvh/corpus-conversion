#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import lxml.etree as etree

def main():

    punctuation = [".", ",", "!", "?", ":", ";", '"', '&quot;']

    # Open data file:
    try:
        with open(sys.argv[1], 'r') as data:
            tree = etree.parse(data)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit()

    # Open output file for writing:
    out_file = open(sys.argv[2], 'w')

    # Add all wanted title languages here (ntk = ikoma, ntk-x-isenye = isenye, ngq = ngoreme, ntk-x-nata = nata, en = english):
    titles = [t for t in tree.findall('//item[@type="title"][@lang="ntk"]')] \
        or [t for t in tree.findall('//item[@type="title"][@lang="ntk-x-isenye"]')] \
        or [t for t in tree.findall('//item[@type="title"][@lang="ngq"]')] \
        or [t for t in tree.findall('//item[@type="title"][@lang="ntk-x-nata"]')] \
        or [t for t in tree.findall('//item[@type="title"][@lang="en"]')]
    paragraphs = [pa for pa in tree.findall('//paragraph')]

    # Find the title of the text and write the first line of the vrt-file:
    for t in titles:
        out_file.write('<text title="{}" datefrom="{}" dateto="{}" timefrom="{}" timeto="{}">'.format(
            t.text, "", "", "", "") + '\n')

    # Paragraphs contain the needed information, loop each paragraph:
    count_p = 1
    for p in paragraphs:
        # Create a list of translations with a recursive loop in paragraphs, and initialize lists for each needed translation:
        translations = [transl.text for transl in p.xpath('phrases/word/item[@type="gls"]')]
        phrases_eng = []
        phrases_swa = []

        # Translations in even index numbers are in Swahili, uneven are English:
        for idx, trans in enumerate(translations):
            if idx % 2 != 0:
                phrases_eng.append(trans)
            else:
                phrases_swa.append(trans)

        # Each sentence is marked with a segment number. Create a list of segnums for help in looping sentences.
        segnum = [s_num for s_num in p.xpath('phrases/word/item[@type="segnum"]')]

        # For each paragraph, write a paragraph-line into the output file, continue looping the paragraphs:
        if count_p <= len(paragraphs):
            out_file.write('<paragraph id="%d">' % count_p + '\n')

            # Loop phrases in swahili and english based on the segment number:
            for s_num, ph_swa, ph_eng in zip(segnum, phrases_swa, phrases_eng):
                # Escape quotes in strigs and write the translations to the output file:
                if ph_swa is not None:
                    ph_swa = ph_swa.replace('"', "&quot;").replace('<', "&lt;").replace('>', "&gt;")
                if ph_eng is not None:
                    ph_eng = ph_eng.replace('"', "&quot;").replace('<', "&lt;").replace('>', "&gt;")
                out_file.write('<sentence id="{}" transl_swa="{}" transl_eng="{}">'.format(
                    s_num.text, ph_swa, ph_eng) + '\n')

                w_i = 0
                # Add word glosses to a lits of words:
                words = [w for w in s_num.xpath('../words/word/item[@lang="ntk"]')] \
                    or [w for w in s_num.xpath('../words/word/item[@lang="ntk-x-isenye"]')] \
                    or [w for w in s_num.xpath('../words/word/item[@lang="ngq"]')] \
                    or [w for w in s_num.xpath('../words/word/item[@lang="ntk-x-nata"]')]

                w_count = 1
                # Recursively loop sentences based on segment number for each needed info x:
                for x in s_num.xpath('../words/word'):
                    root = [r.text for r in x.xpath('morphemes/morph/item[@type="cf"]') if r.text is not None and
                            "-" not in r.text and r.text not in punctuation]
                    morf_list = [m.text for m in x.xpath('morphemes/morph/item[@type="cf"]') if m.text is not None]
                    eng = [e.text for e in x.xpath('item[@type="gls"][@lang="en"]') if e.text is not None]
                    p_o_s = [pos.text for pos in x.xpath('item[@type="pos"]') if pos.text is not None]
                    full_classes = [f.text for f in x.xpath('morphemes/morph/item[@type="msa"]') if f.text is not None]

                    # Build the output string:
                    if w_i < len(words):
                        w = words[w_i].text
                        roots = ''.join(root)
                        english_translation = ''.join(eng)
                        part_of_speech = ''.join(p_o_s)
                        morphs = ' '.join(morf_list)
                        full_class = ' '.join(full_classes)

                        # Replace illegal characters:
                        w = w.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')
                        roots = roots.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')
                        english_translation = english_translation.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')
                        part_of_speech = part_of_speech.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')
                        morphs = morphs.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')
                        full_class = full_class.replace('"', "&quot;").replace('”', "&quot;").replace('<', '&lt;').replace('>', '&gt;')

                        # Write the output string into the file:
                        if w not in punctuation:
                            write_to_file = (w, str(w_count), roots, english_translation,
                                             part_of_speech, morphs, full_class)
                            out_file.write('\t'.join(write_to_file) + '\n')
                            w_count += 1
                        else:
                            punct = (w, str(w_count), 'punct')
                            out_file.write('\t'.join(punct) + '\n')
                            w_count += 1

                        w_i += 1
                # Write the end of sentence:
                out_file.write('</sentence>' + '\n')
            # Write the end of paragraph:
            out_file.write('</paragraph>' + '\n')
            count_p += 1

    # Write the end of text entity:
    out_file.write('</text>')

    # Close all files
    data.close()
    out_file.close()

# Run program:
if (__name__) == '__main__':
    main()
