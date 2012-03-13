# -*- coding: cp1257 -*-
"""V�ikene script serverist uute m�ngude t�mbamiseks/nende
    kasulikku vormingusse viimiseks
    V�tab argumentideks vahemiku, mida t�mmata alguse ja
    l�pu """
import sys
import urllib2
import time
base = 'http://gg.cs.ut.ee/index.php?form=view_game&game_id=%d'
startn = 'Vertikaalne (alustaja)'
endn = '\n</td>\n</tr>\n</table>'

def logify(text, i):
    """Teisendab HTML-i �igesse formaati logide jaoks."""
    if text.find('ei leitud!') != -1:
        raise ValueError
    text = text[text.find(startn):]
    text = text[:text.find(endn)]
    text = text.replace('ü','�').replace('ä','�').replace('õ','�').replace('Ö','�')
    text = text.replace('\n</td>\n<td class="move">\n','\t ')
    text = text.replace('\n</td>\n<td class="contestant">\n','\t ')
    text = text.replace('\n</td>\n</tr>\n','')
    text = text.replace('\n<td class="move_no">','')
    text = text.replace('<tr class="even">','')
    text = text.replace('<tr class="odd">','')
    text = text.replace('<tr>','')
    text = text.replace('\n</td>\n<td class="header_right">\n','\t ')
    text = text.replace('\n<td class="header_left" colspan="2">','')
    text = text.replace('#','')
    names = [x.split('\t ')[1].replace(' #','_') for x in text.split('\n')[:2]]
    open('%s %d.txt' % (' '.join(names), i),'w').write(text)

howmany = 3000
start = 37956
if len(sys.argv) > 1:
    start = int(sys.argv[1])
    if len(sys.argv) == 3:
        end = int(sys.argv[2])
    else:
        end = start + howmany
else:
    end = start + howmany
    
##for i in xrange(start, start - howmany, -1):
for i in xrange(start, end):
    try:
        logify(urllib2.urlopen(base % i).read(), i)
        print i,
    except:
        print 'error'
    time.sleep(0.5)
