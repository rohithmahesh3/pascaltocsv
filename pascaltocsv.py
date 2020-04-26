import os
import sys
import logging
import argparse
import xml.etree.ElementTree as ET

global xmlfolder, cloudbucket, csv_name


def getobjects():
    try:
        xmlfiles = os.listdir(xmlfolder)
        objects = []
        for f in xmlfiles:
            tree = ET.parse(xmlfolder + '/' + f)
            root = tree.getroot()
            size = root.find('size')
            width = float(size.find('width').text)
            height = float(size.find('height').text)
            for obj in root.findall('object'):
                name = obj.find('name').text
                bndbox = obj.find('bndbox')
                x_min = float(bndbox.find('xmin').text) / width
                x_max = float(bndbox.find('xmax').text) / width
                y_min = float(bndbox.find('ymin').text) / height
                y_max = float(bndbox.find('ymax').text) / height
                line = ',gs://' + cloudbucket + '/' + (root[1]).text + ','+name+ ',' + "{:.2f}".format(
                    round(x_min, 2)) + ',' + "{:.2f}".format(round(y_min, 2)) + ',,,' + "{:.2f}".format(
                    round(x_max, 2)) + ',' + "{:.2f}".format(round(y_max, 2)) + ',,\n'
                objects.append(line)
        return objects
    except Exception as e:
        logging.exception("Exception occured during reading objects")
        raise  e


def generatecsv(objects):
    try:
        sets = ['TRAIN', 'VALIDATE', 'TEST']
        set_count = [0] * 3
        counter = 0
        open(csv_name, 'w').close()
        f = open(csv_name, 'a')
        for item in objects:
            if counter % 10 == 0:
                f.write(sets[1] + item)
                set_count[1] += 1
            elif counter % 10 == 1:
                f.write(sets[2] + item)
                set_count[2] += 1
            else:
                f.write(sets[0] + item)
                set_count[0] += 1
            counter += 1
        f.close()
        return set_count
    except Exception as e:
        logging.exception("Exception occured while generating csv")
        raise e

def create_arg_parser():
    parser = argparse.ArgumentParser(description='Convert pascal voc to automl object detector dataset csv')
    parser.add_argument('xml_dir', help='Path to xml files diretory')
    parser.add_argument('bucket_name', help='Google cloud storage bucket name')
    parser.add_argument('csv_file', help='csv file to generate')
    return parser


def main():
    if not os.path.isdir(xmlfolder):
        logging.exception("Folder path is incorrect. " + xmlfolder + " does not exist")
        return
    objects = getobjects()
    total = len(objects)
    if total == 0:
        logging.exception("No objects found")
        return
    print('No. of objects found :' + str(total))
    sets = generatecsv(objects)
    print("Train objects : " + str(sets[0]))
    print("Validate objects :" + str(sets[1]))
    print("Test objects : " + str(sets[2]))


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    xmlfolder, cloudbucket, csv_name = parsed_args.xml_dir, parsed_args.bucket_name, parsed_args.csv_file
    main()
