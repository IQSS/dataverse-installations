import requests

# select id from dvobject where publicationdate is not null and dtype='Dataverse' order by id;

demo_dv_ids = [1, 3, 4, 5, 6, 7, 27, 41, 48, 60, 70, 84, 116, 121, 135, 142, 143, 152, 159, 162, 170, 171, 176, 185, 186, 193, 247, 253, 262, 269, 279, 283, 293, 347, 352, 353, 354, 355, 365, 388, 399, 417, 427, 428, 436, 497, 502, 505, 524, 531, 532, 537, 542, 544, 545, 550, 559, 583, 584, 585, 588, 598, 621, 626, 627, 636, 645, 653, 663, 668, 675, 685, 821, 824, 829, 830, 831, 837, 865, 1066, 1089, 1090, 1091, 1108, 1113, 1125, 1145, 1157, 1160, 1183, 1207, 1216, 1243, 1270, 1307, 1310, 1327, 1331, 1353, 1361, 1372, 1373, 1374, 1399, 1401, 1410, 1424, 1438, 1457, 1466, 1474, 1617, 1620, 1664, 1694, 1700, 1701, 1705, 1721, 1722, 1723, 1724, 1725, 1726, 1735, 1749, 1826, 1827, 1896, 1898, 2016, 2110, 2116, 2122, 2139, 2170, 2174, 2199, 2203, 2384, 2385, 2393, 2421, 2436, 2442, 2447, 2451, 2457, 2478, 2484, 2497, 2501, 2537, 2559, 2576, 2587, 2592, 2599, 2602, 2686, 2714, 2720, 2725, 2759, 2845, 3005, 3006, 3011, 3018, 3024, 3025, 3063, 3089, 3099, 3101, 3105, 3174, 3179, 3188, 3189, 3308, 3319, 4411, 4414, 4416, 4421, 4425, ]

heroku_url = 'https://services-dataverse.herokuapp.com'
demo_url = 'https://demo.dataverse.org'

def run_api_call(metrics=False, limit=100):
    cnt = 0
    for id in demo_dv_ids:
        cnt += 1

        # Format url
        #
        if metrics:
            url = '%s/dvobjects/api/v1/dataverses/%s' % (heroku_url, id)
        else:
            url = '%s/api/dataverses/%s' % (demo_url, id)

        # Make the call
        #
        print '(%d) %s' % (cnt, url)
        r = requests.get(url)
        print r.status_code

        if cnt == limit:
            break

import sys
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'metrics':
        run_api_call(metrics=True)
    else:
        run_api_call()


"""
# API requests don't result in new GuestBookResponse objects
import requests
url = 'http://localhost:8080/api/access/datafile/11'
url += '?key=ad4db0df-2fea-4bea-b4fa-e75462371d69'
r = requests.get(url)
print r.status_code


"""
