#!/usr/bin/python
import sys
import getopt
import csv
import codecs

ATT_SIZES = [32, 64, 128, 256, 512, 640, 768, 1024]
LEN_ATT_SIZES = len(ATT_SIZES)

def formatKMBGT(B, length):
    sout = ''
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776
    if B < KB:
        sout = '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        sout = '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        sout = '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        sout = '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        sout = '{0:.2f} TB'.format(B / TB)
    sout = '{message:{fill}{align}{width}} '.format(
        message=sout, fill=' ', align='>', width=length)
    return sout


def formatPercent(B, length):
    B = float(B)
    sout = '{0:.2f}'.format(B)
    sout = '{message:{fill}{align}{width}} '.format(
        message=sout, fill=' ', align='>', width=length)
    return sout


def createNewDB(row):
    newdb = {
        'db_name': row[1],
        'db_size': row[2],
        'db_atts_perc': 0,
        'attachments_count_total': 0,
        'attachments_size_total': 0,
        'attachments_count': [0] * (LEN_ATT_SIZES + 1),
        'attachments_size': [0] * (LEN_ATT_SIZES + 1),
        'attachments_count_percent': [0] * (LEN_ATT_SIZES + 1),
        'attachments_size_percent': [0] * (LEN_ATT_SIZES + 1)
    }
    return newdb


def parseAttmtRow(db, row):
    # ATTMT*455272*FABIO AFONSO - ATTESTATION.pdf*30*455242*455242*0
    size = int(row[4])

    db['attachments_count_total'] = db['attachments_count_total'] + 1
    db['attachments_size_total'] = db['attachments_size_total'] + size

    for i in range(0, LEN_ATT_SIZES):
        if (size <= (ATT_SIZES[i] * 1024)):
            db['attachments_count'][i] = db['attachments_count'][i] + 1
            db['attachments_size'][i] = db['attachments_size'][i] + size
            break

    if (size > (ATT_SIZES[LEN_ATT_SIZES - 1] * 1024)):
        db['attachments_count'][LEN_ATT_SIZES] = db['attachments_count'][LEN_ATT_SIZES] + 1
        db['attachments_size'][LEN_ATT_SIZES] = db['attachments_size'][LEN_ATT_SIZES] + size

    return db


def doDbStatistics(db):

    for i in range(0, LEN_ATT_SIZES + 1):
        if (db['attachments_count_total'] > 0):
            f = 100 * float(db['attachments_count'][i]) / float(db['attachments_count_total'])
            db['attachments_count_percent'][i] = f

        if (db['attachments_size_total'] > 0):
            f = 100 * float(db['attachments_size'][i]) / float(db['attachments_size_total'])
            db['attachments_size_percent'][i] = f

    if (db['db_size'] > 0):
        db['db_atts_perc'] = 100 * float(db['attachments_size_total']) / (float(db['db_size']) * 1024)
    # return db


def parseDaosCsvFile(filename):
    databases = []

    currentdb = None
    line = 1
    with codecs.open(filename, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='*')  # , quotechar='|')
        for row in spamreader:
            try:
                if (row[0] == 'DBASE'):
                    if currentdb is None:
                        currentdb = createNewDB(row)
                    else:
                        # currentdb =
                        doDbStatistics(currentdb)
                        databases.append(currentdb)
                        currentdb = createNewDB(row)

                elif (row[0] == 'ATTMT'):
                    currentdb = parseAttmtRow(currentdb, row)
                elif (row[0] == 'FOOTR'):
                    # currentdb =
                    doDbStatistics(currentdb)
                    databases.append(currentdb)
            except:
                #print('file %s, line %d: %s' % (filename, spamreader.line_num, e))
                print('Exception on file %s, line %d: ' % (filename, spamreader.line_num))
                continue
            # elif (row0] == 'HEADR'):

    return databases


