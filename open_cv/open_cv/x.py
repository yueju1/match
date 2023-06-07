import cv2
import matplotlib.pyplot as plt
import numpy as np

im = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")
# im = m.copy()
point2 = [[1193.6470336914062, 818.5837097167969], [1194.4179077148438, 819.4917907714844], [1194.9226684570312, 820.3135681152344], [1194.8828735351562, 820.2714538574219], [1195.51953125, 821.0650634765625], [1195.9157104492188, 821.8160400390625], [1196.5064697265625, 822.5262451171875], [1196.3778076171875, 822.4252014160156], [1196.788818359375, 822.9667358398438], [1197.3761596679688, 823.6689453125], [1197.1702880859375, 823.4259948730469], [1197.6320190429688, 823.9737854003906], [1197.8629760742188, 824.6954650878906], [1198.3921508789062, 825.2959899902344], [1198.0093383789062, 824.766357421875], [1198.4732666015625, 825.4314270019531], [1198.7881469726562, 825.8555603027344], [1198.4839477539062, 825.4959411621094], [1198.8125, 825.8670043945312], [1199.1913452148438, 826.3966979980469], [1199.51220703125, 826.7514953613281], [1199.2387084960938, 826.394775390625], [1199.4942016601562, 826.7264404296875], [1199.778076171875, 827.2323913574219], [1199.4342041015625, 826.6283264160156], [1197.92626953125, 828.2136840820312], [1196.3701782226562, 829.8533630371094], [1194.0137329101562, 830.5925903320312], [1190.5162353515625, 833.6106567382812], [1185.7959594726562, 837.6354370117188], [1180.528076171875, 842.3365478515625], [1172.2454223632812, 848.584716796875], [1166.4896240234375, 854.6916809082031], [1161.2252807617188, 860.7254638671875], [1155.9197387695312, 865.87890625], [1151.8013305664062, 871.6211853027344], [1146.7662963867188, 879.0975341796875], [1141.0479736328125, 888.5737915039062], [1134.489990234375, 898.5686645507812], [1130.2863159179688, 907.8800659179688], [1126.63232421875, 917.3229675292969], [1122.4805297851562, 927.0832214355469], [1119.6543579101562, 937.4776611328125], [1117.5640258789062, 947.651123046875], [1116.0364990234375, 957.5377197265625], [1114.1084594726562, 969.2939758300781], [1113.697509765625, 980.4378662109375], [1114.0032958984375, 989.9949645996094], [1114.37451171875, 1001.9828186035156], [1115.8795166015625, 1012.9872436523438], [1117.8724365234375, 1024.0716552734375], [1120.5402221679688, 1035.612060546875], [1123.9088134765625, 1045.9716796875], [1127.6301879882812, 1055.9055786132812], [1131.1734619140625, 1063.8757934570312], [1136.0338745117188, 1073.9765625], [1141.58056640625, 1083.4141235351562], [1147.4754028320312, 1092.2842407226562], [1153.9984130859375, 1100.8351440429688], [1161.1788940429688, 1109.42578125], [1167.6021728515625, 1116.3594360351562], [1175.6373901367188, 1124.2100219726562], [1185.013671875, 1131.4523315429688], [1193.8505859375, 1138.296875], [1203.3260498046875, 1144.376708984375], [1213.85107421875, 1150.2103881835938], [1223.8181762695312, 1155.0818481445312], [1232.5106811523438, 1158.9631958007812], [1244.1865234375, 1162.5730590820312], [1254.8215942382812, 1165.7161865234375], [1265.6112060546875, 1168.2875366210938], [1276.6286010742188, 1170.1683349609375], [1288.6911010742188, 1170.3956298828125], [1299.1971435546875, 1171.1057739257812], [1307.865478515625, 1171.21923828125], [1319.7626953125, 1169.3541870117188], [1330.8204345703125, 1168.1383056640625], [1341.6510009765625, 1166.2731323242188], [1352.4986572265625, 1163.60302734375], [1363.98876953125, 1158.8182373046875], [1372.6690673828125, 1155.7822265625], [1382.3414306640625, 1151.5325927734375], [1392.27490234375, 1145.2271118164062], [1401.6411743164062, 1139.7030029296875], [1410.4276733398438, 1133.9827270507812], [1418.866943359375, 1127.9044189453125], [1427.849853515625, 1118.683837890625], [1434.4978637695312, 1112.5651245117188], [1441.79833984375, 1104.6460571289062], [1449.1804809570312, 1093.8571166992188], [1455.1109619140625, 1085.6153564453125], [1460.765869140625, 1077.1451416015625], [1465.7571411132812, 1068.2198486328125], [1470.58203125, 1055.9056396484375], [1473.9946899414062, 1048.14892578125], [1477.3660278320312, 1038.5899047851562], [1480.1344604492188, 1025.6298828125], [1482.2515258789062, 1015.0612487792969], [1483.7120361328125, 1004.9357299804688], [1484.6187133789062, 994.8478698730469], [1484.3101196289062, 983.9253234863281], [1484.0032958984375, 973.9356689453125], [1483.160400390625, 964.0020446777344], [1480.712158203125, 951.2848510742188], [1478.6878051757812, 941.5048522949219], [1475.8819580078125, 931.6154174804688], [1472.3578491210938, 921.8181762695312], [1467.86474609375, 911.6843872070312], [1463.4425659179688, 902.5621032714844], [1458.364013671875, 893.9388427734375], [1451.206787109375, 883.1552734375], [1445.18017578125, 875.1106872558594], [1438.6785278320312, 867.5087585449219], [1431.0306396484375, 859.3460693359375], [1423.5250854492188, 852.6228942871094], [1415.7559204101562, 846.21875], [1407.5016479492188, 840.486083984375], [1396.6898193359375, 833.3462829589844], [1387.7313232421875, 828.5589294433594], [1378.5183715820312, 824.3557434082031], [1368.29345703125, 819.7319641113281], [1358.58203125, 816.5938110351562], [1348.77978515625, 814.0443725585938], [1338.581298828125, 812.1513061523438], [1325.9714965820312, 809.5376892089844], [1315.701416015625, 808.8421020507812], [1305.4371337890625, 808.6886901855469], [1294.4625854492188, 808.2943115234375], [1284.1635131835938, 809.3126831054688], [1273.9915771484375, 810.8941650390625], [1263.8643798828125, 813.0097351074219], [1251.4268188476562, 815.2740478515625], [1241.7024536132812, 818.6258544921875], [1233.7611083984375, 821.9172668457031], [1220.2975463867188, 826.5580749511719], [1212.7806396484375, 830.7786560058594], [1203.9775390625, 835.9400634765625], [1195.507568359375, 841.7492065429688], [1185.276611328125, 847.9465637207031], [1177.8047485351562, 854.2400207519531], [1172.1672973632812, 859.78173828125], [1164.3688354492188, 866.2436828613281], [1158.9509887695312, 872.4553833007812], [1154.1146240234375, 878.5738220214844], [1149.7959594726562, 884.5643615722656], [1144.72509765625, 890.1216735839844], [1141.5606689453125, 895.6113586425781], [1139.2591552734375, 900.210693359375], [1135.4732055664062, 904.9978637695312], [1133.1834716796875, 909.8646545410156], [1131.3046875, 914.5166320800781], [1128.5664672851562, 918.7279357910156], [1127.0321044921875, 922.7383422851562], [1126.1046752929688, 926.2840270996094], [1124.896728515625, 929.955810546875], [1123.0502319335938, 933.17236328125], [1122.2863159179688, 936.5579833984375], [1121.5089111328125, 939.7899780273438], [1120.9000244140625, 942.9074401855469], [1119.606201171875, 945.16650390625], [1119.2432861328125, 947.5806274414062], [1118.8814697265625, 950.2618713378906], [1117.8189086914062, 952.0237426757812], [1117.6453857421875, 954.3755187988281], [1117.2962646484375, 956.5568542480469], [1116.4759521484375, 957.952880859375], [1116.3717651367188, 959.9071960449219], [1115.737548828125, 960.9766845703125], [1114.8613891601562, 962.1312255859375], [1114.1119995117188, 963.274169921875], [1113.3585815429688, 964.5186462402344], [1112.644775390625, 965.7510681152344], [1111.9176635742188, 966.9435119628906], [1111.2471313476562, 968.0835571289062], [1110.509521484375, 969.2309875488281], [1109.9910888671875, 970.4955139160156], [1109.333251953125, 971.6587219238281], [1108.6651611328125, 972.940185546875], [1107.994384765625, 974.1688232421875], [1107.4495849609375, 975.3793640136719], [1107.0697021484375, 976.3181457519531]]
point = [[1191.570068359375, 815.6308898925781], [1191.669189453125, 815.8158264160156], [1191.6819458007812, 815.8790283203125], [1191.7249755859375, 815.95263671875], [1191.7090454101562, 815.9562072753906], [1191.7388305664062, 816.1187744140625], [1191.753662109375, 816.2366943359375], [1191.728515625, 816.3331298828125], [1191.7213134765625, 816.2980651855469], [1191.7106323242188, 816.3860778808594], [1191.6976318359375, 816.5092163085938], [1191.82666015625, 816.6329650878906], [1191.7725830078125, 816.5438842773438], [1191.8524780273438, 816.6431884765625], [1191.8421630859375, 816.73388671875], [1191.8285522460938, 816.6877136230469], [1191.8494873046875, 816.7383422851562], [1191.8088989257812, 816.7616577148438], [1191.828857421875, 816.8145141601562], [1191.8314208984375, 816.8166198730469], [1191.4761352539062, 817.3117980957031], [1190.5684814453125, 817.7485961914062], [1189.5223388671875, 818.3804626464844], [1188.6576538085938, 818.927978515625], [1187.9921264648438, 819.5147399902344], [1187.37109375, 819.8770446777344], [1186.689697265625, 820.423828125], [1186.0535278320312, 820.8046264648438], [1185.5206298828125, 821.3129577636719], [1184.8125, 821.6113586425781], [1183.606201171875, 822.5458679199219], [1181.81591796875, 823.9266662597656], [1179.2476806640625, 825.6351013183594], [1173.4567260742188, 830.1187133789062], [1167.6134033203125, 835.1493835449219], [1162.1008911132812, 840.2125549316406], [1156.439697265625, 845.7354431152344], [1151.4779052734375, 851.0899658203125], [1146.7212524414062, 856.7738952636719], [1141.7182006835938, 863.0152282714844], [1137.147705078125, 869.51806640625], [1131.50830078125, 878.2212524414062], [1126.388427734375, 887.3125305175781], [1121.1826171875, 897.536865234375], [1117.6407470703125, 906.0751342773438], [1115.03857421875, 912.9984741210938], [1111.9900512695312, 922.2005004882812], [1109.6002807617188, 931.8164672851562], [1107.596923828125, 941.4675598144531], [1106.2295532226562, 950.7255249023438], [1105.2619018554688, 960.5186767578125], [1104.7421264648438, 968.5196533203125], [1104.6388549804688, 974.8968200683594], [1104.8175659179688, 983.2147216796875], [1105.3480224609375, 989.8058166503906], [1106.0126342773438, 995.9601135253906], [1106.8895263671875, 1001.9176025390625], [1107.89306640625, 1008.1469116210938], [1108.83544921875, 1013.2742919921875], [1110.57763671875, 1019.7840270996094], [1112.7484741210938, 1028.0615234375], [1115.20458984375, 1035.581298828125], [1118.1548461914062, 1043.1858520507812], [1121.4900512695312, 1050.8988647460938], [1126.6888427734375, 1061.6038208007812], [1131.6196899414062, 1069.9777221679688], [1135.7666015625, 1076.4760131835938], [1141.6320190429688, 1084.7540893554688], [1147.2791137695312, 1091.9259643554688], [1153.1351928710938, 1098.5950317382812], [1159.164306640625, 1105.0296020507812], [1168.0851440429688, 1113.1929931640625], [1174.3226928710938, 1118.2380981445312], [1181.7051391601562, 1123.8470458984375], [1190.020263671875, 1129.4427490234375], [1198.7340087890625, 1134.5653686523438], [1207.8977661132812, 1139.6196899414062], [1217.380615234375, 1144.0332641601562], [1227.0465698242188, 1147.739013671875], [1236.9205322265625, 1151.0064697265625], [1247.019287109375, 1153.7008666992188], [1259.0742797851562, 1156.0029296875], [1269.445556640625, 1157.4453125], [1279.918701171875, 1158.4271850585938], [1290.559814453125, 1158.6692504882812], [1300.8712768554688, 1158.3155517578125], [1311.3552856445312, 1157.257568359375], [1321.7796020507812, 1155.8048095703125], [1333.7050170898438, 1153.2412109375], [1343.9454345703125, 1150.3638305664062], [1354.0297241210938, 1146.9827880859375], [1364.0259399414062, 1143.08837890625], [1373.5250854492188, 1138.402587890625], [1382.7925415039062, 1133.3750610351562], [1391.73095703125, 1127.7449340820312], [1401.8282470703125, 1120.510986328125], [1410.089599609375, 1114.009033203125], [1417.925537109375, 1106.8717651367188], [1425.3865356445312, 1099.3592529296875], [1432.1586303710938, 1091.1117553710938], [1438.6553344726562, 1082.7191772460938], [1444.6646118164062, 1073.9801635742188], [1450.9969482421875, 1063.1245727539062], [1456.0231323242188, 1053.6978149414062], [1460.3240966796875, 1043.9971923828125], [1464.1438598632812, 1033.9175415039062], [1467.2823486328125, 1023.5793151855469], [1469.7824096679688, 1013.0922241210938], [1471.8355712890625, 1002.6547241210938], [1473.1806640625, 990.1193542480469], [1473.706298828125, 979.4702758789062], [1473.768798828125, 968.8423156738281], [1473.0188598632812, 958.0115356445312], [1471.831787109375, 947.3983154296875], [1469.96044921875, 936.7952575683594], [1467.3158569335938, 926.3791198730469], [1463.562255859375, 914.2739868164062], [1459.7640380859375, 904.1647338867188], [1455.322265625, 894.4215698242188], [1450.2789916992188, 884.6871337890625], [1444.6644897460938, 875.6139221191406], [1438.6133422851562, 866.8190002441406], [1432.0466918945312, 858.3150939941406], [1423.8062133789062, 848.7566833496094], [1416.2626953125, 841.3038330078125], [1408.2550659179688, 834.1622314453125], [1399.7409057617188, 827.4537963867188], [1390.917236328125, 821.3678588867188], [1381.73583984375, 815.7676391601562], [1372.3217163085938, 810.6032104492188], [1360.9420776367188, 805.3505249023438], [1350.939697265625, 801.5020446777344], [1342.4686889648438, 798.7207336425781], [1330.33447265625, 795.490478515625], [1319.8065795898438, 793.4963989257812], [1309.1611328125, 792.1253356933594], [1298.5999145507812, 791.3576049804688], [1286.0513916015625, 790.9902038574219], [1277.2802124023438, 791.4296569824219], [1266.7634887695312, 792.4465637207031], [1254.5198974609375, 794.2483215332031], [1244.1698608398438, 796.6282653808594], [1233.8218994140625, 799.548095703125], [1223.940673828125, 803.06103515625], [1212.374755859375, 807.6558532714844], [1204.450927734375, 811.5885620117188], [1195.2897338867188, 816.6398010253906], [1184.8079223632812, 823.1326599121094], [1174.88037109375, 830.3468322753906], [1165.4563598632812, 838.1910095214844], [1156.502685546875, 846.5318908691406], [1148.1385498046875, 855.6390686035156], [1141.5716552734375, 863.855224609375], [1134.5050659179688, 873.769287109375], [1128.0892944335938, 884.1956176757812], [1122.2622680664062, 894.9834899902344], [1117.3212280273438, 906.0890197753906], [1113.1572265625, 917.6349487304688], [1110.085205078125, 927.6898803710938], [1107.4868774414062, 939.5970153808594], [1105.5386352539062, 951.5958251953125], [1104.6055908203125, 963.7709350585938], [1104.1654663085938, 972.6381530761719]]
dian = [(1363.3588256835938, 823.4493103027344), (1364.0819091796875, 824.3861389160156), (1362.3903198242188, 822.1396179199219), (1365.48193359375, 826.4232482910156), (1363.8484497070312, 824.074951171875), (1364.509033203125, 825.0845947265625), (1365.4219970703125, 826.3670043945312), (1363.7191772460938, 823.9798889160156), (1364.4522705078125, 824.8333740234375), (1365.0435180664062, 825.8369140625), (1365.6801147460938, 826.7227172851562), (1364.1023559570312, 824.4237060546875), (1364.716552734375, 825.459228515625), (1365.6103515625, 826.6066589355469), (1363.9386596679688, 824.271728515625), (1364.5687255859375, 825.219482421875), (1362.8435668945312, 822.7998962402344), (1361.2604370117188, 820.4468688964844), (1362.1854248046875, 821.7363586425781), (1363.2836303710938, 823.3617553710938), (1364.2323608398438, 824.5657348632812), (1362.696044921875, 822.5594787597656), (1363.529052734375, 823.6628112792969), (1364.3707275390625, 824.76123046875), (1362.767578125, 822.6635131835938), (1363.7958984375, 824.0205383300781), (1364.5476684570312, 825.119384765625), (1365.2023315429688, 826.1228637695312), (1363.5931396484375, 823.7937927246094), (1364.3917236328125, 824.7814636230469), (1362.7142333984375, 822.5760192871094), (1363.4559326171875, 823.5990295410156), (1364.4192504882812, 824.8235168457031), (1365.6602172851562, 826.6848754882812), (1364.0802001953125, 824.3928527832031), (1364.6818237304688, 825.4312438964844), (1365.4415893554688, 826.3885498046875), (1363.7225341796875, 823.9871826171875), (1364.6205444335938, 825.3171081542969), (1365.3230590820312, 826.2316284179688), (1364.3534545898438, 824.7156677246094), (1365.0067138671875, 825.75390625), (1363.3236083984375, 823.4281921386719), (1361.6866455078125, 821.049560546875), (1362.623046875, 822.442138671875), (1363.5874633789062, 823.7834167480469), (1362.2158203125, 821.8823852539062), (1363.1266479492188, 823.0782470703125), (1363.9628295898438, 824.2618103027344), (1364.7256469726562, 825.4648742675781), (1363.4199829101562, 823.5585327148438), (1364.2596435546875, 824.6029052734375), (1364.8880615234375, 825.6744995117188), (1363.4021606445312, 823.5242309570312), (1364.185546875, 824.5281982421875), (1364.8162231445312, 825.5419921875), (1363.2802124023438, 823.3446044921875), (1361.7977294921875, 821.4135131835938), (1362.5989990234375, 822.41015625), (1363.5501708984375, 823.7686462402344), (1362.2196655273438, 821.8720397949219), (1363.1270751953125, 823.1099243164062), (1363.9754638671875, 824.3158874511719), (1363.5149536132812, 823.6572875976562), (1362.7527465820312, 822.6200256347656), (1363.526611328125, 823.664794921875), (1364.34521484375, 824.6708984375), (1365.018310546875, 825.7825012207031), (1363.4078369140625, 823.5401916503906), (1362.0653686523438, 821.5554504394531), (1362.718994140625, 822.5772705078125), (1361.4891357421875, 820.8248596191406), (1362.40771484375, 822.1483764648438), (1363.3187255859375, 823.4222412109375), (1364.2511596679688, 824.6049499511719), (1362.899658203125, 822.8611145019531), (1363.68798828125, 823.9447937011719), (1364.5061645507812, 825.0798950195312), (1362.9746704101562, 822.9149475097656)]
a=[]
b=[]
# for i in dian:
#     a.append(i[0])
# for i in dian:
#     b.append(i[1])
# print(b)
d = np.array(point2)
e = np.array(dian)
print(e.shape)
x = d.reshape(181,1,2)
print(x)
print(d.shape)

