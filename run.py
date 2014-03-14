#! /bin/python

# Initialization copied from hamadr with mods, no point reinventing the wheel

import json,sys
from random import randint, choice

if len(sys.argv) != 2:
    print "{\"error\": \"Expected one argument\"}"
    exit(0)

try:
    jsonIn = json.loads(sys.argv[1])
except:
    print "{\"error\": \"Could not decode JSON from argument %s\"}" % sys.argv[1].replace('"', '\\"')
    exit(0)

cmdStr = jsonIn["cmd"]
jsonOut = {}

board = [
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]
        ]

def getnearbycells(inp):
    def check_if_in_range(a):
        valid = set('01234567')
        return set(str(inp)) <= valid
    if not check_if_in_range(inp):
        return None
    if len(inp) < 2:
        inp = "0" + inp
    elif len(inp) > 2:
        return None
    out = []
    iinp = int(inp)
    if check_if_in_range(iinp - 10):
        out.append(str(iinp - 10))
    if check_if_in_range(iinp - 1):
        out.append(str(iinp - 1))
    if check_if_in_range(iinp + 10):
        out.append(str(iinp + 10))
    if check_if_in_range(iinp + 1):
        out.append(str(iinp + 1))
    newout = []
    for a in out:
        if "-" in a or "8" in a:
            continue
        a = ("0" + a) if len(a) == 1 else a
        newout.append(a)
    return newout


def getvalidmoves(blacklist):
    a = []
    for x in xrange(0,8):
        for y in xrange(0,8):
            a.append(str(x) + str(y))
    for b in blacklist:
        if b in a:
            a.pop(a.index(b))
    return a


if cmdStr == "init":
	#initialize the grid
	generating = 2
	while generating <= 5:
		orientation = randint(0, 1)
		x = 0
		y = 0

		if orientation == 0:
			#h
			x = randint(0, 7)
			y = randint(0, 7 - generating)
		else:
			#v
			x = randint(0, 7 - generating)
			y = randint(0, 7)

		toFill = generating
		if orientation == 0:
			#horizontal
			for c in range(y, y + generating):
				if board[x][c] != 0:
					break
				else:
					toFill -= 1
			if toFill != 0:
				continue
			for c in range(y, y + generating):
				board[x][c] = 1
		else:
			#vertical
			for c in range(x, x + generating):
				if board[c][y] != 0:
					break
				else:
					toFill -= 1
			if toFill != 0:
				continue
			for c in range(x, x + generating):
				board[c][y] = 1
		orientationStr = "horizontal" if (orientation == 0) else "vertical"
		point = "%d%d" % (y, x)
		jsonOut[generating] = {"point": point, "orientation": orientationStr}
		generating += 1

elif cmdStr == "move":
    blacklist = jsonIn['hit'] + jsonIn['missed']
    valid = getvalidmoves(blacklist)
    if len(jsonIn['hit']) == 0:
        print "{'move': '%s'}".replace("'", '"') % choice(valid)
        exit(0)
    mymoves = [a[1:3] for a in jsonIn['moves'] if (a[0] == "0")]
    for a in jsonIn['hit']:
        if not a in blacklist:
            near = getnearbycells(a)
            for b in near:
                if not b in blacklist:
                    print json.dumps({'move': b}).replace("'", '"')
                    exit(0)

if jsonOut:
    print json.dumps(jsonOut).replace("'", '"')
else:
    valid = getvalidmoves([])
    print "{'move': '%s'}".replace("'", '"') % choice(valid)
