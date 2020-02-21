# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:52:10 2020

@author: wany105
"""

Tadjl = [
    ("1", ["2", "12"]),
    ("2", ["1", "3", "11"]),
    ("3", ["2", "4", "10"]),
    ("4", ["3", "5"]),
    ("5", ["4", "6", "8"]),
    ("6", ["5", "7"]),
    ("7", ["6", "8", "13"]),
    ("8", ["9", "7"]),
    ("9", ["4", "10", "8"]),
    ("10", ["3", "11", "9", "14"]),
    ("11", ["2", "12", "10", "15"]),
    ("12", ["1", "11", "16"]),
    ("13", ["7", "14"]),
    ("14", ["10", "15", "13"]),
    ("15", ["11", "16", "14"]),
    ("16", ["12", "15"]),
]

Padjl = [
    ("1", ["2", "21", ]), ("2", ["3", ]), ("3", ["4", "14"]),
    ("4", ["5", ]), ("5", ["6"]), ("6", ["7"]),
    ("7", ["8", "11"]), ("8", ["9"]), ("9", ["10"]),
    ("10", ["11"]), ("11", ["12"]), ("12", ["60"]),
    ("13", ["20"]), ("14", ["15"]), ("15", ["18", "16"]),
    ("16", ["17"]), ("17", ["19"]), ("18", ["22", "19"]),
    ("19", ["23", "13"]), ("20", ["24"]), ("21", ["26"]),
    ("22", ["25", "23"]),  ("23", ["24"]), ("24", ["32"]),
    ("25", ["27"]), ("26", ["28"]), ("27", ["30"]),
    ("28", ["34", "29"]), ("29", ["30", ]), ("30", ["35", "31"]),
    ("31", ["38"]), ("31", ["33"]), ("32", ["33"]),
    ("33", ["36"]), ("34", ["35"]), ("35", ["37"]),
    ("36", ["56"]), ("37", ["39", "38"]), ("38", ["45"]),
    ("39", ["40", "43", ]), ("40", ["41"]), ("41", ["42"]),
    ("42", ["46"]), ("43", ["41", "44", "48"]), ("44", ["54", ]),
    ("45", ["47"]), ("46", ["45"]), ("47", ["50"]),
    ("48", ["53", ]), ("49", []), ("50", ["49"]),
    ("51", ["52"]), ("52", []), ("53", ["57", "55"]),
    ("54", ["53", "58", ""]), ("55", ["51"]), ("56", []),
    ("57", []), ("58", ["57", "59"]), ("59", []),
    ("60", ["13"])
]

Tgraph = Graph(graph_dict = Tadjl, color = 'blue', name = 'TX-transportation', lat = [29.286, 29.313], lon = [-94.8, -94.777], nodenum = 16, edgenum = 44)
Pgraph = Graph(graph_dict = Padjl, color = 'red', name = 'TX-power', lat = [29.286, 29.313], lon = [-94.8, -94.777], nodenum = 60, edgenum = 73)

Tgraph.topology('TN.csv', 'TL.csv', Type = 'local')
Tgraph.Networkplot()

Pgraph.topology('PN.csv', 'PL.csv', Type = 'local')
Pgraph.Networkplot()

Tgraph.Dmatrix()
Pgraph.Dmatrix()

##Define the interdependency
TX_TPInter1 = Interdependency(Pgraph, Tgraph, name = 'TX_PowerSignal', color = 'orange')
TX_TPInter1.distadj()
DepenNum = [2]*TX_TPInter1.network2.Nnum
TX_TPInter1.dependadj(DepenNum)

TX_TP = System(name = 'TX_TP', networks = [Tgraph, Pgraph], inters = [TX_TPInter1])
TX_TP.Systemplot3d()