# for i in range(len(point)):
#     for x in range(2):

#         a.append(point[i][x])
# print(a)
# c = np.array(a)
# c.reshape()

# for i in point2:
#     plt.scatter(i[0],i[1])

# plt.show()
print(np.array([[[1102,  922]],

       [[1103,  921]],

       [[1107,  921]],
https://opencv-laboratory.readthedocs.io/en/stable/nodes/imgproc/fitEllipse.html
       [[1108,  922]],

       [[1110,  922]],

       [[1132,  928]],

       [[1088, 1032]],

       [[1095,  924]],

       [[1096,  923]],

       [[1098,  923]],

       [[1099,  922]]]).shape)
# for i in point2:
  
#     cv2.circle(im, (int(i[0]),int(i[1])),1, (0, 0, 255), -2)
cv2.fitEllipse(x)
cv2.namedWindow('ellip',0)
cv2.resizeWindow('ellip',1000,1000)
cv2.imshow("ellip", im)
cv2.waitKey()

# x = np.array(a)
# y= np.array(b)
# plt.plot(x, y)
# plt.show()

# c = np.array([[[1102,  922]],

#        [[1103,  921]],

#        [[1107,  921]],

#        [[1108,  922]],

#        [[1110,  922]],

#        [[1132,  928]],

#        [[1088, 1032]],

#        [[1095,  924]],

#        [[1096,  923]],

#        [[1098,  923]],

#        [[1099,  922]]])   # , dtype=int32)

# print(c.shape)

# for x in range(len(dian)):
#     # for y in b:
#         cv2.circle(im, (int(dian[x][0]), int[x][1]), 2, (0, 0, 255), -1)

# cv2.namedWindow('camera', 0)
# cv2.resizeWindow("camera", 1000, 1000)
    

# cv2.imshow("camera", im)
       
# cv2.waitKey()

