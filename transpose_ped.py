"""
Main entry point for the transpose_ped parser.
"""
import argparse
import csv
import itertools
from collections import deque


class Snp(object):
    def __init__(self, row):
        self.chromosome = row["chromosome"]
        self.marker_id = row["marker_id"]
        self.genetic_distance = row["genetic_distance"]
        self.position = row["position"]


class Alleles(object):
    def __init__(self, row):
        self.alleles = [row]


class Individual(object):
    def __init__(self, row, storage):
        self.family_id = row[0]
        self.individual_id = row[1]
        self.father_id = row[2]
        self.mother_id = row[3]
        self.sex = row[4]
        self.status = row[5]
        self.alleles = {}
        snp_store = storage.snp_store
        marker_names = [s.marker_id for s in snp_store]
        these_alleles = deque(row[6:])

        for marker in marker_names:
            self.alleles[marker] = [these_alleles.popleft(), these_alleles.popleft()]


class Storage(object):
    """Storage class with merge methods"""

    def __init__(self):
        self.snp_store = []
        self.ped_store = []

    def add_prefix(self):
        for p in self.ped_store:
            p.family_id = "INCH_" + p.family_id

    def change_status(self):
        for p in self.ped_store:
            if int(p.individual_id) != 27 & int(p.individual_id) % 2 == 0:
                p.status = 2
            elif int(p.individual_id) != 27 & int(p.individual_id) % 2 != 0:
                p.status = 1

    def transpose(self, filename):
        with open(filename, "w", newline='') as outfile:
            writer = csv.writer(outfile, delimiter=' ')
            for s in self.snp_store:
                out_arr = [s.chromosome, s.marker_id, s.genetic_distance, s.position]
                for p in self.ped_store:
                    out_arr = out_arr + (p.alleles.get(s.marker_id))
                writer.writerow(out_arr)

    def generate_tfam(self, filename):
        with open(filename, "w", newline='') as outfile:
            writer = csv.writer(outfile, delimiter=' ')
            for p in self.ped_store:
                out_arr = [p.family_id, p.individual_id, p.father_id, p.mother_id, p.sex, p.status]
                writer.writerow(out_arr)

class MapParser(object):
    """
   MAP file parser
    """

    def read_map(self, file_path, storage):
        """
      Reads in MAP text file, with SNP information
      Args:
         file_path (str): Given filepath to MAP file
      Returns:
         storage : A Storage object with a List of MAP file rows
         :param file_path:
         :param storage:
        """

        with open(file_path) as map_file:
            tsv_reader = csv.DictReader(map_file,
                                        fieldnames=["chromosome", "marker_id", "genetic_distance", "position"],
                                        delimiter="\t")
            for row in tsv_reader:
                this_snp = Snp(row)
                storage.snp_store.append(this_snp)
        return storage


class PedParser(object):
    """
   PED file parser
    """

    def read_ped(self, file_path, storage):
        """
      Reads in MAP text file, with SNP information
      Args:
         file_path (str): Given filepath to MAP file
      Returns:
         storage : A Storage object with a List of MAP file rows
         :param file_path:
         :param storage:
        """

        with open(file_path) as ped_file:
            tsv_reader = csv.reader(ped_file, delimiter=" ")
            for row in tsv_reader:
                this_individual = Individual(row, storage)
                storage.ped_store.append(this_individual)
        return storage


class Main(object):
    """
   Main class
    """

    def __init__(self):
        parser = argparse.ArgumentParser(description='Transpose PED files')
        parser.add_argument('-m', '--map_path', dest='map_path',
                            help='MAP file to be parsed')
        parser.add_argument('-p', '--ped_path', dest='ped_path',
                            help='PED file to be merged and transposed')
        parser.add_argument('-fp', '--fam_prefix', dest='fam_prefix',
                            help='Family prefix')
        parser.add_argument('-s', '--status_change', dest='status_change',
                            help='Change individual status')
        parser.add_argument('-sx', '--status_change_except', dest='status_change_except',
                            help='Change status except these individual ids')
        parser.add_argument('--test')
        args = parser.parse_args()
        args.map_path = "test/test.map"
        args.ped_path = "test/test.ped"
        map_reader = MapParser()
        ped_reader = PedParser()
        storage = Storage()

        map_reader.read_map(args.map_path, storage)

        ped_reader.read_ped(args.ped_path, storage)
        storage.add_prefix()
        storage.change_status()
        storage.transpose("test/test.tped")
        storage.generate_tfam("test/test.tfam")


if __name__ == '__main__':
    Main()
