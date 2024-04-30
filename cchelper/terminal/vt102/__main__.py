from . import stream, screen

st = stream()
sc = screen((24,80))

sc.attach(st)

st.process(u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H" +
    u"\u001b[2;1HNetHack, Copyright 1985-2003\r\u001b[3;1" +
    u"H         By Stichting Mathematisch Centrum and M. " +
    u"Stephenson.\r\u001b[4;1H         See license for de" +
    u"tails.\r\u001b[5;1H\u001b[6;1H\u001b[7;1HShall I pi" +
    u"ck a character's race, role, gender and alignment f" +
    u"or you? [ynq] ")

print(sc)