def generateDbReport(db):

    sout = db['db_name'] + '\n'

    sout = sout + '|- DB Size             : %s\n' % formatKMBGT(float(db['db_size']) * 1024, 9)
    sout = sout + '|- Attachments Count   : %s\n' % db['attachments_count_total']
    sout = sout + '|- Attachments Size    : %s\n' % formatKMBGT(float(db['attachments_size_total']), 8)
    sout = sout + '|- Attachments Size  %s : %s\n' % ('%', formatPercent(db['db_atts_perc'], 6))

    #sout = sout + 'attachments_size_total B:  %s\n' % db['attachments_size_total']
    #count = 0
    # for i in range(0, LEN_ATT_SIZES+1):
    #    count = count + db['attachments_size'][i]
    #sout = sout + 'Attachments Size Tota B2:  %s\n' % count
    #sout = sout + 'attachments_count =  %s |\n' % db['attachments_count']
    #sout = sout + 'attachments_count_percent =  %s |\n' % db['attachments_count_percent']
    #sout = sout + 'attachments_size =  %s |\n' % db['attachments_size']
    #sout = sout + 'attachments_size_percent =  %s |\n' % db['attachments_size_percent']

    newline = '|-- {0: <17}:'.format('Sizes (KB)')
    prev = 0
    for i in range(0, LEN_ATT_SIZES):
        newline = newline + '| {0: >10}'.format(str(prev) + '<=' + str(ATT_SIZES[i]) + ' ')
        prev = ATT_SIZES[i]
    newline = newline + '| {0: >12}'.format('> ' + str(ATT_SIZES[LEN_ATT_SIZES - 1]) + ' |\n')
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Count')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| {0: >9} '.format(str(db['attachments_count'][i]))
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Count %')
    for i in range(0, LEN_ATT_SIZES + 1):
        v = formatPercent(db['attachments_count_percent'][i], 9)
        newline = newline + '| ' + v
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Sizes')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| ' + formatKMBGT(float(db['attachments_size'][i]), 9)
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Sizes %')
    for i in range(0, LEN_ATT_SIZES + 1):
        v = formatPercent(db['attachments_size_percent'][i], 9)
        newline = newline + '| ' + v
    newline = newline + '|\n\n'
    return sout + newline


def printDbToConsole(db):

    print generateDbReport(db)


def printDbToFile(filename, db):

    of = open(filename, 'a')
    of.write(generateDbReport(db))
    of.close()


def doServerStatistics(databases):
    server = {
        'db_count': 0,
        'db_size': 0,
        'db_atts_perc': 0,
        'attachments_count_total': 0,
        'attachments_size_total': 0,
        'attachments_count': [0] * (LEN_ATT_SIZES + 1),
        'attachments_size': [0] * (LEN_ATT_SIZES + 1),
        'attachments_count_percent': [0] * (LEN_ATT_SIZES + 1),
        'attachments_size_percent': [0] * (LEN_ATT_SIZES + 1),
        'estimated_daos_size_total': [0] * (LEN_ATT_SIZES + 1),
        'estimated_daos_size_percent': [0] * (LEN_ATT_SIZES + 1)
    }
    for db in databases:
        server['db_count'] = server['db_count'] + 1
        server['db_size'] = server['db_size'] + (int(db['db_size']) * 1024)
        server['attachments_count_total'] = server['attachments_count_total'] + db['attachments_count_total']
        server['attachments_size_total'] = server['attachments_size_total'] + db['attachments_size_total']
        for i in range(0, LEN_ATT_SIZES + 1):
            server['attachments_count'][i] = server['attachments_count'][i] + db['attachments_count'][i]
            server['attachments_size'][i] = server['attachments_size'][i] + db['attachments_size'][i]

    server['db_atts_perc'] = 100 * float(server['attachments_size_total']) / (float(server['db_size']))

    for i in range(0, LEN_ATT_SIZES + 1):
        if (server['attachments_count_total'] > 0):
            server['attachments_count_percent'][i] = 100 * \
                float(server['attachments_count'][i]) / float(server['attachments_count_total'])

        if (server['attachments_size_total'] > 0):
            server['attachments_size_percent'][i] = 100 * \
                float(server['attachments_size'][i]) / float(server['attachments_size_total'])

    count = float(0)
    for i in range(LEN_ATT_SIZES, -1, -1):
        count = count + server['attachments_size'][i]
        server['estimated_daos_size_total'][i] = count
        server['estimated_daos_size_percent'][i] = 100 * float(count) / float(server['attachments_size_total'])

    return server


