#! /usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import os


def height(pitch):
    """ Calculate absolute height of given pitch. """
    # pitch example: [u'G', u'5']
    cde_list = ["c","d","e","f","g","a","b"]
    h =  int(pitch[1])*7
    h += cde_list.index(pitch[0].lower())
    return h


def find_key(mode, fifths):
    """ Find key from mode(major/minor) and fifths(-7 to +7). """
    keys = {}
    keys["major"] = ["C","G","D","A","E","B(C-flat)","F-sharp(G-flat)","C-sharp(D-flat)"]
    keys["minor"] = ["A","D","G","C","F","A-sharp(B-flat)","D-sharp(E-flat)","G-sharp(A-flat)"]
    # check
    if (mode.lower() not in keys) or (fifths<-7 or fifths>7):
        print "mode: str of major or minor, fifth: -7 to +7."
    return keys[mode.lower()][fifths] + " " +mode.lower()


def extract_music(soup):
    """ Extract music data from xml file. """
    pitch_list = []
    cur_time = 0 # Current time
    tmp_duration = 0
    # parse
    for m in soup.find_all("measure"):
        for nb in m.find_all({"note", "backup"}):
            if nb.name == "backup": # 巻き戻し
                cur_time -= int(nb.duration.string)
            if nb.name == "note":
                if not nb.chord: # 和音でなければ
                    cur_time += tmp_duration
                if nb.pitch: # 音符
                    pitch_list.append([cur_time,
                                       nb.pitch.step.string,
                                       nb.pitch.octave.string,
                                       nb.staff.string])
                if nb.rest: # 休符
                    pass
                if nb.duration: # 装飾音はdurationないので飛ばす
                    tmp_duration= int(nb.duration.string)
    return pitch_list


def print_info(soup):
    """ Print information of score. """
    print u"%s/%s" % (soup.attributes.beats.string,
                            soup.attributes.find("beat-type").string)
    print u"division: %s" % soup.attributes.divisions.string
    print find_key(soup.attributes.key.mode.string.encode("utf-8"),
                   int(soup.attributes.key.fifths.string.encode("utf-8")))


if __name__ == "__main__":
    xml_name = "lg-203466147999847691.xml"# Your MusicXML file
    dir_name = xml_name.rstrip('.xml')# Directory name for this MusicXML file
    soup = BeautifulSoup(open(xml_name,'r').read(), "lxml")

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    main = open(dir_name + '/main.txt', 'w+')
    sub = open(dir_name + '/sub.txt', 'w+')

    print_info(soup)
    music_data = extract_music(soup)

    main.write("%s/" % soup.attributes.beats.string)
    main.write("%s\n" % soup.attributes.find("beat-type").string)
    main.write(find_key(soup.attributes.key.mode.string.encode("utf-8"),                int(soup.attributes.key.fifths.string.encode("utf-8"))))
    main.write("\n")
    sub.write("%s/" % soup.attributes.beats.string)
    sub.write("%s\n" % soup.attributes.find("beat-type").string)
    sub.write(find_key(soup.attributes.key.mode.string.encode("utf-8"),                int(soup.attributes.key.fifths.string.encode("utf-8"))))
    sub.write("\n")

    for i in music_data:#Separate by staff
        if i[3] == u'1':
            for j in i:
                if j != i[3]:
                    main.write("%s " % j)
            main.write("\n")
        else:
            for j in i:
                if j != i[3]:
                    sub.write("%s " % j)
            sub.write("\n")
    main.close()
    sub.close()
