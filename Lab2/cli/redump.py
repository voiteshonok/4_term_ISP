#!/usr/bin/env python3
import argparse
from Factory.SerializerFactory import get_serializer


def redump(inf, outf, outform):
    if inf.endswith('.json') and outform == 'JSON':
        pass
    elif inf.endswith('.yaml') and outform == 'YAML':
        pass
    else:
        if inf.endswith('.json'):
            serial = get_serializer("json")
        elif inf.endswith('.yaml'):
            serial = get_serializer("yaml")
        obj = serial.load(inf, False)
        serial = get_serializer(outform)
        serial.dump(obj, outf, False)


parser = argparse.ArgumentParser(description='Parser')
parser.add_argument('inf', type=str, help='Input file')
parser.add_argument('outf', type=str, help='Output file')
parser.add_argument('outform', type=str, help='Output format')
args = parser.parse_args()

redump(args.inf, args.outf, args.outform)