def printServerToConsole(srv):

    print generateServerReport(srv)


def printServerToFile(filename, srv):

    of = open(filename, 'w')
    of.write(generateServerReport(srv))
    of.close()


def generateServerReport(srv):

    sout = ('=' * 79) + '\n'
    sout = sout + 'Server Report\n'
    sout = sout + '|- Databases Count :  %s\n' % srv['db_count']
    sout = sout + '|- Databases Size  :  %s\n' % formatKMBGT(srv['db_size'], 8)
    sout = sout + '|- Attachments Count Total :  %s\n' % srv['attachments_count_total']
    sout = sout + '|- Attachments Size Total :  %s\n' % formatKMBGT(srv['attachments_size_total'], 8)
    sout = sout + '|- Attachments Size %s :  %s\n' % ('%', formatPercent(srv['db_atts_perc'], 8))
    #sout = sout + 'Attachments Size Total B:  %s\n' % srv['attachments_size_total']
    #count = 0
    # for i in range(0, LEN_ATT_SIZES+1):
    #    count = count + srv['attachments_size'][i]
    #sout = sout + 'Attachments Size Tota B2:  %s\n' % count
    #sout = sout + 'attachments_count =  %s |\n' % srv['attachments_count']
    #sout = sout + 'attachments_count_percent =  %s |\n' % srv['attachments_count_percent']
    #sout = sout + 'attachments_size =  %s |\n' % srv['attachments_size']
    #sout = sout + 'attachments_size_percent =  %s |\n' % srv['attachments_size_percent']
    #sout = sout + 'estimated_daos_size_percent =  %s |\n' % srv['estimated_daos_size_percent']
    #sout = sout + 'estimated_daos_size_total =  %s |\n' % srv['estimated_daos_size_total']
    #sout = sout + ('=' * 79) + '\n'

    newline = '|-- {0: <17}:'.format('Sizes (KB)')
    prev = 0
    for i in range(0, LEN_ATT_SIZES):
        newline = newline + '| {0: >10}'.format(str(prev) + '<=' + str(ATT_SIZES[i]) + ' ')
        prev = ATT_SIZES[i]
    newline = newline + '| {0: >12}'.format('> ' + str(ATT_SIZES[LEN_ATT_SIZES - 1]) + ' |\n')
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Count')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| {0: >9} '.format(str(srv['attachments_count'][i]))
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Count %')
    for i in range(0, LEN_ATT_SIZES + 1):
        v = formatPercent(srv['attachments_count_percent'][i], 9)
        newline = newline + '| ' + v
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Sizes')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| ' + formatKMBGT(float(srv['attachments_size'][i]), 9)
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Atts Sizes %')
    for i in range(0, LEN_ATT_SIZES + 1):
        v = formatPercent(srv['attachments_size_percent'][i], 9)
        newline = newline + '| ' + v
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|\n|-- {0: <17}:'.format('Daos Sizes')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| ' + formatKMBGT(float(srv['estimated_daos_size_total'][i]), 9)
    newline = newline + '|\n'
    sout = sout + newline

    newline = '|-- {0: <17}:'.format('Daos Sizes %')
    for i in range(0, LEN_ATT_SIZES + 1):
        newline = newline + '| ' + formatPercent(srv['estimated_daos_size_percent'][i], 9)
    newline = newline + '|\n'
    sout = sout + newline

    sout = sout + ('=' * 79) + '\n\n'
    return sout


def usage():
    print 'Usage: AnalizeDaos.py -i <inputfile> -o <outputfile>'


def main():
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print err
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        else:
            assert False, "unhandled option"
    if (inputfile == '') or (outputfile == ''):
        usage()
        sys.exit(1)

    print 'Input file is [%s]' % inputfile
    print 'Output file is [%s]' % outputfile

    databases = parseDaosCsvFile(inputfile)

    server = doServerStatistics(databases)
    printServerToConsole(server)
    printServerToFile(outputfile, server)

    for db in databases:
        printDbToFile(outputfile, db)


# ====== main
if __name__ == "__main__":
    main()
