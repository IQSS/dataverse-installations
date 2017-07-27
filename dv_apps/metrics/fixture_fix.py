"""
Hackish script to update the fixtures due to db changes
"""

def add_createdtime_to_users(infile, outfile):

    outlines = []
    prevline = ''
    with open(infile) as f:
        for line in f:
            if prevline.find('"lastname"') > -1:
                val = """        "createdtime": "2015-07-09T12:39:32.287","""
                outlines.append(val)
            else:
                outlines.append(line.rstrip())
            prevline = line


    open(outfile, 'w').write('\n'.join(outlines))
    print ('file written: %s' % outfile)

if __name__ == '__main__':
    input_json_file = 'fixtures/test_2016_0820.json'
    new_json_file = 'fixtures/test_2017_0727.json'
    add_createdtime_to_users(input_json_file, new_json_file)
