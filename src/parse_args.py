import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("vfem", type=str, help="path to vfem.vtu file")
    parser.add_argument("wing", type=str, help="path to wing.vtp file")

    return parser.parse_args()
