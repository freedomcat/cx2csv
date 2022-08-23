from lxml import etree
import argparse
import os
import csv
import subprocess


def pathConvert(file):
    if ('\\' in file) and (os.name == "posix"):
        try:
            ret = subprocess.run(["wslpath", file], check=True,
                                 capture_output=True, text=True)
            return ret.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(e.cmd)
            print(e.returncode)
            print(e.output)
            print(e.stdout)
            print(e.stderr)
    else:
        return file


def getTarget(replaceData, id):
    for row in replaceData:
        if row['id'] == id:
            return row['target']


parser = argparse.ArgumentParser(
        description="Crowdin EXPORT/IMPORT XLIFF PROCESSER.\
                This script does the following:  \
Output the exported xliff from crowdin to csv format.\
 If you modify the target with csv, when\
 you specify csv for the replace option, apply it to\
 xliff and generate an xliff for import into\
 the crowdin specified by the output option.")

parser.add_argument('exportXliff', help='\
        Specifies the xliff file exported from crowdin.')
parser.add_argument('-r', '--replace',
                    nargs='?', action='store', const='NOFILE',
                    help='Specify csv file with id and target to replace.\
 If this argument is omitted, a file with the extension csv \
that exists in the same path as the file specified by exportXliff is read.')

args = parser.parse_args()

infile = pathConvert(args.exportXliff)

replaceData = []
print(args)
if args.replace:
    print(args.replace)
    if args.replace == "NOFILE":
        repfile = pathConvert(args.exportXliff).replace(".xliff", ".csv")
    else:
        repfile = pathConvert(args.replace)
    with open(repfile, mode='r', encoding="utf-8-sig") as f:
        csvfile = csv.DictReader(f)
        replaceData = [row for row in csvfile]

tree = etree.parse(infile)
root = tree.getroot()
mynsmap = dict()
mynsmap['x'] = root.nsmap[None]
body = tree.xpath("//x:body/*", namespaces=mynsmap)
outcsv = []
outcsv.append(["id",  "context",  "source", "target"])
for b in body:
    id = b.attrib['id']
    try:
        resname = b.attrib['resname']
    except KeyError:
        continue
    for t in b:
        tag = t.tag.rsplit("}")[1]
        if tag == "source":
            source = t.text
        if tag == "target":
            target = t.text
            if args.replace:
                t.text = getTarget(replaceData, id)
    outcsv.append([id, resname, source, target])

outfile = pathConvert(args.exportXliff).replace('.xliff', '.csv')
with open(outfile, 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    for row in outcsv:
        writer.writerow(row)

if args.replace:
    outfile = pathConvert(args.exportXliff).replace('.', '-import.')
    tree.write(outfile, encoding='UTF-8')
